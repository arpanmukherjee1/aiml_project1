import os
from azure.storage.blob import BlobServiceClient
from pathlib import Path
from datetime import datetime as dt

def download_if_required(config, force=False):
    STORAGEACCOUNTURL = os.environ['STORAGEACCOUNTURL']
    STORAGEACCOUNTKEY = os.environ['STORAGEACCOUNTKEY']
    CONTAINERNAME = os.environ['CONTAINERNAME']
    
    client = BlobServiceClient(account_url=STORAGEACCOUNTURL, credential=STORAGEACCOUNTKEY)
    for file in config:
        f = Path(file)
        os.makedirs(f.parent, exist_ok=True)        
        if not f.exists() or force:
            instance = client.get_blob_client(CONTAINERNAME, config[file], snapshot=None)
            download(instance, file)
            
def download(blob_instance, destination_file):
    print("[{}]:[INFO] : Downloading {} ...".format(dt.utcnow(), destination_file))
    with open(destination_file, "wb") as blob:
        blob_data = blob_instance.download_blob()
        blob_data.readinto(blob)
    print("[{}]:[INFO] : download finished".format(dt.utcnow())) 