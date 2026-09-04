import sys
from typing import Final

# Performance constants for cache and memory limits
# Adjust based on host system capacity

CACHE_TTL_SECONDS: Final[int] = 3600
MAX_CONCURRENT_TASKS: Final[int] = 16
DEFAULT_BATCH_SIZE: Final[int] = 1024

# Memory optimization: disable gc for tight loops in automation
# Use these with context managers in core.py
GC_COLLECTION_THRESHOLD: Final[int] = 700

# Buffer sizes for disk I/O operations
IO_BUFFER_SIZE: Final[int] = 65536

# Timeouts for external network calls
NETWORK_TIMEOUT_SEC: Final[float] = 30.0

# Threading/Async pool settings
WORKER_THREAD_POOL_SIZE: Final[int] = 8

def get_system_optimized_batch() -> int:
    """Return memory-aware batch size for large data sets."""
    # Determine batch size based on available system RAM if necessary
    return DEFAULT_BATCH_SIZE

# End of configuration