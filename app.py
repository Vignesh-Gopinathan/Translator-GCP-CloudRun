import streamlit as st
from transformers import pipeline, AutoTokenizer, TFAutoModelForSeq2SeqLM
from pathlib import Path


@st.cache(allow_output_mutation=True)
def load_model():
    model_dir = 'models/'
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = TFAutoModelForSeq2SeqLM.from_pretrained(model_dir)
    translator_pipe = pipeline("translation_en_to_fr", model=model, tokenizer=tokenizer)
    return translator_pipe


if __name__ == '__main__':
    st.title('Text translator from English to French')
    if list(Path('models/').glob('*.h5')) and list(Path('models/').glob('*.json')):
        translator = load_model()
        text = st.text_input('Input text (required):', 'Please enter the text to be translated here.')
        if not text:
            st.warning("Please fill out so required fields")

        with st.spinner('Translating...'):
            if st.button('Translate'):
                result = translator(text)
                st.write('Translated text:')
                st.write(result[0]['translation_text'])
    else:
        st.write('Model not found')
