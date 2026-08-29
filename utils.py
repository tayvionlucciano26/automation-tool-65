import time
import random
from functools import wraps

def retry_network_operation(max_retries=3, base_delay=1.0, backoff=2.0):
    """Decorator to add retry logic for network operations.
    Retries on exceptions with exponential backoff and jitter.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    if attempt == max_retries:
                        raise
                    delay = base_delay * (backoff ** attempt)
                    jitter = random.uniform(0, 0.1 * delay)
                    time.sleep(delay + jitter)
            return None
        return wrapper
    return decorator

# Example usage
@retry_network_operation(max_retries=2)
def simulate_network_call():
    """Simulate a network operation that may fail."""
    if random.random() < 0.7:
        raise ConnectionError("Network timeout")
    return "Success"

if __name__ == "__main__":
    try:
        result = simulate_network_call()
        print(result)
    except Exception as e:
        print("Failed after retries: " + str(e))
