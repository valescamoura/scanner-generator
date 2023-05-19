from classes.automata import Automata
from classes.state import State
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

    a1 = Automata(states,alphabet,initial_state,final_states)

    a1.insert_transition(q1, 'ε',q3)
    #a1.insert_transition('q3', 'ε','q2')
    a1.insert_transition(q1, 'b',q2)
    a1.insert_transition(q2, 'a',q2)
    a1.insert_transition(q2, 'a',q3)
    a1.insert_transition(q2, 'b',q3)
    a1.insert_transition(q3, 'a',q1)
    #a1.insert_transition(q3, 'ε',q1)

    #print(a.initial_state)

    print(convert_to_dfa(a1).transition)
    
    a = State('A')
    b = State('B')
    c = State('C')
    d = State('D')
    e = State('E')
    f = State('F')

    states = [a,b,c,d,e,f]
    alphabet = ['0', '1']
    final = [c,d,e]
    a2 = Automata(states, alphabet, a, final)

    a2.insert_transition(a, '0', b)
    a2.insert_transition(a, '1', c)
    a2.insert_transition(b, '0', a)
    a2.insert_transition(b, '1', d)
    a2.insert_transition(c, '0', e)
    a2.insert_transition(c, '1', f)
    a2.insert_transition(d, '0', e)
    a2.insert_transition(d, '1', f)
    a2.insert_transition(e, '0', e)
    a2.insert_transition(e, '1', f)
    a2.insert_transition(f, '0', f)
    a2.insert_transition(f, '1', f)

    res = minimize_afd(a2)

    print(res.states, res.transition)
