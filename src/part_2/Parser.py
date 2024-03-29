# Parser.py
from Scanner import Scanner, Token

class Parser:
    def __init__(self, filename):
        self.scanner = Scanner(filename)
        # open file

    def begin(self):
        self.start()

    def start(self):
        token, lexeme, position = self.scanner.get_next_token() # we have to do this first or we wount have a token to check for end 
        while token != Token.END:
            # based on token we have print statements 
            if token == Token.IDENTIFIER:
                print(f"The Token at position {position} is an Identifier and the Lexeme is", lexeme)
            elif token == Token.NUMBER:
                print(f"The Token at position {position} is a Number and the Lexeme is", lexeme)
            elif token == Token.SEMICOLON:
                print(f"The Token at position {position} is a Semicolon\n")
            elif token == Token.ASSIGN:
                print(f"The Token at position {position} is an Assignment")
            elif token == Token.LPAREN:
                print(f"The Token at position {position} is a Left Parenthesis")
            elif token == Token.RPAREN:
                print(f"The Token at position {position} is a Right Parenthesis")
            elif token == Token.PLUS:
                print(f"The Token at position {position} is a Plus symbol")
            elif token == Token.MINUS:
                print(f"The Token at position {position} is a Minus symbol")
            elif token == Token.MULTIPLY:
                print(f"The Token at position {position} is a Multiply symbol")
            elif token == Token.DIVIDE:
                print(f"The Token at position {position} is a Divide symbol")
            elif token == Token.COMMENT:
                print(f"The Token at position {position} a Comment and the Lexeme is", lexeme)
            token, lexeme, position = self.scanner.get_next_token()
            # we update the tokens here for the next pass

if __name__ == "__main__":
    # start program
    input_file = "input.scl"
    parser = Parser(input_file)
    parser.begin()
