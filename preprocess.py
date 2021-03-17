import re
from logger import Logger, LogTypes


class PreProcess:
    COMMENT_START = "/*"
    COMMENT_END = "*/"
    commentRegex: str = r"/\*.*?\*/"
    logger: Logger

    def filter(self, code: str, logger: Logger) -> str:
        # Replace all comments with "".
        filteredCode = re.sub(self.commentRegex, "", code)

        if self.COMMENT_START in filteredCode or self.COMMENT_END in filteredCode:
            logger.log(LogTypes.ERROR, "Input contains invalid comments")
        else:
            logger.log(LogTypes.NORMAL, f"Pre processed input: {filteredCode}")
            return filteredCode
