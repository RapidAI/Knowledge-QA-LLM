# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import io
import sqlite3
import time
from typing import List

import faiss
import numpy as np


def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())


def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out, allow_pickle=True)


sqlite3.register_adapter(np.ndarray, adapt_array)
sqlite3.register_converter("array", convert_array)


class DBUtils:
    def __init__(
        self,
        db_path: str,
    ) -> None:
        self.db_path = db_path

        self.table_name = 'embedding_texts'
        self.vector_nums = 0

        self.top_k = 5
        self.max_prompt_length = 4096

        self.connect_db()

    def connect_db(
        self,
    ):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        cur = con.cursor()
        cur.execute(
            f'create table if not exists {self.table_name} (file_name TEXT, embeddings array, texts TEXT)'
        )
        return cur, con

    def load_vectors(
        self,
    ):
        cur, _ = self.connect_db()

        cur.execute(f'select file_name, embeddings, texts from {self.table_name}')
        all_vectors = cur.fetchall()

        self.file_names = np.vstack([v[0] for v in all_vectors]).squeeze()
        all_embeddings = np.vstack([v[1] for v in all_vectors])
        self.all_texts = np.vstack([v[2] for v in all_vectors]).squeeze()

        self.search_index = faiss.IndexFlatIP(all_embeddings.shape[1])
        self.search_index.add(all_embeddings)
        self.vector_nums = len(all_vectors)

    def count_vectors(
        self,
    ):
        cur, _ = self.connect_db()

        cur.execute(f'select file_name from {self.table_name}')
        all_vectors = cur.fetchall()
        return len(all_vectors)

    def search_local(self, embedding_query: np.ndarray):
        cur_vector_nums = self.count_vectors()
        if cur_vector_nums <= 1:
            return None, None

        if cur_vector_nums != self.vector_nums:
            self.load_vectors()

        D, I = self.search_index.search(embedding_query, self.top_k)
        mean_D = np.mean(D[0])

        new_I, texts_nums = [], len(self.all_texts)
        for i in range(len(I[0])):
            D_i = D[0][i]
            I_i = I[0][i]
            if D_i >= mean_D:
                for index in range(I_i - 2, I_i + 4):
                    if 0 <= index < texts_nums:
                        if index not in new_I:
                            new_I.append(index)
            else:
                if I_i not in new_I:
                    new_I.append(I_i)

        from_file_names = [self.file_names[idx] for idx in new_I]
        from_file_names = list(set(from_file_names))
        return '\n'.join(self.all_texts[new_I]), from_file_names

    def insert(self, file_name: str, embeddings: np.ndarray, texts: List):
        cur, con = self.connect_db()

        file_names = [file_name] * len(embeddings)

        print('插入数据中')
        t1 = time.perf_counter()
        insert_sql = f'insert or replace into {self.table_name} (file_name, embeddings, texts) values (?, ?, ?)'
        cur.executemany(insert_sql, list(zip(file_names, embeddings, texts)))
        print(f'insert {len(embeddings)} data cost: {time.perf_counter() - t1}s')
        con.commit()

    def is_exist(self, embeddings, texts):
        cur, _ = self.connect_db()

        search_sql = f'select count(*) from {self.table_name} where embeddings="{embeddings}" and texts="{texts}"'
        cur.execute(search_sql)
        search_nums = cur.fetchall()[0][0]
        if search_nums <= 0:
            return False
        return True

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.cur.close()
        self.con.close()
