from dataclasses import dataclass
from typing import List

@dataclass
class Token:
    value: str
    type_: str
    line: int


@dataclass
class TokenError:
    token: Token
    errorType: str

    def print_error(self):
        print(f'Error')


@dataclass
class Rule:
    var: str
    rule: List[str]


@dataclass
class Heap():
    heap: List[str]

    def __init__(self, elems: List[str]):
        self.heap = []
        for elem in elems:
            self.heap.append(elem)

    def push(self, elems: List[str]) -> None:
        for elem in elems:
            self.heap.append(elem)

    def pop(self) -> str:
        return self.heap.pop()
    
    def get_top(self) -> str:
        return self.heap[-1]

    def len(self) -> int:
        return len(self.heap)
