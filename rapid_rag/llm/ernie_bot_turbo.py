# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from typing import List, Optional

import erniebot


class ERNIEBot:
    def __init__(self, api_type: str = None, access_token: str = None):
        self.api_type = api_type
        self.access_token = access_token

    def __call__(self, prompt: str, history: Optional[List] = None, **kwargs):
        if not history:
            history = []

        response = erniebot.ChatCompletion.create(
            _config_={
                "api_type": self.api_type,
                "access_token": self.access_token,
            },
            model="ernie-bot",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        result = response.get("result", None)
        return result
