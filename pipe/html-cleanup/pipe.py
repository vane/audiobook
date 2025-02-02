#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import logging
import os.path
import sys

class Config:
    output_dir = "data"

log = logging.getLogger("html-cleanup")

def get_output_dir(doc_path: str):
    document_name = doc_path.split(os.sep)[-1]

    safe_fname = re.sub('\W+',' ', document_name)
    safe_fname = '_'.join(safe_fname.split(' '))

    converted_path = os.path.join(Config.output_dir, safe_fname)

    output_dir = os.path.join(converted_path, 'html')

    if not os.path.exists(output_dir):
        log.debug(f"!!! failed output dir {output_dir} not exists")
        sys.exit(os.EX_DATAERR)

    return output_dir

def run(doc_path: str):
    if not os.path.exists(doc_path):
        log.debug(f"!!! failed document {doc_path} not exists")
        sys.exit(os.EX_DATAERR)
    output_dir = get_output_dir(doc_path)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    log.debug(f"html-cleanup {sys.argv}")
    try:
        run(sys.argv[1])
        sys.exit(os.EX_OK)
    except Exception as e:
        log.error("error", e)
        sys.exit(os.EX_IOERR)
