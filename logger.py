from enum import Enum


class LogTypes(Enum):
    ERROR = 1
    NORMAL = 2
    WARN = 3


class Logger:
    debug: bool

    def __init__(self, debug):
        self.debug = debug

    def log(self, _type: LogTypes, msg: str):
        if self.debug:
            if _type == LogTypes.ERROR:
                print(f"[DEBUG] {msg}")
                exit(0)
            elif _type == LogTypes.NORMAL:
                print(f"[LOG] {msg}")
            elif _type == LogTypes.WARN:
                print(f"[WARN] {msg}")
        else:
            if _type == LogTypes.ERROR:
                raise ValueError(msg)
