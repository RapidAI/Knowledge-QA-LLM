# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from pathlib import Path

cur_dir = Path(__file__).resolve().parent

from knowledge_qa_llm.utils import read_yaml
from knowledge_qa_llm.vector_utils import DBUtils, EncodeText

config_path = Path("knowledge_qa_llm") / "config.yaml"
config = read_yaml(config_path)

model = EncodeText(config["encoder_model_path"])
db = DBUtils(config["vector_db_path"])

query = "蔡徐坤"
embedding = model(query)
search_res = db.search_local(embedding_query=embedding, top_k=3)

print(search_res)
print("ok")
