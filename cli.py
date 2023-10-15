# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import uuid
from pathlib import Path

from knowledge_qa_llm.encoder import EncodeText
from knowledge_qa_llm.file_loader import FileLoader
from knowledge_qa_llm.llm import ERNIEBot
from knowledge_qa_llm.utils import make_prompt, read_yaml
from knowledge_qa_llm.vector_utils import DBUtils

config = read_yaml("knowledge_qa_llm/config.yaml")

extract = FileLoader()

# 解析文档
file_path = "tests/test_files/office/word_example.docx"
text = extract(file_path)
sentences = text.get(Path(file_path).name)

# 提取特征
model_path = config.get("Encoder")["m3e-small"]
embedding_model = EncodeText(**model_path)
embeddings = embedding_model(sentences)

# 插入数据到数据库中
db_tools = DBUtils(config.get("vector_db_path"))
uid = str(uuid.uuid1())
db_tools.insert(file_path, embeddings, sentences, uid=uid)

params = config.get("LLM_API")["ERNIEBot"]
llm_engine = ERNIEBot(**params)

print("欢迎使用 🧐 Knowledge QA LLM，输入“stop”终止程序 ")
while True:
    query = input("\n😀 用户: ")
    if query.strip() == "stop":
        break

    embedding = embedding_model(query)

    search_res, search_elapse = db_tools.search_local(embedding_query=embedding)

    context = "\n".join(sum(search_res.values(), []))
    print(f"上下文：\n{context}\n")

    prompt = make_prompt(query, context, custom_prompt=config.get("DEFAULT_PROMPT"))
    response = llm_engine(prompt, history=None)
    print(f"🤖 LLM:\n {response}")
