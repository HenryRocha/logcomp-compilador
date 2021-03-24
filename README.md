# Lógica da Computação - Compilador

Projeto da matéria de Lógica da Computação.

## Como utilizar

Para utilizar o programa basta executar o seguinte comando:

```bash
python3 main.py "1+1"
```

Para rodar em modo `debug` basta executar o programa com a _flag_ `-d`:
```bash
python3 main.py -d "1+1"
```

## Diagrama sintático

![Diagrama sintático][1]

## EBNF

A **EBNF** da versão atual só leva em consideração as operações de `+`, `-`, `*`, `/`, sem parênteses.

```
EXPRESSION = TERM, {ADDSUB, TERM}
TERM = RECURSION, {MULTDIV, RECURSION}
RECURSION = "(", EXPRESSION, ")" | NUMBER
ADDSUB = "+" | "-"
MULTDIV = "*" | "/"
```

[1]: ./diagrama-sintatico.drawio.svg
