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

def convert(fpath, output_dir):
    log.debug("converting")
    result = convert_pdfium(fpath)

    for i, page in enumerate(result.pages):
        html = result.document.export_to_html(page_no=i)
        html_fname = f'{i}'.rjust(6, '0') + '.html'
        html_path = os.path.join(output_dir, html_fname)

        if os.path.exists(html_path):
            log.debug(f"skipping {output_dir}/{html_fname}")
            continue

        log.debug(f'saving {output_dir}/{html_fname}')
        with open(html_path, 'wb+') as f:
            f.write(html.encode('utf8'))
    log.debug("convert ok")