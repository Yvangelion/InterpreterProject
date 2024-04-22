class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

class Scanner:
    def __init__(self, code):
        self.code = code
        self.current_position = 0

    def scan(self):
        tokens = []
        while self.current_position < len(self.code):
            char = self.code[self.current_position]
            if char.isdigit():
                num_str = char
                while (self.current_position + 1) < len(self.code) and self.code[self.current_position + 1].isdigit():
                    self.current_position += 1
                    num_str += self.code[self.current_position]
                tokens.append(Token("NUMBER", int(num_str)))
            elif char.isalpha():
                identifier = char
                while (self.current_position + 1) < len(self.code) and self.code[self.current_position + 1].isalnum():
                    self.current_position += 1
                    identifier += self.code[self.current_position]
                if identifier == "if":
                    tokens.append(Token("IF", identifier))
                elif identifier == "else":
                    tokens.append(Token("ELSE", identifier))
                elif identifier == "while":
                    tokens.append(Token("WHILE", identifier))
                elif identifier == "print":
                    tokens.append(Token("PRINT", identifier))
                elif identifier == "True" or identifier == "False":
                    tokens.append(Token("BOOLEAN", bool(identifier)))
                else:
                    tokens.append(Token("IDENTIFIER", identifier))
            elif char == "'":
                string_literal = ""
                self.current_position += 1  # Skip the opening quote
                while (self.current_position) < len(self.code):
                    if self.code[self.current_position] == "'":
                        # End of string literal
                        self.current_position += 1  # Skip the closing quote
                        break
                    else:
                        string_literal += self.code[self.current_position]
                        self.current_position += 1
                tokens.append(Token("STRING", string_literal))
            elif char in "=+-*/":
                tokens.append(Token("OPERATOR", char))
            elif char in "<>=":
                if (self.current_position + 1) < len(self.code) and self.code[self.current_position + 1] == "=":
                    self.current_position += 1
                    tokens.append(Token("OPERATOR", char + "="))
                else:
                    tokens.append(Token("OPERATOR", char))
            elif char == "!":
                if (self.current_position + 1) < len(self.code) and self.code[self.current_position + 1] == "=":
                    self.current_position += 1
                    tokens.append(Token("OPERATOR", "!="))
                else:
                    raise SyntaxError("Invalid character '!'")
            elif char in "(){}":
                tokens.append(Token("PUNCTUATION", char))
            elif char.isspace():
                pass
            else:
                raise SyntaxError("Invalid character: {}".format(char))
            self.current_position += 1
        return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def parse(self):
        if not self.tokens:
            return None
        return self.statements()

    def statements(self):
        statements = []
        while self.current_token_index < len(self.tokens):
            token = self.tokens[self.current_token_index]
            if token.type == "IF":
                statements.append(self.if_statement())
            elif token.type == "WHILE":
                statements.append(self.while_loop())
            elif token.type == "PRINT":
                statements.append(self.print_statement())
            else:
                statements.append(self.assignment())
        return statements

    def if_statement(self):
        self.consume("IF")
        condition = self.expr()
        self.consume("PUNCTUATION", "{")
        if_body = self.statements()
        self.consume("PUNCTUATION", "}")
        else_body = []
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index].type == "ELSE":
            self.consume("ELSE")
            self.consume("PUNCTUATION", "{")
            else_body = self.statements()
            self.consume("PUNCTUATION", "}")
        return {"type": "If", "condition": condition, "if_body": if_body, "else_body": else_body}

    def while_loop(self):
        self.consume("WHILE")
        condition = self.expr()
        self.consume("PUNCTUATION", "{")
        body = self.statements()
        self.consume("PUNCTUATION", "}")
        return {"type": "While", "condition": condition, "body": body}

    def print_statement(self):
        self.consume("PRINT")
        expr_to_print = self.expr()
        return {"type": "Print", "expression": expr_to_print}

    def assignment(self):
        variable = self.consume("IDENTIFIER")
        self.consume("OPERATOR", "=")
        expression = self.expr()
        return {"type": "Assignment", "variable": variable.value, "expression": expression}

    def expr(self):
        return self.or_expr()

    def or_expr(self):
        expr = self.and_expr()
        while self.current_token_index < len(self.tokens):
            token = self.tokens[self.current_token_index]
            if token.type == "OPERATOR" and token.value == "or":
                self.current_token_index += 1
                right = self.and_expr()
                expr = {"type": "Or", "left": expr, "right": right}
            else:
                break
        return expr

    def and_expr(self):
        expr = self.equality_expr()
        while self.current_token_index < len(self.tokens):
            token = self.tokens[self.current_token_index]
            if token.type == "OPERATOR" and token.value == "and":
                self.current_token_index += 1
                right = self.equality_expr()
                expr = {"type": "And", "left": expr, "right": right}
            else:
                break
        return expr

    def equality_expr(self):
        expr = self.relational_expr()
        while self.current_token_index < len(self.tokens):
            token = self.tokens[self.current_token_index]
            if token.type == "OPERATOR" and token.value in ("==", "!="):
                self.current_token_index += 1
                right = self.relational_expr()
                expr = {"type": "Equality", "operator": token.value, "left": expr, "right": right}
            else:
                break
        return expr

    def relational_expr(self):
        expr = self.addition()
        while self.current_token_index < len(self.tokens):
            token = self.tokens[self.current_token_index]
            if token.type == "OPERATOR" and token.value in ("<", ">", "<=", ">="):
                self.current_token_index += 1
                right = self.addition()
                expr = {"type": "Relational", "operator": token.value, "left": expr, "right": right}
            else:
                break
        return expr

    def addition(self):
        left = self.multiplication()
        while self.current_token_index < len(self.tokens):
            token = self.tokens[self.current_token_index]
            if token.type == "OPERATOR" and token.value in "+-":
                self.current_token_index += 1
                right = self.multiplication()
                left = {"type": "Addition", "left": left, "right": right}
            else:
                break
        return left

    def multiplication(self):
        left = self.unary()
        while self.current_token_index < len(self.tokens):
            token = self.tokens[self.current_token_index]
            if token.type == "OPERATOR" and token.value in "*/":
                self.current_token_index += 1
                right = self.unary()
                left = {"type": "Multiplication", "left": left, "right": right}
            else:
                break
        return left

    def unary(self):
        token = self.tokens[self.current_token_index]
        if token.type == "OPERATOR" and token.value in "+-":
            self.current_token_index += 1
            return {"type": "Unary", "operator": token.value, "operand": self.unary()}
        else:
            return self.primary()

    def primary(self):
        token = self.tokens[self.current_token_index]
        if token.type == "NUMBER" or token.type == "BOOLEAN":
            self.current_token_index += 1
            return token
        elif token.type == "STRING":  
            self.current_token_index += 1
            return token
        elif token.type == "IDENTIFIER":
            self.current_token_index += 1
            return {"type": "Variable", "name": token.value}
        elif token.type == "PUNCTUATION" and token.value == "(":
            self.current_token_index += 1
            expr = self.expr()
            self.consume("PUNCTUATION", ")")
            return expr
        else:
            raise SyntaxError("Invalid expression")


    def consume(self, token_type, expected=None):
        if self.current_token_index < len(self.tokens):
            token = self.tokens[self.current_token_index]
            if expected is None or (expected is not None and token.value == expected):
                if token.type == token_type:
                    self.current_token_index += 1
                    return token
                else:
                    raise SyntaxError(f"Expected {token_type}, found {token.type}")
            else:
                raise SyntaxError(f"Expected {expected}, found {token.value}")
        else:
            raise SyntaxError("Unexpected end of input")

