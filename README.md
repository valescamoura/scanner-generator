# scanner-generator

## Descrição do trabalho:
Sobre o gerador de scanners: sua entrada deve ser um conjunto de expressões regulares identificadas pelo tipo de token denotado com alguma possível anotação. A saída deverá ser um scanner para os tokens especificados na entrada.

Sobre o parser: sua entrada deverá ser uma lista de tokens gerada pelo scanner correspondente à linguagem Mini-C e sua saída deverá ser uma árvore sintática para o programa dado como entrada ao scanner, em caso de aceitação do programa, ou uma lista de erros, em caso de não-aceitação.

Os entregáveis são:
- Código fonte
- Makefile e/ou intruções de compilação e execução
- Arquivos de exemplos
- Relatório descrevendo a atuação de cada membro, em caso de trabalho feito em dupla.

## Distribuição das Tasks:

- Gerador de scanner (Integrante: Daniel)
    - [x] Transformar expressões regulares em um AFN. (Daniel)
    - [x] Transformar cada AFN em um AFD. (Daniel)
    - [x] Minimização de cada AFD. (Daniel)
    - [ ] Implementar algoritmo que leia o autômato e imprima os tokens. (Daniel)
- Parser top-down (Integrante: Valesca)
    - [x] Transformar a BNF para LL e simplificar regras onde for possível: https://github.com/TangoEnSkai/mini-c-compiler-c/blob/master/mini_c.gr.
    - [x] Calcular First e Follow.
    - [x] Montar tabela de lookahed com first, follow e informações de desempilha a pilha e avançar na lista de erros para contrução das mensagens de erro. Manipulação da tabela para tranformar em formato suportado pelo python.

    - [x] Implementar da lógica "básica" do parser (sem backtracking) -> resolução das regras de cada variáveis, match etc.
    - [x] Implementação das mensagens de erro.
    - [x] Geração da árvore de derivação.
        - [x] Impressão no terminal.
        - [x] Gerar imagem com esquema da árvore como output.
    - [x] Backtracking.

## Configuração do ambiente

- Tenha o python 3 instalado em sua máquina. 

- Necessário instalar GraphViz para geração dos arquivos PNG: https://graphviz.org/download/.
    - Versão utilizada: ```graphviz version 8.0.5 (20230430.1635)```

- Instalar os requirements: ```pip install -r requirements.txt```

## Como utilizar

### Gerador de scanner

### Execução

Os exemplos gerados podem ser visualizados através da execução do scanner-generator.py

python3 scanner-generator.py

#### Formato do input

O input é fornecido no formato JSON, com a seguinte caracterização (Exemplo):

```
{ 
    "identifier": { # identifier representa o nome do token
        "regexp": "([A-z]°(([A-z]|[0-9]))*)", # expressão regular que define o token
        "prio": "2", # Prioridade do token em relação aos outros que possam aceitar a mesma cadeia
        "sep": [" "] # Separadores necessários para o token
    }
}
```

Para simplificação da implementação do parser, foi adotado o seguinte formato para expressões regulares:

- **CONCATENAÇÃO -> ab** : (a°b)

- **ESTRELA -> a\***: (a)*

- **OU -> a | b**: (a|b)

*Como demonstrado acima, nunca usar espaços em branco na expressão e sempre utilizar os parêntesis, como especificado.*

#### Output

Os estados de cada AFD e a tabela de transição.

#### Limitações conhecidas

No momento está faltando a implementação do scanner em si que irá fazer o scan dos tokens utilizando os autômatos gerados e um arquivo de entrada.
Não temos uma forma de visualizar graficamente os autômatos gerados.

### Parser

#### Formato do input

O parser recebe como input uma lista de objetos do tipo Token (veja abaixo). 

```
class Token:
    value: str # representa o valor do token
    type_: str # representa o tipo do token (number, identifier, if etc...)
    line: int # linha onde o Token se encontra no arquivo de entrada.
```

Essa lista é gerada pelo scanner.

#### Output 

O parser percorre toda a lista de tokens e em caso de não-aceitação, a saída é uma série de erros que indicam o caractere e a linha onde o erro surgiu. Ele indica a ocorrência de um token inesperado ou se após algum token era esperado outro token que não apareceu, de acordo com a natureza do erro.

Em caso de aceitação, ele exibe a árvore sintática do programa recebido como input através da lista de tokens. Isso é feito através da impressão da árvore via terminal. Além disso, ele gera uma visualização gráfica em formato de árvore PNG e DOT no diretório ```/data/parser_tree.png```.

#### Limitações conhecidas

?

#### Como executar

```
python .\parser_without_backtracking.py
```
