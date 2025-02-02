# audiobook
convert pdf document to audiobook

## Description
This is proof of concept ML pipe to convert books to audiobooks using couple of incompatible libraries.   
Tested on `Divine Comedy` polish `pdf` 357 pages
from [wolnelektury.pl](https://wolnelektury.pl/katalog/lektura/boska-komedia/) see [benchmark](https://github.com/vane/audiobook#Benchmark) 

Each page is separate file.   
Each pipe produces it's own output that can be adjusted.  
Exising files are skipped from output.

For example if you convert from `pdf` to `html` using `document-to-html` pipe 
and then from `html` to `txt` using `html-to-text` pipe and after that 
delete `wav` directory or files from `wav` directory that are invalid.
You can adjust `txt` files to make better audio output for `wav` files.  
Be aware that file names should always stay the same !

Files are numerated with page numbers from original document.

[docling](https://github.com/DS4SD/docling) - for pdf to html conversion  
[beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/) - for html cleanup    
[coqui-ai/TTS](https://github.com/coqui-ai/TTS) - for TTS

## Install

1. go to each directory inside pipe
2. create `.venv` with python version from `.python-version`
   1. ex. `cd pipe/text-to-speech` python version `3.11.11`
   2. use `pyenv` to install `3.11.11` python version
   3. in `pipe/text-to-speech directory` execute `~/.pyenv/versions/3.11.11/bin/python -m venv .venv`
   4. execute `source .venv/bin/activate` to activate virtual env
   5. run `pip install -r requirements.txt` to install requirements for given pipe
   6. run `deactivate` and go to next `pipe` directory
3. after each pipe environment is installed run `python -m audiobook validate` to check if everything is correct


after correct installation `pipe` directory structure should look like that
```shell
pipe/
   document-to-html/
      .venv/ (python 3.13)
      ...
   html-to-text/
      .venv/ (python 3.13)
      ...
   text-to-speech
      .venv/ (python 3.11)
      ...
```

## Run

Assuming that you managed to install everything, run with command line

```shell
python3 -m audiobook -d /path/to/some_pdf.pdf -m tts_models/en/ljspeech/vits
```

Help

```shell
python3 -m audiobook -h
```

tested models
```shell
tts_models/en/ljspeech/vits
tts_models/pl/mai_female/vits
```

## TODO

1. list models from TTS on command line
2. provide steps as command line args
3. test with other types than pdf
4. support document ocr
5. support for coqui-ai/TTS multilingual models
6. fix text-to-speech pipe logging

## Benchmark
on rtx3090 with power limit 250W (book with 357 pages)
```shell
time python -m audiobook -d boska-komedia.pdf -m tts_models/pl/mai_female/vits
real    8m38.380s
user    11m40.027s
sys     0m21.981s
```