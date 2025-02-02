#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import uuid
import logging
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from docling.models.tesseract_ocr_model import TesseractOcrOptions

log = logging.getLogger(__name__)

def convert_tesseract(fpath):
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True
    pipeline_options.table_structure_options.do_cell_matching = True
    pipeline_options.ocr_options = TesseractOcrOptions()
    pipeline_options.ocr_options.force_full_page_ocr = True
    doc_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )
    result = doc_converter.convert(fpath)
    return result

def convert_pdfium(fpath):
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False
    pipeline_options.do_table_structure = True
    pipeline_options.table_structure_options.do_cell_matching = False

    doc_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options, backend=PyPdfiumDocumentBackend
            )
        }
    )
    result = doc_converter.convert(fpath)
    return  result

def convert(base, path, fname):
    fpath = os.path.join(base, path, fname)
    if not os.path.exists(fpath):
        return f'not exists {path}/{fname}'

    result = convert_pdfium(fpath)

    safe_fname = re.sub('\W+',' ', fname)
    safe_fname = '_'.join(safe_fname.split(' '))
    converted_path = os.path.join(base, path, safe_fname)
    os.makedirs(converted_path, exist_ok=True)
    os.makedirs(os.path.join(converted_path, 'html'), exist_ok=True)

    for i, page in enumerate(result.pages):
        html = result.document.export_to_html(page_no=i)
        html_fname = f'{i}'.rjust(6, '0') + '.html'
        log.debug(f'saving {path}/{safe_fname}/html/{html_fname}')
        with open(os.path.join(converted_path, 'html', html_fname), 'wb+') as f:
            f.write(html.encode('utf8'))

    return f'{path}/{safe_fname}'