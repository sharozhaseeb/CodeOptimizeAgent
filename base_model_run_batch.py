from base_models import base_models_req
from tqdm import tqdm
import json
from pprint import pprint
from termcolor import colored

def run_flow():
    new_ds = json.load(open("interim_ds.json"))
    final_ds = new_ds
    for code_instance in tqdm(new_ds):
        try:


            vgpt = base_models_req(code=code_instance,
                            test_case=new_ds[code_instance]["payload"][0]["original code"]["testcase"]
                            )


            vas = vgpt.run_flow()
            final_ds[code_instance]["payload"][0]["vanilla_gpt-3.5"] = vas
            final_ds[code_instance]["payload"][1]["vanilla_gpt-3.5"] = vas["exec_info"]
            pprint(final_ds[code_instance])
        except Exception as e:
            print(colored("--------------", "white"))
            print(colored("--------------", "white"))
            print(colored("--------------", "white"))
            print(e)
            print(colored("--------------", "white"))
            print(colored("--------------", "white"))
            print(colored("--------------", "white"))
            continue



    with open("final_ds.json", "w") as f:
        json.dump(final_ds, f)


if __name__ == "__main__" :
    run_flow()