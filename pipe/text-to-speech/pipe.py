#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os.path
import sys

class Config:
    output_dir = "data"

log = logging.getLogger("text-to-speech")

def run(document: str):
    if not os.path.exists(document):
        log.debug(f"!!! document {document} not exists")
        sys.exit(os.EX_DATAERR)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    log.debug(f"text-to-speech {sys.argv}")
    try:
        run(sys.argv[1])
        sys.exit(os.EX_OK)
    except Exception as e:
        log.error("error", e)
        sys.exit(os.EX_IOERR)
