from typing import Final

VERSION: Final[str] = "1.0.0"
DEFAULT_TIMEOUT: Final[int] = 30
MAX_RETRIES: Final[int] = 3
DEFAULT_ENCODING: Final[str] = "utf-8"

class ExitCodes:
    """System exit status codes for automation tool execution."""
    SUCCESS: Final[int] = 0
    GENERAL_ERROR: Final[int] = 1
    CONFIG_ERROR: Final[int] = 2
    TIMEOUT_ERROR: Final[int] = 3

class LogFormats:
    """Standardized logging format strings."""
    DEFAULT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    VERBOSE: Final[str] = "%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) - %(message)s"
