#!/usr/bin/env python
# -*- coding: utf-8 -*-
def convert_html(html_data: str):
    soup = BeautifulSoup(html_data, 'html.parser')
    soup.title.decompose()
    text = soup.get_text()
    text = text.replace('\n\n', '\n').replace('\n\n', '\n') \
        .replace('\n\n', '\n').replace('\n\n', '\n') \
        .replace('\n\n', '\n').replace('\n\n', '\n')
    return text.strip('\n')
