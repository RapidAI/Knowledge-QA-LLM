# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from knowledge_qa_llm.encoder import EncodeText
from knowledge_qa_llm.file_loader import FileLoader
from knowledge_qa_llm.llm import Qwen7B_Chat
from knowledge_qa_llm.utils import make_prompt, read_yaml
from knowledge_qa_llm.vector_utils import DBUtils

config = read_yaml("knowledge_qa_llm/config.yaml")

extract = FileLoader()

# 解析文档
# file_path = "tests/test_files/office/word_example.docx"
# text = extract(file_path)
# sentences = text[0][1]

# 提取特征
embedding_model = EncodeText(config.get("Encoder")["m3e-small"])
# embeddings = embedding_model(sentences)

# 插入数据到数据库中
db_tools = DBUtils(config.get("vector_db_path"))
# db_tools.insert(file_path, embeddings, sentences)

llm_engine = Qwen7B_Chat(api_url=config.get("LLM_API")["Qwen7B_Chat"])

print(
    "Welcom to 🧐 Knowledge QA LLM，enter the content to start the conversation, enter stop to terminate the program."
)
while True:
    query = input("\n😀 User：")
    if query.strip() == "stop":
        break

    embedding = embedding_model(query)

    search_res, search_elapse = db_tools.search_local(embedding_query=embedding)

    context = "\n".join(sum(search_res.values(), []))
    print(f"上下文：\n{context}\n")

    prompt = make_prompt(query, context, custom_prompt=config.get("DEFAULT_PROMPT"))
    response = llm_engine(prompt, history=None)
    print(f"🤖 LLM:{response}")
