from typing import List, Dict, Tuple
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import os
import subprocess

from classes.obj import Token, TokenError, Heap, Rule
from bnf.lookahed import LOOKAHEAD


RULES = {}
heap: Heap
errors: List[TokenError] = []
parser_tree: List[Node]
index = 0  # Índice para percorrer a lista de tokens
current_root_id = 0
backtrack_list = []
backtrack_count = 0
childrens: Dict[str, str] = {}
def parser(tokens: List[Token], lookahead: Dict[str, Dict[str, List[str]]], rules: List[Rule]) -> Tuple[Node, List[TokenError]]:
    global heap
    global errors
    global parser_tree
    global index
    global current_root_id
    global backtrack_list
    global backtrack_count
    global childrens

    heap = Heap(['$', 'Function']) # Inicializa a pilha com o símbolo inicial
    parser_tree = [Node('Function')]
    
    def backtrack(symbol: str):
        global heap
        global errors
        global parser_tree
        global index
        global current_root_id
        global backtrack_list
        global backtrack_count
        global childrens

        current_symbol = symbol
        if current_symbol[0].isupper(): # Simbolo é uma variável
            lookahead_ = lookahead[current_symbol].get(tokens[index].type_, None)
            if lookahead_ == None: # token não esperado/chave tokens[index].type_ incorreta
                index += 1
                errors.append(TokenError(tokens[index], 'avanca')) # tokens a mais
                return True
            elif lookahead_[0] == 'desempilha':
                backtrack_list.append(heap.get_top())
                heap.pop()
                errors.append(TokenError(tokens[index], 'desempilha'))
                return True
            elif lookahead_[0] == 'avanca':
                errors.append(TokenError(tokens[index], 'avanca'))
                index += 1
                backtrack_count += 1
                return True
            else:
                ids_rules = lookahead_

                for id_rule in ids_rules:
                    rule: List[str] = [r for r in rules[id_rule].rule if r != 'Îµ'] # Îµ == ε
    
                    heap.backup()
                    new_nodes = [Node(r, parent=parser_tree[current_root_id]) for r in rule]
                    current_root_id += 1
                    parser_tree[current_root_id:current_root_id] = new_nodes

                    backtrack_list.append(heap.get_top())
                    heap.pop()

                    success = True
                    for s in rule:
                        heap.push([s])
                        if s in LOOKAHEAD.keys(): # s é variável
                            backtrack_count += 1
                            success = backtrack(s)
                        else: # s é terminal
                            if s != tokens[index].type_ and len(ids_rules) != 1: # se dois terminais não dão match mas não tem nenhuma outra regra, aquele caractere pode estar sobrando, tratar diferente
                                success = False

                                for i in range(len(backtrack_list)):
                                    heap.pop()
                                heap.push(backtrack_list)

                                index -= backtrack_count

                                backtrack_list = []
                                backtrack_count = 0
                                break
                            else:
                                success = backtrack(s) # aplicar backtrack pra cair no caso base e dar match

                    if not success:
                        heap.restore()
                        continue # ir para próx iteração do for/próxima regra
                    
                if success:
                    return True
                    # new_nodes = []
                    # for r in rule:
                    #     node = Node(r, parent=parser_tree[current_root_id])
                    #     if childrens.get(r, None) is not None:
                    #         children = Node(childrens[r], parent=node)
                    #         childrens[r] = None
                    #     new_nodes.append(node)

                    # current_root_id += 1
                    # parser_tree[current_root_id:current_root_id] = new_nodes

                    # backtrack_list = []
                    # backtrack_count = 0
        else: # current_symbol[0].islower() -> Simbolo é um terminal
            if current_symbol == tokens[index].type_:
                if tokens[index].type_ != tokens[index].value:
                    # childrens[parser_tree[current_root_id].name] = tokens[index].value
                    if tokens[index].type_ != tokens[index].value:
                        new_nodes = [Node(tokens[index].value, parent=parser_tree[current_root_id])]
                        # current_root_id += 2
                        # parser_tree[current_root_id:current_root_id] = new_nodes
                    # else:
                    #     current_root_id += 1
                   
                backtrack_list.append(heap.get_top())
                backtrack_count += 1
                heap.pop() # Desempilha simbolo
                index += 1 # Avanca na lista de tokens
                return True
            else:
                errors.append(TokenError(tokens[index], 'avanca'))
                index += 1
                backtrack_count += 1
                return True
        
        return False

    backtrack('Function')

    if heap.len() <= 1 and len(tokens) == index+1 and len(errors) == 0:
        print(' Accepted')
    else:
        print(' Not accepted')
        if len(tokens) > index:
            errors.append(TokenError(None, 'avanca'))
        elif heap.len() > 0: 
            errors.append(TokenError(None, 'desempilha'))
    
    # print(f'Tokens:{tokens}')
    # print

    return parser_tree, errors


