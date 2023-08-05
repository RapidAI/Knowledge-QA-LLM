# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from knowledge_qa_llm.llm.llama2 import Llama2_7BChat

api = "http://qdetest01v.jcpt.zzbm.qianxin-inc.cn:31380/svc-cu6m8gv5gji9/"
llm = Llama2_7BChat(api_url=api)


prompt = "你是谁？"

response = llm(prompt)
print(response)
