# ════════════════════════════════════════════════════════════════════════════
# CK3 / Paradox – Unified Error Patterns (Python version)
# Поддерживается классом ErrorClassifier
# Версия: 2025‑10‑rebuild + merged update
# ════════════════════════════════════════════════════════════════════════════

error_patterns = {
    # ─────────────────────────────────────────────
    # Localization / data‑lookup / scripting references
    # ─────────────────────────────────────────────
    "unlocalized_like": {
        "description": "Ошибки, связанные с отсутствием локализаций, game concepts и data‑ссылками",
        "patterns": [
            {"type": "MISSING_LOC_ENTRY",
             "regex": r"Missing loc\s+(?P<key>[\w.\-]+):\s*\"(?P<message>[^\"]+)\""},
            {"type": "MISSING_FAITH_LOC",
             "regex": r"faith\s+'(?P<element>[^']+)':\s+missing custom localization\s+'(?P<key>[^']+)'"}, 
            {"type": "UNRECOGNIZED_LOC_KEY",
             "regex": r"Unrecognized loc key\s+(?P<key>[a-zA-Z0-9_.\-]+).*file:\s+(?P<file>[^\s]+)\s+line:\s*(?P<line>\d+)"},
            {"type": "LOC_DATA_ERROR",
             "regex": r"Data error in loc string\s+'(?P<key>[^']+)'"}, 
            {"type": "MISSING_GAME_CONCEPT",
             "regex": r"Missing game concept\s+'(?P<key>[^']+)'\s+for text\s+'(?P<message>[^']+)'"}, 
            {"type": "INVALID_CUSTOM_TEXT_OBJECT",
             "regex": r"Object of type\s+'(?P<element>[^']+)'\s+is not valid for\s+'(?P<key>[^']+)'"}, 
            {"type": "MISSING_DATA_FUNCTION",
             "regex": r"Could not find data system function\s+'(?P<key>[^']+)'\s+in\s+'.+'"}, 
            {"type": "FAILED_CONVERT_STATEMENT",
             "regex": r"Failed (?:to\s)?convert(?:ing)? statement.*?'(?P<element>[^']+)'"}
        ]
    },

    # ─────────────────────────────────────────────
    # GUI parsing (обновлено)
    # ─────────────────────────────────────────────
    "gui": {
        "description": "Ошибки интерфейса (onclick, tooltip, widget, localize, duplicate)",
        "patterns": [
            # восстановлен старый широкий парсер ошибок
            {"type": "GUI_PARSE_ERROR",
             "regex": r"gui/[^\s:]+:(?P<line>\d+)\s+-\s+Failed parsing data statement\s+'(?P<message>[^']+)'"},

            {"type": "GUI_INVALID_WIDGET",
             "regex": r"gui/[^\s:]+:(?P<line>\d+)\s+-\s+'(?P<element>[^']+)'\s+is not a valid (?:widget|type|property)"},

            # из копии: вернули старый «хвост», чтобы ловило варианты с цифрами
            {"type": "GUI_DUPLICATE_PROPERTY",
             "regex": r"gui/[^\s:]+:(?P<line>\d+)\s*-\s*Duplicate property\s+'(?P<element>[^']+)'(?:\(\d+\))?"},

            {"type": "UNLOCALIZED_GUI_TEXT",
             "regex": r"Unlocalized text\s+'(?P<key>[^']+)'\s+at\s+(?P<file>gui/[^\s:]+):(?P<line>\d+)"},

            {"type": "GUI_FAILED_READING_PROPERTY",
             "regex": r"failed reading property, at line\s+(?P<line>\d+)\s+in file\s+(?P<file>gui/[^\s]+)"},
        ]
    },

    # ─────────────────────────────────────────────
    # Localization structure and encoding (обновлено)
    # ─────────────────────────────────────────────
    "localization": {
        "description": "Ошибки локализационных файлов (.yml): символы, кавычки, токены, BOM",
        "patterns": [
            {"type": "LOC_ILLEGAL_CHAR",
             "regex": r"Illegal localization break character\s+`(?P<char>.+)`.*line\s+(?P<line>\d+).*in\s+(?P<file>[^\s]+)"},

            {"type": "LOC_MISSING_QUOTE",
             "regex": r"Missing quoted string value for key\s+'(?P<key>[^']+)'.*line\s+(?P<line>\d+).*in\s+(?P<file>[^\s]+)"},

            # вернули менее жёсткий вариант "Missing colon"
            {"type": "LOC_MISSING_COLON",
             "regex": r"Missing colon.*separator.*line\s+(?P<line>\d+).+in\s+(?P<file>[^\s]+)"},

            {"type": "LOC_UNEXPECTED_TOKEN",
             "regex": r"Unexpected localization token\s+'(?P<element>[^']+)'.*line\s+(?P<line>\d+).+in\s+(?P<file>[^\s]+)"},

            {"type": "LOC_INVALID_HEADER_INDENT",
             "regex": r"Invalid localization header indentation.*line\s+(?P<line>\d+).+in\s+(?P<file>[^\s]+)"},

            {"type": "LOC_INVALID_CHAR_IN_KEY",
             "regex": r"Invalid character\s+'(?P<char>[^']+)'\s+in key name\s+'(?P<key>[^']+)'.+in\s+(?P<file>[^\s]+)"},

            {"type": "LOC_HASH_COLLISION",
             "regex": r"Localization key hash collision.*Key\s+'(?P<key1>[^']+)'\s+and\s+'(?P<key2>[^']+)'.*hash"},

            {"type": "MISSING_UTF8_BOM",
             "regex": r"Missing UTF8 BOM in\s+'(?P<file>[^\']+)'"},
        ]
    },

    # ─────────────────────────────────────────────
    # Duplicate localization keys
    # ─────────────────────────────────────────────
    "duplicate_loc_keys": {
        "description": "Дублирующиеся ключи локализации",
        "patterns": [
            {"type": "DUPLICATE_LOC_KEY",
             "regex": r"Duplicate localization key\.\s+Key\s+'(?P<key>[^']+)'\s+is defined in both\s+'(?P<file>[^']+)'\s+and\s+'(?P<file2>[^']+)'"}
        ]
    },

    # ─────────────────────────────────────────────
    # Encoding / BOM / charset
    # ─────────────────────────────────────────────
    "encoding": {
        "description": "Ошибки кодировки (UTF‑8 BOM)",
        "patterns": [
            {"type": "ENCODING_ERROR",
             "regex": r"File\s+'?(?P<file>[^'\s]+)'?\s+should be in utf8\-bom encoding"}
        ]
    },

    # ─────────────────────────────────────────────
    # Defines
    # ─────────────────────────────────────────────
    "defines": {
        "description": "Ошибки defines.txt: неверные значения, диапазоны",
        "patterns": [
            {"type": "INVALID_DEFINE_VALUE",
             "regex": r"Define\s+'(?P<key>[^']+)'\s+not valid with given value,\s*reason:\s*(?P<message>.+)"}
        ]
    },

    # ─────────────────────────────────────────────
    # MOD descriptor
    # ─────────────────────────────────────────────
    "mod_descriptor": {
        "description": "Ошибки descriptor.mod и ugc_*.mod",
        "patterns": [
            {"type": "INVALID_SUPPORTED_VERSION",
             "regex": r"Invalid supported_version in file:\s+(?P<file>mod/[^\s]+)\s+line:\s*(?P<line>\d+)"}
        ]
    },

    # ─────────────────────────────────────────────
    # Content structures (dynasties, holdings)
    # ─────────────────────────────────────────────
    "content_struct": {
        "description": "Ошибки парсера игровых файлов (dynasties, holdings, script‑values)",
        "patterns": [
            {"type": "MISSING_DYNASTY_NAME",
             "regex": r"Missing name for dynasty\s+(?P<element>\S+)\s+in file\s+(?P<file>[^\s:]+):(?P<line>\d+)"},
            {"type": "UNEXPECTED_TOKEN",
             "regex": r"Unexpected token:\s*(?P<element>[\w\-\_]+),\s+near line:\s*(?P<line>\d+).+file:\s+\"(?P<file>[^\"]+)\""},
            {"type": "INVALID_BUILDING_TYPE",
             "regex": r"Invalid building type\s+(?P<element>[\w\-\_]+),\s+at file:\s+(?P<file>[^\s]+)\s+line:\s*(?P<line>\d+)"}
        ]
    },

    # ─────────────────────────────────────────────
    # Script core (triggers / effects / actions)
    # ─────────────────────────────────────────────
    "script_core": {
        "description": "Ошибки эффектов, триггеров и on_action",
        "patterns": [
            {"type": "UNKNOWN_EFFECT",
             "regex": r"Unknown effect\s+(?P<element>\S+)\s+at\s+file:\s+(?P<file>[^\s]+)\s+line:\s*(?P<line>\d+)"},
            {"type": "UNKNOWN_TRIGGER",
             "regex": r"Unknown trigger\s+(?P<element>\S+)\s+at\s+file:\s+(?P<file>[^\s]+)\s+line:\s*(?P<line>\d+)"},
            {"type": "UNKNOWN_ON_ACTION",
             "regex": r"Unknown on_action\s+(?P<element>\S+)\s+at\s+file:\s+(?P<file>[^\s]+)\s+line:\s*(?P<line>\d+)"},
            {"type": "SCRIPT_SYSTEM_ERROR",
             "regex": r"Script system error!\s*Error:\s*(?P<message>.+)"}
        ]
    },

    # ─────────────────────────────────────────────
    # Gene / DNA / Ethnicity
    # ─────────────────────────────────────────────
    "gene_data": {
        "description": "Ошибки ДНК‑данных и шаблонов внешности",
        "patterns": [
            {"type": "UNKNOWN_GENE_TEMPLATE",
             "regex": r"Unknown\s+(?P<element>gene_[^ ]+)\s+gene template\s+(?P<key>[^ ]+)\s+at file:\s+(?P<file>[^\s]+)\s+line:\s*(?P<line>\d+)"},
            {"type": "INVALID_GENE_TEMPLATE_KEY",
             "regex": r"invalid gene template key\s+'(?P<key>[^']+)'\s+for gene category\s+(?P<element>\w+)\s+at file:\s+(?P<file>[^\s]+)\s+line:\s*(?P<line>\d+)"}
        ]
    },

    # ─────────────────────────────────────────────
    # GFX / meshes / materials
    # ─────────────────────────────────────────────
    "gfx": {
        "description": "Ошибки ассетов (текстуры, меши, материалы)",
        "patterns": [
            {"type": "MISSING_TEXTURE",
             "regex": r"VFSOpen Error:\s*(?P<file>gfx/[^\s']+\.dds)\s+not found"},
            {"type": "MISSING_TEXTURE_DIRECT",
             "regex": r"Failed to find texture\s+'(?P<file>[^']+\.dds)'"},
            {"type": "MATERIAL_CREATION_ERROR",
             "regex": r"Failed to create material with shader\s+(?P<element>\S+).*in\s+(?P<file>gfx/[^\)]+)\)"},
            {"type": "UVSET_INVALID_TRIANGLE",
             "regex": r"UV-Set:\s*\d+\s+in mesh\s+'(?P<element>[^']+)'\s+in file\s+'(?P<file>[^']+\.mesh)'.*no valid triangle"}
        ]
    },

    # ─────────────────────────────────────────────
    # Assets advanced
    # ─────────────────────────────────────────────
    "assets_advanced": {
        "description": "Дубли ассетов и анимационные предупреждения",
        "patterns": [
            {"type": "DUPLICATE_ENTITY",
             "regex": r"Duplicate of\s+(?P<element>[^ ]+)\s+added to entity system"},
            {"type": "ANIMATION_ONE_FRAME",
             "regex": r"Animation has only one sample:\s*(?P<element>\S+)"}
        ]
    },

    # ─────────────────────────────────────────────
    # Flags and variables (новая категория)
    # ─────────────────────────────────────────────
    "flags_and_vars": {
        "description": "Ошибки использования флагов и переменных",
        "patterns": [
            {"type": "FLAG_USED_BUT_NOT_SET",
             "regex": r"Flag '(?P<element>[^']+)' is used but is never set"},
            {"type": "FLAG_SET_BUT_NOT_USED",
             "regex": r"Flag '(?P<element>[^']+)' is set but is never used"},
            {"type": "VARIABLE_USED_BUT_NOT_SET",
             "regex": r"Variable '(?P<element>[^']+)' is used but is never set"}
        ]
    },

    # ─────────────────────────────────────────────
    # Generic fallback
    # ─────────────────────────────────────────────
    "generic": {
        "description": "Общие ошибки и fallback‑сообщения движка",
        "patterns": [
            {"type": "WARNING_GENERIC",
             "regex": r"Warning:\s*(?P<message>.+)"},
            {"type": "ERROR_GENERIC",
             "regex": r"Error:\s*(?P<message>.+)"},
            {"type": "ERROR_ENGINE",
             "regex": r"\$E\$\s*(?P<message>.+)"}
        ]
    },

    # ─────────────────────────────────────────────
    # Unrecognized localization key (legacy)
    # ─────────────────────────────────────────────
    "unrecognized_loc_key": {
        "description": "Отдельная группа Unrecognized loc key сообщений",
        "patterns": [
            {"type": "UNRECOGNIZED_LOC_KEY_NEAR",
             "regex": r"Unrecognized loc key\s+(?P<key>[\w.\-]+)\.\s+Near file:\s+(?P<file>[^\s]+)\s+line:\s+(?P<line>\d+)"},
            {"type": "UNRECOGNIZED_LOC_KEY_FILE_CAT",
             "regex": r"Unrecognized loc key\s+(?P<key>[\w.\-]+)\.\s+file:\s+(?P<file>[^\s]+)\s+line:\s+(?P<line>\d+)"},
            {"type": "UNRECOGNIZED_LOC_KEY_SIMPLE",
             "regex": r"Unrecognized loc key\s+(?P<key>[\w.\-]+)\.\s+file:\s+(?P<file>[^\s]+)\s+line:\s+(?P<line>\d+)"}
        ]
    },
}
