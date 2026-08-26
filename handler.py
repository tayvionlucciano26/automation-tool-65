import time
import random

def with_retry(max_retries=3, base_delay=1.0):
    """Decorator to add retry logic to network operations."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries:
                        raise
                    delay = base_delay * (2 ** (attempt - 1)) + random.random() * 0.5
                    print(f"Attempt {attempt} failed with {type(e).__name__}. Retrying after {delay:.2f} seconds.")
                    time.sleep(delay)
        return wrapper
    return decorator

class NetworkHandler:
    def __init__(self):
        self.attempt_count = 0

    @with_retry(max_retries=5, base_delay=0.2)
    def perform_network_operation(self, payload):
        """Simulate a network operation that may fail initially."""
        self.attempt_count += 1
        if self.attempt_count < 3:
            raise ConnectionError("Temporary network failure")
        return {"status": "success", "data": payload, "attempts": self.attempt_count}

if __name__ == "__main__":
    handler = NetworkHandler()
    try:
        result = handler.perform_network_operation("test data")
        print("Operation result:", result)
    except Exception as e:
        print("Operation failed:", e)
