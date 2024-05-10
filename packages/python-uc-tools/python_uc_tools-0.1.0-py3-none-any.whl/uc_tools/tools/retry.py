import asyncio

from typing import Any, Callable, Coroutine, TypeVar, Union
from ..logger import setup_logger

T = TypeVar("T")


def retry(
    max_retries: int = 5, max_delay: Union[int, float] = 5
) -> Callable[
    [Callable[..., Coroutine[Any, Any, T]]], Callable[..., Coroutine[Any, Any, T]]
]:
    """
    Decorator that retries a coroutine function multiple times if it fails.

    Args:
        max_retries (int): The maximum number of retries.
        max_delay (Union[int, float]): The maximum delay between retries.

    Returns:
        Callable[[Callable[..., Coroutine[Any, Any, T]]], Callable[..., Coroutine[Any, Any, T]]]:
            The decorated function.
    """

    def decorator(
        func: Callable[..., Coroutine[Any, Any, T]],
    ) -> Callable[..., Coroutine[Any, Any, T]]:
        logger = setup_logger(__name__)

        async def wrapper(*args: Any, **kwargs: Any) -> T:
            for retries_count in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if retries_count < max_retries:
                        logger.warning(
                            f"Retry attempt {retries_count+1} for function "
                            f"{func.__name__}: {e}"
                        )
                        await asyncio.sleep(
                            min(
                                max_delay,
                                max_delay / max_retries * (max_retries - retries_count),
                            )
                        )
                    else:
                        logger.error(
                            f"Max retries reached for function {func.__name__}"
                        )
                        raise

        return wrapper

    return decorator
