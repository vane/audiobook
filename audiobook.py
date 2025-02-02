#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import argparse
import os
import shlex

log = logging.getLogger("audiobook")


class PipeStep:
    def __init__(self, name, arg_names):
        self.name = name
        self.arg_names = arg_names


steps = [
    # PipeStep("document-to-html", ["document"]),
    PipeStep("html-cleanup", ["document"]),
    PipeStep("text-to-speech", ["document"])
]

def check():
    is_ok = True
    log.debug("checking pipe python versions")
    for step in steps:
        python_installed = os.popen(f"pipe/{step.name}/.venv/bin/python --version").read()
        python_installed = python_installed.split(" ")[1].strip()
        with open(f"pipe/{step.name}/.python-version") as f:
            python_required = f.read().strip()
        if python_installed != python_required:
            log.debug(f"wrong python version for step '{step.name}' required '{python_required}' installed '{python_installed}'")
            is_ok = False
        else:
            log.debug(f"step '{step.name}' ok")
    if is_ok:
        log.debug("success")
    else:
        log.debug("!!! failed check ")



def run(args):
    log.debug("-"*50)
    check()
    log.debug("-"*50)
    if not args.document:
        log.debug("!!! document  argument required")
        return
    for step in steps:
        log.debug("-"*50)
        log.debug("-"*10+f" STEP {step.name} "+"-"*10)
        log.debug("-"*50)
        cmd_args = ""
        for name in step.arg_names:
            cmd_args += getattr(args, name)
        p = os.popen(f"pipe/{step.name}/.venv/bin/python pipe/{step.name}/pipe.py {cmd_args}")
        result = p.read()
        exit_code = p.close()
        log.debug(f"exit code '{exit_code}'")
        if exit_code is not None:
            log.debug(f"result: {result}")
            log.debug(f"!!! failed step '{step.name}'")
            return
        log.debug(result)
        log.debug("-"*50)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", "-ch", type=bool, default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument("--document", "-d", required=False, default="")
    args = parser.parse_args()
    if args.check:
        check()
    else:
        run(args)