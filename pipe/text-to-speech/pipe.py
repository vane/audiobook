#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import logging
import os.path
import sys
import lib.tts_converter

class Config:
    output_dir = "data"

log = logging.getLogger("text-to-speech")

def get_io_dir(doc_path: str):
    document_name = doc_path.split(os.sep)[-1]

    safe_fname = re.sub('\W+',' ', document_name)
    safe_fname = '_'.join(safe_fname.split(' '))

    converted_path = os.path.join(Config.output_dir, safe_fname)

    input_dir = os.path.join(converted_path, 'txt')

    if not os.path.exists(input_dir):
        log.debug(f"!!! failed input dir {input_dir} not exists")
        sys.exit(os.EX_DATAERR)

    output_dir = os.path.join(converted_path, 'wav')
    os.makedirs(output_dir, exist_ok=True)

    return input_dir, output_dir

def convert(input_dir, output_dir, model_name):
    for fname in os.listdir(input_dir):
        with open(os.path.join(input_dir, fname), 'rb') as f:
            txt_data = f.read()

        base_name = fname.split(".")[0]
        wav_fname = os.path.join(output_dir, os.path.join(f"{base_name}.wav"))

        if os.path.exists(wav_fname):
            log.debug(f"skipping {output_dir}/{wav_fname}")
            continue

        if not txt_data:
            log.debug(f"empty file '{fname}' '{txt_data}'")
            log.debug(f"skipping {output_dir}/{wav_fname}")
            continue

        log.debug(f'saving {output_dir}/{wav_fname}')
        lib.tts_converter.to_wav(txt_data.decode('utf8'), wav_fname, model_name)

def run(doc_path: str, model_name: str):
    if not os.path.exists(doc_path):
        log.debug(f"!!! document {doc_path} not exists")
        sys.exit(os.EX_DATAERR)
    input_dir, output_dir = get_io_dir(doc_path)
    convert(input_dir, output_dir, model_name)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    log.debug(f"text-to-speech {sys.argv}")
    try:
        run(sys.argv[1], sys.argv[2])
        sys.exit(os.EX_OK)
    except Exception as e:
        log.error("error", e)
        sys.exit(os.EX_IOERR)
