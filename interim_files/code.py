from line_profiler import LineProfiler

def do_stuff(numbers):
    s = sum(numbers)
    prod = 1
    for n in numbers:
        prod *= n
    return s, prod

numbers = [1, 2, 3, 4, 5]
do_stuff(numbers)