from typing import Set, Dict
from classes.state import State

def find_equally_formed(single_state_composition: Set[State], multiple_state_compositions: Dict[State, Set[State]]):

    for state in multiple_state_compositions.keys():

        if multiple_state_compositions[state] == single_state_composition:
            return state
    
    return None