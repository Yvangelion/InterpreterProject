import re
import json
import sys
from Tokens import *


# kewords lists
keywords_list = ["create", "calculate", "of", "as"]
operators_list = ["+", "-", "*", "/"]

# varaibles for output
variables_dict = {}

# constatants and tokens and identifiers
identifiers_list = []
constants_list = []
tokens_list = []

# data
token_patterns_list = T_data 

# sort data
def tokenize_code(input_code):
    position_index = 0
    while position_index < len(input_code):
        match_result = None
        for pattern_obj, token_type_str in token_patterns_list:
            match_result = pattern_obj.match(input_code, position_index)
            if match_result:
                value_str = match_result.group(0)
                position_index = match_result.end()
                if token_type_str == "IDENTIFIER":
                    if value_str not in keywords_list:
                        identifiers_list.append(value_str)
                elif token_type_str == "CONSTANT":
                    constants_list.append(value_str)
                if token_type_str:
                    tokens_list.append({"type": token_type_str, "value": value_str})
                break
        else:
            sys.exit(f"Error: Unexpected character '{input_code[position_index]}' at position {position_index + 1}")

# if expresion do expression
def evaluate_expression_code(expression_tokens):
    stack_list = []
    for token_obj in expression_tokens:
        if token_obj["type"] == "IDENTIFIER":
            stack_list.append(variables_dict.get(token_obj["value"], 0))
        elif token_obj["type"] == "CONSTANT":
            stack_list.append(int(token_obj["value"]))
        elif token_obj["type"] == "OPERATOR":
            operand2 = stack_list.pop()
            operand1 = stack_list.pop()
            if token_obj["value"] == "+":
                stack_list.append(operand1 + operand2)
            elif token_obj["value"] == "-":
                stack_list.append(operand1 - operand2)
            elif token_obj["value"] == "*":
                stack_list.append(operand1 * operand2)
            elif token_obj["value"] == "/":
                stack_list.append(operand1 / operand2)
    return stack_list[0] if stack_list else None

#  what file to read from
if len(sys.argv) != 2:
    sys.exit("Usage: python scl_scanner.py <input_file.scl>")

input_filename = sys.argv[1]

try:
    with open(input_filename, "r") as file:
        source_code_str = file.read()
        print("Input Source Code:")
        print(source_code_str)
        print("\nTokenizing...\n")
        tokenize_code(source_code_str)

        # processes tokens
        create_variable_bool = None
        n_count = 0
        save_results_list = []
        for token_obj in tokens_list:            
            token_obj["Token ID"] = n_count
            n_count += 1
            if token_obj["type"] == "CREATE":
                create_variable_bool = True
            elif token_obj["type"] == "CALCULATE":
                expression_start_index = tokens_list.index(token_obj) + 1
                expression_end_index = tokens_list.index({"type": "AS", "value": "as"})
                expression_tokens_list = tokens_list[expression_start_index:expression_end_index]
                result_value = evaluate_expression_code(expression_tokens_list)
                save_results_list.append(result_value)

                variables_dict[tokens_list[expression_end_index + 1]["value"]] = result_value
            elif token_obj["type"] == "INPUT":
                # Take user input for variable value
                variable_name_str = identifiers_list.pop(0)
                user_input_str = input(f"Enter value for variable '{variable_name_str}': ")
                variables_dict[variable_name_str] = float(user_input_str)
            # future use 
            """elif token_obj["type"] == "SAVEAS":
                create_variable_bool = True
                result_value = save_results_list[0]

                saveas_name_str = identifiers_list.pop(0)
                if result_value is not None:
                    variables_dict[saveas_name_str] = result_value
                else: 
                    variables_dict[saveas_name_str] = "0"""


except FileNotFoundError:
    sys.exit(f"Error: File '{input_filename}' not found.")

# output variable values to console
print("\nVariable Values:")
print(json.dumps(variables_dict, indent=2))

# output tokens to console
print("\nTokens:")
print(json.dumps(tokens_list, indent=2))

# save tokens to JSON file tokens
output_filename = "tokens.json"
with open(output_filename, "w") as file:
    json.dump(tokens_list, file, indent=2)

print(f"\nTokens saved to {output_filename}")

