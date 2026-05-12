from typing import Any

class Token:
    type: str
    value: Any

    def __init__(self, type: str, value: Any = None):
        self.type = type
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {self.value})'

class Tokenizer:
    text: str
    idx: int

    def __init__(self, text: str):
        self.text = text
        self.idx = 0

    def get_next_token(self) -> Token:

        if self.idx >= len(self.text):
            return Token('EOF')
        
        char = self.text[self.idx]
        self.idx += 1

        if char == '|':   return Token('PIPE')
        elif char == '*': return Token('STAR')
        elif char == '(': return Token('LPAREN')
        elif char == ')': return Token('RPAREN')
        elif char == '+': return Token('PLUS')
        elif char == '?': return Token('QUESTION')
        else:             return Token('CHAR', char)
