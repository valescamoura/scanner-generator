"""
This class is used to hold the data structure that represents an Automata.
The transition table is stored in the Automata.transition variable as a dictionary and has the following organization:
transition = {
    state_name: {
        symbol1: list()
        symbol2: list()
    } 
}

That means:
    from each state, each symbol from the alphabet leads to a subset of the state set represented by a list.
    The automata is deterministic if the size of each subset is at maximum 1 and ε is not in the alphabet.
"""

from Classes.State import State

class Automata:

    def __init__(self, states: list, alphabet: list, initial_state: State, final_states=[], token='') -> None:
        
        self.states = states
        self.alphabet = alphabet
        self.token = token
        self.final_states = []

        for state in final_states:
            self.set_final_state(state)
        self.set_initial_state(initial_state)
        self.build_transition_table()

    #Build a clean transition table based on the current set of states and alphabet 
    #The transition table will be wiped out
    def build_transition_table(self):
        
        self.transition = dict()

        for state in self.states:

            state_string = str(state)

            self.transition[state_string] = dict()

            for symbol in self.alphabet:
                self.transition[state_string][symbol] = []

    def set_initial_state(self, initial_state: str):
        
        if initial_state in self.states:
            self.initial_state = initial_state
        else:
            raise Exception(f'Cannot set {initial_state} as the initial state: State not found')

    def insert_transition(self, initial_state: State, symbol : str, destination_state: State):

            try:
                init_state_str = str(initial_state)
                dest_state_str = str(destination_state)
                if destination_state not in self.states:
                    raise Exception(f'Destination state {destination_state} not found')
                if destination_state not in self.transition[init_state_str][symbol]:
                    self.transition[init_state_str][symbol].append(dest_state_str)
                else:
                    print(f'Transition ({initial_state},{symbol}) -> {destination_state} already in transition table')
            except:
                raise Exception(f'transition ({initial_state},{symbol}) -> {destination_state} doesnt match the transition table. Ensure that the states and the symbol are inserted in the automata')
        

    #Turn a state into a final state
    def set_final_state(self, state: State):

        if state in self.states and state not in self.final_states:
                self.final_states.append(state)
        else:
            print(f'State {state} not found or is already final')

    #insert a new state and update the transition table
    def insert_state(self, state: State):
        
        state_str = str(state)

        if state not in self.states:
            self.states.append(state)
            self.transition[state_str] = dict()
            for symbol in self.alphabet:
                self.transition[state_str][symbol] = []
        else:
            print(f'State {state} already exists')
    
    #insert a new symbol and update the transition table
    def insert_symbol(self, symbol: str):
        if symbol not in self.alphabet:
            self.alphabet.append(symbol)
            for state in self.transition.keys():
                self.transition[state][symbol] = []
        else:
            print(f'Symbol {symbol} is already in the alphabet')