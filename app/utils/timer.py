import time
from typing import Callable

def timer(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 소요 시간: {end_time - start_time}초")
        return result
    return wrapper

def atimer(func: Callable) -> Callable:
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 소요 시간: {end_time - start_time}초")
        return result
    return wrapper