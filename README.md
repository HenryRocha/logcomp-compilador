# Lógica da Computação - Compilador

![svg](http://3.129.230.99/svg/HenryRocha/logcomp-compilador/)

Projeto da matéria de Lógica da Computação.

## Como utilizar

Para utilizar o programa basta executar o seguinte comando:

```bash
python3 main.py source.c
```

Para rodar em modo `debug` basta executar o programa com a _flag_ `-d` e `-vvvv` (o número de `v` controla a quantidade de informações geradas):
```bash
python3 main.py -d source.c
```

```
-d : CRITICAL & ERROR
-d -v : CRITICAL & ERROR & WARN & SUCCESS
-d -vv : CRITICAL & ERROR & WARN & SUCCESS & INFO
-d -vvv : CRITICAL & ERROR & WARN & SUCCESS & INFO & DEBUG
-d -vvvv : CRITICAL & ERROR & WARN & SUCCESS & INFO & DEBUG & TRACE
```

## Tests

Para rodar os testes é necessário ter o `pytest` instalado ou criar um _virtual environment_ usando o [Pipfile](Pipfile) dado.

```bash
pytest test.py
```
Ou
```bash
pipenv run pytest test.py
```

## Diagrama sintático

![Diagrama sintático][1]

## EBNF

A **EBNF** da versão atual só leva em consideração as operações de `+`, `-`, `*`, `/`, sem parênteses.

```
BLOCK = "{", { COMMAND }, "}";
COMMAND = ( λ | ASSIGNMENT | PRINT | IF | WHILE | BLOCK), ";" ;

ASSIGNMENT = IDENTIFIER, "=", EXPRESSION ;
PRINT = "println", "(", EXPRESSION, ")" ;
WHILE = "while", "(", OREXPR, ")", COMMAND;
IF = "if", "(", OREXPR, ")", COMMAND |
     "if", "(", OREXPR, ")", COMMAND, "else", COMMAND;

OREXPR = ANDEXPR, {"||", ANDEXPR};
ANDEXPR = EQEXPR, {"&&", EQEXPR};
EQEXPR = RELEXPR, {"==", RELEXPR};
RELEXPR = EXPRESSION, {(">" | "<"), EXPRESSION};
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = (("+" | "-"), FACTOR) | NUMBER | "(", EXPRESSION, ")" | IDENTIFIER ;

IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
NUMBER = DIGIT, { DIGIT } ;

LETTER = ( a | ... | z | A | ... | Z ) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
```

[1]: ./diagrama-sintatico.drawio.svg
