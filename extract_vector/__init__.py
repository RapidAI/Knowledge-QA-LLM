# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import sys
from pathlib import Path
from typing import List, Union

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
from text2vec import SentenceModel

from read_file.utils import mkdir, read_txt


class ExtractVector():
    def __init__(self, model_path: str = './text2vec-base-chinese'):
        print(f'Init {model_path}...')
        self.model = SentenceModel(model_path)

    def encode(self, sentences: List,
               save_dir: str = None, file_name: str = None) -> np.ndarray:
        if isinstance(sentences, str):
            return self.model.encode([sentences])

        mkdir(save_dir)

        embedding_path = Path(save_dir) / f'embedding_{file_name}.npy'
        if embedding_path.exists():
            print(f'{embedding_path} exists, return direct.')
            return self.load_npy(embedding_path)

        embeddings = self.model.encode(sentences, device='cuda')
        self.save_vector(embedding_path, embeddings)

        texts_path = Path(save_dir) / f'texts_{file_name}.npy'
        if not texts_path.exists():
            self.save_vector(texts_path, sentences)
        return embeddings

    def save_vector(self, save_path: str, content: np.ndarray):
        np.save(str(save_path), content)

    def load_npy(self, path: Union[Path, str]) -> np.ndarray:
        return np.load(str(path), allow_pickle=True)
