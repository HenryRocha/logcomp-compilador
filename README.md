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

## Como rodar os testes

Para rodar os testes, é necessário ter o pacote `make` instalado. Feito isso, basta rodar `make` para rodar todos os testes.

É possível também especificar qual grupo de testes deseja rodar, com `make valid` ou `make invalid`.

Caso queira passar _flags_ para os tests basta executar o comando a seguir:
```bash
make ARGS="-d" valid
```

## Diagrama sintático

![Diagrama sintático][1]

## EBNF

A **EBNF** da versão atual só leva em consideração as operações de `+`, `-`, `*`, `/`, sem parênteses.

```
EXPRESSION = NUMBER, {("+", "-", "*", "/"), NUMBER}
```

[1]: ./diagrama-sintatico.drawio.svg
