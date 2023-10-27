import os

class code_executor:
    def __init__(self, code:str, testcase:list):
        self.code = code
        self.testcase = testcase
        self.interim_path = "interim_files"

    def run(self):

        tcb = open("prompts/test_case_base.txt").read()

        _ = []
        for iteration in self.testcase:
            tcb_ = tcb + self.code
            tcb_1 = tcb_.replace(
                                    "func(*args)",
                                    iteration
                                )

            tcb_1 = tcb_1 + "\ntest_case()"
            _.append(tcb_1)

        terminal_grabs = []
        for idx, testcase in enumerate(_):
            
            with open(f"{self.interim_path}/test_{idx}.py", 'w') as file:
                file.write(testcase)

            command = f"python {self.interim_path}/test_{idx}.py"
            terminal_grab = os.popen(command).read()

            terminal_grabs.append(terminal_grab)

        return_list = []
        for terminal_grab in terminal_grabs:
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

        