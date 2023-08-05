# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from knowledge_qa_llm.llm.qwen7b_chat import Qwen7B

api = "http://qdetest01v.jcpt.zzbm.qianxin-inc.cn:31380/svc-cujf5fikl2zw/"
llm = Qwen7B(api_url=api)


prompt = "杭州有哪些景点？"

response = llm(prompt, history=None)
print(response)
