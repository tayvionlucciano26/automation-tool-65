import os
import json
from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Any] = {
    "app_name": "automation-tool-65",
    "debug": False,
    "max_retries": 3,
    "timeout": 30.0,
    "log_level": "INFO"
}

class ConfigLoader:
    """Loads and manages application configuration with default values."""

    def __init__(self, config_path: str = "config.json") -> None:
        self.config_path = config_path
        self.config = DEFAULT_CONFIG.copy()

    def load(self) -> Dict[str, Any]:
        """Loads config from file and overrides with matching environment variables."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                    if isinstance(file_config, dict):
                        self.config.update(file_config)
            except (json.JSONDecodeError, IOError):
                # Suppress exceptions to ensure default configuration fallback
                pass

        # Override config using prefixed environment variables
        for key in self.config:
            env_key = f"AUTO_{key.upper()}"
            if env_key in os.environ:
                self._apply_env_override(key, os.environ[env_key])

        return self.config

    def _apply_env_override(self, key: str, value: str) -> None:
        """Casts env variable values to match default type schemas."""
        default_val = DEFAULT_CONFIG[key]
        if isinstance(default_val, bool):
            self.config[key] = value.lower() in ("true", "1", "yes")
        elif isinstance(default_val, int):
            try:
                self.config[key] = int(value)
            except ValueError:
                pass
        elif isinstance(default_val, float):
            try:
                self.config[key] = float(value)
            except ValueError:
                pass
        else:
            self.config[key] = value
