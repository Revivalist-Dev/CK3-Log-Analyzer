import re
import json
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any, List, DefaultDict
from collections import defaultdict

# 🔹 Используем Python‑файл с паттернами
from error_patterns import error_patterns


# ─────────────────────────────────────────────
# 📘 Dataclass — ParsedError
# ─────────────────────────────────────────────
@dataclass(eq=True)
class ParsedError:
    """Нормализованная структура ошибки из CK3‑лога"""
    category: str
    type: str
    file: Optional[str] = None
    line: Optional[str] = None
    key: Optional[str] = None
    element: Optional[str] = None
    message: Optional[str] = None
    log_line: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────
# ⚙️ Основной класс‑классификатор
# ─────────────────────────────────────────────
class ErrorClassifier:
    """
    Класс‑классификатор логов CK3.
    Теперь использует Python‑файл error_patterns.py вместо YAML.
    """

    def __init__(self, patterns: Optional[Dict[str, Any]] = None):
        # 🔹 Подключаем словарь из error_patterns.py
        self.patterns = patterns or error_patterns
        self.compiled = self._compile_patterns(self.patterns)
        print("📘 Загружены паттерны из Python (error_patterns.py)")

    # ─────────────────────────────────────────
    def _compile_patterns(self, patterns_dict=None):
        """Компилирует все регулярные выражения из словаря pattern"""
        compiled = []
        patterns_dict = patterns_dict or self.patterns

        for category, block in patterns_dict.items():
            for p in block.get("patterns", []):
                try:
                    rgx = re.compile(p["regex"])
                    compiled.append({
                        "regex": rgx,
                        "category": category,
                        "type": p.get("type", "UNKNOWN")
                    })
                except re.error as e:
                    print(f"[RegexError] {category}/{p.get('type')}: {e}")

        return compiled

    # ─────────────────────────────────────────
    def classify_line(self, line: str) -> Optional[ParsedError]:
        """Проверяет одну строку лога против всех паттернов"""
        try:
            for rule in self.compiled:
                m = rule["regex"].search(line)
                if m:
                    data = m.groupdict()
                    return ParsedError(
                        category=rule["category"],
                        type=rule["type"],
                        file=data.get("file") or data.get("file1") or None,
                        line=data.get("line"),
                        key=data.get("key"),
                        element=data.get("element"),
                        message=data.get("message")
                    )
        except Exception as e:
            print(f"[ErrorClassifier] Ошибка классификации строки: {e}\n→ {line.strip()}")
        return None

    # ─────────────────────────────────────────
    def classify_block(self, text: str, deduplicate: bool = True) -> List[ParsedError]:
        """Обрабатывает весь текст лог‑файла"""
        results = []
        seen = set()
        for i, line in enumerate(text.splitlines(), start=1):
            parsed = self.classify_line(line)
            if not parsed:
                continue
            parsed.log_line = i

            if deduplicate:
                # ключ для защиты от дубликатов
                key = (
                    parsed.category,
                    parsed.type,
                    parsed.file,
                    parsed.line,
                    parsed.key,
                    parsed.element,
                    parsed.message,
                )
                if key in seen:
                    continue
                seen.add(key)

            results.append(parsed)
        return results

    # ─────────────────────────────────────────
    def group_by_category(self, errors: List[ParsedError]) -> DefaultDict[str, List[ParsedError]]:
        """Группирует ParsedError по категориям"""
        grouped: DefaultDict[str, List[ParsedError]] = defaultdict(list)
        for e in errors:
            grouped[e.category].append(e)
        return grouped

    # ─────────────────────────────────────────
    def save_to_json(
        self,
        parsed_errors: List[ParsedError],
        path: str,
        group_by_category: bool = True
    ):
        """Сохраняет ошибки в JSON (по категориям или единым списком)"""
        try:
            unique_errors = list({e: None for e in parsed_errors}.keys())

            if group_by_category:
                grouped = defaultdict(list)
                for e in unique_errors:
                    grouped[e.category].append(e.to_dict())
                data = [{"category": cat, "errors": grouped[cat]} for cat in sorted(grouped)]
            else:
                data = [e.to_dict() for e in unique_errors]

            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"[✔] Отчёт сохранён: {path} (уникальных ошибок: {len(unique_errors)})")
        except Exception as e:
            print(f"[ErrorClassifier] Ошибка при сохранении JSON: {e}")