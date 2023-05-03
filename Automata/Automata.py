"""
This class is used to hold the data structure that represents an Automata.
The transition table is stored in the Automata.transition variable as a dictionary and has the following organization:
transition = {
    state_name: {
        letter1: set()
        letter2: set()
    } 
}

That means:
    from each state, each letter from the alphabet leads to a subset of the state set.
    The automata is deterministic if the size of each subset is at maximum 1 and ε is not in the alphabet.

The final states are organized in a dictionary by the token they represent.
final_states = {
    token: set()
}
"""

class Automata:

    def __init__(self, states: list, alphabet: list, tokens: list) -> None:
        
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.tokens = set(tokens)
        self.initial_state = ''
        self.build_transition_table()
        self.build_final_states_table()

    #Build a clean transition table based on the current set of states and alphabet 
    #The transition table will be wiped out
    def build_transition_table(self):
        
        self.transition = dict()

        for state in self.states:
            self.transition[state] = dict()

            for letter in self.alphabet:
                self.transition[state][letter] = set()
    
    def build_final_states_table(self):

        self.final_states = dict()

        for token in self.tokens:
            self.final_states[token] = set()

    def set_initial_state(self, initial_state: str):
        
        if initial_state in self.states:
            self.initial_state =  initial_state
        else:
            raise Exception('State not found')

    def insert_transition(self, initial_state: str, letter : str, destination_state: str):

            try:
                if not (destination_state in self.states):
                    raise Exception
                self.transition[initial_state][letter].add(destination_state)
            except:
                raise Exception(f'The transition doesnt match the transition table. Ensure that the states and the letter are inserted in the automata')
        

    #Turn a state into a final state
    def define_final_state(self, state: str, token: str):

        if state in self.states:
            if token in self.tokens:
                self.final_states[token].add(state)
            else:
                raise Exception(f'Token {token} not found')
        else:
            raise Exception(f'State {state} not found')


    #insert a new state and update the transition table
    def insert_state(self, state: str):
        
        self.states.add(state)
        self.transition[state] = dict()
        for letter in self.alphabet:
            self.transition[state][letter] = set()
    
    #insert a new token and update the final states dict
    def insert_token(self, token: str):
        self.tokens.add(token)
        self.final_states[token] = set()
    
    #insert a new letter and update the transition table
    def insert_letter(self, letter: str):
        self.alphabet.add(letter)
        for state in self.transition.keys():
            self.transition[state][letter] = set()