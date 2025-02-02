#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import logging
import os.path
import sys
import lib.converter

class Config:
    output_dir = "data"

log = logging.getLogger("html-to-text")

def get_io_dir(doc_path: str):
    document_name = doc_path.split(os.sep)[-1]

    safe_fname = re.sub('\W+',' ', document_name)
    safe_fname = '_'.join(safe_fname.split(' '))

    converted_path = os.path.join(Config.output_dir, safe_fname)

    input_dir = os.path.join(converted_path, 'html')

    if not os.path.exists(input_dir):
        log.debug(f"!!! failed input dir {input_dir} not exists")
        sys.exit(os.EX_DATAERR)

    output_dir = os.path.join(converted_path, 'txt')
    os.makedirs(output_dir, exist_ok=True)

    return input_dir, output_dir

def cleanup(input_dir, output_dir):
    for fname in os.listdir(input_dir):
        with open(os.path.join(input_dir, fname), 'rb') as f:
            html_data = f.read()
        text = lib.converter.html_to_text(html_data)

        base_name = fname.split(".")[0]
        txt_fname = os.path.join(output_dir, os.path.join(f"{base_name}.txt"))
        if os.path.exists(txt_fname):
            log.debug(f"skipping {output_dir}/{txt_fname}")
            continue
        with open(txt_fname, 'wb+') as f:
            f.write(text)

def run(doc_path: str):
    if not os.path.exists(doc_path):
        log.debug(f"!!! failed document {doc_path} not exists")
        sys.exit(os.EX_DATAERR)
    input_dir, output_dir = get_io_dir(doc_path)
    cleanup(input_dir, output_dir)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    log.debug(f"html-cleanup {sys.argv}")
    try:
        run(sys.argv[1])
        sys.exit(os.EX_OK)
    except Exception as e:
        log.error("error", e)
        sys.exit(os.EX_IOERR)
