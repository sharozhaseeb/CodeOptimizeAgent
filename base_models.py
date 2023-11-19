import openai
import os
from helper import extract_code
from executor_agent import code_executor
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.environ.get('API-KEY')

class base_models_req:
    def __init__(self, code, test_case):
        self.code = code
        self.test_case = test_case

    def vanilla_gpt_req(self):

        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {
        "role": "user",
        "content": " ```python\ndef do_stuff(numbers):\n    s = sum(numbers) #percent_time: 32.2%\n    prod = 1 #percent_time: 5.0%\n    for n in numbers: #percent_time: 28.8%\n        prod *= n #percent_time: 28.8%\n    return s, prod #percent_time: 5.2%```\nWorst Case;\nTime taken: 0.00013065338134765625\nMemory used: 0.0\n\nMedium Case;\nTime taken: 0.0002562999725341797\nMemory used: 0.0\n\nBest Case;\nTime taken: 0.00021123886108398438\nMemory used: 0.0\n\n\nCritically analyze the code and suggest built-in improvements."
        },
        # {
        # "role": "assistant",
        # "content": "The given code has a function that calculates the sum and the product of a list of numbers. The sum is calculated using the built-in function and the product in a for loop. The memory used in all the cases is negligible however the time taken seems to vary with the size of the input.\n\nImprovements and Optimization:\n\n1) Use built-in libraries for product calculation: The time-taken for product calculation is quite high as it is done using a for-loop. This can be optimized by using built-in python libraries like numpy that are faster and efficient. numpy.prod function can be used for this.\n\n2) Use a more efficient way to handle large lists: If the list has large number of elements, using numpy arrays instead of list can make computation more efficient.\n\n3) Using numexpr for large computations: If the calculations are too heavy, instead of numpy libraries, one can use numexpr which is efficient in handling large computations.\n\n4) Using functools reduce for product calculation: The python's functools library's reduce function can be used to calculate the product which can be faster than a simple for loop.\n\nHere is the optimized code incorporating the above suggestions:\n\n```python\nimport numpy as np\nfrom functools import reduce\nimport operator\n\ndef do_stuff(numbers):\n    # Convert list to array for faster computation if list is too large\n    numbers = np.array(numbers)\n    \n    s = np.sum(numbers)\n    \n    # Using numpy product function\n    prod = np.prod(numbers)\n    \n    # Alternatively, using reduce for product calculation\n    #prod = reduce(operator.mul, numbers, 1)\n    \n    return s, prod\n```\nPlease note that the time gain will actually be noticeable only when the size of the input list is large."
        # },
                {
        "role": "assistant",
        "content": "```python\nimport numpy as np\nfrom functools import reduce\nimport operator\n\ndef do_stuff(numbers):\n    # Convert list to array for faster computation if list is too large\n    numbers = np.array(numbers)\n    \n    s = np.sum(numbers)\n    \n    # Using numpy product function\n    prod = np.prod(numbers)\n    \n    # Alternatively, using reduce for product calculation\n    #prod = reduce(operator.mul, numbers, 1)\n    \n    return s, prod\n```\nPlease note that the time gain will actually be noticeable only when the size of the input list is large."
        },
        {
        "role": "user",
        "content": f"```python\n{self.code}\n```\nOptimize the code and return it no need to explain anything.Keep the name of the function or class the same along with the inputs and output. Donot split the function into multiple functions, create higher order functions if necessary."
        }
        ],

        temperature=1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        self.v_gpt_resp = response.choices[0].message.content
        return response.choices[0].message.content

    def code_extract(self):
        self.v_gpt_resp = extract_code(self.v_gpt_resp)
        return self.v_gpt_resp

    def exec_code(self):
        cd_exec = code_executor(
            code = self.v_gpt_resp,
            testcase= self.test_case
        )

        self.cd_run = cd_exec.run()

        return self.cd_run

    def run_flow(self):


        self.vanilla_gpt_req()
        print("gpt hit")
        print(self.v_gpt_resp)
        print("--"*10)
        self.code_extract()
        print("code Extracted")
        print(self.v_gpt_resp)
        print("--"*10)
        self.exec_code()
        print("running code")
        print(self.cd_run)
        print("--"*10)

        return {"optimized_code":self.v_gpt_resp,
                "exec_info":self.cd_run}