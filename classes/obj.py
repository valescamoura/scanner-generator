from dataclasses import dataclass
from classes.automata import Automata
from typing import List, Optional, Literal

@dataclass
class Token:
    value: str
    type_: str
    line: int


@dataclass
class TokenError:
    token: Optional[Token]
    errorType: Literal['desempilha', 'avanca']

    def print_error(self):
        if self.token is not None:
            print(f'=== Error at line {self.token.line}, token "{self.token.value}".')
            if self.errorType == 'desempilha':
                # print(f'===== Era esperado outro token antes do token {self.token.value}. É provável que este token esteja faltando ou no lugar errado do código.')
                print(f'===== Another token was expected before the "{self.token.value}" token. It is likely that this token is missing or in the wrong place in the code.')
            elif self.errorType == 'avanca':
                # print(f'===== O token {self.token.value} não era esperado. É provável que este token esteja sobrando ou no lugar errado do código.')
                print(f'===== The token "{self.token.value}" was not expected. It is likely that this token is left over or in the wrong place in the code.')
        else: 
            # print('Não foi possível dar match entre todos os tokens informados e a pilha de regras.')
            print('It was not possible to match all the given tokens to the rule stack.')
        print()

@dataclass
class AutomataWrapper:
    token: str
    automata: Automata
    prio: int
    sep: List[str]

@dataclass
class Rule:
    var: str
    rule: List[str]


@dataclass
class Heap():
    heap: List[str]
    heap_aux: List[str]

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
    
    def backup(self) -> None:
        self.heap_aux = self.heap[:]

    def restore(self) -> None:
        self.heap = self.heap_aux[:]
