from line_profiler import LineProfiler
import io
import sys
import json
import ast
import sys
import signal
sys.setrecursionlimit(3000)  # Set the recursion limit to a higher value

def profile_print(func_to_profile, *func_args):
    lp = LineProfiler()
    lp.add_function(func_to_profile)
    lp.enable_by_count()
    
    # Set an alarm signal to interrupt after 1 minute
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(60)  # Set the alarm for 1 minute
    
    try:
        lp.runctx('func_to_profile(*func_args)', locals=locals(), globals=globals())
    except TimeoutError:
        print("Execution timed out. Exiting...")
    
    stdout_ = sys.stdout  # Keep track of the previous value.
    stream = io.StringIO()
    sys.stdout = stream  # Redirect output to the stream
    lp.print_stats(output_unit=0.001)  # Values are in milliseconds
    sys.stdout = stdout_  # Restore the previous stdout.

    profile_output = stream.getvalue().split('\n')
    for line in profile_output:
        print(line)
    code_time_dict = {}
    for line in profile_output:
        cols = line.split()
        # Only process complete lines
        if len(cols) >= 6:
            hit_str = cols[0]
            time_perc_str = cols[4]
            code_str = " ".join(cols[5:])
            # Exclude any empty/whitespace lines or profiling metadata
            if hit_str.isdigit() and time_perc_str.replace('.', '', 1).isdigit():
                code_time_dict[code_str] = {"hits": hit_str, "percent_time": time_perc_str}
    return code_time_dict


def save_dict_as_json(data, output_path):
    """
    Save a dictionary as a JSON file.

    Parameters:
        data (dict): The dictionary to be saved.
        output_path (str): The file path to save the JSON data.

    Returns:
        None
    """
    try:
        # Write the dictionary to a JSON file
        with open(output_path, 'w') as json_file:
            json.dump(data, json_file)
        print('JSON data has been saved to', output_path)
    except IOError as e:
        print(f"An error occurred while saving the JSON data: {e}")
        
def timeout_handler(signum, frame):
    raise TimeoutError


def collatz(n, memo = {1:[1]}):
    if n not in memo: 
        if n % 2 == 0:
            memo[n] = [n] + collatz(n // 2)
        else:
            memo[n] = [n] + collatz(3*n + 1)
    return memo[n]

result_dict = profile_print(collatz, 1)
save_dict_as_json(result_dict, 'interim_files/profiler_obj.json')