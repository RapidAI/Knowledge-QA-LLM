# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import sys
from pathlib import Path

cur_dir = Path(__file__).resolve().parent
root_dir = cur_dir.parent
sys.path.append(str(root_dir))

from knowledge_qa_llm.utils import read_yaml
from knowledge_qa_llm.vector_utils import DBUtils, EncodeText

config_path = root_dir / "config.yaml"
config = read_yaml(config_path)

model = EncodeText(config["encoder_model_path"])
db = DBUtils(config["vector_db_path"])


def test_input_normal():
    query = "背景"
    embedding = model(query)
    context, _ = db.search_local(embedding_query=embedding)

    assert len(context) == 584
