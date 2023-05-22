from typing import List, Dict, Tuple, Set
from classes.state import State
from classes.util import find_equally_formed
from classes.automata import Automata

#This function returns all states reachable from a given state using 0 or more ε transitions
def find_E(automata: Automata, state: State):

    return find_E_aux(automata, state, set())
    
def find_E_aux(automata: Automata, state: State, reached_states):

    reached_states.add(state)
    try:
        for reached in automata.transition[state]['ε']:
            if reached not in reached_states:
                reached_states = reached_states.union(find_E_aux(automata, reached, reached_states))
    except KeyError:
        return reached_states
    
    return reached_states

#Returns the set of final states based on each state composition 
#If a state A on the new automata has a final state from the old automata in its composition, then A is final as well
def compute_dfa_final_states(nfa_final_states: List[State], dfa_states_composition: Dict[State, Set[State]]):

    dfa_final_states = []

    for dfa_state in dfa_states_composition.keys():

        for state in dfa_states_composition[dfa_state]:

            if state in nfa_final_states:
                dfa_final_states.append(dfa_state)
                break
    
    return dfa_final_states


def convert_to_dfa(automata: Automata):
    
    #Thrash state, indicates that the computation has reached a dead end
    d =  State('d')

    dfa_states_composition = dict()

    for state in automata.states:
        dfa_states_composition[state] = set([state])

    dfa_states = automata.states[:]

    dfa_states += [d]

    dfa_initial_state_composition = find_E(automata, automata.initial_state)

    #creates the new initial state
    new_state = State('Gen')
    dfa_states += [new_state]
    dfa_states_composition[new_state] = dfa_initial_state_composition
    dfa_initial_state = new_state

    dfa_final_states = []

    dfa_alphabet = automata.alphabet[:]
    if 'ε' in dfa_alphabet:
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
                if dest_state == None:
                    new_state = State('Gen')
                    dfa_automata.insert_state(new_state)
                    dfa_states_composition[new_state] = dest
                    dest_state = new_state
            
            dfa_automata.insert_transition(dfa_state, symbol, dest_state)
    
    for symbol in dfa_alphabet:
        dfa_automata.insert_transition(d, symbol, d)
    
    final = compute_dfa_final_states(automata.final_states, dfa_states_composition)
    for state in final:
        dfa_automata.set_final_state(state)

    return dfa_automata
