# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from knowledge_qa_llm.llm.qwen7b_chat import Qwen7B_Chat

api = ""
llm = Qwen7B_Chat(api_url=api)


prompt = "杭州有哪些景点？"

response = llm(prompt, history=None)
print(response)
