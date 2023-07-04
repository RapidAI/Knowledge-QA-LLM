# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from datetime import datetime
from pathlib import Path
from string import Template

import yaml


def make_prompt(query: str, context: str, custom_prompt: str = None) -> str:
    if "$query" not in custom_prompt or "$context" not in custom_prompt:
        raise ValueError("prompt中必须含有$query和$context两个值")

    msg_template = Template(custom_prompt)
    message = msg_template.substitute(query=query, context=context)
    return message


def read_yaml(yaml_path):
    with open(yaml_path, "rb") as f:
        data = yaml.load(f, Loader=yaml.Loader)
    return data


def mkdir(dir_path):
    Path(dir_path).mkdir(parents=True, exist_ok=True)


def get_timestamp():
    return datetime.strftime(datetime.now(), "%Y-%m-%d-%H-%M-%S")
