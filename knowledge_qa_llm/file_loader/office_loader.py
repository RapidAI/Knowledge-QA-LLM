# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path
from typing import Union

from extract_office_content import ExtractOfficeContent


class OfficeLoader:
    def __init__(self) -> None:
        self.extracter = ExtractOfficeContent()

    def __call__(self, office_path: Union[str, Path]) -> str:
        content = self.extracter(office_path)
        return content
