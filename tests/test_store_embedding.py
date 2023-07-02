# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from extract_office_content import ExtractWord

from vector_utils import DBUtils, EncodeText

# 读取文档
word_extract = ExtractWord()

file_path = 'tests/test_files/office/word_example.docx'
text = word_extract(file_path)
sentences = [v.strip() for v in text if v.strip()]

# 提取特征
model = EncodeText()
embeddings = model(sentences)

db_path = 'db/Vector.db'
db_tools = DBUtils(db_path)

db_tools.insert(file_path, embeddings, sentences)

print('ok')
