import numpy as np
import copy
import torch
from transformers import logging
logging.set_verbosity_error()

from PIL import Image
import matplotlib.pyplot as plt

from fromage import models
from fromage import utils

def trunc_caption(caption: str) -> str:
    # Truncate at period.
    trunc_index = caption.find('.') + 1
    if trunc_index < 0:
        trunc_index = caption.find('\n') + 1
    caption = caption[:trunc_index]
    return caption

def display_interleaved_outputs(model_outputs, one_img_per_ret=True):
    for output in model_outputs:
        if type(output) == str:
            print(output)
        elif type(output) == list:
            if one_img_per_ret:
                plt.figure(figsize=(3, 3))
                plt.imshow(np.array(output[0]))
            else:
                fig, ax = plt.subplots(1, len(output), figsize=(3 * len(output), 3))
                for i, image in enumerate(output):
                    image = np.array(image)
                    ax[i].imshow(image)
                    ax[i].set_title(f'Retrieval #{i+1}')
            plt.show()
        elif type(output) == Image.Image:
            plt.figure(figsize=(3, 3))
            plt.imshow(np.array(output))
            plt.show()

# Load model used in the paper.
model_dir = './runs/fromage_exp_1'
model = models.load_fromage(model_dir)

# Load an image of a cat.
inp_image = utils.get_image_from_url('https://img.pokemondb.net/artwork/large/scizor.jpg')

# Get FROMAGe to retrieve images of cats in other styles.
for inp_text in ['model [RET]', 'trading card [RET]']:
    prompt = [inp_image, inp_text]
    print('Prompt:')
    display_interleaved_outputs(prompt)
    print('=' * 30)
    model_outputs = model.generate_for_images_and_texts(prompt, max_img_per_ret=3)

    # Display outputs.
    print('Model generated outputs:')
    display_interleaved_outputs(model_outputs, one_img_per_ret=False)
