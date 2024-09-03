from abc import ABC, abstractmethod


class Formula(ABC):
    symbol: str
    childs: list["Formula"]

    def __init__(self, childs: list["Formula"]):
        self.childs = list(childs)

    @abstractmethod
    def evaluate(self, atom_values: dict[str, bool]) -> bool:
        pass

    def resolve(self) -> set[str]:
        result = set()
        for child in self.childs:
            result |= child.resolve()

        return result

    def __str__(self) -> str:
        return self.symbol.join([f"({i})" for i in self.childs])


class Conjunction(Formula):
    symbol = "/\\"

    def evaluate(self, atom_values: dict[str, bool]) -> bool:
        for child in self.childs:
            if not child.evaluate(atom_values):
                return False

        return True


class Disjunction(Formula):
    symbol = "\\/"

    def evaluate(self, atom_values: dict[str, bool]) -> bool:
        for child in self.childs:
            if child.evaluate(atom_values):
                return True

        return False


class Constant(Formula):
    def __init__(self, value: bool) -> None:
        self.value = value

    def evaluate(self, atom_values: dict[str, bool]) -> bool:
        return self.value

    def __str__(self) -> str:
        return "T" if self.value else "F"

    def resolve(self) -> set[str]:
        return set()


class Atom(Formula):
    def __init__(self, name: str) -> None:
        self.name = name

    def evaluate(self, atom_values: dict[str, bool]) -> bool:
        if not self.name in atom_values:
            raise KeyError(f"No value for atom {self.name}")

        return atom_values[self.name]

    def resolve(self) -> set[str]:
        return {self.name}

    def __str__(self) -> str:
        return self.name


class Implication(Formula):
    symbol = "->"

    def evaluate(self, atom_values: dict[str, bool]) -> bool:
        left = self.childs[0].evaluate(atom_values)
        right = self.childs[1].evaluate(atom_values)

        if left and not right:
            return False

        return True


class Equivalence(Formula):
    symbol = "<->"

    def evaluate(self, atom_values: dict[str, bool]) -> bool:
        left = self.childs[0].evaluate(atom_values)
        right = self.childs[1].evaluate(atom_values)

        return left == right


class ExclusiveDisjunction(Formula):
    symbol = "^"

    def evaluate(self, atom_values: dict[str, bool]) -> bool:
        left = self.childs[0].evaluate(atom_values)
        right = self.childs[1].evaluate(atom_values)

        return left != right


class Negation(Formula):
    def __init__(self, childs: list[Formula] | Formula) -> None:
        try:
            self.childs = list(childs)
        except TypeError:
            self.childs = [childs]

    def evaluate(self, atom_values: dict[str, bool]) -> bool:
        return not self.childs[0].evaluate(atom_values)

    def __str__(self) -> str:
        return f"!({self.childs[0]})"
