# scanner-generator

Sobre o gerador de scanners: sua entrada deve ser um conjunto de expressões regulares identificadas pelo tipo de token denotado com alguma possível anotação. A saída deverá ser um scanner para os tokens especificados na entrada.

Sobre o parser: sua entrada deverá ser uma lista de tokens gerada pelo scanner correspondente à linguagem Mini-C e sua saída deverá ser uma árvore sintática para o programa dado como entrada ao scanner, em caso de aceitação do programa, ou uma lista de erros, em caso de não-aceitação.

Os entregáveis são:
- Código fonte
- Makefile e/ou intruções de compilação e execução
- Arquivos de exemplos
- Relatório descrevendo a atuação de cada membro, em caso de trabalho feito em dupla (não serão aceitas entregas feitas por mais do que dois componentes)

### TODO:

- [ ] Gerador de scanner
    - [ ] Transformar expressões regulares em um AFN
    - Estratégia 1:
        - [ ] Transformar cada AFN em um AFD. (Daniel)
        - [ ] Minimização.
        - [ ] Juntar tudo em um único AFN e transformar em um AFD novamente.
    - Estratégia 2:
        - [ ] Juntar tudo em um único AFN e transformar em um AFD.
        - Minimização (x) ?
    - [ ] Implementar algoritmo que leia o autômato e: 
        - Estratégia 1: gere o código do scanner que imprime os tokens
        - Estratégia 2: imprima os tokens
- [ ] Parser top-down
    - [ ] Transformar a BNF para LL: https://github.com/TangoEnSkai/mini-c-compiler-c/blob/master/mini_c.gr.
    - [ ] Calcular First e Follow.
    - [ ] Implementar o parser de acordo com o algoritmo dado.


Estrutura de dados: A definir
