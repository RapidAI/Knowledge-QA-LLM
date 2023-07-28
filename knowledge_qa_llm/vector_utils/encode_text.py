# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from typing import List, Optional

from sentence_transformers import SentenceTransformer


class EncodeText:
    def __init__(self, model_path: Optional[str] = None) -> None:
        if model_path is None:
            raise EncoderTextError("model_path is None.")

        self.model = SentenceTransformer(model_path)

    def __call__(self, sentences: List[str]):
        if not isinstance(sentences, List):
            sentences = [sentences]
        return self.model.encode(sentences)


class EncoderTextError(Exception):
    pass
