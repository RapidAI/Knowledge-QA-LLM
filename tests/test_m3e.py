# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import sys
from pathlib import Path

cur_dir = Path(__file__).resolve().parent
root_dir = cur_dir.parent
sys.path.append(str(root_dir))

from knowledge_qa_llm.utils import read_yaml
from knowledge_qa_llm.vector_utils import EncodeText

config_path = root_dir / "config.yaml"
config = read_yaml(config_path)
model = EncodeText(config["encoder_model_path"])


def test_normal_input():
    sentences = [
        "* Moka 此文本嵌入模型由 MokaAI 训练并开源，训练脚本使用 uniem",
        "* Massive 此文本嵌入模型通过**千万级**的中文句对数据集进行训练",
        "* Mixed 此文本嵌入模型支持中英双语的同质文本相似度计算，异质文本检索等功能，未来还会支持代码检索，ALL in one",
    ]

    embeddings = model(sentences)
    assert embeddings.shape == (3, 512)
