import pandas as pd
import json

filename = 'lookahead.tsv'
df = pd.read_csv(filename, sep='\t')

variaveis = [var for var in df['Unnamed: 0']]
terminais = [terminal for terminal in df.columns if terminal != 'Unnamed: 0']
lookahead = {}

for var in variaveis:
    lookahead[var] = {}

for terminal in terminais:
    for i in range(len(variaveis)):
        lookahead[variaveis[i]][terminal] = df[terminal][i]

# print(json.dumps(lookahead, indent=4))
with open('lookahed.py', 'w') as file:
    file = file.write(f'LOOKAHEAD = {json.dumps(lookahead, indent=4)}')
