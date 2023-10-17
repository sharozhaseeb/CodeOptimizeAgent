from line_profiler import LineProfiler
import io
import sys
from helper import (
    extract_function_name_from_string,
    extract_string_between_parentheses
      )

class profiler:
    def __init__(self, code: str, testcase: str, interim_path = "interim_files"):

        self.code = code
        self.testcase = testcase
        self.interim_path = interim_path
    

    def initialize_profiler(self):
        func_name = extract_function_name_from_string(self.code)
        args      = extract_string_between_parentheses(self.testcase
                                                       )
        profiler_base = open("prompts/profiler_case_base.txt").read()
        
        profiler_base = profiler_base + f"\n\n{self.code}" + \
                                        f"\nresult_dict = profile_print({func_name}, {args})" + \
                                        f"\nsave_dict_as_json(result_dict, '{self.interim_path}/profiler_obj.json')"
                                        
    
        print(profiler_base)
        
