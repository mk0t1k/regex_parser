from itertools import product
from ast import ASTNode, CharNode, ConcatNode, UnionNode, StarNode, PlusNode, QuestionNode
from lexer import Tokenizer, Token

class Parser:
    current_token: Token
    tokenizer: Tokenizer

    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer
        self.current_token = self.tokenizer.get_next_token()

    def consume(self, token_type: str):
        if self.current_token.type == token_type:
            self.current_token = self.tokenizer.get_next_token()
        else:
            raise Exception(f"Expected {token_type}, got {self.current_token.type}")
    
    def parse_regex(self):
        """
        <regex> ::= <term> ('|' <term>)*
        """
        node = self.parse_term()

        while self.current_token.type == 'PIPE':
            self.consume('PIPE')
            right_node = self.parse_term()
            node = UnionNode(node, right_node)

        return node

    def parse_term(self) -> ASTNode:
        """
        <term> ::= <factor>+
        """
        node = self.parse_factor()

        while self.current_token.type in ('CHAR', 'LPAREN'):
            right_node = self.parse_factor()
            node = ConcatNode(node, right_node)

        return node

    def parse_factor(self) -> ASTNode:
        """
        <factor> ::= <atom> ('*' | '+' | '?')?
        """
        node = self.parse_atom()
        token = self.current_token

        if token.type == 'STAR':
            self.consume('STAR')
            return StarNode(node)
        elif token.type == 'PLUS':
            self.consume('PLUS')
            return PlusNode(node)
        elif token.type == 'QUESTION':
            self.consume('QUESTION')
            return QuestionNode(node)
        else:
            return node

    def parse_atom(self) -> ASTNode:
        """
        <atom> ::= char | '(' <regex> ')'
        """
        token = self.current_token

        if token.type == 'CHAR':
            self.consume('CHAR')
            return CharNode(token.value)
        elif token.type == 'LPAREN':
            self.consume('LPAREN')
            node = self.parse_regex()
            self.consume('RPAREN')
            return node
        else:
            raise Exception(f"Unexpected token in <atom>: {token}")


reg = "ab*c|d"
t = Tokenizer(reg)
p = Parser(t)
ast = p.parse_regex()
nfa = ast.to_nfa()
dfa = nfa.to_dfa()

strings = ["".join(p) for n in range(1, 7) for p in product("abcd", repeat=n)]
accepted = [s for s in strings if dfa.accepts(s)]
print(len(accepted))