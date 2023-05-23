from classes.automata import Automata
from classes.obj import Token
from p4rser import exec_parser
from util.scanner_generator import read_tokens_file, write_automata_to_file
from util.scanner import scan_file

if __name__ == '__main__':
    
    print(f'1 - Gerar os autômatos\n2 - Fazer o parse do programa')
    op = int(input('Digite a opção desejada: \n'))

    if op == 1:
        tokens_file = input('Digite o nome (caminho) do arquivo que contém as definições dos tokens e expressões regulares: \n')
        automata_output_file = input('Digite o nome (caminho) do arquivo de resultado: \n')

        wrapper_list = read_tokens_file(tokens_file)
        write_automata_to_file(automata_output_file, wrapper_list)
    elif op == 2:
        program = input('Digite o nome (caminho) do arquivo que contém o programa: \n')
        automata_output_file = input('Digite o nome (caminho) do arquivo que contém os autômatos: \n')
    
        tokens, errors = scan_file(program, automata_output_file)
        for token in tokens:

            print(f'Token: {token.value}, Type: {token.type_}, line: {token.line}')
        
        if len(errors) > 0:
            print('Found lexical errors in the program. exiting...\n\nErrors:')
            for error in errors:
                print(error)
        else:
            exec_parser(tokens)
