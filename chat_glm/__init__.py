# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from transformers import AutoModel, AutoTokenizer


class ChatGLM():
    def __init__(self, model_dir: str):
        print('Init ChatGLM tokenizer...')
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir,
                                                       trust_remote_code=True,
                                                       revision="")

        print('Init ChatGLM model...')
        model = AutoModel.from_pretrained(model_dir,
                                          trust_remote_code=True,
                                          revision="").half().cuda()
        self.model = model.eval()

    def stream_chat(self, prompt, history,
                    max_length: int = 2048, top_p: float = 0.7,
                    temperature: float = 0.95):
        response, history = self.model.stream_chat(self.tokenizer,
                                                   prompt, history=history,
                                                   max_length=max_length,
                                                   top_p=top_p,
                                                   temperature=temperature)
        return response, history

    def chat(self, prompt, history,
             max_length: int = 2048, top_p: float = 0.7,
             temperature: float = 0.95):
        response, history = self.model.chat(self.tokenizer,
                                            prompt, history=history,
                                            max_length=max_length, top_p=top_p,
                                            temperature=temperature)
        return response, history
