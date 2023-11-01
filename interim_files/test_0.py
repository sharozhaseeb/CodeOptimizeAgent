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
    monte_carlo_pi(1000000)
    
    end_time = time.time()
    end_memory = memory_usage_psutil()

    print(f"Time taken: {end_time - start_time} seconds")
    print(f"Memory used: {end_memory - start_memory} B")


import numpy as np
import numexpr as ne

def monte_carlo_pi(iterations):
    points = np.random.rand(iterations, 2)
    sum_points = np.sum(points**2, axis=1)

    # Using numexpr for optimization
    inside_circle = np.count_nonzero(ne.evaluate("sum_points <= 1"))
    
    return inside_circle

test_case()