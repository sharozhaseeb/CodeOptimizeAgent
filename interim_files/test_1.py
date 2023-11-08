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
    merge_sort([5, 2, 9, 1, 7, 3, 6, 4, 8])
    
    end_time = time.time()
    end_memory = memory_usage_psutil()

    print(f"Time taken: {end_time - start_time} seconds")
    print(f"Memory used: {end_memory - start_memory} B")


def merge_sort(lst, start=0, end=None):
    if end is None: end = len(lst)
    if end - start > 1:
        mid = (start + end) // 2
        merge_sort(lst, start, mid)
        merge_sort(lst, mid, end)
        merge(lst, start, mid, end)
        
def merge(lst, start, mid, end):
    left = lst[start: mid]
    right = lst[mid: end]
    i = j = 0
    for k in range(start, end):
        if i >= len(left):
            lst[k] = right[j]
            j += 1
        elif j >= len(right):
            lst[k] = left[i]
            i += 1
        elif left[i] < right[j]:
            lst[k] = left[i]
            i += 1
        else: # if right[j] <= left[i]
            lst[k] = right[j]
            j += 1

test_case()