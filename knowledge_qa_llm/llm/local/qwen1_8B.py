# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from modelscope import AutoModelForCausalLM, AutoTokenizer, GenerationConfig


class Qwen1_8B:
    def __init__(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(
            "Qwen/Qwen-1_8B-Chat", revision="master", trust_remote_code=True
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            "Qwen/Qwen-1_8B-Chat", device_map="auto", trust_remote_code=True, fp16=True
        ).eval()

    def __call__(self, text):
        response, history = self.model.chat(self.tokenizer, text, history=None)
