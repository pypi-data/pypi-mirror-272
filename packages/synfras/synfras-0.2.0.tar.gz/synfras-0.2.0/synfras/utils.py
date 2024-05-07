import time
from contextlib import contextmanager


def timer(func):

    def wrapper(*args, **kwargs):
        s = time.time()
        result = func(*args, **kwargs)
        e = time.time() - s
        print(f'[{func.__name__}] {e:.2f}s')

        return result

    return wrapper


@contextmanager
def time_block(task_name: str):
    s = time.time()
    yield
    e = time.time() - s
    print(f"[{task_name}] {e:.2f}s")
