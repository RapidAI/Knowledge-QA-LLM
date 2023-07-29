# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from knowledge_qa_llm.file_loader import FileLoader
from knowledge_qa_llm.llm import ChatGLM26B
from knowledge_qa_llm.utils import make_prompt, read_yaml
from knowledge_qa_llm.vector_utils import DBUtils, EncodeText

config = read_yaml("knowledge_qa_llm/config.yaml")

extract = FileLoader()

# 解析文档
# file_path = "tests/test_files/office/word_example.docx"
# text = extract(file_path)
# sentences = text[0][1]

# 提取特征
embedding_model = EncodeText(config.get("encoder_model_path"))
# embeddings = embedding_model(sentences)

# 插入数据到数据库中
db_tools = DBUtils(config.get("vector_db_path"))
# db_tools.insert(file_path, embeddings, sentences)

llm_engine = ChatGLM26B(api_url=config.get("llm_api_url"))

print("欢迎使用 Knowledge QA LLM，输入内容即可进行对话，stop 终止程序")
while True:
    query = input("\n用户：")
    if query.strip() == "stop":
        break

    embedding = embedding_model(query)

    context, which_file = db_tools.search_local(embedding_query=embedding)

    prompt = make_prompt(query, context, custom_prompt=config.get("DEFAULT_PROMPT"))
    response = llm_engine(prompt, history=None)
    print(response)
