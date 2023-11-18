

from overseer import flow_master
from termcolor import colored
from tqdm import tqdm
import re
import pickle
import json
import time

# print(*dataset_mutated, sep= "\n---\n----")



# counter = 0
# value_error = 0 # no code found
# r_err = 0

def flow(): 
    dataset_raw = open("dataset/single_input_functions.txt").read()
    dataset_mutated = re.sub(r'#\$%\d+\$%#', '', dataset_raw)

    dataset_mutated = dataset_mutated.split("\n\n")
    dataset = [item for item in dataset_mutated if item.strip() != ""]
    print(len(dataset))
    # while True:
    data_l = []
    dataset_response = {}


    for instance in tqdm(dataset):
        # time.sleep(15)
        # print(len(dataset))
        try:
            flow = flow_master(code= instance)

            parent, t_m = flow.start()

            for key in t_m.keys():
                print(key)
                print(t_m[key][0])
            dataset_response[instance] = (parent, t_m)
            data_l.append((parent, t_m))
            print("____________________")
            print(colored("--------------", 'red'))
            print(colored("--------------", 'red'))
            print(colored("--------------", 'red'))
            print(colored("--------------", 'red'))

            print(("____________________" + '\n') * 10, end='')

        # counter += 1
        except ValueError as exp:
            print(colored("--------------", 'white'))
            print(colored("--------------", 'white'))
            print(colored("--------------", 'white'))
            print(colored("--------------", 'white'))
            # value_error += 1
            print(exp)
            print(colored("--------------", 'white'))
            print(colored("--------------", 'white'))
            print(colored("--------------", 'white'))
            print(colored("--------------", 'white'))
            dataset_response[instance] = []
            data_l.append([])
            continue

        except Exception as exp:
            print(colored("--------------", 'white'))
            print(colored("--------------", 'white'))
            print(colored("--------------", 'white'))
            print(colored("--------------", 'white'))
            # r_err += 1
            print(exp)
            print(colored("--------------", 'white'))
            print(colored("--------------", 'white'))
            print(colored("--------------", 'white'))
            print(colored("--------------", 'white'))
            continue

    with open("data_l.json", 'w') as json_file:
        json.dump(data_l, json_file)


    with open("data.json", 'w') as json_file:
        json.dump(dataset_response, json_file)

    with open("data.pkl", 'wb') as pickle_file:
        pickle.dump(dataset_response, pickle_file)


if __name__ == "__main__":

    flow()