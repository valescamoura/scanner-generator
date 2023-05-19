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
    - [ ] Backtracking 

## Configuração do ambiente

- Tenha o python 3 instalado em sua máquina. 

- Necessário instalar GraphViz para geração dos arquivos PNG: https://graphviz.org/download/.
    - Versão utilizada: ```graphviz version 8.0.5 (20230430.1635)```

- Instalar os requirements: ```pip install -r requirements.txt```

## Como utilizar

### Gerador de scanner

#### Formato do input

a ° b = (a°b)
a* = (a)*
a | b = (a|b)

#### Output
Imagem do AFN?

#### Limitações conhecidas
Falta do scanner para interpretar a AFN e ?

### Parser

#### Formato do input

O parser recebe como input uma lista de objetos do tipo Token (veja abaixo). 

```
class Token:
    value: str # representa o valor do token
    type_: str # representa o tipo do token (number, identifier, if etc...)
    line: int # linha onde o Token se encontra no arquivo de entrada.
```

Essa lista idealmente deve ser gerada pelo scanner. Na implementação atual, ainda falta o scanner, geramos algumas entradas de exemplo, no formato esperado como input através da função get_tokens() no código fonte do parser.

#### Output 

O parser percorre toda a lista de tokens e em caso de não-aceitação, a saída é uma série de erros que indicam o caractere e a linha onde o erro surgiu. Ele indica a ocorrência de um token inesperado ou se após algum token era esperado outro token que não apareceu, de acordo com a natureza do erro.

Em caso de aceitação, ele exibe a árvore sintática do programa recebido como input através da lista de tokens. Isso é feito através da impressão da árvore via terminal, com cada um dos níveis da árvore coloridos de forma distinta. As folhas da árvore são sempre coloridas de vermelho. Além disso, ele gera uma visualização gráfica em formato de árvore/grafo PNG e DOT no diretório ```parser_output```.

#### Limitações conhecidas

Atualmente,existem duas versões do parser implementadas. A versão sem backtracking, e a versão com backtracking;

A versão sem backtracking é a versão que estamos utilizando pois ela gera a árvore corretamente. No entanto, ela tem problemas para executar quando para uma determinada variável temos mais de uma opção de regra possível, pois ela só olha a primeira regra.

A versão com backtracking está imcompleta pois não conseguimos gerar a árvore com as relações de pai e filho entre cada par de nós corretamente.

####
