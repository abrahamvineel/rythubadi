from pathlib import Path
import re

def test_no_sql_in_domain():
    python_files = Path("backend/domain").rglob("*.py")
    banned_list = ["select", "create", "insert", "update", "delete"]
    for file in python_files:
        content = file.read_text()
        for keyword in banned_list:
             if re.search(r'\b' + keyword + r'\b', content.lower()):
                assert False, f"{file} SQL queries are present in domain."
                