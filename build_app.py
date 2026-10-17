"""Make app.py from the code cells of business_agent.ipynb.

The script skips the test cells (tag "test") and the print lines at the top level of a cell.
Run it after each change in the notebook: python build_app.py
"""
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

HEADER = '''"""CampusNest Assistant: the chatbot as a standalone Gradio app.

This file is made from business_agent.ipynb by build_app.py. Do not edit it by hand.
To start the chatbot, run: python app.py
"""
import os
from pathlib import Path

# Use the project folder, so that the paths "me", "logs" and ".env" work from any folder.
os.chdir(Path(__file__).resolve().parent)'''


def without_top_level_prints(source):
    """Remove the print calls at the top level of the code. Keep the print calls in functions (the logs)."""
    lines = source.splitlines()
    for node in reversed(ast.parse(source).body):
        is_print = isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and getattr(node.value.func, "id", None) == "print"
        if is_print:
            del lines[node.lineno - 1 : node.end_lineno]
    return "\n".join(lines).strip()


def main():
    notebook = json.loads((ROOT / "business_agent.ipynb").read_text(encoding="utf-8"))
    parts = [HEADER]
    for cell in notebook["cells"]:
        source = "".join(cell["source"]).strip()
        is_test = "test" in cell.get("metadata", {}).get("tags", [])
        if cell["cell_type"] == "code" and source and not is_test:
            parts.append(without_top_level_prints(source))
    (ROOT / "app.py").write_text("\n\n\n".join(part for part in parts if part) + "\n", encoding="utf-8")
    print(f"app.py written from {len(parts) - 1} code cells.")


if __name__ == "__main__":
    main()
