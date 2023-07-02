# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path
from typing import Union

import filetype

INPUT_TYPE = Union[str, Path]


def mkdir(dir_path):
    Path(dir_path).mkdir(parents=True, exist_ok=True)


class FilePreProcess:
    """该类主要用来对传入的file_path作处理，包括是目录还是文件，以及格式是否满足要求。"""

    def __init__(self) -> None:
        self.OfficeSuffix = ['docx', 'doc', 'ppt', 'pptx', 'xlsx', 'xlx']

    def __call__(self, file_path: INPUT_TYPE):
        file_list = self.get_file_list(file_path)
        filter_file = [
            file for file in file_list if self.which_type(file) in self.OfficeSuffix
        ]
        return filter_file

    def get_file_list(self, file_path: INPUT_TYPE):
        if not isinstance(file_path, Path):
            file_path = Path(file_path)

        if file_path.is_dir():
            # 获取目录下所有文件的全路径
            return list(file_path.rglob('*.*'))
        return [file_path]

    @staticmethod
    def which_type(content: Union[bytes, str, Path]) -> str:
        if isinstance(content, (str, Path)) and not Path(content).exists():
            raise FileExistsError(f"{content} does not exist.")

        kind = filetype.guess(content)
        if kind is None:
            raise TypeError(f"The type of {content} does not support.")

        return kind.extension
