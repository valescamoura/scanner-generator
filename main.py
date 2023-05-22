from typing import List

from classes.automata import Automata
from classes.obj import Token
from classes.state import State
from p4rser import exec_parser
from util.conversion import convert_to_dfa
from util.minimization import minimize_afd
from util.reparser import recursive_solver

#put here some examples 

if __name__ == '__main__':
    
    tokens: List[Token]
    exec_parser(tokens)
