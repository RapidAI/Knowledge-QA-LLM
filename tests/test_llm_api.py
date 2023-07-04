# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from llm import ChatGLM26B
from utils import read_yaml

config = read_yaml("config.yaml")

llm_model = ChatGLM26B(config.get("llm_api_url"))

prompt = "你是谁？"
history = []

res = llm_model(prompt, history)
print(res)
