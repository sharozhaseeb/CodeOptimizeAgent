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
    calculate_factorials_up_to_number(10)
    
    end_time = time.time()
    end_memory = memory_usage_psutil()

    print(f"Time taken: {end_time - start_time} seconds")
    print(f"Memory used: {end_memory - start_memory} B")

def calculate_factorials_up_to_number(n):
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")

    factorials = [1]  # Initialize with the factorial of 0

    factorial = 1
    for i in range(1, n + 1):
        factorial *= i
        factorials.append(factorial)

    return factorials
test_case()