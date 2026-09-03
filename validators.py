import os
import re
from urllib.parse import urlparse

# Regular expression for simple email validation
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


def is_valid_url(url: str) -> bool:
    """Check if a given string is a properly formatted URL."""
    if not url:
        return False
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def is_valid_email(email: str) -> bool:
    """Validate email format using a standard regular expression."""
    if not email:
        return False
    return bool(EMAIL_REGEX.match(email))


def is_safe_path(path: str, base_directory: str) -> bool:
    """Ensure the path is within the allowed base directory boundary."""
    if not path or not base_directory:
        return False
    resolved_base = os.path.abspath(base_directory)
    resolved_path = os.path.abspath(path)
    return resolved_path.startswith(resolved_base)


def validate_config_structure(config: dict, required_fields: list) -> None:
    """Validate that all required fields exist in the configuration dictionary.

    Raises:
        ValueError: If a required key is missing or the config is invalid.
    """
    if not isinstance(config, dict):
        raise ValueError("Configuration must be a dictionary")

    missing_fields = [field for field in required_fields if field not in config]
    if missing_fields:
        raise ValueError(
            f"Missing required configuration fields: {', '.join(missing_fields)}"
        )
