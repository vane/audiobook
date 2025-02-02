#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os.path
import logging
import urllib.parse
import torch
from TTS.api import TTS

log = logging.getLogger(__name__)

device = "cpu"
if torch.cuda.is_available():
    device = "cuda"
if torch.mps.is_available():
    device = "mps"

def list_models():
    models = TTS().list_models()
    return models.models_dict

def to_wav(text, output_path, model_name: str):
    log.debug(f"to_wav with device '{device}' model name '{model_name}'")
    tts = TTS(model_name=model_name, progress_bar=False).to(device)
    tts.tts_to_file(text=text, file_path=output_path)
