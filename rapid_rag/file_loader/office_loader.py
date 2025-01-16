# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path
from typing import Union

from extract_office_content import ExtractOfficeContent

from ..text_splitter.chinese_text_splitter import ChineseTextSplitter


class OfficeLoader:
    def __init__(self) -> None:
        self.extracter = ExtractOfficeContent()
        self.splitter = ChineseTextSplitter()

    def __call__(self, office_path: Union[str, Path]) -> str:
        contents = self.extracter(office_path)
        split_contents = [self.splitter.split_text(v) for v in contents]
        return sum(split_contents, [])
