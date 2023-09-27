import ast
from collections import OrderedDict
import json
import sys

http_request_types = ['get', 'post', 'put', 'delete', 'patch', 'head', 'options', 'connect', 'trace', "route"]

def extract_functions_and_top_level(code):
    functions_and_top_level = []
    parsed_code = ast.parse(code)
    for node in parsed_code.body:
        if isinstance(node, ast.FunctionDef):
        
            if len(node.decorator_list) != 0:

                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                        if decorator.func.attr in http_request_types:
                            functions_and_top_level.append(('api-call', node.name, ast.unparse(node), node.lineno))
                        else:
                            functions_and_top_level.append(('function', node.name, ast.unparse(node), node.lineno))
                    else:
                        functions_and_top_level.append(('function', node.name, ast.unparse(node), node.lineno))

            else:   
                functions_and_top_level.append(('function', node.name, ast.unparse(node), node.lineno))

        elif isinstance(node, ast.ClassDef):
            functions_and_top_level.append(('class', node.name, ast.unparse(node), node.lineno))

        elif isinstance(node, ast.AsyncFunctionDef):
            functions_and_top_level.append(('async function', node.name, ast.unparse(node), node.lineno))
            
        elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            import_names = [alias.name for alias in node.names]
            functions_and_top_level.append(('import', ast.unparse(node), None, node.lineno))
        else:
            functions_and_top_level.append(('other', None, ast.unparse(node), node.lineno))

    return functions_and_top_level

def parsing_code(PATH: str):
    # Read the Python code from a file
    with open(PATH, 'r') as file:
        code_content = file.read()

    # Extract functions and other top-level elements
    elements = extract_functions_and_top_level(code_content)

    # Prepare the final ordered dictionary
    result_dict = OrderedDict()
    result_dict['functions_and_top_level'] = []
    result_dict['other_lines'] = {}

    for element_type, element_name, element_content, line_number in elements:
        if element_type == 'import':
            result_dict['functions_and_top_level'].append({'type': element_type, 'content': element_name, 'line_number': line_number})
        else:
            if element_content:
                result_dict['functions_and_top_level'].append({'type': element_type, 'name': element_name, 'content': element_content, 'line_number': line_number})
            else:
                result_dict['other_lines'][line_number] = {'code': code_content.split('\n')[line_number - 1]}

    return result_dict

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 parse_code.py file_path")
        sys.exit(1)

    file_path = sys.argv[1]
    result = parsing_code(file_path)
    print(json.dumps(result, indent=4))
