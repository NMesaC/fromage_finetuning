"""
A Script that iterates through a dataset and downloads all the associated image files
"""

import pandas as pd
import requests
import os
from urllib.parse import urlparse

# 0. Helper function
def download_and_save_image(url, directory):
    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Get the filename from the URL
    filename = os.path.basename(urlparse(url).path)

    # Full path for the image
    filepath = os.path.join(directory, filename)
    if ('jpg' not in filepath) and ('png' not in filepath) and ('webp' not in filepath) and ('jpeg' not in filepath):
        print(f"{filepath} does not have any file extension!")
        filepath += '.jpg'

    # Download the image
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Write the image content to the file
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Image downloaded successfully: {filepath}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

# 0. Setup
training_path     = './datasets/scizor_train.tsv'
val_path          = './datasets/scizor_val.tsv'

training_img_path = './images/scizor/training/'
val_img_path      = './images/scizor/validation/'

train_df          = pd.read_table(training_path, delimiter='\t')
val_df            = pd.read_table(val_path, delimiter='\t')

train_urls        = train_df.iloc[:,1].to_list()
val_urls          = val_df.iloc[:,1].to_list()

# 1. Iterate
for url in train_urls:
    download_and_save_image(url, training_img_path)

for url in val_urls:
    download_and_save_image(url, val_img_path)

print("Done!")
