from line_profiler import LineProfiler
import io
import sys
import json
import ast

def profile_print(func_to_profile, *func_args):
    lp = LineProfiler()
    lp.add_function(func_to_profile)
    lp.enable_by_count()
    lp.runctx('func_to_profile(*func_args)', locals=locals(), globals=globals())

    stdout_ = sys.stdout  # keep track of the previous value.
    stream = io.StringIO()
    sys.stdout = stream  # redirect output to the stream
    lp.print_stats(output_unit=0.001)  # values are in milliseconds
    sys.stdout = stdout_  # restore the previous stdout.

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


def calculate_factorials_up_to_number(n):
    factorial = 1
    yield factorial  # The factorial of 0 is 1
    for i in range(1, n + 1):
        factorial *= i
        yield factorial

result_dict = profile_print(calculate_factorials_up_to_number, 0)
save_dict_as_json(result_dict, 'interim_files/profiler_obj.json')