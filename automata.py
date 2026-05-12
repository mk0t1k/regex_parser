class State:
    id: int
    transitions: dict[str | None, list['State']]	

    def __init__(self):
        self.transitions = {}
        self.id = None

    def __repr__(self): return f"q{self.id}"

    def add_transition(self, symbol: str | None, to_state: 'State'):
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        self.transitions[symbol].append(to_state)

class DFA:
    def __init__(self, start: State, accept: set[State]):
        self.start  = start
        self.accept = accept
    
    def accepts(self, s: str) -> bool:
        current_state = self.start

        for char in s:
            if char not in current_state.transitions:
                return False
            current_state = current_state.transitions[char][0]

        return current_state in self.accept

class NFA:
    def __init__(self, start: State, accept: State):
        self.start  = start
        self.accept = accept

    def enumerate_states(self):
        visited = set()
        stack = [self.start]
        id_counter = 0

        while stack:
            state = stack.pop()
            if state in visited:
                continue
            visited.add(state)
            state.id = id_counter
            id_counter += 1

            for next_states in state.transitions.values():
                stack.extend(next_states)
    
    def e_closure(self, states: set[State]) -> set[State]:
        closure = set(states)
        stack = list(states)

        while stack:
            state = stack.pop()
            for next_state in state.transitions.get(None, []):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)

        return closure
    
    def to_dfa(self) -> DFA:
        self.enumerate_states()
        start_closure = frozenset(self.e_closure({self.start}))
        dfa_start = State()
        dfa_accept = set()

        state_map = {start_closure: dfa_start}
        stack = [start_closure]

        while stack:
            current_closure = stack.pop()
            current_dfa_state = state_map[current_closure]

            if self.accept in current_closure:
                dfa_accept.add(current_dfa_state)

            symbol_map = {}
            for nfa_state in current_closure:
                for symbol, next_states in nfa_state.transitions.items():
                    if symbol is not None:
                        if symbol not in symbol_map:
                            symbol_map[symbol] = set()
                        symbol_map[symbol].update(next_states)

            for symbol, next_states in symbol_map.items():
                next_closure = frozenset(self.e_closure(next_states))
                if next_closure not in state_map:
                    state_map[next_closure] = State()
                    stack.append(next_closure)
                current_dfa_state.add_transition(symbol, state_map[next_closure])

        return DFA(dfa_start, dfa_accept)
    
    def accepts(self, s: str) -> bool:
        current = self.e_closure({self.start})

        for char in s:
            moves = set()
            for q in current:
                moves.update(q.transitions.get(char, []))
            current = self.e_closure(moves)

        return self.accept in current