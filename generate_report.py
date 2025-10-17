#!/usr/bin/env python3
"""
Отдельный генератор HTML‑отчёта по логам CK3.
Использует JSON‑файл, созданный ErrorClassifier.save_to_json()
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from html import escape


def load_json(path: str):
    """Загружает JSON‑отчёт"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Ошибка чтения {path}: {e}")
        sys.exit(1)


def generate_html(data, output_path: str):
    """Создаёт HTML‑отчёт из данных"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html_parts = [
        "<!DOCTYPE html>",
        "<html><head><meta charset='UTF-8'>",
        f"<title>CK3 Error Report – {timestamp}</title>",
        """<style>
        body { font-family: 'Segoe UI', sans-serif; margin: 20px; background: #f5f5f5; }
        h1 { color: #333; }
        .category { margin-bottom: 20px; background: #fff; padding: 10px; border-radius: 6px; }
        .category h2 { cursor: pointer; background: #333; color: #fff; padding: 8px; margin: 0; border-radius: 4px; }
        .error-list { display: none; margin-top: 10px; }
        .error { padding: 6px 10px; border-bottom: 1px solid #ddd; }
        .error:nth-child(odd) { background: #fafafa; }
        .file { color: #555; font-size: 0.9em; }
        .type { font-weight: bold; color: #c33; }
        .meta { color: #666; font-size: 0.8em; }
        </style>
        <script>
        document.addEventListener("DOMContentLoaded", () => {
          document.querySelectorAll(".category h2").forEach(el => {
            el.addEventListener("click", () => {
              const div = el.nextElementSibling;
              div.style.display = (div.style.display === 'none') ? 'block' : 'none';
            });
          });
        });
        </script></head><body>""",
        f"<h1>CK3 Error Report</h1><div>Generated on: {timestamp}</div><hr>"
    ]

    # Категории
    for category_block in data:
        category = category_block.get("category")
        errors = category_block.get("errors", [])

        html_parts.append(f"<div class='category'>")
        html_parts.append(f"<h2>{escape(category)} ({len(errors)})</h2>")
        html_parts.append("<div class='error-list'>")
        for e in errors:
            type_ = escape(e.get("type", ""))
            file_ = escape(str(e.get("file", "")))
            line = e.get("line") or ""
            key = escape(str(e.get("key", ""))) if e.get("key") else ""
            element = escape(str(e.get("element", ""))) if e.get("element") else ""
            msg = escape(str(e.get("message", ""))) if e.get("message") else ""
            html_parts.append(
                f"<div class='error'>"
                f"<div class='type'>{type_}</div>"
                f"<div class='file'>{file_} {line}</div>"
                f"<div class='meta'>{key or element}</div>"
                f"<div>{msg}</div>"
                f"</div>"
            )
        html_parts.append("</div></div>")

    html_parts.append("</body></html>")

    Path(output_path).write_text("\n".join(html_parts), encoding="utf-8")
    print(f"✅ HTML‑отчёт сохранён: {output_path}")


def main():
    if len(sys.argv) < 3:
        print("Использование: python generate_report.py parsed_errors.json report.html")
        sys.exit(0)

    input_json = sys.argv[1]
    output_html = sys.argv[2]

    data = load_json(input_json)
    generate_html(data, output_html)


if __name__ == "__main__":
    main()
