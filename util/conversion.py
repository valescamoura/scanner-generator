from typing import List, Dict, Tuple, Set
from classes.state import State
from classes.util import find_equally_formed
from classes.automata import Automata

def generate_new_states(states: List[State]) -> Tuple[List[State], Dict[str, set]]:

    new_state_list = states[:]
    state_composition = dict()

    for state in states:
        state_composition[state] = set([state])

    for width in range(1, len(states)):
        for start in range(len(states)):
            for end in range(start+width, len(states)):
                
                new_state = State('Gen')
                new_state_list.append(new_state)
                state_composition[new_state] = set([states[start]])

                for i in range(width):
                    state_composition[new_state].add(states[end-i])

    return new_state_list, state_composition

def find_E(automata: Automata, state: State):

    return find_E_aux(automata, state, set())
    
def find_E_aux(automata: Automata, state: State, reached_states):

    reached_states.add(state)
    for reached in automata.transition[state]['ε']:
        if reached not in reached_states:
            reached_states = reached_states.union(find_E_aux(automata, reached, reached_states))
    
    return reached_states


def compute_dfa_final_states(nfa_final_states: List[State], dfa_states_composition: Dict[State, Set[State]]):

    dfa_final_states = []

    for dfa_state in dfa_states_composition.keys():

        for state in dfa_states_composition[dfa_state]:

            if state in nfa_final_states:
                dfa_final_states.append(dfa_state)
                break
    
    return dfa_final_states


def convert_to_dfa(automata: Automata):
    
    d =  State('d')
    #generate every possible combination of states for the new automata
    dfa_states, dfa_states_composition = generate_new_states(automata.states)

    dfa_states += [d]

    dfa_initial_state_composition = find_E(automata, automata.initial_state)

    dfa_initial_state = find_equally_formed(dfa_initial_state_composition, dfa_states_composition)

    dfa_final_states = compute_dfa_final_states(automata.final_states, dfa_states_composition)

    dfa_alphabet = automata.alphabet[:]
    dfa_alphabet.remove('ε')

    dfa_automata = Automata(dfa_states, dfa_alphabet, dfa_initial_state, dfa_final_states)

    for dfa_state in dfa_states:

        if dfa_state == d:
            continue

        dfa_state_composition = dfa_states_composition[dfa_state]

        for symbol in dfa_alphabet:
            
            dest = set()

            for composition_state in dfa_state_composition:

                for state in automata.transition[composition_state][symbol]:

                    dest = dest.union(find_E(automata, state))

            dest_state = d
            if len(dest) != 0:
                dest_state = find_equally_formed(dest, dfa_states_composition)
            
            dfa_automata.insert_transition(dfa_state, symbol, dest_state)
    
    for symbol in dfa_alphabet:
        dfa_automata.insert_transition(d, symbol, d)

    return dfa_automata
