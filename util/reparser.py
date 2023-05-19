from classes.automata import Automata
from classes.automata import State

er = "[A-z]°([A-z]|[0-9]°[A-Z])*"
"([A-z])°([A-z]|[0-9])*"
"""
a ° b = (a°b)
a* = (a)*
a | b = (a|b)
([A-z]°(([A-z]|[0-9]))*)
([A-z]°(([A-z]|[0-9]))*)
"""


def recursive_solver(regex: str) -> Automata:
    
    par_count = 0
    for ind, char in enumerate(regex):
        if char == '(':
            par_count += 1
        elif char == ')':
            par_count -= 1
        elif char == '°' and par_count == 1:
            return concat(regex[1:ind], regex[ind+1:-1])
        elif char == '|' and par_count == 1:
            return union(regex[1:ind], regex[ind+1:-1])
        elif char == '*' and par_count == 0:
            return star(regex[1:ind-1])

    return create_automata(regex)

def create_automata(terminal: str) -> Automata:
    
    upper_case = range(65,91)
    lower_case = range(97,123)
    num = range(48,58)
    alphabet = []
    q0 = State('q0')
    q1 = State('q1')
    states = [q0,q1]
    initial_state = q0
    final_states = [q1]

    res = Automata(states, alphabet, initial_state, final_states)

    def insert_range(r: range, automata: Automata):
        for char in r:
            symbol = chr(char)
            automata.insert_symbol(symbol)
            automata.insert_transition(initial_state, symbol, q1)

    if terminal == '[A-z]':
        insert_range(upper_case, res)
        insert_range(lower_case, res)
    elif terminal == '[A-Z]':
        insert_range(upper_case, res)
    elif terminal == '[a-z]':   
        insert_range(lower_case, res)
    elif terminal == '[0-9]':
        insert_range(num, res)
    else:
        res.insert_symbol(terminal)
        res.insert_transition(q0, terminal, q1)
    
    return res



def concat(exp1: str, exp2: str) -> Automata:
    
    a1 = recursive_solver(exp1)
    a2 = recursive_solver(exp2)

    new_alphabet = list(set(a1.alphabet).union(set(a2.alphabet + ['ε'])))
    new_states = list(set(a1.states).union(set(a2.states)))
    initial_state = a1.initial_state
    final_states = a2.final_states

    res = Automata(new_states, new_alphabet, initial_state, final_states)

    copy_transition(a1, res)
    copy_transition(a2, res)

    for state in a1.final_states:
        res.insert_transition(state, 'ε', a2.initial_state)
    
    return res

def star(exp: str):
    
    a1 = recursive_solver(exp)

    new_state = State('q1')
    initial_state = new_state
    new_states = a1.states + [new_state]
    final_states = a1.final_states + [new_state]
    new_alphabet = list(set(a1.alphabet).union(set(['ε'])))

    res = Automata(new_states, new_alphabet, initial_state, final_states)

    copy_transition(a1, res)

    for state in final_states:
        res.insert_transition(state, 'ε', a1.initial_state)

    return res


def union(exp1: str, exp2:str):
    
    a1 = recursive_solver(exp1)
    a2 = recursive_solver(exp2)

    new_state = State('q1')
    new_alphabet = list(set(a1.alphabet).union(set(a2.alphabet + ['ε'])))
    final_states = list(set(a1.final_states).union(set(a2.final_states)))
    new_states = list(set(a1.states).union(set(a2.states))) + [new_state]
    initial_state = new_state

    res = Automata(new_states, new_alphabet, initial_state, final_states)

    copy_transition(a1, res)
    copy_transition(a2, res)

    res.insert_transition(initial_state, 'ε', a1.initial_state)
    res.insert_transition(initial_state, 'ε', a2.initial_state)

    return res

def copy_transition(a1: Automata, a2: Automata):

    for state in a1.transition.keys():

        for symbol in a1.transition[state]:
            
            for destination in a1.transition[state][symbol]:
                a2.insert_transition(state, symbol, destination)