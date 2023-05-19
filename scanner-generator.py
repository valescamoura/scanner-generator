import json
import jsonpickle
from classes.obj import AutomataWrapper
from util.reparser import recursive_solver
from util.conversion import convert_to_dfa
from util.minimization import minimize_afd

#((([0-9])*°.)°([0-9])*)
#([0-9])*°.°([0-9])*

def read_tokens_file(filename):

    with open(filename, 'r') as file:
        data = file.read()

    js = json.loads(data)

    wrapper_list = []

    for token in js.keys():

        automata = recursive_solver(js[token]['regexp'])
        automata = convert_to_dfa(automata)
        automata = minimize_afd(automata)

        wrapper = AutomataWrapper(token, automata, js[token]['prio'], js[token]['sep'])

        wrapper_list.append(wrapper)

    return wrapper_list

def write_automata_to_file(filename, wrappper_list):

    with open(filename, 'w') as file:

        serialized_list = jsonpickle.encode(wrappper_list)

        file.write(serialized_list)

def read_automata_from_file(filename):

    with open(filename, 'r') as file:

        encoded_list = file.readlines()

        decoded_list = jsonpickle.decode(encoded_list[0])
    
    return decoded_list

wrapper_list = read_tokens_file('tokens.txt')
write_automata_to_file('minic_automata.dat', wrapper_list)

abc = read_automata_from_file('minic_automata.dat')
print(abc)