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
    calculate_factorials_up_to_number(1000)
    
    end_time = time.time()
    end_memory = memory_usage_psutil()

    print(f"Time taken: {end_time - start_time} seconds")
    print(f"Memory used: {end_memory - start_memory} B")

import math

def calculate_factorials_up_to_number(n):
    assert n >= 0, "Input must be a non-negative integer."

    factorials = [math.factorial(i) for i in range(n + 1)]

    return factorials
test_case()