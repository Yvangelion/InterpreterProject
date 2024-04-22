import sys
import re

# Token types
class TokenType:
    KEYWORD = 'KEYWORD'
    IDENTIFIER = 'IDENTIFIER'
    STRING_LITERAL = 'STRING_LITERAL'
    REAL_CONSTANT = 'REAL_CONSTANT'
    INTEGER_CONSTANT = 'INTEGER_CONSTANT'
    OPERATOR = 'OPERATOR'
    DELIMITER = 'DELIMITER'
    COMMENT = 'COMMENT'
    EOF = 'EOF'

# Token class
class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

# Lexer class
class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.current_char = self.code[self.position] if self.position < len(self.code) else None
        self.keywords = {'set', 'print', 'if', 'else', 'while'}  # Add more keywords as needed

    def advance(self):
        self.position += 1
        if self.position < len(self.code):
            self.current_char = self.code[self.position]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha():
                return self.get_keyword_or_identifier()
            elif self.current_char.isdigit() or self.current_char == '.':
                return self.get_number()
            elif self.current_char == '"':
                return self.get_string_literal()
            elif self.current_char in {'+', '-', '*', '/'}:
                token = Token(TokenType.OPERATOR, self.current_char)
                self.advance()
                return token
            elif self.current_char in {'=', '(', ')', ';'}:
                token = Token(TokenType.DELIMITER, self.current_char)
                self.advance()
                return token
            elif self.current_char == '#':
                return self.get_comment()
            else:
                raise SyntaxError(f'Invalid character: {self.current_char}')

        return Token(TokenType.EOF, None)

    def get_keyword_or_identifier(self):
        identifier = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            identifier += self.current_char
            self.advance()
        if identifier.lower() in self.keywords:
            return Token(TokenType.KEYWORD, identifier)
        return Token(TokenType.IDENTIFIER, identifier)

    def get_number(self):
        number = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            number += self.current_char
            self.advance()
        if '.' in number:
            return Token(TokenType.REAL_CONSTANT, float(number))
        else:
            return Token(TokenType.INTEGER_CONSTANT, int(number))

    def get_string_literal(self):
        self.advance()  # Skip opening quote
        string_literal = ''
        while self.current_char is not None and self.current_char != '"':
            string_literal += self.current_char
            self.advance()
        if self.current_char == '"':
            self.advance()  # Skip closing quote
            return Token(TokenType.STRING_LITERAL, string_literal)
        else:
            raise SyntaxError('Unterminated string literal')

    def get_comment(self):
        comment = ''
        while self.current_char is not None and self.current_char != '\n':
            comment += self.current_char
            self.advance()
        return Token(TokenType.COMMENT, comment.strip())

# Main function
def main():
    if len(sys.argv) != 2:
        print("Usage: python interpreter.py input.scl")
        return

    file_path = sys.argv[1]
    try:
        with open(file_path, 'r') as file:
            code = file.read()
            lexer = Lexer(code)
            token = lexer.get_next_token()
            while token.type != TokenType.EOF:
                print(token)
                token = lexer.get_next_token()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")

if __name__ == "__main__":
    main()
