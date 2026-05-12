from automata import State, NFA

class ASTNode:
    def to_nfa(self): pass

class CharNode(ASTNode):
    def __init__(self, value): self.value = value
    def __repr__(self): return f"Char('{self.value}')"

    def to_nfa(self) -> NFA:
        s1 = State()
        s2 = State()
        s1.add_transition(self.value, s2)
        return NFA(s1, s2) 

class ConcatNode(ASTNode):
    def __init__(self, left, right): self.left, self.right = left, right
    def __repr__(self): return f"Concat({self.left}, {self.right})"

    def to_nfa(self) -> NFA:
        right_nfa = self.right.to_nfa()
        left_nfa = self.left.to_nfa()

        left_nfa.accept.add_transition(None, right_nfa.start)
        return NFA(left_nfa.start, right_nfa.accept)

class UnionNode(ASTNode):
    def __init__(self, left, right): self.left, self.right = left, right
    def __repr__(self): return f"Union({self.left}, {self.right})"

    def to_nfa(self) -> NFA:
        right_nfa = self.right.to_nfa()
        left_nfa = self.left.to_nfa()

        s1 = State()
        s2 = State()
        s1.add_transition(None, left_nfa.start)
        s1.add_transition(None, right_nfa.start)
        right_nfa.accept.add_transition(None, s2)
        left_nfa.accept.add_transition(None, s2)
        return NFA(s1, s2)

class StarNode(ASTNode):
    def __init__(self, child): self.child = child
    def __repr__(self): return f"Star({self.child})"

    def to_nfa(self) -> NFA:
        child_nfa = self.child.to_nfa()

        s1 = State()
        s2 = State()
        s1.add_transition(None, child_nfa.start)
        s1.add_transition(None, s2)
        child_nfa.accept.add_transition(None, s2)
        child_nfa.accept.add_transition(None, child_nfa.start)
        return NFA(s1, s2)

class PlusNode(ASTNode):
    def __init__(self, child): self.child = child
    def __repr__(self): return f"Plus({self.child})"

    def to_nfa(self) -> NFA:
        child_nfa = self.child.to_nfa()

        s1 = State()
        s2 = State()
        s1.add_transition(None, child_nfa.start)
        child_nfa.accept.add_transition(None, s2)
        child_nfa.accept.add_transition(None, child_nfa.start)
        return NFA(s1, s2)

class QuestionNode(ASTNode):
    def __init__(self, child): self.child = child
    def __repr__(self): return f"Question({self.child})"

    def to_nfa(self) -> NFA:
        child_nfa = self.child.to_nfa()

        s1 = State()
        s2 = State()
        s1.add_transition(None, child_nfa.start)
        s1.add_transition(None, s2)
        child_nfa.accept.add_transition(None, s2)
        return NFA(s1, s2)