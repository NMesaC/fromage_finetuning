# Finetuning Fromage for Scizor (Pokemon)

This repository hosts the code and model weights for finetuning FROMAGE. The Scizor Dataset included is a small dataset for the Pokemon Scizor.

The below links are of the original Paper, Webpage and Github links.

[Paper](https://arxiv.org/abs/2301.13823) | [Project Webpage](https://jykoh.com/fromage) | [Github](https://github.com/kohjingyu/fromage)


## Setup instructions

### Data Collection and Annotation

I collected the data using the files in the webscraper folder. Get a Serpapi key and set the parameters in the scraper.py file to get the desired images.
Then run the following:
```
python scraper.py
python parser.py
```
To scrape the images from Google Images and then parse the JSON file into a .xlsx file in the form of
```
Description | URL | Image
```
For each row.

### Environment
I performed experiments on a Lambda Lab machine, which utilizes a fresh Ubuntu image using either 1xA100 or 1xA6000.
I then followed these next steps.

Download the repository.
```
git clone https://github.com/NMesaC/fromage_finetuning_pokemon.git
```
Set up the environment and environment variables
```
cd fromage_finetuning_pokemon
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=$PYTHONPATH:~/fromage_finetuning_pokemon/
```
Install gdown to download google drive links (and upgrade pip) and use gdown to download the Precomputed cc3m Embeddings for Image Retrieval
```
python3 -m pip install --upgrade pip
pip install gdown
cd fromage_model
gdown 1wMojZNqEwApNlsCZVvSgQVtZLgbeLoKi
```
I ran these commands instead of updating the requirements.txt, but either work.
```
pip3 uninstall torch torchvision torchaudio
pip3 install torch torchvision torchaudio
```
Run the following Python script to turn a given training and validation dataset from .tsv files with URL's to .tsv files with local paths to images.
The script may need to be edited to change the .tsv files initially fed and where some paths point.
```
python3 download_images_change_tsv.py
```
Now, we need to run the finetuning script for 1 epoch quickly so we can get an unpruned version of the model for training.
```
randport=$(shuf -i8000-9999 -n1)  # Generate a random port number
python -u finetuning.py \
    --dist-url "tcp://127.0.0.1:${randport}" --dist-backend 'nccl' \
    --multiprocessing-distributed --world-size 1 --rank 0 \
    --epochs=1 --steps-per-epoch=10 \
    --dataset=scizor  --val-dataset=scizor \
    --opt-version='facebook/opt-6.7b' --visual-model='openai/clip-vit-large-patch14' \
    --exp_name='fromage_exp' --image-dir='images/'  --log-base-dir='runs/' \
    --batch-size=2  --val-batch-size=2  --learning-rate=0.0003 --precision='bf16'  --print-freq=100
```
Next, we need to update the weights of this unpruned model to have the pre-trained models weights.
In essence, we uncompress our model with the above step so we can perform the finetuning step on a pre-trained checkpoint, instead of from scratch.
```
python3 update_weights.py
```
Finally, we can perform finetuning.
```
randport=$(shuf -i8000-9999 -n1)  # Generate a random port number
python -u finetuning.py \
    --dist-url "tcp://127.0.0.1:${randport}" --dist-backend 'nccl' \
    --multiprocessing-distributed --world-size 1 --rank 0 \
    --epochs=20 --steps-per-epoch=10000 \
    --max-len=50 \
    --resume='./fromage_model/ckpt.pth.tar' \
    --dataset=scizor  --val-dataset=scizor \
    --opt-version='facebook/opt-6.7b' --visual-model='openai/clip-vit-large-patch14' \
    --exp_name='fromage_exp' --image-dir='images/'  --log-base-dir='runs/' \
    --batch-size=2  --val-batch-size=2  --learning-rate=0.0003 --precision='bf16'  --print-freq=100
```
Now, this full model is uncompressed, and will not fit on most GPU's, so for using the notebook file, we prune it again.
```
cd fromage
python3 prune_scizor.py
```
This script might need to be edited slightly for different uses.
With the pruned model, we need to copy over the embedding .pkl files so the notebook can run, as well as the model args.
We do so with the following line: (Some paths may change)
```
cd ..
cp ./runs/fromage_exp_1/model_args.json ./scizor_model
cp ./fromage_model/cc3m_embeddings.pkl ./scizor_model
cp ./fromage_model/scizor_embeddings.pkl ./scizor_model
```
Now, we can simply run the notebook and use the model in a demo!


## Citation

If you find this work useful, please consider citing:

```
@inproceedings{koh2023grounding,
  title={Grounding Language Models to Images for Multimodal Inputs and Outputs},
  author={Koh, Jing Yu and Salakhutdinov, Ruslan and Fried, Daniel},
  journal={ICML},
  year={2023}
}
```
