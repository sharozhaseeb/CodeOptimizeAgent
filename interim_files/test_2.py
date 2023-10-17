import time
import sys
import os
import psutil

def memory_usage_psutil():
    # return the memory usage in MB
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

def test_case():
    start_time = time.time()
    start_memory = memory_usage_psutil()

    # Call the function here
    calculate_factorials_up_to_number(0)
    
    end_time = time.time()
    end_memory = memory_usage_psutil()

    print(f"Time taken: {end_time - start_time} seconds")
    print(f"Memory used: {end_memory - start_memory} B")

def calculate_factorials_up_to_number(n):
    if not isinstance(n, int) or n < 0:
        raise ValueError("Input must be a non-negative integer.")

    factorials = {}

    def factorial(k):
        if k in factorials:
            return factorials[k]
        elif k == 0:
            return 1
        else:
            result = k * factorial(k - 1)
            factorials[k] = result
            return result

    return [factorial(i) for i in range(n + 1)]
test_case()