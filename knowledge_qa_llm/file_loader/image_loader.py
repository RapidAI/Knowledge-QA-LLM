# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path
from typing import List, Union

from rapidocr_onnxruntime import RapidOCR


class ImageLoader:
    def __init__(
        self,
    ):
        self.ocr = RapidOCR()

    def __call__(self, img_path: Union[str, Path]) -> List[str]:
        ocr_results, _ = self.ocr(img_path)
        _, rec_res, _ = list(zip(*ocr_results))
        return list(rec_res)
