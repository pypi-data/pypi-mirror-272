import time

def timer(func):
    """装饰器:计时
    """
    def inner(*args, **kwargs):
        start_time = time.time()
        re = func(*args, **kwargs)
        end_time = time.time()
        print("Program execution time: ", end_time - start_time)
        return re
    return inner