def read_rules(filename: str) -> Dict[str, Rule]:
    with open(filename) as file:
        file = file.read()

    file = file.split('\n')
    rules_ = [line for line in file if line.strip() != '']
    for rule in rules_:
        id_, var_ = [r.strip() for r in rule.split('->')[0].split(')')]
        rule_ = [r.strip() for r in rule.split('->')[1].split(' ') if r != '']
        RULES[id_] = Rule(var=var_, rule=rule_)

    # import json
    # print(json.dumps(rules, indent=4))

    return RULES


def get_tokens() -> List[Token]:
    token = Token('int', 'int', 1)
    token1 = Token('hello', 'identifier', 1)
    token2 = Token('(', '(', 1)
    token3 = Token('int', 'int', 1)
    token4 = Token('h', 'identifier', 1)
    tokenerr = Token('(', '(', 1)
    token5 = Token(')', ')', 1)
    token6 = Token('{', '{', 1)
    tokenerr = Token('(', '(', 1)
    token7 = Token('}', '}', 1)
    token8 = Token('$', '$', 1)
    # return [token, token1, token2, token3, token4, tokenerr, token5, token6, tokenerr, token7, token8]
    return [token, token1, token2, token3, token4, token5, token6, token7, token8]


def print_derivation_tree(root):
    print(' The tree leaves are represented in red color...')
    for pre, _, node in RenderTree(root):
        if not node.children and node.name[0].isupper():
            Node('ε', parent=node)
            
    def _get_leaf_color(node):
        color_scheme = ["\033[33m", "\033[32m", "\033[35m", "\033[36m"] # amarelo, verde, azul e ciano
        if not node.children: # folha
            return "\033[31m" # vermelho
        elif node.is_root:
            return "\033[34m" # roxo
        
        color = color_scheme[node.depth % len(color_scheme)]
        return color
    
    for pre, _, node in RenderTree(root):
        print(f"{pre}{_get_leaf_color(node)}{node.name}\033[0m")


def gen_view_for_parser_tree(root):
    node_names = set()
    for pre, _, node in RenderTree(root):
        if node.name in node_names:
            node.name = f'{node.name}_{id(node)}'
        node_names.add(node.name)
        
    root_ = os.path.join(os.getcwd(), 'data')
    path = os.path.join(root_, 'parser_tree.dot')
    path_png = os.path.join(root_, 'parser_tree.png')
    DotExporter(root).to_dotfile(path) # Exportar a árvore para um arquivo DOT
    subprocess.call(['dot', '-Kneato','-Tpng', path, '-o', path_png]) # Usa a instalação do GraphViz


if __name__ == '__main__':
    print('=> Reading rules...')
    rules = read_rules('./bnf/bnf_minic.txt')

    lookahed = LOOKAHEAD

    print('=> Reading tokens...')
    tokens = get_tokens()

    print('=> Start parsing...')
    parser_tree, errors = parser(tokens, lookahed, rules)
    
    if len(errors) == 0:
        print('=> Print derivation tree...')
        print_derivation_tree(parser_tree[0])
        
        print('=> Generate view for parser tree...')
        gen_view_for_parser_tree(parser_tree[0])
        print(f'See the parser_tree.png file.')
    else:
        print('=> Errors...')
        for err in errors:
            err.print_error()
 