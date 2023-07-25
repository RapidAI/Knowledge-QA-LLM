# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import json
from typing import List

import requests


class ChatGLM26B:
    def __init__(self, api_url: str = None):
        self.api_url = api_url

    def __call__(self, prompt: str, history: List, **kwargs):
        data = {"prompt": prompt, "history": history}
        if kwargs:
            temperature = kwargs.get("temperature", 0.1)
            top_p = kwargs.get("top_p", 0.7)
            max_length = kwargs.get("max_length", 4096)

            data.update(
                {"temperature": temperature, "top_p": top_p, "max_length": max_length}
            )
        req = requests.post(self.api_url, data=json.dumps(data), timeout=60)
        try:
            rdata = req.json()
            if rdata["status"] == 200:
                return rdata["response"]
            else:
                return "网络出错"
        except Exception as e:
            return f"网络出错:{e}"


if __name__ == "__main__":
    prompt = "你是谁？"
    history = []
    t = ChatGLM26B()

    res = t(prompt, history)
    print(res)
