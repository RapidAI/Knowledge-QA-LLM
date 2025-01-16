# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path
from typing import List, Union

from rapidocr_onnxruntime import RapidOCR

from ..text_splitter.chinese_text_splitter import ChineseTextSplitter


class ImageLoader:
    def __init__(
        self,
    ):
        self.ocr = RapidOCR()
        self.splitter = ChineseTextSplitter()

    def __call__(self, img_path: Union[str, Path]) -> List[str]:
        ocr_results, _ = self.ocr(img_path)
        _, rec_res, _ = list(zip(*ocr_results))
        split_contents = [self.splitter.split_text(v) for v in rec_res]
        return sum(split_contents, [])
