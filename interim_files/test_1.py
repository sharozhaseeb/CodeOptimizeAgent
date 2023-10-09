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
    documents = ["This is a short document.", "Another short document."]
unoptimized_word_count(documents)
    
    end_time = time.time()
    end_memory = memory_usage_psutil()

    print(f"Time taken: {end_time - start_time} seconds")
    print(f"Memory used: {end_memory - start_memory} B")


def unoptimized_word_count(documents):
    word_count = {}
    
    for doc in documents:
        words = doc.split()
        for word in words:
            # Remove punctuation and convert to lowercase
            word = word.strip('.,!?()[]{}"'').lower()
            if word:
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1
    
    return word_count



test_case()