# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path
from typing import List, Union


class TXTLoader:
    def __init__(self) -> None:
        pass

    def __call__(self, txt_path: Union[str, Path]) -> List[str]:
        txts = read_txt(txt_path)
        return txts


def read_txt(txt_path: Union[Path, str]) -> List[str]:
    if not isinstance(txt_path, str):
        txt_path = str(txt_path)

    with open(txt_path, "r", encoding="utf-8") as f:
        data = list(map(lambda x: x.rstrip("\n"), f))
    return data
