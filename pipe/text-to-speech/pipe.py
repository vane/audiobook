#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os.path
import sys

log = logging.getLogger("text-to-speech")

def run(document: str):
    if not os.path.exists(document):
        print(f"!!! document {document} not exists")
        sys.exit(os.EX_DATAERR)
    sys.exit(os.EX_OK)

if __name__ == '__main__':
    print("text-to-speech", sys.argv)
    run(sys.argv[1])