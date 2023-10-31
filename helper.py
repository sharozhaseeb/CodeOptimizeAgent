import ast
import re


def extract_function_name_from_string(func_str):
    """
    Extracts the name of a Python function from a string containing the function definition.

    Parameters:
        func_str (str): The string containing the function definition.

    Returns:
        str: The name of the function.
    """
    # Parse the function definition using AST
    try:
        parsed_ast = ast.parse(func_str)
    except SyntaxError as e:
        raise ValueError(f"Unable to parse the provided function string: {str(e)}")

    # Extract the function name
    if isinstance(parsed_ast.body[0], ast.FunctionDef):
        return parsed_ast.body[0].name
    else:
        raise ValueError("Input is not a valid function definition.")
    



def extract_string_between_parentheses(input_str):
    """
    Extracts the string between the first pair of parentheses in the input string using regex.

    Parameters:
        input_str (str): The input string.

    Returns:
        str: The string between the first pair of parentheses.
    """
    # Define a regex pattern to match content between parentheses
    pattern = r'\((.*?)\)'
    
    # Search for the pattern in the input string
    match = re.search(pattern, input_str)
    
    if match:
        return match.group(1)
    else:
        raise ValueError("Input does not contain a valid pair of parentheses.")

def extract_code(text:str) -> str:
    if '```python' not in text:
        raise ValueError('no code found')
    else:
        pattern = r'```python(.*?)```'

        match = re.search(pattern, text, re.DOTALL)

        if match:
            extracted_text = match.group(1)
            # print(extracted_text)
        return extracted_text