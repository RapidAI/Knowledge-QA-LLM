# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from knowledge_qa_llm.file_loader import ExtractOfficeLoader
from knowledge_qa_llm.llm import ChatGLM26B
from knowledge_qa_llm.utils import make_prompt, read_yaml
from knowledge_qa_llm.vector_utils import DBUtils, EncodeText

config = read_yaml("config.yaml")

print("读取文档")
office_extract = ExtractOfficeLoader()

file_path = "tests/test_files/office/word_example.docx"
text = office_extract(file_path)
sentences = text[0][1]

print("提取特征")
extract_model = EncodeText()
embeddings = extract_model(sentences)

db_tools = DBUtils(config.get("vector_db_path", "db/DefaultVector.db"))
db_tools.insert(file_path, embeddings, sentences)

print("基于faiss，从数据库查询上下文")
query = "蔡徐坤是几班的？"
embedding = extract_model(query)
context, which_file = db_tools.search_local(embedding_query=embedding)
print(context)
print(which_file)

print("模型问答")
llm_engine = ChatGLM26B(api_url=config.get("llm_api_url"))
prompt = make_prompt(query, context, custom_prompt=config.get("DEFAULT_PROMPT"))

response = llm_engine(prompt, history=None)
print(response)
