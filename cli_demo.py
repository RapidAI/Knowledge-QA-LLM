# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path
import sys

import faiss
import numpy as np

from extract_vector import ExtractVector
from chat_glm import ChatGLM
from read_file import read_txt


def process(prompt: str):
    embedding_query = extracter.encode(prompt, )

    k = 50
    D, I = search_index.search(embedding_query, k)
    mean_D = np.mean(D[0])
    new_I, texts_nums = [], len(sentences)
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

    text = '\n'.join(sentences[new_I])
    max_prompt_length = 4096
    prompt = '请根据以下内容回答：'+prompt+'\n'
    prompt += text
    prompt = prompt[:max_prompt_length]
    return prompt


if __name__ == '__main__':
    model_dir = 'models/chatglm-6b-int4'
    chat_glm = ChatGLM(model_dir)

    model_path = './models/text2vec-base-chinese'
    extracter = ExtractVector(model_path)

    txt_path = 'test_files/1.txt'
    sentences = read_txt(txt_path)
    save_dir = 'embeddings'
    embeddings = extracter.encode(sentences, save_dir,
                                  file_name=Path(txt_path).stem)

    search_index = faiss.IndexFlatIP(embeddings.shape[1])
    search_index.add(embeddings)
    sentences = np.array(sentences)

    prompt = '你好'
    result = process(prompt)
    print(result)

    history = [[None, None]]
    while True:
        query = input("Input your question 请输入问题：")
        if query.strip() == 'stop':
            sys.exit()

        response, history = chat_glm.chat(query, history)
        print('OUTPUT:')
        print(response)
