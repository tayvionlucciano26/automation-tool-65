import json
import os
from typing import Any, Dict, Optional

class ConfigLoader:
    """Loads configuration from a JSON file merging with defaults."""

    def __init__(self, config_file: str = "config.json", defaults: Optional[Dict[str, Any]] = None) -> None:
        self.config_file = config_file
        self.defaults = defaults or {
            "timeout": 30,
            "retries": 3,
            "log_level": "INFO",
            "output_dir": "output",
            "debug": False,
            "max_workers": 4
        }
        self.config: Dict[str, Any] = {}
        self.load_config()

    def load_config(self) -> None:
        """Load config from file if exists, else use defaults."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                self.config = self.defaults.copy()
                self.config.update(loaded)
            except (json.JSONDecodeError, IOError, OSError) as e:
                print(f"Warning: Could not load {self.config_file}: {e}")
                self.config = self.defaults.copy()
        else:
            self.config = self.defaults.copy()
            self.save_config()

    def save_config(self) -> None:
        """Save the current config to file."""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
        except (IOError, OSError) as e:
            print(f"Warning: Could not save config: {e}")

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Retrieve a value from config."""
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a value and persist to file."""
        self.config[key] = value
        self.save_config()

    def get_all(self) -> Dict[str, Any]:
        """Return a copy of the full configuration."""
        return self.config.copy()


# Demonstration
if __name__ == "__main__":
    loader = ConfigLoader("settings.json")
    print("Loaded config:", loader.get_all())
    print("Timeout setting:", loader.get("timeout"))
    loader.set("debug", True)
    print("Updated debug:", loader.get("debug"))
