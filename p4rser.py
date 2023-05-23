from typing import List, Dict, Tuple, Optional
from graphviz import Digraph
from treelib import Tree
import os

from classes.obj import Token, TokenError, Heap, Rule
from bnf.lookahed import LOOKAHEAD


RULES = {}
heap: Heap
errors: List[TokenError] = []
tree: Tree
index = 0  # Índice para percorrer a lista de tokens
backup_index = 0
def parser(tokens: List[Token], lookahead: Dict[str, Dict[str, List[str]]], 
                                rules: List[Rule]) -> Tuple[Tree, List[TokenError]]:
    global heap
    global errors
    global index
    global tree
    global backup_index

    heap = Heap(['$', 'Function']) # Inicializa a pilha com o símbolo inicial
    tree = Tree()
    
    def backtrack(symbol: str, parent_node_uri: Optional[str], parent_node_depth: int) -> bool:
        global heap
        global errors
        global index
        global tree
        global backup_index

        current_symbol = symbol
        if current_symbol[0].isupper(): # Simbolo é uma variável
            lookahead_ = lookahead[current_symbol].get(tokens[index].type_, None)
            if lookahead_ == None: # token não esperado/chave tokens[index].type_ incorreta
                index += 1
                errors.append(TokenError(tokens[index], 'avanca')) # tokens a mais
                return True
            elif lookahead_[0] == 'desempilha':
                heap.pop()
                errors.append(TokenError(tokens[index], 'desempilha'))
                return True
            elif lookahead_[0] == 'avanca':
                errors.append(TokenError(tokens[index], 'avanca'))
                index += 1
                return True
            else:
                rules_id = lookahead_
                for rule_id in rules_id:
                    rule: List[str] = [r for r in rules[rule_id].rule]

                    heap.backup()
                    backup_index = index
                    node_id = current_symbol if parent_node_uri is None else f'{current_symbol}{parent_node_depth+1}'
                    if parent_node_uri is None:
                        tree.create_node(current_symbol, node_id)
                    else:
                        node_id = f'{current_symbol}{parent_node_depth+1}'
                        node = tree.get_node(node_id)
                        while node != None:
                            parent_node_depth += 1
                            node_id = f'{current_symbol}{parent_node_depth+1}'
                            node = tree.get_node(node_id)
                        tree.create_node(current_symbol, node_id, parent=parent_node_uri)
                    heap.pop()

                    success = True
                    for s in rule:
                        heap.push([s])
                        if s in LOOKAHEAD.keys(): # s é uma variável
                            success = backtrack(s, node_id, tree.depth(tree.get_node(node_id)))
                            # print(success)
                        else: # s é terminal ou s é epsilon
                            if s == 'Îµ' or s == 'ε': # Îµ == ε:
                                heap.pop() # desempilha símbolo
                                tree.create_node('ε', f'epsilon{parent_node_depth}', parent=node_id)
                            else:
                                success = backtrack(s, node_id, tree.depth(tree.get_node(node_id))) # aplicar backtrack pra cair no caso base e dar match
                                # print(success)
                        if not success:
                            break
                    if not success:
                        heap.restore()
                        index = backup_index
                        tree.remove_node(node_id)
                        continue # ir para próx iteração do for/próxima regra
                    else:
                        return True                 
        else: # current_symbol[0].islower() -> Simbolo é um terminal
            if current_symbol == tokens[index].type_:
                node_id = f'{current_symbol}{parent_node_depth+1}'
                node = tree.get_node(node_id)
                while node != None:
                    parent_node_depth += 1
                    node_id = f'{current_symbol}{parent_node_depth+1}'
                    node = tree.get_node(node_id)
                tree.create_node(current_symbol, node_id, parent=parent_node_uri)
                if tokens[index].type_ != tokens[index].value:
                    tree.create_node(tokens[index].value, f'{tokens[index].value}{parent_node_depth+1}', parent=node_id)
                heap.pop() # Desempilha simbolo
                index += 1 # Avanca na lista de tokens
                return True
            else:
                return False
        return False

    backtrack('Function', None, 0)

    if heap.len() <= 1 and len(tokens) == index+1 and len(errors) == 0:
        print('=====> Accepted')
    else:
        print('=====> Not accepted')
        if len(tokens) > index:
            errors.append(TokenError(None, 'avanca'))
        elif heap.len() > 0: 
            errors.append(TokenError(None, 'desempilha'))

    return tree, errors


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


def print_derivation_tree(tree: Tree):
    tree.show(key=False)


def gen_view_for_derivation_tree(tree: Tree):
    dot = Digraph(format="png")

    def add_nodes_to_digraph(parent_node):
        current_node = tree.get_node(parent_node)
        dot.node(current_node.identifier, label=current_node.tag)
        for child_id in current_node.successors(tree_id=tree.identifier):
            child_node = tree.get_node(child_id)
            dot.edge(current_node.identifier, child_node.identifier)
        for child_id in current_node.successors(tree_id=tree.identifier):
            add_nodes_to_digraph(child_id)

    root_ = os.path.join(os.getcwd(), 'data')
    path_png = os.path.join(root_, 'parser_tree')
    add_nodes_to_digraph('Function')

    dot.render(path_png, view=False)
    print(f'=====> See the data/parser_tree.png file.')


def exec_parser(tokens: List[Token]) -> None:
    print('=> Reading rules...')
    rules = read_rules('./bnf/bnf_minic.txt')

    lookahed = LOOKAHEAD

    print('=> Start parsing...')
    parser_tree, errors = parser(tokens, lookahed, rules)
    
    if len(errors) == 0:
        print('=> Print derivation tree...')
        print_derivation_tree(parser_tree)
        
        print('=> Generate view for parser tree...')
        gen_view_for_derivation_tree(parser_tree)
    else:
        print('=> Errors...')
        for err in errors:
            err.print_error()

if __name__ == '__main__':
   print('=> Reading tokens...')
   tokens = get_tokens()
   exec_parser(tokens)
 