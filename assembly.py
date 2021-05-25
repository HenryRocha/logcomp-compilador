from logger import logger
from typing import List


class Assembly:
    insts: List[str] = []

    def configure(self, filePath: str) -> None:
        self.filePath = filePath

    def writeInstruction(self, inst: str) -> None:
        logger.debug(f"[Assembly] {inst}")
        self.insts.append(f"\t{inst}\n")

    def writeComment(self, msg: str) -> None:
        logger.debug(f"[Assembly] ; {msg}")
        self.insts.append(f"\t; {msg}\n")

    def writeToFile(self) -> None:
        with open("./base.asm", "r") as f:
            baseCmds = f.readlines()

        with open(self.filePath, "w") as f:
            for line in range(0, len(baseCmds)):
                if line == 85:
                    f.writelines(self.insts)
                    f.write("\n")
                else:
                    f.write(baseCmds[line])


assembly = Assembly()
