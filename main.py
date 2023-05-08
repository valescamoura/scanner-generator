from Classes.Automata import Automata
from util.conversion import convert_to_dfa


if __name__ == '__main__':

    states = ['q1', 'q2', 'q3']
    alphabet = ['a', 'b', 'ε']
    initial_state = 'q1'
    final_states = ['q1']

    a = Automata(states,alphabet,initial_state,final_states)

    a.insert_transition('q1', 'ε','q3')
    #a.insert_transition('q3', 'ε','q2')
    a.insert_transition('q1', 'b','q2')
    a.insert_transition('q2', 'a','q2')
    a.insert_transition('q2', 'a','q3')
    a.insert_transition('q2', 'b','q3')
    a.insert_transition('q3', 'a','q1')
    #a.insert_transition('q3', 'ε','q1')

    print(convert_to_dfa(a).transition)