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
        ("./tests/in08.c", "./tests/out08.txt"),
        ("./tests/in09.c", "./tests/out09.txt"),
        ("./tests/in11.c", "./tests/out11.txt"),
        ("./tests/in12.c", "./tests/out12.txt"),
        ("./tests/in13.c", "./tests/out13.txt"),
        ("./tests/in14.c", "./tests/out14.txt"),
        ("./tests/in15.c", "./tests/out15.txt"),
        ("./tests/in16.c", "./tests/out16.txt"),
        ("./tests/in17.c", "./tests/out17.txt"),
        ("./tests/in18.c", "./tests/out18.txt"),
        ("./tests/in19.c", "./tests/out19.txt"),
        ("./tests/in20.c", "./tests/out20.txt"),
        ("./tests/in21.c", "./tests/out21.txt"),
        ("./tests/in22.c", "./tests/out22.txt"),
        ("./tests/in23.c", "./tests/out23.txt"),
        ("./tests/in24.c", "./tests/out24.txt"),
        ("./tests/in25.c", "./tests/out25.txt"),
        ("./tests/in26.c", "./tests/out26.txt"),
        ("./tests/in27.c", "./tests/out27.txt"),
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
        "./tests/fail07.c",
        "./tests/fail08.c",
        "./tests/fail09.c",
        "./tests/fail10.c",
        "./tests/fail11.c",
        "./tests/fail12.c",
        "./tests/fail13.c",
        "./tests/fail14.c",
        "./tests/fail15.c",
        "./tests/fail16.c",
        "./tests/fail17.c",
        "./tests/fail18.c",
        "./tests/fail19.c",
        "./tests/fail20.c",
        "./tests/fail21.c",
        "./tests/fail22.c",
        "./tests/fail23.c",
        "./tests/fail24.c",
        "./tests/fail25.c",
    ],
)
def test_invalid(input_file: str, capsys) -> None:
    command = ["python3", "./main.py", f"{input_file}"]
    out, err, exitcode = capture(command)

    assert exitcode == 1
