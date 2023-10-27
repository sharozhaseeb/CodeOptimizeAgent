from line_profiler import LineProfiler
import io
import sys
from helper import (
    extract_function_name_from_string,
    extract_string_between_parentheses
      )
import os
import json

class profiler:
    def __init__(self, code: str, testcase: str, interim_path = "interim_files"):

        self.code = code
        self.testcase = testcase
        self.interim_path = interim_path
        self.profiler_obj_path = f"interim_files/profiler_obj.json"
    

    def initialize_profiler(self):
        func_name = extract_function_name_from_string(self.code)
        args      = extract_string_between_parentheses(self.testcase
                                                       )
        profiler_base = open("prompts/profiler_case_base.txt").read()
        
        profiler_base = profiler_base + f"\n\n{self.code}" + \
                                        f"\nresult_dict = profile_print({func_name}, {args})" + \
                                        f"\nsave_dict_as_json(result_dict, '{self.interim_path}/profiler_obj.json')"
                                        
        with open(f"{self.interim_path}/profiler.py", 'w') as file:
                file.write(profiler_base)
        command = f"python {self.interim_path}/profiler.py"
        terminal_grab = os.popen(command).read()
        print("command ran")

    def mutate_code(self) -> str:
        with open(self.profiler_obj_path) as file:
            #   print(type(file))
            profiler_obj = json.load(file)
        _code = self.code.split("\n")

        __code = []
        print(profiler_obj.keys())
        for code_line in _code:
            if code_line.strip() in profiler_obj.keys():
                __code.append(f"{code_line} #percent_time: {profiler_obj[code_line.strip()]['percent_time']}%")
            else:
                __code.append(code_line)

        print(*__code, sep = "\n")

        self.code_mutated = "\n".join(__code)
        return self.code_mutated
    
    def run_flow(self) -> str:
        self.initialize_profiler()
        self.mutate_code()

        return self.code_mutated
        
