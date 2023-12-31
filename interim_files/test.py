import time
import sys
import os
import psutil

def memory_usage_psutil():
    # return the memory usage in MB
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss / (1024.0 ** 2)

def test_case():
    start_time = time.time()
    start_memory = memory_usage_psutil()

    # Call the function here
    fibonacci_unoptimized(5)
    
    end_time = time.time()
    end_memory = memory_usage_psutil()

    print(f"Time taken: {end_time - start_time} seconds")
    print(f"Memory used: {end_memory - start_memory} MB")


def fibonacci_unoptimized(n):
    if n <= 1:
        return n
    else:
        return fibonacci_unoptimized(n - 1) + fibonacci_unoptimized(n - 2)

test_case()