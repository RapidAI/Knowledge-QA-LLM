# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import sys
from pathlib import Path

cur_dir = Path(__file__).resolve().parent
root_dir = cur_dir.parent
sys.path.append(str(root_dir))

import pytest

from rapid_rag.file_loader.office_loader import ExtractOfficeLoader

extracter_office = ExtractOfficeLoader()


test_file_dir = cur_dir / "test_files" / "office"


@pytest.mark.parametrize(
    "file_path, gt1, gt2",
    [
        ("word_example.docx", 221, "我与父亲不"),
        ("ppt_example.pptx", 350, "| 0  "),
        ("excel_with_image.xlsx", 361, "|    "),
    ],
)
def test_extract(file_path, gt1, gt2):
    file_path = test_file_dir / file_path
    extract_res = extracter_office([file_path])

    assert len(extract_res[0][1][0]) == gt1
    assert extract_res[0][1][0][:5] == gt2
