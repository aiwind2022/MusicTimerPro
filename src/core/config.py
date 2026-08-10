import json
from pathlib import Path
from typing import Any

from .constants import (
    DEFAULT_APPEARANCE_MODE,
    DEFAULT_INTERVAL_MINUTES,
    DEFAULT_THEME,
    DEFAULT_VOLUME,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)


class ConfigManager:
    """Load and save application configuration."""

    def __init__(self, config_file: Path | None = None):
        project_root = Path(__file__).resolve().parents[2]

        self.data_directory = project_root / "data"
        self.data_directory.mkdir(parents=True, exist_ok=True)

        self.config_file = (
            config_file
            if config_file is not None
            else self.data_directory / "config.json"
        )

        self.defaults: dict[str, Any] = {
            "interval_minutes": DEFAULT_INTERVAL_MINUTES,
            "volume": DEFAULT_VOLUME,
            "theme": DEFAULT_THEME,
            "appearance_mode": DEFAULT_APPEARANCE_MODE,
            "window_width": WINDOW_WIDTH,
            "window_height": WINDOW_HEIGHT,
            "last_music_directory": "",
            "auto_start": False,
            "shuffle": False,
        }

        self.settings: dict[str, Any] = self.defaults.copy()

        self.load()

    def load(self) -> dict[str, Any]:
        """Load settings from disk."""

        if not self.config_file.exists():
            self.settings = self.defaults.copy()
            self.save()
            return self.settings

        try:
            with self.config_file.open("r", encoding="utf-8") as file:
                stored_settings = json.load(file)

            self.settings = self.defaults.copy()
            self.settings.update(stored_settings)

        except (OSError, json.JSONDecodeError):
            self.settings = self.defaults.copy()
            self.save()

        return self.settings

    def save(self) -> None:
        """Save current settings to disk."""

        self.config_file.parent.mkdir(parents=True, exist_ok=True)

        with self.config_file.open("w", encoding="utf-8") as file:
            json.dump(self.settings, file, indent=4)

    def get(self, key: str, default: Any = None) -> Any:
        """Return a configuration value."""

        return self.settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set and persist a configuration value."""

        self.settings[key] = value
        self.save()

    def update(self, values: dict[str, Any]) -> None:
        """Update multiple configuration values."""

        self.settings.update(values)
        self.save()