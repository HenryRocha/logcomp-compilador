all: valid invalid

valid:
	# These should run just fine.
	-python3 main.py "1+1" "2"
	-python3 main.py "1 + 1" "2"
	-python3 main.py " 1 + 1 " "2"
	-python3 main.py " 1 - 1 " "0"
	-python3 main.py " 1 - 2 " "-1"
	-python3 main.py "          1     -           2            " "-1"
	-python3 main.py "          1     -2                  " "-1"
	-python3 main.py "          1-           2              " "-1"
	-python3 main.py " 10 + 1 - 10" "1"
	-python3 main.py " 10 - 10 + 100 - 100 + 1000 - 1000" "0"

invalid:
	# These should throw some kind of error.
	-python3 main.py "+"
	-python3 main.py "-"
	-python3 main.py "+1"
	-python3 main.py "1-"
	-python3 main.py ""
	-python3 main.py "1 1"
	-python3 main.py "1 10"
	-python3 main.py "10 10"
	-python3 main.py "10 1"
	-python3 main.py "+1 1"
	-python3 main.py "1 1-"
	-python3 main.py "1 1+1"
	-python3 main.py "1 1++1"
	-python3 main.py "1 1--1"
	-python3 main.py "1--1"
	-python3 main.py "1*1"
	-python3 main.py "1  *  1"
	-python3 main.py "1+1  *  1"
	-python3 main.py "1/1"
	-python3 main.py "1  /  1"
	-python3 main.py "1+1  /  1"
