"""Custom exceptions for automation-tool-65.

Defines exceptions with a base class supporting details for automation tasks.
"""

from typing import Optional, Dict, Any


class AutomationError(Exception):
    """Base class for all automation tool exceptions."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        if self.details:
            return f"{self.message} | {self.details}"
        return self.message

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for structured error info."""
        return {
            "type": self.__class__.__name__,
            "message": self.message,
            "details": self.details
        }


class ConfigurationError(AutomationError):
    """Raised when configuration is invalid or missing."""
    pass


class ValidationError(AutomationError):
    """Raised on data validation failure."""

    def __init__(self, message: str, field: Optional[str] = None) -> None:
        details = {"field": field} if field else None
        super().__init__(message, details)


class FileError(AutomationError):
    """Raised for file related operation errors."""
    pass


class NetworkError(AutomationError):
    """Raised for network connectivity problems."""

    def __init__(self, message: str, status: Optional[int] = None) -> None:
        super().__init__(message, {"status": status} if status is not None else None)


class TaskTimeoutError(AutomationError):
    """Raised when a task exceeds the allowed time."""
    pass


def extract_error_details(error: Exception) -> Dict[str, Any]:
    """Return structured details from any exception."""
    if isinstance(error, AutomationError):
        return error.to_dict()
    return {"type": error.__class__.__name__, "message": str(error), "details": {}}


def format_error_for_log(error: Exception) -> str:
    """Format the error message for logging purposes."""
    if isinstance(error, AutomationError):
        return str(error)
    return f"Unexpected: {str(error)}"