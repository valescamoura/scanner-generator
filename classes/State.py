
class State:

    counter = 0

    def combine(new_name, state_list):
        
        formed_by = set()
        for state in state_list:
            formed_by.add(str(state))

        return State(new_name, formed_by)

    def __init__(self, name, formed_by=None) -> None:

        self.id = State.counter
        self.name = name

        self.formed_by = set()

        if formed_by == None:
            self.formed_by.add(self.__str__())
        else:
            self.formed_by = formed_by 

        State.counter += 1

    def __eq__(self, __value: object) -> bool:

        return str(__value) == self.__str__()

    def __str__(self) -> str:
        return f'{self.name}:{self.id}'