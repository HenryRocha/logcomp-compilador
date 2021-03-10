all: valid invalid

valid:
	# These should run just fine.
	-python3 main.py "1+1"
	-python3 main.py "1 + 1"
	-python3 main.py " 1 + 1 "
	-python3 main.py " 1 - 1 "
	-python3 main.py " 1 - 2 "
	-python3 main.py "          1     -           2            "
	-python3 main.py "          1     -2                  "
	-python3 main.py "          1-           2              "
	-python3 main.py " 10 + 1 - 10"
	-python3 main.py " 10 - 10 + 100 - 100 + 1000 - 1000"

invalid:
	# These should throw some kind of error.
	-python3 main.py "+"
	-python3 main.py "-"
	-python3 main.py "A"
	-python3 main.py "1A+1B"
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
