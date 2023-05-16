from Classes.Automata import Automata
from Classes.State import State
from Classes.util import find_equally_formed

def generate_new_states(states):

    new_states = []

    for width in range(1, len(states)):
        for start in range(len(states)):
            for end in range(start+width, len(states)):

                new_state_composition = [states[start]]

                for i in range(width):
                    new_state_composition.append(states[end-i])

                new_states.append(State.combine('Gen', new_state_composition))

    return new_states

def find_E(automata: Automata, state: str):

    return find_E_aux(automata, state, set())
    
def find_E_aux(automata: Automata, state: str, reached_states):

    reached_states.add(state)
    for reached in automata.transition[state]['ε']:
        if reached not in reached_states:
            reached_states = reached_states.union(find_E_aux(automata, reached, reached_states))
    
    return reached_states


def compute_dfa_final_states(nfa_final_states, dfa_states):

    dfa_final_states = []

    for dfa_state in dfa_states:

        dfa_state_composition = dfa_state.formed_by

        for state in dfa_state_composition:

            if state in nfa_final_states:
                dfa_final_states.append(dfa_state)
                break
    
    return dfa_final_states


def convert_to_dfa(automata: Automata):
    
    d =  State('d')
    dfa_states = automata.states + generate_new_states(automata.states) + [d]

    dfa_initial_state_composition = find_E(automata, str(automata.initial_state))

    dfa_initial_state = find_equally_formed(dfa_initial_state_composition, dfa_states)

    dfa_final_states = (compute_dfa_final_states(automata.final_states, dfa_states))

    dfa_alphabet = automata.alphabet[:]
    dfa_alphabet.remove('ε')

    dfa_automata = Automata(dfa_states, dfa_alphabet, dfa_initial_state, dfa_final_states)

    for dfa_state in dfa_states:

        if dfa_state == d:
            continue

        dfa_state_composition = dfa_state.formed_by

        for symbol in dfa_alphabet:
            
            dest = set()

            for composition_state in dfa_state_composition:

                for state in automata.transition[composition_state][symbol]:

                    dest = dest.union(find_E(automata, state))

            dest_state = d
            if len(dest) != 0:
                dest_state = find_equally_formed(dest, dfa_states)
            
            dfa_automata.insert_transition(dfa_state, symbol, dest_state)
    
    for symbol in dfa_alphabet:
        dfa_automata.insert_transition(d, symbol, d)

    return dfa_automata
