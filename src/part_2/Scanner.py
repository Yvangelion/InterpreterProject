import re

class Token:
    # valid tokens 
    INVALID = "INVALID"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    SEMICOLON = "SEMICOLON"
    ASSIGN = "ASSIGN"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    COMMENT = "COMMENT"
    END = "END"

class Scanner:
    def __init__(self, filename): 
        # open file
        with open(filename, 'r') as file:
            self.input_string = file.read()
        self.current_pos = 0
        self.length = len(self.input_string)

    def get_next_token(self):
        # loop through scl file 
        while self.current_pos < self.length and self.input_string[self.current_pos].isspace():
            self.current_pos += 1

        if self.current_pos >= self.length:
            return Token.END, None, self.current_pos

        if self.input_string[self.current_pos] == ';':
            self.current_pos += 1
            return Token.SEMICOLON, None, self.current_pos
        
        elif self.input_string[self.current_pos] == '=':
            self.current_pos += 1
            return Token.ASSIGN, None, self.current_pos
        
        elif self.input_string[self.current_pos] == '(':
            self.current_pos += 1
            return Token.LPAREN, None, self.current_pos
        
        elif self.input_string[self.current_pos] == ')':
            self.current_pos += 1
            return Token.RPAREN, None, self.current_pos
        
        elif self.input_string[self.current_pos] == '+':
            self.current_pos += 1
            return Token.PLUS, None, self.current_pos
        
        elif self.input_string[self.current_pos] == '-':
            self.current_pos += 1
            return Token.MINUS, None, self.current_pos
        
        elif self.input_string[self.current_pos] == '*':
            self.current_pos += 1
            return Token.MULTIPLY, None, self.current_pos
        
        elif self.input_string[self.current_pos] == '/':
            self.current_pos += 1
            return Token.DIVIDE, None, self.current_pos
        
        elif self.input_string[self.current_pos] == '#':
            comment = ""
            self.current_pos += 1 
            while self.current_pos < self.length and self.input_string[self.current_pos] != '\n': # ignore comments until the nextline is found
                comment +=  self.input_string[self.current_pos]
                self.current_pos += 1
            return Token.COMMENT, comment, self.current_pos
        
        elif re.match(r'[a-zA-Z_]', self.input_string[self.current_pos]): # if it starts with letter in the alphabet we assume its idenitfier 
            identifier = ""
            while self.current_pos < self.length and (self.input_string[self.current_pos].isalnum() or self.input_string[self.current_pos] == '_'): 
                identifier += self.input_string[self.current_pos]
                self.current_pos += 1
            return Token.IDENTIFIER, identifier, self.current_pos
        
        elif self.input_string[self.current_pos].isdigit(): # if its digit we make it a number
            number = ""
            while self.current_pos < self.length and self.input_string[self.current_pos].isdigit():
                number += self.input_string[self.current_pos]
                self.current_pos += 1
            return Token.NUMBER, number, self.current_pos

        return Token.INVALID, None, self.current_pos # return none if we dont have a number/identifier, then reutrn current position and the token
