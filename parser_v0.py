from typing import List, Dict, Tuple
from anytree import Node, RenderTree
from treelib import Tree
from anytree.exporter import DotExporter
import os
import subprocess

from classes.obj import Token, TokenError, Heap, Rule
from bnf.lookahed import LOOKAHEAD

RULES = {}


def parser(tokens: List[Token], lookahead: Dict[str, Dict[str, List[str]]], rules: List[Rule]) -> Tuple[Node, List[TokenError]]:
    heap = Heap(['$', 'Function']) # Inicializa a pilha com o símbolo inicial
    index = 0 # Índice para percorrer a lista de tokens
    errors: List[TokenError] = []
    parser_tree: List[Node] = [Node('Function')]
    current_root_id = 0

    while index < len(tokens):
        current_symbol = heap.get_top()

        if current_symbol[0].isupper(): # Simbolo é uma variável
            lookahead_ = lookahead[current_symbol].get(tokens[index].type_, None)
            if lookahead_ == None:
                index += 1
                errors.append(TokenError(tokens[index], 'avanca')) # tokens a mais
            elif lookahead_ == 'desempilha':
                heap.pop()
                errors.append(TokenError(tokens[index], 'desempilha'))
            elif lookahead_ == 'avanca':
                index += 1
                errors.append(TokenError(tokens[index], 'avanca'))
            else:
                ids_rules = lookahead_
                # for id_rule in ids_rules:
                id_rule = ids_rules[0]
                rule: List[str] = [r for r in rules[id_rule].rule if r != 'Îµ'] # Îµ == ε
        
                heap.pop()
                heap.push(rule[::-1])
                
                new_nodes = [Node(r, parent=parser_tree[current_root_id]) for r in rule]
                current_root_id += 1
                parser_tree[current_root_id:current_root_id] = new_nodes

                # break # tratar. ver se regra aceita, backtracking etc

        else: # current_symbol[0].islower() -> Simbolo é um terminal
            if current_symbol == tokens[index].type_:
                if tokens[index].type_ != tokens[index].value:
                    new_nodes = [Node(tokens[index].value, parent=parser_tree[current_root_id])]
                    current_root_id += 2
                    parser_tree[current_root_id:current_root_id] = new_nodes
                else:
                    current_root_id += 1

                heap.pop() # Desempilha simbolo
                index += 1 # Avanca na lista de tokens
            else:
                raise Exception('Error')
            
    if heap.len() == 0 and len(tokens) == index:
        print(' Aceito!')
    else:
        raise Exception('Error')
    
    # print(parser_tree)
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
    token5 = Token(')', ')', 1)
    token6 = Token('{', '{', 1)
    token7 = Token('}', '}', 1)
    token8 = Token('$', '$', 1)
    return [token, token1, token2, token3, token4, token5, token6, token7, token8]


def print_derivation_tree(root):
    print('The tree leaves are represented in red color...')
    for pre, _, node in RenderTree(root):
        if not node.children and node.name[0].isupper():
            Node('ε', parent=node)
            
    def _get_leaf_color(node):
        if not node.children:
            return "\033[31m"
        return ''
    
    for pre, _, node in RenderTree(root):
        print(f"{pre}{_get_leaf_color(node)}{node.name}\033[0m")


def gen_view_for_parser_tree(root):
    node_names = set()
    for pre, _, node in RenderTree(root):
        if node.name in node_names:
            node.name = f'{node.name}_{id(node)}'
        node_names.add(node.name)
        
    path = os.path.join(os.getcwd(), 'parser_tree.dot')
    path_png = os.path.join(os.getcwd(), 'parser_tree.png')
    DotExporter(root).to_dotfile(path) # Exportar a árvore para um arquivo DOT
    subprocess.call(['dot', '-Kneato','-Tpng', path, '-o', path_png]) # Usa a instalação do GraphViz


def gen_view_for_parser_tree_temp(nodes):
    tree = Tree()

    count = 0
    for node in nodes:
        if node.parent is None:
            tree.create_node(node.name, count)
        else:
            id_ = f'{node.name.lower()}{node.height}'
            tree.create_node(node.name, id_, parent=f'{node.name.lower()}{node.height-1}')
        count += 1

    path = os.path.join(os.getcwd(), 'parser_tree.dot')
    path_png = os.path.join(os.getcwd(), 'parser_tree.png')
    DotExporter(tree).to_dotfile(path) # Exportar a árvore para um arquivo DOT
    subprocess.call(['dot', '-Kneato','-Tpng', path, '-o', path_png]) # Usa a instalação do GraphViz


if __name__ == '__main__':
    print('Reading rules...')
    rules = read_rules('./bnf/bnf_minic.txt')

    lookahed = LOOKAHEAD

    print('Reading tokens...')
    tokens = get_tokens()

    print('Start parsing...')
    parser_tree, errors = parser(tokens, lookahed, rules)
    
    print('Print derivation tree...')
    print_derivation_tree(parser_tree[0])
    
    print('Generate view for parser tree...')
    gen_view_for_parser_tree(parser_tree[0])
    print(f'See the parser_tree.png file.')