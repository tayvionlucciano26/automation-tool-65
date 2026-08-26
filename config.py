import os
from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Any] = {
    "app_name": "automation-tool-65",
    "timeout": 30,
    "retries": 3,
    "debug_mode": False,
    "log_level": "INFO",
}

class ConfigLoader:
    """Loads and manages application configuration with default fallbacks."""

    def __init__(self, custom_config: Dict[str, Any] = None):
        self._config = DEFAULT_CONFIG.copy()
        if custom_config:
            self._config.update(custom_config)

    def get(self, key: str) -> Any:
        """Retrieve a configuration value by key, checking environment variables first."""
        env_key = f"AUTOTOOL_{key.upper()}}"
        if env_key in os.environ:
            return os.environ[env_key]
        return self._config.get(key)

    def load_from_env(self) -> None:
        """Override configuration values from matching environment variables."""
        for key in self._config:
            env_key = f"AUTOTOOL_{key.upper()}"
            if env_key in os.environ:
                val = os.environ[env_key]
                if isinstance(self._config[key], bool):
                    self._config[key] = val.lower() in ("true", "1", "yes")
                elif isinstance(self._config[key], int):
                    self._config[key] = int(val)
                else:
                    self._config[key] = val

    @property
    def all(self) -> Dict[str, Any]:
        """Return the complete configuration dictionary."""
        return self._config
