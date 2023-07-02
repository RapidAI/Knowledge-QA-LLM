# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path
from typing import List

from sentence_transformers import SentenceTransformer

root_dir = Path(__file__).resolve().parent.parent
model_path = root_dir / 'models' / 'm3e-small'


class EncodeText:
    def __init__(self, model_path: str = str(model_path)) -> None:
        self.model = SentenceTransformer(model_path)

    def __call__(self, sentences: List):
        if not isinstance(sentences, List):
            sentences = [sentences]
        return self.model.encode(sentences)
