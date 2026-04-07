import json
from pathlib import Path
from typing import Any, Dict


class AppSettings:
    """Handles persistent application settings (e.g., optional content toggles)."""

    _SETTINGS_PATH = Path(__file__).parent.parent / "data" / "user_settings.json"
    _DEFAULTS: Dict[str, Any] = {
        "optional_content": {
            "tashas_spells": False,
            "xanathars_spells": False,
        }
    }

    _cache: Dict[str, Any] | None = None

    @classmethod
    def _ensure_file(cls) -> None:
        cls._SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not cls._SETTINGS_PATH.exists():
            cls.save(cls._DEFAULTS)

    @classmethod
    def load(cls) -> Dict[str, Any]:
        if cls._cache is not None:
            return cls._cache

        cls._ensure_file()
        try:
            with open(cls._SETTINGS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            data = {}

        merged = cls._merge_defaults(cls._DEFAULTS, data)
        cls._cache = merged
        return merged

    @classmethod
    def save(cls, data: Dict[str, Any]) -> None:
        cls._SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(cls._SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        cls._cache = data

    @classmethod
    def set_optional_content_flag(cls, key: str, value: bool) -> None:
        settings = cls.load()
        optional = settings.setdefault("optional_content", {})
        optional[key] = bool(value)
        cls.save(settings)

    @classmethod
    def get_optional_content_flag(cls, key: str) -> bool:
        settings = cls.load()
        optional = settings.get("optional_content", {})
        return bool(optional.get(key, False))

    @classmethod
    def _merge_defaults(cls, defaults: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for key, default_value in defaults.items():
            if isinstance(default_value, dict):
                result[key] = cls._merge_defaults(default_value, data.get(key, {}))
            else:
                result[key] = data.get(key, default_value)
        # include any extra keys that might exist in data but not defaults
        for key, value in data.items():
            if key not in result:
                result[key] = value
        return result
