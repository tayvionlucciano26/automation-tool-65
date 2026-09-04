import time
import random
import functools
from typing import Callable, Any

def retry_operation(retries: int = 3, backoff: float = 1.0):
    """Decorator for retrying network operations with exponential backoff."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            current_delay = backoff
            
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_exception = e
                    if attempt < retries - 1:
                        time.sleep(current_delay + random.uniform(0, 0.1))
                        current_delay *= 2
            
            raise last_exception
        return wrapper
    return decorator

@retry_operation(retries=3, backoff=2.0)
def fetch_data(url: str):
    """Example network operation protected by retry logic."""
    # Simulating a volatile network request
    if random.random() < 0.7:
        raise ConnectionError(f"Failed to connect to {url}")
    return {"status": "success", "data": "sample response"}

if __name__ == "__main__":
    try:
        result = fetch_data("https://api.example.com")
        print(f"Operation successful: {result}")
    except Exception as e:
        print(f"Operation failed after retries: {e}")