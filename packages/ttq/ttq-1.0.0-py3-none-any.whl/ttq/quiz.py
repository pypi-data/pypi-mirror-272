import random
from .question import Question


class Quiz:
    
    def __init__(self, questions: list[Question]) -> None:
        self.questions = questions

    def shuffle(self) -> None:
        random.shuffle(self.questions)
