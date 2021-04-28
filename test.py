import sys
import pytest
import subprocess


def capture(command: [str]):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    return out, err, proc.returncode


@pytest.mark.parametrize(
    "input_file, output_file",
    [
        ("./tests/in00.c", "./tests/out00.txt"),
        ("./tests/in01.c", "./tests/out01.txt"),
        ("./tests/in02.c", "./tests/out02.txt"),
        ("./tests/in03.c", "./tests/out03.txt"),
        ("./tests/in04.c", "./tests/out04.txt"),
        ("./tests/in05.c", "./tests/out05.txt"),
        ("./tests/in06.c", "./tests/out06.txt"),
        ("./tests/in07.c", "./tests/out07.txt"),
    ],
)
def test_valid(input_file: str, output_file: str, capsys) -> None:
    command = ["python3", "./main.py", f"{input_file}"]
    out, err, exitcode = capture(command)

    with open(output_file, "r") as f:
        expectedOutput = f.read()

    assert exitcode == 0
    assert out.decode("UTF-8") == expectedOutput


@pytest.mark.parametrize(
    "input_file",
    [
        "./tests/fail00.c",
        "./tests/fail01.c",
        "./tests/fail02.c",
        "./tests/fail03.c",
        "./tests/fail04.c",
        "./tests/fail05.c",
        "./tests/fail06.c",
        "./tests/fail07.c",
        "./tests/fail08.c",
        "./tests/fail09.c",
        "./tests/fail10.c",
        "./tests/fail11.c",
    ],
)
def test_invalid(input_file: str, capsys) -> None:
    command = ["python3", "./main.py", f"{input_file}"]
    out, err, exitcode = capture(command)

    assert exitcode == 1
