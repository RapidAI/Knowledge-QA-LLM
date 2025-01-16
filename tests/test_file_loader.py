# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
from rapid_rag.file_loader.main import FileLoader

loader = FileLoader()

file_dir = "tests/test_files"

res = loader(file_dir)
print("ok")
