# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path
from typing import List, Union

from rapidocr_pdf import PDFExtracter

from ..text_splitter.chinese_text_splitter import ChineseTextSplitter


class PDFLoader:
    def __init__(
        self,
    ):
        self.extracter = PDFExtracter()
        self.splitter = ChineseTextSplitter(pdf=True)

    def __call__(self, pdf_path: Union[str, Path]) -> List[str]:
        contents = self.extracter(pdf_path)
        split_contents = [self.splitter.split_text(v[1]) for v in contents]
        return sum(split_contents, [])
