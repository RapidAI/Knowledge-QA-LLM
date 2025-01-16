# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path
from typing import List, Union

from ..text_splitter.chinese_text_splitter import ChineseTextSplitter
from ..utils.utils import read_txt


class TXTLoader:
    def __init__(self) -> None:
        self.splitter = ChineseTextSplitter()

    def __call__(self, txt_path: Union[str, Path]) -> List[str]:
        contents = read_txt(txt_path)
        split_contents = [self.splitter.split_text(v) for v in contents]
        return sum(split_contents, [])
