#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import argparse
import os
import sys
import shlex

log = logging.getLogger("audiobook")


class PipeStep:
    def __init__(self, name, arg_names):
        self.name = name
        self.arg_names = arg_names


steps = [
    PipeStep("document-to-html", ["document"]),
    PipeStep("html-to-text", ["document"]),
    PipeStep("text-to-speech", ["document", "model"])
]

def check():
    is_ok = True
    log.debug("checking pipe python versions")
    for step in steps:
        if not os.path.exists(f"pipe/{step.name}"):
            log.debug(f"!!! failed step '{step.name}' not exists")
            sys.exit(0)
        python_installed = os.popen(f"pipe/{step.name}/.venv/bin/python --version").read()
        python_installed = python_installed.split(" ")[1].strip()
        with open(f"pipe/{step.name}/.python-version") as f:
            python_required = f.read().strip()

        python_installed_minor = '.'.join(python_installed.split('.')[:-1])
        python_required_minor = '.'.join(python_installed.split('.')[:-1])

        if python_installed_minor != python_required_minor:
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
    for step in steps:
        log.debug("-"*50)
        log.debug("-"*10+f" STEP {step.name} "+"-"*10)
        log.debug("-"*50)
        cmd_args = ""
        for name in step.arg_names:
            arg = getattr(args, name)
            if not arg:
                log.debug(f"!!! failed step {step.name} argument '{name}' required but not provided")
                sys.exit(0)
            cmd_args += f"{shlex.quote(arg)} "
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
    parser.add_argument("--model", "-m", required=False, default="", help="example model: tts_models/en/ljspeech/vits")
    args = parser.parse_args()
    if args.check:
        check()
    else:
        run(args)