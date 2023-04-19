# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import faiss
from pathlib import Path
import numpy as np


class SearchVector():
    def __init__(self, embedding_dir: str) -> None:
        pre_embeddings, pre_texts = self.pre_load(embedding_dir)

        self.search_index = faiss.IndexFlatIP(pre_embeddings.shape[1])
        self.search_index.add(pre_embeddings)
        self.pre_texts = pre_texts

        self.top_k = 5
        self.max_prompt_length = 4096

    def pre_load(self, embedding_dir: str):
        embedding_list = list(Path(embedding_dir).glob('embedding_*.npy'))
        texts_list = list(Path(embedding_dir).glob('texts*.npy'))

        embeddings = np.concatenate([np.load(str(path), allow_pickle=True)
                                     for path in embedding_list], axis=0)
        texts = np.concatenate([np.load(str(path), allow_pickle=True)
                               for path in texts_list], axis=0)
        return embeddings, texts

    def __call__(self, input_txt: str, embedding_query: np.ndarray):
        D, I = self.search_index.search(embedding_query, self.top_k)

        mean_D = np.mean(D[0])
        new_I, texts_nums = [], len(self.pre_texts)
        for i in range(len(I[0])):
            D_i = D[0][i]
            I_i = I[0][i]
            if D_i >= mean_D:
                for index in range(I_i-2, I_i+4):
                    if 0 <= index < texts_nums:
                        if index not in new_I:
                            new_I.append(index)
            else:
                if I_i not in new_I:
                    new_I.append(I_i)

        text = '\n'.join(self.pre_texts[new_I])
        prompt = f'背景：{text}\n\n请根据上述背景回答：{input_txt}？'
        prompt = prompt[:self.max_prompt_length]
        return prompt


if __name__ == '__main__':
    embedding_dir = 'embeddings'
    s = SearchVector(embedding_dir)

    print('ok')
