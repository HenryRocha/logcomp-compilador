all: run

compile:
	nasm -f elf32 -F dwarf -g $(ARGS).asm
	ld -m elf_i386 -o out $(ARGS).o

run: compile
	sh -c "./out"

test:
	pipenv run pytest test.py
