from typing import List, Dict, Set
from classes.automata import Automata
from classes.state import State

def create_nerode_table(states: List[State]) -> Dict[State, Dict[State, bool]]:

    table = dict()

    for first_state in range(len(states)-1):
        table[states[first_state]] = dict()

        for second_state in range(first_state+1, len(states)):
            table[states[first_state]][states[second_state]] = False

    return table

def simple_elimination(nerode_table: Dict, final_states: list):

    for first_state in nerode_table.keys():

        for second_state in nerode_table[first_state].keys():

            first_is_final = first_state in final_states
            second_is_final = second_state in final_states

            if first_is_final != second_is_final:

                nerode_table[first_state][second_state] = True
    
    return nerode_table

#TODO: finish this
def iterative_elimination(nerode_table: Dict[State, Dict[State, bool]], transition_table: Dict[State, Dict[State, List[State]]], alphabet: List[str]):
    
    marked_state = True

    while marked_state:

        marked_state = False

        for first_state in nerode_table.keys():

            for second_state in nerode_table[first_state].keys():

                if nerode_table[first_state][second_state] == False:

                    for symbol in alphabet:

                        #An afd can only have one destination state for each symbol
                        trans_first_state = transition_table[first_state][symbol][0]
                        trans_second_state = transition_table[second_state][symbol][0]
                        
                        #this entry is not on the table, just ignore
                        if trans_first_state == trans_second_state:
                            continue
                        
                        #could be in the wrong order
                        try:
                            is_marked = nerode_table[trans_first_state][trans_second_state]
                        except KeyError:
                            is_marked = nerode_table[trans_second_state][trans_first_state]

                        if is_marked:
                            nerode_table[first_state][second_state] = True
                            marked_state = True
                            break
    
    return nerode_table

def generate_combined_states(nerode_table: Dict[State, Dict[State, bool]]):
    
    new_states_composition = dict()

    for first_state in nerode_table.keys():

        for second_state in nerode_table[first_state].keys():

            if not nerode_table[first_state][second_state]:

                new_state = State('Gen')
                new_states_composition[new_state] = set([first_state, second_state])
    
    gen_new_state = True

    while gen_new_state:

        gen_new_state = False

        new_table = dict()
        banned = set()

        for first_new_state in new_states_composition.keys():
            
            acc = new_states_composition[first_new_state]

            if first_new_state not in banned:

                for second_new_state in new_states_composition.keys():

                    if first_new_state != second_new_state and second_new_state not in banned:

                        if len(acc & new_states_composition[second_new_state]) > 0:

                            acc = acc | new_states_composition[second_new_state]

                            banned = banned | set([first_new_state,second_new_state])
                            gen_new_state = True

                new_table[first_new_state] = acc
        
        new_states_composition = new_table
    
    return new_states_composition
            
def combine_equivalent_states(new_states: Dict[State, Set[State]], automata: Automata):

    equivalency_table = dict()
    
    for state in automata.states:

        equivalency_table[state] = state
    
    for state1 in new_states.keys():
        
        automata.insert_state(state1)

        for state2 in new_states[state1]:

            equivalency_table[state2] = state1
    
    for state in equivalency_table.keys():

        for symbol in automata.alphabet:

            try:
                v = equivalency_table[automata.transition[state][symbol][0]]
                automata.update_transition(equivalency_table[state], symbol, v)
            except:
                continue
    
    automata.set_initial_state(equivalency_table[automata.initial_state])
    
    return automata

def remove_not_reachable(automata: Automata):
    
    reachable = find_reachable(automata, automata.initial_state)

    states = automata.states[:]

    for state in states:
        if state not in reachable:
            automata.remove_state(state)
    

def find_reachable(automata: Automata, state: State):

    return find_reachable_aux(automata, state, set())

def find_reachable_aux(automata: Automata, state: State, reached: Set):
    reached.add(state)
    for symbol in automata.alphabet:
        next = automata.transition[state][symbol][0]
        if next not in reached:
            reached = reached.union(find_reachable_aux(automata, next, reached))
    return reached


def minimize_afd(automata: Automata):
    
    nerode_table = create_nerode_table(automata.states)

    nerode_table = simple_elimination(nerode_table, automata.final_states)

    nerode_table = iterative_elimination(nerode_table, automata.transition, automata.alphabet)

    new_states = generate_combined_states(nerode_table)

    automata = combine_equivalent_states(new_states, automata)

    remove_not_reachable(automata)

    return automata