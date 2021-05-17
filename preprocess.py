import re

from logger import logger


class PreProcess:
    COMMENT_START: str = "/*"
    COMMENT_END: str = "*/"
    commentRegex: str = r"/\*.*?\*/"
    parenthesisRegex: str = r"\(.*?\)"

    def filter(self, code: str) -> str:
        logger.info("[PreProccess] Started PREPROCCESS...")

        # Replace all comments with "".
        logger.debug("[PreProccess] Removing comments...")
        filteredCode = re.sub(self.commentRegex, "", code)

        if self.COMMENT_START in filteredCode or self.COMMENT_END in filteredCode:
            logger.critical("[PreProccess] Input contains invalid comments")

        logger.debug("[PreProccess] Checking if the number of parenthesis is correct...")
        if filteredCode.count("(") != filteredCode.count(")"):
            logger.critical("[PreProccess] Input contains invalid parenthesis")

        logger.info("[PreProccess] Ended PREPROCCESS...")
        return filteredCode
