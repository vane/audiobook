#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import logging
import os.path
import lib.converter

class Config:
    output_dir = "data"

log = logging.getLogger("document-to-html")

def prepare_output_dir(doc_path: str):
    document_name = doc_path.split(os.sep)[-1]

    safe_fname = re.sub('\W+',' ', document_name)
    safe_fname = '_'.join(safe_fname.split(' '))

    converted_path = os.path.join(Config.output_dir, safe_fname)

    os.makedirs(converted_path, exist_ok=True)

    output_dir = os.path.join(converted_path, 'html')
    os.makedirs(output_dir, exist_ok=True)

    return output_dir

def convert(path: str, output_dir: str):
    lib.converter.convert(path, output_dir)

def run(doc_path: str):
    if not os.path.exists(doc_path):
        log.debug(f"!!! document {doc_path} not exists")
        sys.exit(os.EX_DATAERR)
    output_dir = prepare_output_dir(doc_path)
    convert(doc_path, output_dir)
    sys.exit(os.EX_OK)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    log.debug(f"document-to-html {sys.argv}")
    run(sys.argv[1])