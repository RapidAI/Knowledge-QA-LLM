# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from sentence_transformers import SentenceTransformer

queries = ["手机开不了机怎么办？"]
passages = ["样例段落-1", "样例段落-2"]
instruction = "为这个句子生成表示以用于检索相关文章："
model = SentenceTransformer("assets/models/bge-small-zh")
q_embeddings = model.encode(
    [instruction + q for q in queries], normalize_embeddings=True
)
p_embeddings = model.encode(passages, normalize_embeddings=True)
scores = q_embeddings @ p_embeddings.T

print(scores)
