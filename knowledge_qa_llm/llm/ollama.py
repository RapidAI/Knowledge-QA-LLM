# -*- encoding: utf-8 -*-
# @Author: Leo Peng
# @Contact: leo@promptcn.com
from typing import List, Optional

import ollama


class Ollama:
    def __init__(self, host: str = "http://localhost:11434", model: str = None):
        self.host = host
        self.model = model
        self.client = ollama.Client(host=self.host)
    
    def __call__(self, prompt: str, history: Optional[List] = None, **kwargs):
        if not history:
            history = []

        response = self.client.chat(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model,
        )
        result = response['message']['content']
        return result
