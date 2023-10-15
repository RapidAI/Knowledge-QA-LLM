# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from typing import List

import erniebot
import numpy as np


class ErnieEncodeText:
    def __init__(self, api_type: str, access_token: str):
        erniebot.api_type = api_type
        erniebot.access_token = access_token

    def __call__(self, sentences: List[str]):
        if not isinstance(sentences, List):
            sentences = [sentences]

        response = erniebot.Embedding.create(
            model="ernie-text-embedding",
            input=sentences,
        )
        datas = response.get("data", None)
        if not datas:
            return None

        embeddings = np.array([v["embedding"] for v in datas])
        return embeddings
