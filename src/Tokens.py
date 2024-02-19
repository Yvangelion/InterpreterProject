import re

token_patterns_list = {
    re.compile(r'\bcreate\b'): 'CREATE',
    re.compile(r'\bcalculate\b'): 'CALCULATE',
    re.compile(r'\bof\b'): 'OF',
    re.compile(r'\bas\b'): 'AS',
    re.compile(r'\binput\b'): 'INPUT',
    re.compile(r'[a-zA-Z][a-zA-Z0-9]*'): 'IDENTIFIER',
    re.compile(r'\d+'): 'CONSTANT',
    re.compile(r'[-+*/]'): 'OPERATOR',
    re.compile(r'\s+'): None,
    re.compile(r'\('): 'LPAREN',
    re.compile(r'\)'): 'RPAREN'
}


T_data = (list(token_patterns_list.items()))