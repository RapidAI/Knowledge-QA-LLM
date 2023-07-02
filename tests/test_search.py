# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from vector_utils import DBUtils, EncodeText

model = EncodeText()
db = DBUtils('db/Vector.db')

query = '背景'
embedding = model(query)
context, which_file = db.search_local(embedding_query=embedding)
print(context)
print(which_file)
