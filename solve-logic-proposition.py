import argparse

from logic_solver.parser import (Formula, parse_atom_values,
                                 parse_logic_proposition)


def create_truth_table(
    formula: Formula,
) -> tuple[list[str], list[tuple[dict[str, bool], bool]]]:
    atoms = list(formula.resolve())

    table = []
    for state in range(2 ** len(atoms)):
        atom_values = {}
        for i in range(len(atoms)):
            atom_values[atoms[i]] = bool(state & 1)  # Get rightmost bit
            state >>= 1  # Shift state bits

        table.append((atom_values, formula.evaluate(atom_values)))

    return atoms, table


def print_truth_table(atoms: list[str], table: list[tuple[dict[str, bool], bool]]):
    atoms = sorted(atoms)
    column_widths = {i: len(i) for i in atoms}

    line = " ".join(atoms)
    if line:
        line += " ="
    else:
        line += "="
    print(" " + line)

    for atom_values, result in table:
        line = ""
        for column in atoms:
            # Convert bool to T/F
            value = "T" if atom_values[column] else "F"
            line += value + " " * column_widths[column]

        line += "T" if result else "F"
        print(" " + line)


def command_truth_table():
    formula = parse_logic_proposition(input("Enter logic proposition: "))
    print_truth_table(*create_truth_table(formula))


def command_is_tautology(inverted: bool = False):
    formula = parse_logic_proposition(input("Enter logic proposition: "))
    _, table = create_truth_table(formula)
    for _, result in table:
        # If inverted and result is True, then proposition is not a tautology
        # If not inverted and result is False, then proporsition also is not a tautology
        if result == inverted:
            print_truth_table([], [({}, False)])
            return

    print_truth_table([], [({}, True)])


def command_evaluate():
    formula = parse_logic_proposition(input("Enter logic proposition: "))
    atom_values = parse_atom_values(input("Enter atom values: "))

    value = formula.evaluate(atom_values)

    print_truth_table(list(atom_values.keys()), [(atom_values, value)])


parser = argparse.ArgumentParser("Logic propositions solver")
subparsers = parser.add_subparsers(dest="command")

parser_truth_table = subparsers.add_parser("truth-table")
parser_always_true = subparsers.add_parser("is-tautology")
parser_always_true.add_argument("--inverted", action="store_true", default=False)
parser_evaluate = subparsers.add_parser("evaluate")

args = parser.parse_args()

match args.command:
    case "truth-table":
        command_truth_table()
    case "is-tautology":
        command_is_tautology(args.inverted)
    case "evaluate":
        command_evaluate()
