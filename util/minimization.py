from classes.automata import Automata

def create_nerode_table(states: list):

    table = dict()

    for first_state in range(len(states)-1):
        table[states[first_state]] = dict()

        for second_state in range(first_state+1, len(states)):
            table[states[first_state]][states[second_state]] = False

    return table

def simple_elimination(nerode_table: dict, final_states: list):

    for first_state in nerode_table.keys():

        for second_state in nerode_table[first_state].keys():

            first_is_final = first_state in final_states
            second_is_final = second_state in final_states

            if first_is_final != second_is_final:

                nerode_table[first_state][second_state] = True
    
    return nerode_table

#TODO: finish this
def iterative_elimination(nerode_table: dict, transition_table: dict, alphabet: list):
    
    marked_state = True

    while marked_state:

        for first_state in nerode_table.keys():

            for second_state in nerode_table[first_state].keys():

                if nerode_table[first_state][second_state] == False:

                    for symbol in alphabet:

                        pass
