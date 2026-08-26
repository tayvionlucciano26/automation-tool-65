import logging
from typing import Any, Dict, Optional

logging.basicConfig(level=logging.ERROR)

class AutomationError(Exception):
    """Base exception for the automation tool."""
    pass

class EdgeCaseError(AutomationError):
    """Raised for edge cases during processing."""
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.context = context or {}

def handle_edge_cases(func):
    """Decorator to add error handling for edge cases."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ZeroDivisionError:
            logging.error("Edge case: division by zero")
            raise EdgeCaseError("Division by zero encountered", {"args": args})
        except (ValueError, TypeError) as e:
            logging.error(f"Edge case: invalid input - {e}")
            raise EdgeCaseError("Invalid input type or value", {"error": str(e)})
        except Exception as e:
            logging.error(f"Unexpected edge case: {e}")
            raise AutomationError("Automation failed due to unexpected error") from e
    return wrapper

@handle_edge_cases
def process_item(item: Any) -> Any:
    """Process a single item handling various edge cases."""
    if item is None:
        raise ValueError("Item cannot be None")
    if isinstance(item, str) and not item:
        raise ValueError("Empty string not allowed")
    if isinstance(item, (list, dict)) and len(item) == 0:
        raise ValueError("Empty collection not allowed")
    if isinstance(item, (int, float)) and item == 0:
        pass
    if isinstance(item, (int, float)):
        return item / 1
    elif isinstance(item, list):
        return sum(item)
    elif isinstance(item, dict):
        return sum(item.values()) if all(isinstance(v, (int, float)) for v in item.values()) else 0
    return item

def safe_process(data: Any) -> Any:
    """Additional error handling for edge cases in data processing."""
    try:
        if data is None or (isinstance(data, (str, list, dict)) and len(data) == 0):
            raise EdgeCaseError("Empty or null input", {"data": str(data)})
        if isinstance(data, list):
            return [process_item(x) for x in data]
        return process_item(data)
    except EdgeCaseError as e:
        logging.error(f"Handled edge case: {e} with context {e.context}")
        return None
    except AutomationError as e:
        logging.error(f"Automation error: {e}")
        raise
