import os
from gdown import download
from pathlib import Path

def download_if_required(config, force=False):
    for file in config:
        f = Path(file)
        os.makedirs(f.parent, exist_ok=True)
        if not f.exists() or force:
            download(config[file], file)