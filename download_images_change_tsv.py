"""
A Script that iterates through a dataset, downloads all the associated image files locally and then updates tsv files to point to these local copies
"""

import pandas as pd
import requests
import os
from urllib.parse import urlparse

# 0. Helper functions
def download_image(url, img_dir):
    # Create the directory if it doesn't exist
    os.makedirs(img_dir, exist_ok=True)

    # Get the filename from the URL
    filename = os.path.basename(urlparse(url).path)

    # Full path for the image
    filepath = os.path.join(img_dir, filename)
    if ('jpg' not in filepath) and ('png' not in filepath) and ('webp' not in filepath) and ('jpeg' not in filepath):
        print(f"{filepath} does not have any file extension!")
        filepath += '.jpg'
        filename += '.jpg'

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
    return filename

# 0. Setup
training_path     = './datasets/scizor_train.tsv'
val_path          = './datasets/scizor_val.tsv'

training_img_path = './images/scizor/training/'
val_img_path      = './images/scizor/validation/'

train_df          = pd.read_table(training_path, delimiter='\t')
val_df            = pd.read_table(val_path, delimiter='\t')

train_urls        = train_df.iloc[:,1].to_list()
val_urls          = val_df.iloc[:,1].to_list()

train_names       = []
val_names         = []

# 1. Download all images and collect all filenames
for i in range(len(train_urls)):
    filename = download_image(train_urls[i],training_img_path)
    train_names.append(filename)

for i in range(len(val_urls)):
    filename = download_image(val_urls[i],training_img_path)
    val_names.append(filename)

# 2. Open the new tsv files
local_train_df      = pd.read_table(training_path, delimiter='\t')
local_val_df        = pd.read_table(val_path, delimiter='\t')

# 3. Create dataframes from the lists
train_col = pd.DataFrame(train_names)
val_col   = pd.DataFrame(val_names)

# 4. Update the local dataframes
local_train_df.image = train_col
local_val_df.image = val_col

# 5. Save new tsv files for local use
local_train_df.to_csv('./datasets/scizor_train_local.tsv', sep="\t")
local_val_df.to_csv('./datasets/scizor_val_local.tsv', sep="\t")
