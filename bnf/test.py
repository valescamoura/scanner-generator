from rules import RULES

for k in RULES.keys():
    rules = RULES[k]['rule']
    for r in rules:
        if r == '\u00ce\u00b5': # \u00ce\u00b5 == ε
            print(k)
