# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path
from typing import List, Union

from rapidocr_pdf import PDFExtracter


class PDFLoader:
    def __init__(
        self,
    ):
        self.extracter = PDFExtracter()

    def __call__(self, pdf_path: Union[str, Path]) -> List[List[str]]:
        content = self.extracter(pdf_path)
        return content
