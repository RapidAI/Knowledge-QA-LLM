# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import json
from typing import List, Optional

import requests


class ERNIEBotTurbo:
    def __init__(
        self, api_url: str = None, api_key: str = None, secret_key: str = None
    ):
        self.api_url = api_url
        self.api_key = api_key
        self.secret_key = secret_key

    def __call__(self, prompt: str, history: Optional[List] = None, **kwargs):
        if not history:
            history = []
        url = self.api_url + self.get_access_token()
        payload = json.dumps({"messages": [{"role": "user", "content": prompt}]})
        headers = {"Content-Type": "application/json"}

        req = requests.request("POST", url, headers=headers, data=payload, timeout=60)
        try:
            rdata = req.json()
            return rdata["result"]
        except Exception as e:
            return f"网络出错:{e}"

    def get_access_token(
        self,
    ):
        url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={self.api_key}&client_secret={self.secret_key}"
        payload = json.dumps("")
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        response = requests.request(
            "POST", url, headers=headers, data=payload, timeout=60
        )
        return response.json().get("access_token")
