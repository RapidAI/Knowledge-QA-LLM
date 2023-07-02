# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from string import Template


def make_prompt(query: str, context: str, custom_prompt: str = None) -> str:
    if '$query' not in custom_prompt or '$context' not in custom_prompt:
        raise ValueError('prompt中必须含有$query和$context两个值')

    msg_template = Template(custom_prompt)
    message = msg_template.substitute(query=query, context=context)
    return message