class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        self.variables = {}

    def execute(self):
        if self.ast:
            for statement in self.ast:
                self.execute_node(statement)

    def execute_node(self, node):
        if isinstance(node, dict):
            if node["type"] == "Assignment":
                variable = node["variable"]
                value = self.evaluate_expression(node["expression"])
                self.variables[variable] = value
            elif node["type"] == "If":
                condition = self.evaluate_expression(node["condition"])
                if condition:
                    for statement in node["if_body"]:
                        self.execute_node(statement)
                else:
                    for statement in node["else_body"]:
                        self.execute_node(statement)
            elif node["type"] == "While":
                condition = self.evaluate_expression(node["condition"])
                while condition:
                    for statement in node["body"]:
                        self.execute_node(statement)
                    condition = self.evaluate_expression(node["condition"])
            elif node["type"] == "Print":
                value = self.evaluate_expression(node["expression"])
                print(value)
            else:
                raise NotImplementedError("Node type not implemented")
        elif isinstance(node, Token):
            return node.value
        else:
            raise TypeError("Invalid node type")

    #def evaluate_expression(self, expr):
    def evaluate_expression(self, expr):
        if isinstance(expr, dict):
            if expr["type"] == "Variable":
                return self.variables[expr["name"]]
            elif expr["type"] == "NUMBER":
                return expr["value"]
            elif expr["type"] == "BOOLEAN":
                return expr["value"]
            elif expr["type"] == "Unary":
                operand = self.evaluate_expression(expr["operand"])
                if expr["operator"] == "+":
                    return +operand
                elif expr["operator"] == "-":
                    return -operand
                else:
                    raise SyntaxError("Invalid unary operator")
            elif expr["type"] == "Addition":
                left = self.evaluate_expression(expr["left"])
                right = self.evaluate_expression(expr["right"])
                return left + right
            elif expr["type"] == "Multiplication":
                left = self.evaluate_expression(expr["left"])
                right = self.evaluate_expression(expr["right"])
                return left * right
            elif expr["type"] == "Or":
                left = self.evaluate_expression(expr["left"])
                right = self.evaluate_expression(expr["right"])
                return left or right
            elif expr["type"] == "And":
                left = self.evaluate_expression(expr["left"])
                right = self.evaluate_expression(expr["right"])
                return left and right
            elif expr["type"] == "Equality":
                left = self.evaluate_expression(expr["left"])
                right = self.evaluate_expression(expr["right"])
                if expr["operator"] == "==":
                    return left == right
                elif expr["operator"] == "!=":
                    return left != right
                else:
                    raise SyntaxError("Invalid equality operator")
            elif expr["type"] == "Relational":
                left = self.evaluate_expression(expr["left"])
                right = self.evaluate_expression(expr["right"])
                if expr["operator"] == "<":
                    return left < right
                elif expr["operator"] == "<=":
                    return left <= right
                elif expr["operator"] == ">":
                    return left > right
                elif expr["operator"] == ">=":
                    return left >= right
                else:
                    raise SyntaxError("Invalid relational operator")
            else:
                raise NotImplementedError("Expression type not implemented")
        elif isinstance(expr, Token):
            return expr.value
        else:
            raise SyntaxError("Invalid expression")

# Example usage
# Read code from the input file
with open('input3.scl', 'r') as file:
    code = file.read()

scanner = Scanner(code)
tokens = scanner.scan()

parser = Parser(tokens)
ast = parser.parse()

interpreter = Interpreter(ast)
interpreter.execute()
