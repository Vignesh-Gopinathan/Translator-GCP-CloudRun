import yaml
from google.cloud import storage
from pathlib import Path


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


if __name__ == '__main__':
    if list(Path('models/').glob('*.h5')) and list(Path('models/').glob('*.json')):
        pass
    else:
        download_model()
