import os
import openai
import re
from helper import extract_code
from dotenv import load_dotenv
from executor_agent import code_executor
from profiler_agent import profiler
load_dotenv()
openai.api_key = os.environ.get('API-KEY')


class optimization_suggestor_agent:
    def __init__(
                        self,
                        code : str,
                        execution_obj : list[dict]
                ):
        
        self.phase_info = []
        self.code = code
        self.execution_obj = execution_obj['response']
        self.testcases_obj = execution_obj['testcase']

    def optimize(self) -> str:
        exec_str = f"```python\n{self.code}\n```\n"
        case_list = ["Worst Case", "Medium Case", "Best Case"]

        for idx, exec_obj in enumerate(self.execution_obj):
            exec_str += f"{case_list[idx]};\nTime taken: {exec_obj['Time taken']}\nMemory used: {exec_obj['Memory used']}\n\n"
        exec_str += "Critically analyze the code and suggest improvements. Focus on the lines with the higher percentage. Keep the name of the function or class the same along with the inputs and output. Donot split the function into multiple functions, create higher order functions if necessary."

        BASE_PROMPT = eval(open("prompts/op_case_base.json").read())
        _EXT        = {
                        "role": "user",
                        "content": exec_str
                        }
        BASE_PROMPT.append(_EXT)
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=BASE_PROMPT,
            temperature=1,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
        
        self.gpt_resp = response.choices[0].message.content
        BASE_PROMPT.append({"role" : "assistant",
                            "content": self.gpt_resp})
        self.phase_1_tuples = BASE_PROMPT
        return self.gpt_resp


    def create_resp(self) -> dict:

       self.phase_info.append((extract_code(self.gpt_resp), self.gpt_resp.split("```python")[0]))
       return self.phase_info
    
    def run_current_phase(self) -> list:

        cd_exec = code_executor(
        code = self.phase_info[-1][0],
        testcase = self.testcases_obj 
                                )
        
        self.current_phase_testrun = cd_exec.run()
        return self.current_phase_testrun

    def run_flow_phase_1(self):
        response = {}
        self.optimize()
        resp = self.create_resp()
        response["optimized_code"] = resp[-1][0]
        response["suggestions"]    = resp[-1][1]
        test_run = self.run_current_phase()
        response["exec_info"]      = test_run
        return response
    
    def phase_2(self):
        print("++++++")
        print("the code going into phase 2")
        print(self.phase_info[-1][0])
        print("+++++++")

        profiler_ins = profiler(code = self.phase_info[-1][0],
                                testcase = self.testcases_obj[-1])
        mutated_code = profiler_ins.run_flow()

        exec_str = f"```python\n{mutated_code}\n```\n"
        case_list = ["Worst Case", "Medium Case", "Best Case"]

        for idx, exec_obj in enumerate(self.current_phase_testrun):
            exec_str += f"{case_list[idx]};\nTime taken: {exec_obj['Time taken']}\nMemory used: {exec_obj['Memory used']}\n\n"
        exec_str += "This is the information of the updated code, can it be made better? Your main concern is execution time and memory consumption. Critically think and write error free code without using any third party packages . If the code cannot be optimized further return the same code."
        _EXT = {"role":"user",
                "content": exec_str}
        
        self.phase_2_tuples = self.phase_1_tuples
        self.phase_2_tuples.append(_EXT)
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=self.phase_2_tuples,
            temperature=1,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
        
        self.gpt_resp = response.choices[0].message.content

        return self.gpt_resp
    
    def run_flow_phase_2(self):
        
        self.phase_2()
        response = {}
        resp = self.create_resp()
        response["optimized_code"] = resp[-1][0]
        response["suggestions"]    = resp[-1][1]
        test_run = self.run_current_phase()
        response["exec_info"]      = test_run
        return response






    # def raw_optimizations(self) -> str:
        
    #     exec_str = f"```python\n{self.code}\n```\n"
    #     case_list = ["Worst Case", "Medium Case", "Best Case"]
        
    #     for idx, exec_obj in enumerate(self.execution_obj):
    #         exec_str += f"{case_list[idx]};\nTime taken: {exec_obj['Time taken']}\nMemory used: {exec_obj['Memory used']}\n\n"
    #     exec_str += "Critically analyze the code and suggest built-in improvements such as list comprehensions and lambda expressions. No need for updated code."
    #     response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {
    #         "role": "system",
    #         "content": "You are a senior python developer. You will be given an input code with its execution time and memory used. \nYou will critically analyse the code and suggest optimizations which should include use of built-in functions etc.\nContext;\nYou are a part of a larger system, the optimizations you offer will help make the code more efficient in terms of time and memory."
    #         },
    #         {
    #         "role": "user",
    #         "content": "```python\nimport csv\n\ndef unoptimized_csv_processing(filename):\n    # Open the CSV file\n    with open(filename, 'r') as file:\n        reader = csv.reader(file)\n        \n        # Initialize variables to store data and results\n        data = []\n        results = []\n        \n        # Read data from the CSV file into a list\n        for row in reader:\n            data.append(row)\n            \n        # Perform some calculations on the data\n        for row in data:\n            if len(row) >= 3:\n                result = 0\n                for value in row:\n                    try:\n                        num = float(value)\n                        result += num\n                    except ValueError:\n                        pass\n                results.append(result)\n                \n    # Close the file\n    file.close()\n    \n    # Return the results\n    return results```\nWorst Case;\nTime taken: 0.00013065338134765625\nMemory used: 0.0\n\nMedium Case;\nTime taken: 0.0002562999725341797\nMemory used: 0.0\n\nBest Case;\nTime taken: 0.00021123886108398438\nMemory used: 0.0\n\n\nCritically analyze the code and suggest built-in improvements. No need for updated code."
    #         },
    #         {
    #         "role": "assistant",
    #         "content": "1. Use Direct Processing Instead of Reading Data into a List: Right now, the code first reads all of the rows of the CSV into a list and then goes through this list again to perform calculations. Instead, these two steps could be combined into one - the code could calculate and store the sum as soon as each row of data is read, removing the need for the intermediate \"data\" list and saving memory.\n\n2. Nested handling of CSV rows: There is a nested for loop for traversing each row of the CSV file. The outer loop traverses all rows, and the inner loop traverses each value in the row. This can be optimized using list comprehension along with the 'map' function. Inside the try block, we can use the 'map' function to attempt converting all values into float.\n\n3. Unnecessary File Close: The use of \"with open(filename, 'r') as file\" means that Python will automatically close the file once the block of code underneath is finished executing. The explicit file.close() at the end is unnecessary and can be removed.\n\n4. Error Handling for Each Value: Currently, the code tries to convert each value in a row to a float, and if a ValueError is thrown because the value can't be converted, the code simply passes and moves on to the next value. This is a simple and effective way of handling errors, but if there are a lot of values that can't be converted, the overhead from constantly throwing and catching exceptions could become a performance issue.\n\n5. List comprehension and lambda usage: Some of calculations over data can be made inside of list comprehensions and lambda functions to optimize processing time.\n\n6. Unused Variable 'results': The variable 'results' is declared but not used at all. If it's not needed, it can be removed. But I believe the requirement might be to append the sum of each row to 'results'. If so, instead of using a for loop, we can directly append the result by leveraging list comprehension."
    #         },
    #         {
    #         "role": "user",
    #         "content": exec_str
    #         }
    #     ],
    #     temperature=1,
    #     max_tokens=500,
    #     top_p=1,
    #     frequency_penalty=0,
    #     presence_penalty=0
    #     )

    #     self.raw_optimizations = response.choices[0].message.content
        
    #     return response.choices[0].message.content
    

    # def optimizer(self) -> str:

    #     _exec_str = f"```python\n{self.code}\n```\n{self.raw_optimizations}"

    #     response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {
    #         "role": "system",
    #         "content": "You are a senior python developer. You will be given an input code with possible optimization that should be introduced into the code. \nYou will be returning an optimized version of the code. Recursion is frowned upon\n\nContext;\nYou are a part of a larger system, the optimizations you offer will help make the code more efficient in terms of time and memory."
    #         },
    #         {
    #         "role": "user",
    #         "content": "```python\ndef word_count(documents):\n    word_count = {}\n    \n    for doc in documents:\n        words = doc.split()\n        for word in words:\n            # Remove punctuation and convert to lowercase\n            word = word.strip('.,!?()[]{}\"\\'').lower()\n            if word:\n                if word in word_count:\n                    word_count[word] += 1\n                else:\n                    word_count[word] = 1\n    \n    return word_count\n```\n\n1. Use of collections.Counter: Instead of manually checking whether a word is in the dictionary before incrementing the count, you can use the Counter class from the collections module, which simplifies the counting process.\n\n2. String processing: Instead of calling the strip method to remove specific punctuation marks and then converting the string to lower case, you could use the translate and lower methods together. This might help optimize the processing time when you're dealing with large documents.\n\n3. Looping through words: You are using a for loop to iterate through the words. This can be replaced with a list comprehension, which would be faster because it optimizes the iteration process and reduces the overhead of an ordinary loop.\n\n4. Use of regular expressions: Instead of using the strip method, which can only remove characters from the start and end of a string, consider using regular expressions to remove punctuation from anywhere in a word.\n\n5. Use of sets for checking membership: Looking up elements in a list takes O(n) time, but looking up elements in a set takes roughly O(1) time. If you need to look up an element multiple times, it's much faster to look it up in a set than in a list.\n\n6. Use of functools.lru_cache: If you're performing this algorithm repeatedly on the same data, consider using caching to save previously calculated results and speed up future computations. The lru_cache function from the functools module adds caching to any function."
    #         },
    #         {
    #         "role": "assistant",
    #         "content": "```python\nimport re\nfrom collections import Counter\nfrom functools import lru_cache\n\n@lru_cache\ndef remove_punctuation(word):\n    return re.sub(r'[^\\w\\s]', '', word)\n\ndef word_count(documents):\n    word_count = Counter()\n    \n    for doc in documents:\n        words = [remove_punctuation(word.lower()) for word in doc.split()]\n        word_count.update(words)\n    \n    return word_count\n```"
    #         },
    #         {
    #         "role": "user",
    #         "content": _exec_str
    #         }
    #     ],
    #     temperature=0.4,
    #     max_tokens=512,
    #     top_p=1,
    #     frequency_penalty=0,
    #     presence_penalty=0
    #     )

    #     self.intermediate_optimization = response.choices[0].message.content
    #     return response.choices[0].message.content
    
    # def extract_code(self) -> list[str]:
    #     pattern = r"```python(.*?)```"
    #     extracted_code_blocks = re.findall(pattern, self.intermediate_optimization, re.DOTALL)

    #     extracted_code_blocks = [string.strip() for string in extracted_code_blocks]
    #     for i in extracted_code_blocks:
    #         print(i)
    #         print("--------")

    #     self.extracted_code_blocks = extracted_code_blocks
    #     return extracted_code_blocks[0]
    
    # def run_flow(self) -> str:

    #     print("----raw optimizations----")
    #     resp = self.raw_optimizations()
    #     print(resp)
    #     print("\n")
    #     print("------Optimizer----------")
    #     resp = self.optimizer()
    #     print(resp)
    #     print("\n")
    #     print("------Code Extraction-----")
    #     resp = self.extract_code()
    #     print(resp)
    #     return resp



        

