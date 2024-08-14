import torch
import subprocess
import json
import os
from fromage import models, utils


checkpoint1 = torch.load('./fromage_model/pretrained_ckpt.pth.tar', map_location='cuda:0')
checkpoint2 = torch.load('./runs/fromage_exp/ckpt.pth.tar', map_location='cuda:0')

weights = {'model.logit_scale':'module.model.logit_scale',
           'model.text_hidden_fcs.0.0.bias':'module.model.text_hidden_fcs.0.0.bias',
           'model.text_hidden_fcs.0.0.weight':'module.model.text_hidden_fcs.0.0.weight',
           'model.visual_embeddings.bias':'module.model.visual_embeddings.bias',
           'model.visual_embeddings.weight':'module.model.visual_embeddings.weight',
           'model.visual_fc.bias':'module.model.visual_fc.bias',
           'model.visual_fc.weight':'module.model.visual_fc.weight',
           'ret_input_embeddings.weight':'module.model.input_embeddings.weight'}

#write
with open('./runs/fromage_exp/model_args.json', 'r') as f:
        model_kwargs = json.load(f)
        ret_token_idx = model_kwargs['retrieval_token_idx']


for k,v in weights.items():
    if k == 'ret_input_embeddings.weight':
        checkpoint2['state_dict'][v][ret_token_idx:ret_token_idx+1, :] = checkpoint1['state_dict'][k]
    else:
        checkpoint2['state_dict'][v] = checkpoint1['state_dict'][k]
    print(k)

torch.save(checkpoint2, './fromage_model/full_ckpt' + '.pth.tar')
