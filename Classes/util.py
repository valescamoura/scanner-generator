
def find_equally_formed(state_composition, state_list):

    result = None
    for state_elem in state_list:

        if state_elem.formed_by == state_composition:
            result = state_elem
            break
    
    return result