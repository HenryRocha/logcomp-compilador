from enum import Enum


class CompilerError(Exception):
    pass


class Logger:
    enable: bool
    verbosity: int

    def __init__(self, enable: bool, verbosity: int) -> None:
        self.enable = enable
        self.verbosity = verbosity

    def configure(self, enable: bool, verbosity: int) -> None:
        self.enable = enable
        self.verbosity = verbosity

    def critical(self, msg: str) -> None:
        print(f"[CRITCAL] {msg}")
        raise CompilerError(f"{msg}")

    def error(self, msg: str) -> None:
        print(f"[ERROR] {msg}")

    def success(self, msg: str) -> None:
        if self.enable and self.verbosity > 0:
            print(f"[SUCCESS] {msg}")

    def warn(self, msg: str) -> None:
        if self.enable and self.verbosity > 0:
            print(f"[WARNING] {msg}")

    def info(self, msg: str) -> None:
        if self.enable and self.verbosity > 1:
            print(f"[INFO] {msg}")

    def debug(self, msg: str) -> None:
        if self.enable and self.verbosity > 2:
            print(f"[DEBUG] {msg}")

    def trace(self, msg: str) -> None:
        if self.enable and self.verbosity > 3:
            print(f"[TRACE] {msg}")


logger = Logger(False, 1)
