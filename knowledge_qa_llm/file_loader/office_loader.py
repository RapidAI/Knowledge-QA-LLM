# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path
from typing import List, Union

from extract_office_content import ExtractOfficeContent


class ExtractOfficeLoader:
    def __init__(self) -> None:
        self.extracter = ExtractOfficeContent()

    def __call__(
        self, file_list: List[Union[str, Path]]
    ) -> List[List[Union[str, str]]]:
        extract_res = []
        for file_path in file_list:
            content = self.extracter(file_path)
            extract_res.append([str(file_path), content])
        return extract_res
