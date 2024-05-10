import asyncio
import pytest

from uc_tools.tools.retry import retry


async def test_retry_successful_execution():
    async def mock_coroutine(*args, **kwargs):
        return 42

    decorated_func = retry()(mock_coroutine)
    result = await decorated_func()
    assert result == 42


async def test_retry_max_retries_reached():
    async def mock_coroutine(*args, **kwargs):
        raise ValueError("Something went wrong")

    decorated_func = retry(max_retries=3, max_delay=1)(mock_coroutine)
    with pytest.raises(ValueError):
        await decorated_func()
