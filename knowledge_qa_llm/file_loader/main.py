# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path
from typing import Dict, List, Union

import filetype

from ..utils import logger
from .image_loader import ImageLoader
from .office_loader import OfficeLoader
from .pdf_loader import PDFLoader
from .txt_loader import TXTLoader

INPUT_TYPE = Union[str, Path]


class FileLoader:
    def __init__(self) -> None:
        self.file_map = {
            "office": ["docx", "doc", "ppt", "pptx", "xlsx", "xlx"],
            "image": ["jpg", "png", "bmp", "tif", "jpeg"],
            "txt": ["txt", "md"],
            "pdf": ["pdf"],
        }

        self.img_loader = ImageLoader()
        self.office_loader = OfficeLoader()
        self.pdf_loader = PDFLoader()
        self.txt_loader = TXTLoader()

    def __call__(self, file_path: INPUT_TYPE) -> Dict[str, List[str]]:
        all_content = {}

        file_list = self.get_file_list(file_path)
        for file_path in file_list:
            file_name = file_path.name

            if file_path.suffix[1:] in self.file_map["txt"]:
                content = self.txt_loader(file_path)
                all_content[file_name] = content
                continue

            file_type = self.which_type(file_path)
            if file_type in self.file_map["office"]:
                content = self.office_loader(file_path)
            elif file_type in self.file_map["pdf"]:
                content = self.pdf_loader(file_path)
            elif file_type in self.file_map["image"]:
                content = self.img_loader(file_path)
            else:
                logger.warning("%s does not support.", file_path)
                continue

            all_content[file_name] = content
        return all_content

    def get_file_list(self, file_path: INPUT_TYPE):
        if not isinstance(file_path, Path):
            file_path = Path(file_path)

        if file_path.is_dir():
            return file_path.rglob("*.*")
        return [file_path]

    @staticmethod
    def which_type(content: Union[bytes, str, Path]) -> str:
        kind = filetype.guess(content)
        if kind is None:
            raise TypeError(f"The type of {content} does not support.")

        return kind.extension

    def sorted_by_suffix(self, file_list: List[str]) -> Dict[str, str]:
        sorted_res = {k: [] for k in self.file_map}

        for file_path in file_list:
            if file_path.suffix[1:] in self.file_map["txt"]:
                sorted_res["txt"].append(file_path)
                continue

            file_type = self.which_type(file_path)
            if file_type in self.file_map["office"]:
                sorted_res["office"].append(file_path)
                continue

            if file_type in self.file_map["pdf"]:
                sorted_res["pdf"].append(file_path)
                continue

            if file_type in self.file_map["image"]:
                sorted_res["image"].append(file_path)
                continue

        return sorted_res
