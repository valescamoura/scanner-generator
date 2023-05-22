import jsonpickle
from typing import Dict, List
from classes.automata import Automata
from classes.obj import Token

def read_automata_from_file(filename):

    with open(filename, 'r') as file:

        encoded_list = file.readlines()

        decoded_list = jsonpickle.decode(encoded_list[0])
    
    min_prio = 0
    separators = set()

    for automata_wrapper in decoded_list:
        
        automata_wrapper.prio = int(automata_wrapper.prio)
        separators = separators.union(set(automata_wrapper.sep))
        automata_wrapper.dead_states = find_dead_end(automata_wrapper.automata)

        if automata_wrapper.prio < min_prio:
            min_prio = automata_wrapper.prio

        automata_wrapper.current_state = automata_wrapper.automata.initial_state
        automata_wrapper.finished = False

    return decoded_list, min_prio, separators

def reset_computation(automata_wrapper_list):

    for automata_wrapper in automata_wrapper_list:

        automata_wrapper.finished = False
        automata_wrapper.current_state = automata_wrapper.automata.initial_state

def find_dead_end(automata: Automata):

    dead_ends = []

    for state in automata.states:
        if state not in automata.final_states:
            if all(automata.transition[state][symbol][0] == state for symbol in automata.transition[state].keys()):
                dead_ends.append(state)
    
    return dead_ends

def scan_file(program_file, automata_file): 
    buffer = []
    token_list = []
    error_list = []

    automata_list, min_prio, separators = read_automata_from_file(automata_file)

    with open(program_file, 'r') as file:

        still_active = len(automata_list)
        line_counter = 1
        last_word = ''
        last_sep = ''
        read_next = True

        while True:    

            if read_next:
                char = file.read(1)
            else:
                read_next = True

            if char == '\n':
                line_counter += 1
                continue
            
            for automata in automata_list:
                
                if not automata.finished:

                    try:
                        current_automata = automata.automata
                        current_state = automata.current_state
                        next_state = current_automata.transition[current_state][char][0]
                        automata.current_state = next_state
                        if next_state in automata.dead_states:
                            automata.finished = True
                            still_active -= 1
                    except KeyError:
                        automata.finished = True
                        still_active -= 1
            if still_active == 0:

                still_active = len(automata_list)
                word = ''.join(buffer)
                
                current_token_type = None
                current_prio = min_prio - 1 
                origin_automata = None
                for automata in automata_list:
                    if automata.current_state in automata.automata.final_states:
                        if automata.prio > current_prio:
                            current_prio = automata.prio
                            current_token_type = automata.token
                            origin_automata = automata
                        elif automata.prio == current_prio:
                            raise Exception(f'Tokens {current_token_type} and {automata.token} have overlapping languagens and same priority for {word}')
                if current_token_type != None:
                    if len(origin_automata.sep) > 0:
                        if last_sep in origin_automata.sep:
                            token_list.append(Token(word, current_token_type, line_counter))
                            read_next = False
                            last_sep = ''
                        else:
                            error_list.append(f"Could not find the needed separator between {last_word} and {word} at line {line_counter}. {last_word}{word} is not a valid token")
                    else:
                        token_list.append(Token(word, current_token_type, line_counter))
                        read_next = False
                        last_sep = ''
                else:
                    #separadores podem ter apenas tamanho 1
                    if char not in separators:
                        error_list.append(f'Unrecognizable token {char} at line {line_counter}')
                    else:
                        last_sep = char
                reset_computation(automata_list)
                last_word = word
                buffer = []
            else:
                buffer.append(char)
            
            if char == '':
                break
    
    return token_list, error_list

tokens, errors = scan_file('examples/minic-prog.mc', 'examples/minic_automata.dat')

for token in tokens:
    print(f'token: {token.value} , Type: {token.type_}')

for error in errors:
    print(error)
