import time
import functools
from typing import Callable, Any
from src.utils.logger import Logger

logger = Logger()

def retry(max_attempts: int = 3, delay: float = 1.0):
    """Retry decorator for API calls."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(
                        f"Attempt {attempt}/{max_attempts} failed for {func.__name__}: {e}"
                    )
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

def log_api_call(func: Callable) -> Callable:
    """Decorator to log API calls."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        logger.info(f"API Call: {func.__name__} - Args: {args[1:]} Kwargs: {kwargs}")
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        logger.info(f"API Response: {func.__name__} - Status: {result.status_code} - Time: {elapsed:.2f}s")
        return result
    return wrapper
