# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from rapid_rag.llm.llama2 import Llama2_7BChat

api = ""
llm = Llama2_7BChat(api_url=api)


prompt = "你是谁？"

response = llm(prompt)
print(response)
