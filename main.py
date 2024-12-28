import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def get_next_token(self):
        text = self.text

        if self.pos >= len(text):
            return Token("EOF", None)

        current_char = text[self.pos]

        if current_char.isdigit():
            start = self.pos
            while self.pos < len(text) and text[self.pos].isdigit():
                self.pos += 1
            return Token("NUMBER", int(text[start:self.pos]))

        if current_char in "+-*/()":
            self.pos += 1
            return Token(current_char, current_char)

        if current_char.isspace():
            self.pos += 1
            return self.get_next_token()

        raise ValueError(f"Caractère invalide : {current_char}")

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise ValueError(f"Token attendu : {token_type}, trouvé : {self.current_token.type}")

    def factor(self):
        """factor : NUMBER | '(' expr ')'"""
        token = self.current_token
        if token.type == "NUMBER":
            self.eat("NUMBER")
            return token.value
        elif token.type == "(":
            self.eat("(")
            result = self.expr()
            self.eat(")")
            return result

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        result = self.factor()
        while self.current_token.type in "*/":
            token = self.current_token
            if token.type == "*":
                self.eat("*")
                result *= self.factor()
            elif token.type == "/":
                self.eat("/")
                result /= self.factor()
        return result

    def expr(self):
        """expr : term ((ADD | SUB) term)*"""
        result = self.term()
        while self.current_token.type in "+-":
            token = self.current_token
            if token.type == "+":
                self.eat("+")
                result += self.term()
            elif token.type == "-":
                self.eat("-")
                result -= self.term()
        return result

class Interpreter:
    def __init__(self, parser):
        self.parser = parser

    def interpret(self):
        return self.parser.expr()

if __name__ == "__main__":
    expression = input("Entrez une expression mathématique : ")
    lexer = Lexer(expression)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    try:
        result = interpreter.interpret()
        print(f"Résultat : {result}")
    except ValueError as e:
        print(f"Erreur : {e}")
