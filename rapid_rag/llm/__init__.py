# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from .baichuan_7b import BaiChuan7B
from .chatglm2_6b import ChatGLM2_6B
from .ernie_bot_turbo import ERNIEBot
from .internlm_7b import InternLM_7B
from .qwen7b_chat import Qwen7B_Chat
from .openai import OpenAI
from .ollama import Ollama

__all__ = [
    "BaiChuan7B",
    "ChatGLM2_6B",
    "ERNIEBot",
    "Qwen7B_Chat",
    "InternLM_7B",
    "OpenAI",
    "Ollama",
]
