from profiler_agent import profiler
from test_case_agent import testcase_agent
from executor_agent import code_executor
from optimization_agent import optimization_suggestor_agent
from pprint import pprint

class flow_master:
    def __init__(
            self,
            code:str,
            initial_testcases:str = []
            ):
        self.code = code
        self.initial_testcases =initial_testcases

    def start(self):
        PARENT_TIME_MEM_DICT = {}
        PARENT = {}
        agent = testcase_agent(code = self.code)
        self.initial_testcase_info = agent.run_flow()

        print("------------------------------------------")
        print("this is the initial testcase information\n")
        pprint(self.initial_testcase_info)
        PARENT_TIME_MEM_DICT['original code'] = self.initial_testcase_info['response']
        PARENT['original code'] = self.initial_testcase_info
        print("\n")
        print("------------------------------------------")

        profiler_agent = profiler(
            code = self.code,
            testcase= self.initial_testcase_info['testcase'][-1]
        )
        self.initial_profiled_code = profiler_agent.run_flow()

        print("------------------------------------------")
        print("this is the initial profiled code\n")
        pprint(self.initial_profiled_code)
        print("\n")
        print("------------------------------------------")

        op_agent = optimization_suggestor_agent(code= self.initial_profiled_code,
                                        execution_obj= self.initial_testcase_info)
        self.op_phase_1_resp = op_agent.run_flow_phase_1()
        
        print("------------------------------------------")
        print("this is the optimized code agents first phase response\n")
        pprint(self.op_phase_1_resp)
        PARENT_TIME_MEM_DICT['phase 1'] = self.op_phase_1_resp['exec_info']
        PARENT['phase 1'] = self.op_phase_1_resp
        print("\n")
        print("------------------------------------------")

        self.op_phase_2_resp = op_agent.run_flow_phase_2()
        print("------------------------------------------")
        print("this is the optimized code agents second phase response\n")
        pprint(self.op_phase_2_resp)
        PARENT_TIME_MEM_DICT['phase 2'] = self.op_phase_2_resp['exec_info']
        PARENT['phase 2'] = self.op_phase_2_resp
        print("\n")
        print("------------------------------------------")

        return PARENT, PARENT_TIME_MEM_DICT
        # cd_exec = code_executor(
        #     code = self.optimization_suggestion,
        #     testcase = self.initial_testcase_info['testcase'] 
        # )

        # print(self.initial_testcase_info['testcase'] )
        # self.optimized_code_testcase_response = cd_exec.run()

        # print("------------------------------------------")
        # print("this is the optimized codes testcase response\n")
        # pprint(self.optimized_code_testcase_response)
        # pprint(self.initial_testcase_info['response'])
        # print("\n")
        # print("------------------------------------------")