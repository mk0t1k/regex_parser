import unittest
import re
from itertools import product

from parser import Parser
from automata import NFA
from lexer import Tokenizer

class TestParser(unittest.TestCase):
    def test1(self):
        regex = "(ab)*abb"
        parser = Parser(Tokenizer(regex))
        dfa = NFA.to_dfa(parser.parse_regex().to_nfa())

        strings = ["".join(p) for n in range(1, 9) for p in product("ab", repeat=n)]
        for s in strings:
            self.assertEqual(dfa.accepts(s), re.fullmatch(regex, s) is not None)

    def test2(self):
        regex = "0*(10*10*)*"
        parser = Parser(Tokenizer(regex))
        dfa = NFA.to_dfa(parser.parse_regex().to_nfa())

        strings = ["".join(p) for n in range(1, 11) for p in product("01", repeat=n)]
        for s in strings:
            self.assertEqual(dfa.accepts(s), re.fullmatch(regex, s) is not None)
    
    def test3(self):
        regex = "0*1?0+"
        parser = Parser(Tokenizer(regex))
        dfa = NFA.to_dfa(parser.parse_regex().to_nfa())

        strings = ["", "0", "3"] # symbol not in alphabet
        for s in strings:
            self.assertEqual(dfa.accepts(s), re.fullmatch(regex, s) is not None)