import os
import json
import openai
import re
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ.get('API-KEY')



class testcase_agent:
    def __init__(
                    self,
                    code,
                    interim_path = "interim_files",
                    test_case_list = []
                ):
        self.code = code
        self.interim_path = interim_path
        self.extracted_code_blocks = test_case_list



    def gen_test_case(self):

        BASE_MESSAGE = json.loads(open("prompts/gen_test_case.json").read())

        USER_DICT    =  {
            "role": "user",
            "content": F"```python\n{self.code}\n```"
                        }

        BASE_MESSAGE.append(USER_DICT)
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= BASE_MESSAGE,
        temperature=0.1,
        max_tokens=1110,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

        self.test_case = response.choices[0].message.content
        return response.choices[0].message.content



    def extract_test_cases(
            self : str
            ) -> list[str]:
        
        pattern = r"```python(.*?)```"
        extracted_code_blocks = re.findall(pattern, self.test_case, re.DOTALL)

        extracted_code_blocks = [string.strip() for string in extracted_code_blocks]
        for i in extracted_code_blocks:
            print(i)
            print("--------")
        
        self.extracted_code_blocks = extracted_code_blocks


    def join_test_case(
                        self
                      ) -> list[str]:
    
        tcb = open("prompts/test_case_base.txt").read()

        _ = []
        for iteration in self.extracted_code_blocks:
            tcb_ = tcb + self.code
            tcb_1 = tcb_.replace(
                                    "func(*args)",
                                    iteration
                                )

            tcb_1 = tcb_1 + "\ntest_case()"
            _.append(tcb_1)
        self.test_case_list = _

        return self.test_case_list



    def run_test_case(self) -> str:
        
        terminal_grabs = []
        for idx, testcase in enumerate(self.test_case_list):

            with open(f"{self.interim_path}/test_{idx}.py", 'w') as file:
                file.write(testcase)


            command = f"python {self.interim_path}/test_{idx}.py"
            terminal_grab = os.popen(command).read()


            terminal_grabs.append(terminal_grab)


        self.terminal_grabs = terminal_grabs
        return self.terminal_grabs



    def extract_info_tg(self,
                         )-> list[dict]:
        return_list = []
        try:
            for terminal_grab in self.terminal_grabs:
                info_dict = {}
                lines = terminal_grab.strip().split('\n')
                for line in lines:
                    key, value = line.strip().split(': ')
                    key = key.strip()
                    if key == 'Time taken':
                        value = float(value.split()[0])
                    elif key == 'Memory used':
                        value = float(value.split()[0])
                    info_dict[key] = value
                return_list.append(info_dict)
            return return_list
        except ValueError as exp:
            print(f"Encountered a ValueError: {exp}")
            return [
                {
                    "Time taken":"0.0",
                    "Memory used":"0.0"
                },
                                {
                    "Time taken":"0.0",
                    "Memory used":"0.0"
                },
                                {
                    "Time taken":"0.0",
                    "Memory used":"0.0"
                }

            ]
            






































