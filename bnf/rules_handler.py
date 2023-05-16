import json

def read_and_build_rules(filename: str) -> None:
    rules = {} 
    with open(filename) as file:
        file = file.read()

    file = file.split('\n')
    rules_ = [line for line in file if line.strip() != '']
    for rule in rules_:
        id_, var_ = [r.strip() for r in rule.split('->')[0].split(')')]
        rule_ = [r.strip() for r in rule.split('->')[1].split(' ') if r != '']
        # print(id_, var_, rule_)

        rules[id_] = {
            'var': var_,
            'rule': rule_
        }

    # print(json.dumps(rules, indent=4))
    with open('rules.py', 'w') as file:
        file = file.write(f'RULES = {json.dumps(rules, indent=4)}')


if __name__ == '__main__':
    filename = 'bnf_minic.txt'
    print('Reading and building rules...')
    read_and_build_rules(filename)
