# validators.py - Error handling for edge cases in automation-tool-65
import re
from typing import Any, Dict
class ValidationError(Exception):
    pass
def validate_string(value: Any, min_length: int = 1, max_length: int = 100, allow_none: bool = False) -> str:
    if value is None:
        if allow_none:
            return ""
        raise ValidationError("Value cannot be None")
    if not isinstance(value, str):
        raise ValidationError(f"Expected string, got {type(value).__name__}")
    stripped = value.strip()
    if len(stripped) < min_length:
        raise ValidationError(f"String too short, minimum {min_length} characters")
    if len(stripped) > max_length:
        raise ValidationError(f"String too long, maximum {max_length} characters")
    return stripped
def validate_positive_int(value: Any, allow_none: bool = False) -> int:
    if value is None:
        if allow_none:
            return 0
        raise ValidationError("Value cannot be None")
    try:
        num = int(value)
    except (ValueError, TypeError) as exc:
        raise ValidationError(f"Invalid integer: {value}") from exc
    if num <= 0:
        raise ValidationError(f"Value must be positive, got {num}")
    return num
def validate_email(value: Any, allow_none: bool = False) -> str:
    if value is None:
        if allow_none:
            return ""
        raise ValidationError("Value cannot be None")
    if not isinstance(value, str):
        raise ValidationError("Email must be a string")
    stripped = value.strip()
    if not stripped:
        raise ValidationError("Email cannot be empty")
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, stripped):
        raise ValidationError("Invalid email format")
    return stripped
def validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(config, dict):
        raise ValidationError("Configuration must be a dictionary")
    if len(config) == 0:
        raise ValidationError("Configuration dictionary cannot be empty")
    validated = {}
    if 'name' not in config:
        raise ValidationError("Missing required field: name")
    if 'timeout' not in config:
        raise ValidationError("Missing required field: timeout")
    if 'recipients' not in config:
        raise ValidationError("Missing required field: recipients")
    try:
        validated['name'] = validate_string(config['name'], min_length=3, max_length=50)
    except ValidationError as e:
        raise ValidationError(f"Name error: {e}") from e
    try:
        validated['timeout'] = validate_positive_int(config['timeout'])
    except ValidationError as e:
        raise ValidationError(f"Timeout error: {e}") from e
    try:
        items = config['recipients']
        if not isinstance(items, (list, tuple)):
            raise ValidationError(f"Expected list or tuple, got {type(items).__name__}")
        if len(items) < 1:
            raise ValidationError("Too few items: minimum 1")
        if len(items) > 5:
            raise ValidationError("Too many items: maximum 5")
        validated['recipients'] = [validate_email(r) for r in items]
    except ValidationError as e:
        raise ValidationError(f"Recipients error: {e}") from e
    validated['debug'] = bool(config.get('debug', False))
    return validated