# -*- encoding: utf-8 -*-
# @Author: Leo Peng
# @Contact: leo@promptcn.com
from typing import List, Optional

import openai


class OpenAI:
    def __init__(self, base_url: str = None, api_key: str = None, model: str = "gpt-4o"):
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        self.client = openai.OpenAI(base_url=self.base_url, api_key=self.api_key)
    
    def __call__(self, prompt: str, history: Optional[List] = None, **kwargs):
        if not history:
            history = []

        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model,
        )
        result = response.choices[0].message.content
        return result
