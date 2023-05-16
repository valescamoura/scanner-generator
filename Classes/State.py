
class State:

    counter = 0

    def combine(state_list):
        
        formed_by = set()
        for state in state_list:
            formed_by.add(str(State))

        return State(formed_by)

    def __init__(self, formed_by=set()) -> None:

        self.id = State.counter
        
        self.formed_by = formed_by

        if self.formed_by == set():
            self.formed_by.add(self.__str__())

        State.counter += 1

    def __eq__(self, __value: object) -> bool:

        return str(__value) == self.__str__()

    def __str__(self) -> str:
        return f'q{self.id}'