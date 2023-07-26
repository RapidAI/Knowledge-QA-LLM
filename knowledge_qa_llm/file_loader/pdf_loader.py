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

    def __call__(self, pdf_list: List[Union[str, Path]]) -> List[str]:
        all_content = []
        for pdf_path in pdf_list:
            content = self.extracter(pdf_path)
            all_content.append(content)
        return all_content
