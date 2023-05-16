from Classes.Automata import Automata
from Classes.State import State
from util.conversion import convert_to_dfa
from util.minimization import * 


if __name__ == '__main__':


    q1 = State('q1')
    q2 = State('q2')
    q3 = State('q3')
    states = [q1, q2, q3]
    alphabet = ['a', 'b', 'ε']
    initial_state = q1
    final_states = [q1]

    a = Automata(states,alphabet,initial_state,final_states)

    a.insert_transition(q1, 'ε',q3)
    #a.insert_transition('q3', 'ε','q2')
    a.insert_transition(q1, 'b',q2)
    a.insert_transition(q2, 'a',q2)
    a.insert_transition(q2, 'a',q3)
    a.insert_transition(q2, 'b',q3)
    a.insert_transition(q3, 'a',q1)
    #a.insert_transition(q3, 'ε',q1)

    print(a.initial_state)

    #print(convert_to_dfa(a).transition)
    """
    states = ['A', 'B', 'C', 'D', 'E', 'F']
    final = ['C', 'D', 'E']

    nerode_table = create_nerode_table(states)

    nerode_table = simple_elimination(nerode_table, final)

    print(nerode_table)
    """