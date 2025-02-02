#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup


def html_to_text(html_data):
    soup = BeautifulSoup(html_data, 'html.parser')
    soup.title.decompose()
    text = soup.get_text()
    while text.find("\n\n") != -1:
        text = text.replace("\n\n", "\n")
    return text.strip('\n').encode('utf8')
