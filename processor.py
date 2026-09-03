import time
import random
import logging
import urllib.request
import urllib.error
from typing import Callable, Any, Type, Tuple

logger = logging.getLogger("automation_tool.processor")

def retry(
    retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,)
) -> Callable:
    """
    Decorator that retries a function call with exponential backoff and jitter.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_delay = delay
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    if attempt == retries:
                        logger.error(f"Operation failed permanently after {retries} attempts: {err}")
                        raise err
                    
                    # Add a small random jitter to prevent synchronized retries
                    jitter = random.uniform(0, 0.2 * current_delay)
                    sleep_duration = current_delay + jitter
                    
                    logger.warning(
                        f"Attempt {attempt}/{retries} failed: {err}. "
                        f"Retrying in {sleep_duration:.2f} seconds..."
                    )
                    time.sleep(sleep_duration)
                    current_delay *= backoff
        return wrapper
    return decorator

@retry(retries=3, delay=1.0, exceptions=(urllib.error.URLError, ConnectionError))
def execute_network_request(url: str, timeout: int = 10) -> str:
    """
    Executes a network request to the given URL and returns the decoded response content.
    """
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'AutomationTool/1.0'}
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode('utf-8')
