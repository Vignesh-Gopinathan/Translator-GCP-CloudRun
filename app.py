import streamlit as st
from transformers import pipeline, AutoTokenizer, TFAutoModelForSeq2SeqLM
import yaml
from google.cloud import storage
import os
from pathlib import Path

st.title('Text translator from English to French')


def download_model():
    with open("app_config.yaml", 'r') as f:
        dirs = yaml.load(f, Loader=yaml.FullLoader)
        cloud_model_dir = dirs['cloud_model_dir']

    storage_client = storage.Client()
    buckets = list(storage_client.list_buckets())

    print('\nBuckets:')
    for bucket in buckets:
        print('\t', bucket.name)

        blobs = storage_client.list_blobs(bucket)
        for blob in blobs:
            if cloud_model_dir in blob.name:
                if blob.name.endswith('.h5') or blob.name.endswith('.json'):
                    destination_file_name = 'models/' + blob.name.split('/')[-1]
                    blob.download_to_filename(destination_file_name)

    print('All models downloaded from Cloud storage')


@st.cache(allow_output_mutation=True)
def load_model():
    model_dir = 'models/'
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = TFAutoModelForSeq2SeqLM.from_pretrained(model_dir)
    translator_pipe = pipeline("translation_en_to_fr", model=model, tokenizer=tokenizer)
    return translator_pipe


if list(Path('models/').glob('*.h5')) and list(Path('models/').glob('*.json')):
    st.write('Model already download. Loading model.....')
    translator = load_model()
else:
    st.write('Model not found. Downloading model.....')
    download_model()
    if not(list(Path('models/').glob('*.h5')) and list(Path('models/').glob('*.json'))):
        st.write('Downloaded model not found')
    st.write('Downloaded model. Loading model.....')
    translator = load_model()

text = st.text_input('Input text (required):', 'Please enter the text to be translated here.')
if not text:
    st.warning("Please fill out so required fields")

with st.spinner('Translating...'):
    if st.button('Translate'):
        result = translator(text)
        st.write('Translated text:')
        st.write(result[0]['translation_text'])
