from .option import Option
from .type import QuestionType


class Question:

    def __init__(self, text: str, type: QuestionType, options: list[Option]):
        self.text = text
        self.type = type
        self.options = options

    def is_valid(self) -> bool:
        corrects = 0
        for option in self.options:
            if option.is_correct:
                corrects += 1

        return corrects > 0