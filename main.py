import sys
from classes.automata import Automata
from classes.obj import Token
from p4rser import exec_parser
from util.scanner_generator import read_tokens_file, write_automata_to_file
from util.scanner import scan_file

if __name__ == '__main__':
    
    tokens_file = 'examples/tokens.txt'
    automata_output_file = 'data/minic_automata.dat'
    minic_program = 'examples/minic-sucess.mc'

    wrapper_list = read_tokens_file(tokens_file)
    write_automata_to_file(automata_output_file, wrapper_list)

    tokens, errors = scan_file(minic_program, automata_output_file)
    tokens.append(Token('$', '$', 1))
    for token in tokens:

        print(f'Token: {token.value}, Type: {token.type_}')
    
    if len(errors) > 0:
        print('Found lexical errors in the program. exiting...\n\nErrors:')
        for error in errors:
            print(error)
        sys.exit(1)

    exec_parser(tokens)
