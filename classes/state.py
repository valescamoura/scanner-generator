
class State:

    counter = 0

    def __init__(self, name) -> None:

        self.id = State.counter
        self.name = name

        State.counter += 1

    def __eq__(self, __value: object) -> bool:

        return str(__value) == str(self)

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f'{self.name}:{self.id}'
    
    def __hash__(self) -> int:
        return hash(str(self))