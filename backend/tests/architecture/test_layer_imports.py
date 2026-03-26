from pathlib import Path
import ast

def test_domain_has_no_infrastructre_imports():
    python_files = Path("backend/domain").rglob("*.py")
    banned_list = ["httpx", "supabase", "redis", "fastapi", "pydantic", "anthropic", "mqtt"]
    for file in python_files:
        parsed = ast.parse(file.read_text())
        nodes = ast.walk(parsed)
        for node in nodes:
            if (isinstance(node, ast.ImportFrom) and node.module in banned_list) or (isinstance(node, ast.Import) and node.names[0].name in banned_list):
                assert False, f"{file} imports banned module: {node.module}"
                