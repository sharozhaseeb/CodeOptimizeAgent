import time
import sys
import os
import psutil
import sys
import signal
sys.setrecursionlimit(3000)  # Set the recursion limit to a higher value

def memory_usage_psutil():
    # Return the memory usage in bytes
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

def test_case():
    start_time = time.time()
    start_memory = memory_usage_psutil()

    # Set an alarm signal to interrupt after 10sec
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(10)  # Set the alarm for 10sec

    # Call the function here
    try:
        collatz(10000)
        end_time = time.time()
        end_memory = memory_usage_psutil()

        print(f"Time taken: {end_time - start_time} seconds")
        print(f"Memory used: {end_memory - start_memory} bytes")

    except TimeoutError:
        #print("Execution timed out. Exiting...")
        end_time = time.time()
        end_memory = memory_usage_psutil()

        print(f"Time taken: 60 seconds")
        print(f"Memory used: 1100 bytes")

def timeout_handler(signum, frame):
    raise TimeoutError
def collatz(n, memo = {1:[1]}):
    if n not in memo:  #percent_time: 69.3%
        if n % 2 == 0:
            memo[n] = [n] + collatz(n // 2)
        else:
            memo[n] = [n] + collatz(3*n + 1)
    return memo[n] #percent_time: 30.7%

test_case()