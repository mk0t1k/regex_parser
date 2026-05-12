# Regex Parser

A simple regex parser built from scratch that converts regex patterns into automata to match text.

## How it works

This project uses a recursive descent parser to read regex patterns and build a state machine. The grammar:

```
<regex>  ::= <term> ( '|' <term> )*
<term>   ::= <factor>+
<factor> ::= <atom> ( '*' | '+' | '?' )?
<atom>   ::= char | '(' <regex> ')'
```

## Components

- **lexer.py** - Breaks regex string into tokens
- **parser.py** - Reads tokens and builds an abstract syntax tree (AST)
- **ast.py** - AST node classes and Thompson's construction algorithm (converts regex to NFA)
- **automata.py** - DFA and NFA classes that can accept or reject words

## How to use it

```python
from parser import Parser
from automata import NFA

# Create parser and build automaton
parser = Parser("a|b")
dfa = parser.parse()

print(dfa.accepts("a"))    # True
print(dfa.accepts("b"))    # True
print(dfa.accepts("ab"))   # False
```

## Testing

The tests compare my regex parser against Python's built-in `re` module.

Run the tests to verify everything works:

```bash
python -m unittest discover
```
---

<div align="center">
  
By Michael Kotkin | M3100 group

</div>

---