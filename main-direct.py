from classes.automata import Automata
from classes.obj import Token
from p4rser import exec_parser
from util.scanner_generator import read_tokens_file, write_automata_to_file
from util.scanner import scan_file

if __name__ == '__main__':

        #Use to avoid creating the automata again on subsequent executions
        generate_automata = True

        #file containing the regex definition for each token
        tokens_file = 'examples/tokens.txt'
        
        #file where the generated automata will be stored
        automata_output_file = 'minic-automata.dat'

        if generate_automata:
            wrapper_list = read_tokens_file(tokens_file)
            write_automata_to_file(automata_output_file, wrapper_list)

        program = 'examples/minic-lex-sucess.mc'
    
        tokens, errors = scan_file(program, automata_output_file)
        for token in tokens:

            print(f'Token: {token.value}, Type: {token.type_}, line: {token.line}')
        
        if len(errors) > 0:
            print('Found lexical errors in the program. exiting...\n\nErrors:')
            for error in errors:
                print(error)
        else:
            exec_parser(tokens)
