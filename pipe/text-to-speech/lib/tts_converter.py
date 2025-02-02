#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os.path
import urllib.parse
from bs4 import BeautifulSoup

import torch
from TTS.api import TTS

device = "cpu"
if torch.cuda.is_available():
    device = "cuda"
if torch.mps.is_available():
    device = "mps"

def list_models():
    models = TTS().list_models()
    return models.models_dict

def to_wav(base: str, path: str, fpath: str, model_name: str):
    fpath = urllib.parse.unquote(fpath)
    html_path = os.path.join(base, path, fpath)
    if not os.path.exists(html_path):
        return f'not exists {path}/{fpath}'
    wav_base_path = fpath.split('/')[0]
    wav_index = fpath.split('/')[-1].split('.')[0]
    wav_path = os.path.join(base, path, wav_base_path, 'wav')
    os.makedirs(wav_path, exist_ok=True)
    with open(html_path, 'rb') as f:
        text = f.read()
    try:
        tts = TTS(model_name=model_name, progress_bar=False).to(device)
        wav_fname = f'{wav_index}.wav'
        p = os.path.join(wav_path, wav_fname)
        tts.tts_to_file(text=text, file_path=p)
    except:
        return f'not exists model {model_name}'
    return f'{wav_base_path}/wav/{wav_fname}'