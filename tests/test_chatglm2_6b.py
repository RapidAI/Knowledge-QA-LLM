# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import sys
from pathlib import Path

cur_dir = Path(__file__).resolve().parent
root_dir = cur_dir.parent
sys.path.append(str(root_dir))

from knowledge_qa_llm.llm import ChatGLM2_6B
from knowledge_qa_llm.utils import read_yaml

config_path = root_dir / "knowledge_qa_llm" / "config.yaml"
config = read_yaml(config_path)

llm_model = ChatGLM2_6B(config.get("LLM_API")["ChatGLM2_6B"])


def test_normal_input():
    prompt = "你是谁？"
    history = []

    res = llm_model(prompt, history)

    assert (
        res
        == "我是一个名为 ChatGLM2-6B 的人工智能助手，是基于清华大学 KEG 实验室和智谱 AI 公司于 2023 年共同训练的语言模型开发的。我的任务是针对用户的问题和要求提供适当的答复和支持。"
    )
