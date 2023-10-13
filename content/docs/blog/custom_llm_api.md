---
weight: 320
date: "2023-09-11"
author: "SWHL"
title: "自定义LLM API"
icon: "tune"
toc: true
publishdate: "2023-09-08"
---

{{% alert context="info" %}}该项目的LLM部分是独立的，用户可在**knowledge_qa_llm/llm**自定义配置所需的LLM接口。{{% /alert %}} 

下面以自定义支持InterLM-7b大模型为例，说明如何支持的。

#### 1. 下载InterLM模型到本地，具体如何下载，参见[internlm-7b](https://huggingface.co/internlm/internlm-7b)。
#### 2. 编写模型的推理代码，这一点可以参考[ChatGLM's API](https://github.com/THUDM/ChatGLM-6B/blob/main/api.py)的实现。只需要替换模型加载部分为InterLM的即可。具体如下：

```python {linenos=table}
from fastapi import FastAPI, Request
from transformers import AutoTokenizer, AutoModel
import uvicorn, json, datetime
import torch

DEVICE = "cuda"
DEVICE_ID = "0"
CUDA_DEVICE = f"{DEVICE}:{DEVICE_ID}" if DEVICE_ID else DEVICE


def torch_gc():
    if torch.cuda.is_available():
        with torch.cuda.device(CUDA_DEVICE):
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()


app = FastAPI()


@app.post("/")
async def create_item(request: Request):
    global model, tokenizer
    json_post_raw = await request.json()
    json_post = json.dumps(json_post_raw)
    json_post_list = json.loads(json_post)
    prompt = json_post_list.get('prompt')
    history = json_post_list.get('history')
    max_length = json_post_list.get('max_length')
    top_p = json_post_list.get('top_p')
    temperature = json_post_list.get('temperature')
    response, history = model.chat(tokenizer,
                                prompt,
                                history=history,
                                max_new_tokens=max_length if max_length else 2048,
                                top_p=top_p if top_p else 0.7,
                                temperature=temperature if temperature else 0.95)
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    answer = {
        "response": response,
        "history": history,
        "status": 200,
        "time": time
    }
    log = "[" + time + "] " + '", prompt:"' + prompt + '", response:"' + repr(response) + '"'
    print(log)
    torch_gc()
    return answer


if __name__ == '__main__':
    tokenizer = AutoTokenizer.from_pretrained("internlm/internlm-chat-7b-v1_1", trust_remote_code=True)
    model = AutoModel.from_pretrained("internlm/internlm-chat-7b-v1_1", trust_remote_code=True).half().cuda()
    model.eval()
    uvicorn.run(app, host='0.0.0.0', port=8000, workers=1)
```

#### 3. 编写`knowledge_qa_llm/llm/internlm_7b.py`

```python {linenos=table}
import json
from typing import List, Optional

import requests


class InternLM_7B:
    def __init__(self, api_url: str = None):
        self.api_url = api_url

    def __call__(self, prompt: str, history: Optional[List] = None, **kwargs):
        if not history:
            history = []

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
            return "Network error"
        except Exception as e:
            return f"Network error:{e}"
```

#### 4. 导入`knowledge_qa_llm/llm/__init__.py`
```python {linenos=table}
from .baichuan_7b import BaiChuan7B
from .chatglm2_6b import ChatGLM2_6B
from .ernie_bot_turbo import ERNIEBotTurbo
from .qwen7b_chat import Qwen7B_Chat
from .internlm_7b import InternLM_7B

__all__ = ["BaiChuan7B", "ChatGLM2_6B", "ERNIEBotTurbo", "Qwen7B_Chat", "InternLM_7B"]
```

#### 5. 更改`knowledge_qa_llm/config.yaml`.
```yaml {linenos=table}
LLM_API:
    InternLM_7B: your_api
    Qwen7B_Chat: your_api
    ChatGLM2_6B: your_api
    BaiChuan7B: your_api
```

#### 6. 启动
```bash {linenos=table}
streamlit run web_ui.py
```
