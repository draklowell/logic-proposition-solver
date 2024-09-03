import string

from logic_solver.reader import ParseEOFError, Reader
from logic_solver.syntax_tree import (Atom, Conjunction, Constant, Disjunction,
                                      Equivalence, ExclusiveDisjunction,
                                      Formula, Implication, Negation)

# There are two types of words:
# text - consist of ascii letters and digits ( but don't start with a digit )
# code - consist of any characters except for text ones and parenthesis
#
# Spaces work as delimiters
CHARS_SPACE = " \t\n\r"
CHARS_TEXT = string.ascii_letters + string.digits
CHARS_SPECIAL = "()"
CHARS_LITERAL_START = string.ascii_letters

WORDS_TRUE = ["T", "1", "⊤"]
WORDS_FALSE = ["F", "0", "⊥"]
WORDS_NOT = ["!", "not", "¬", "~"]
OPERATORS_WTIH_TWO_ARGUMENTS = [
    (["/\\", "and", "∧∧", "·", ".", "&", "&&"], Conjunction),
    (["\\/", "or", "∨", "+", "∥", "||", "|"], Disjunction),
    (["xor", "^", "⊕", "⊻", "↮", "≢"], ExclusiveDisjunction),
    (["->", ">", "impl", "implies", "⇒", "→", "⊃"], Implication),
    (
        ["<->", "<>", "=", "==", "eq", "equals", "≡", "∷", "::", "⇔", "↔", "~", "⟚"],
        Equivalence,
    ),
]
OPERATORS_ORDER = [
    Conjunction,
    Disjunction,
    ExclusiveDisjunction,
    Implication,
    Equivalence,
]

# Create map "word -> formula class" from lists of words
OPERATORS_WTIH_TWO_ARGUMENTS_MAP = {}
for words, formula in OPERATORS_WTIH_TWO_ARGUMENTS:
    for word in words:
        OPERATORS_WTIH_TWO_ARGUMENTS_MAP[word] = formula


class Parser:
    def __init__(self, reader: Reader) -> None:
        self.reader = reader

    # Is used to skip spaces between or before words
    def spaces(self) -> str:
        result = ""
        while not self.reader.is_eof() and self.reader.read() in CHARS_SPACE:
            result += self.reader.read()
            self.reader.forward()

        return result

    def word(self) -> tuple[str, bool, int]:
        length = len(self.spaces())

        # If the first word starts with text character, then it is a text word
        if self.reader.read() in CHARS_TEXT:
            word = self.word_text()
            return word, True, len(word) + length

        # Otherwise it is a code word
        word = self.word_code()
        return word, False, len(word) + length

    def word_code(self) -> str:
        result = ""
        while (
            not self.reader.is_eof()
            and self.reader.read() not in CHARS_SPACE + CHARS_TEXT + CHARS_SPECIAL
        ):
            result += self.reader.read()
            self.reader.forward()

        if not result:
            raise self.reader.eof_error()

        return result

    def word_text(self) -> str:
        result = ""
        while not self.reader.is_eof() and self.reader.read() in CHARS_TEXT:
            result += self.reader.read()
            self.reader.forward()

        if not result:
            raise self.reader.eof_error()

        return result

    def expression(self) -> Formula:
        self.spaces()

        expression = []
        operators = []

        expression.append(self.formula())
        while True:
            self.spaces()

            # If it's an EOF, then finish expression
            try:
                if self.reader.read() == ")":
                    break

                operator, *_ = self.word()
            except ParseEOFError:
                break

            # Check if operator is valid
            if operator.lower() not in OPERATORS_WTIH_TWO_ARGUMENTS_MAP:
                raise self.reader.syntax_error(f"Unknown operator: {operator}")

            operators.append(OPERATORS_WTIH_TWO_ARGUMENTS_MAP[operator.lower()])

            self.spaces()
            expression.append(self.formula())

        # Process operators in their order
        for operator in OPERATORS_ORDER:
            offset = 0
            while offset < len(operators):
                # If operator is valid then join left and right formulas into a new formula
                if operators[offset] == operator:
                    # Replace left formula with the new one
                    expression[offset] = operator(
                        [expression[offset], expression[offset + 1]]
                    )
                    # Remove right formula
                    del expression[offset + 1]
                    del operators[offset]
                else:
                    offset += 1

        return expression[0]

    def assert_literal(self, word, length):
        # Literal must start with a letter, not a digit
        if word[0] not in CHARS_LITERAL_START:
            self.reader.back(length)
            raise self.reader.syntax_error(
                f"Literal starts with invalid character: {word}"
            )

    def formula(self) -> Formula:
        # If formula starts with "(", then it's a new expession
        if self.reader.read() == "(":
            self.reader.forward()  # Skip "("
            formula = self.expression()
            self.reader.forward()  # SKip ")"
            return formula

        word, is_text, length = self.word()
        if word.lower() in WORDS_NOT:
            return Negation(self.formula())

        if is_text:
            if word in WORDS_TRUE:
                return Constant(True)

            if word in WORDS_FALSE:
                return Constant(False)

            self.assert_literal(word, length)

            return Atom(word)

        self.reader.back(length)
        raise self.reader.syntax_error(f"Invalid operator starting formula: {word}")

    def atom(self) -> tuple[str, bool]:
        value = True

        word, is_text, length = self.word()
        if word.lower() in WORDS_NOT:
            word, is_text, length = self.word()
            if not is_text:
                self.reader.back(length)
                raise self.reader.syntax_error(
                    f"After NOT operator there must be literal, not code word: {word}"
                )

            value = False
        elif not is_text:
            self.reader.back(length)
            raise self.reader.syntax_error(
                f"Invalid operator in atom values string: {word}"
            )

        self.assert_literal(word, length)

        return word, value

    def atom_values(self) -> dict[str, bool]:
        self.spaces()

        atom_values = {}
        while not self.reader.is_eof():
            if self.reader.read() in CHARS_SPECIAL:
                raise self.reader.syntax_error(
                    "You can't use special characters in atom values string"
                )

            atom, value = self.atom()
            atom_values[atom] = value

            self.spaces()

        return atom_values


def parse_atom_values(data: str) -> Formula:
    return Parser(Reader(data)).atom_values()


def parse_logic_proposition(data: str) -> Formula:
    return Parser(Reader(data)).expression()
