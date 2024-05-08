from .quiz import Quiz
from .question import Question
from .option import Option
from .type import QuestionType


def parse_text(input_text: str) -> Quiz:
    lines = input_text.strip().split('\n')
    questions = []
    question_text = ""
    options = []
    corrects = 0

    for line in lines:
        line = line.strip()

        if line:
            if line.endswith('{'):
                question_text = line[:-1].strip()
                options = []
            elif line.startswith('='):
                options.append(Option(line[1:].strip(), is_correct=True))
                corrects += 1
            elif line.startswith('~'):
                options.append(Option(line[1:].strip(), is_correct=False))
            if line.endswith('}'):
                if corrects == 0:
                    questions.append(Question(question_text, QuestionType.INVALID, options))
                if corrects > 1:
                    questions.append(Question(question_text, QuestionType.MULTIPLE_SELECTION, options))
                else:
                    questions.append(Question(question_text, QuestionType.SINGLE_SELECTION, options))

                question_text = ""
                options = []
                corrects = 0

    return Quiz(questions)
