# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from rapid_rag.file_loader import FileLoader
from rapid_rag.utils import read_yaml
from rapid_rag.vector_utils import DBUtils, EncodeText

config = read_yaml("knowledge_qa_llm/config.yaml")

extract = FileLoader()

# 解析文档
file_path = "长安三万里.pdf"
text = extract(file_path)
sentences = text[file_path][0]

# 提取特征
embedding_model = EncodeText(config.get("encoder_model_path"))
embeddings = embedding_model(sentences)

# 插入数据到数据库中
db_tools = DBUtils(config.get("vector_db_path"))
db_tools.insert(file_path, embeddings, sentences)
