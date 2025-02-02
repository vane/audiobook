# audiobook

### convert document to audiobook


### install

1. go to each directory inside pipe
2. create `.venv` with python version from `.python-version`
   1. ex. `cd pipe/text-to-speech` python version `3.11.11`
   2. use `pyenv` to install `3.11.11` python version
   3. in `pipe/text-to-speech directory` execute `~/.pyenv/versions/3.11.11/bin/python -m venv .venv`
   4. execute `source .venv/bin/activate` to activate virtual env
   5. run `pip install -r requirements.txt` to install requirements for given pipe
   6. run `deactivate` and go to next `pipe` directory
3. after each pipe environment is installed run `python -m audiobook validate` to check if everything is correct

### run

Assuming that you managed to install everything run 