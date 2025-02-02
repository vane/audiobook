#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import uuid
from fastapi import UploadFile
from fastapi.responses import FileResponse


def path_obj(base: str, path: str):
    p = os.path.join(base, path)
    os.makedirs(p, exist_ok=True)
    return p

def save_obj(base: str, path: str, data: UploadFile):
    p = path_obj(base, path)
    with open(os.path.join(p, data.filename), 'wb') as f:
        shutil.copyfileobj(data.file, f)

def list_obj(base: str, path: str, subpath: str):
    p = os.path.join(base, path, subpath)
    if not os.path.exists(p):
        return f'not exists {path}/{subpath}'
    files = []
    for f in os.listdir(p):
        if os.path.isdir(os.path.join(p, f)):
            files.append({'dir': True, 'file': f})
        else:
            files.append({'dir': False, 'file': f})
    return files

def get_obj(base: str, path: str, fpath: str):
    p = os.path.join(base, path, fpath)
    if not os.path.exists(p):
        return f'not exists {path}/{fpath}'
    return FileResponse(p)