# Logic proposition solver
## Operators and constants
| Operator | Words representing it |
| :- | :- |
| Negation | `!` `not` `¬` `~` |
| Conjunction | `/\` `and` `∧` `·` `.` `&` `&&` |
| Disjunction | `\/` `or` `∨` `+` `∥` `\|\|` `\|` |
| Exclusive disjunction | `xor` `^` `⊕` `⊻` `↮` `≢` |
| Implication  | `->` `>` `impl` `implies` `⇒` `→` `⊃` |
| Equivalence | `<->` `<>` `=` `==` `eq` `equals` `≡` `∷` `::` `⇔` `↔` `~` `⟚` |

| Constant | Words representing it |
| :- | :- |
| True | `T` `1` `⊤` |
| False | `F` `0` `⊥` |

## Usage
Every logic proposition is typed in stdin

#### Example of the logic proposition
You can use parenthesis to group formulas
```
( a -> b ) /\ ( b \/ c ) == (!c -> a)
```

#### Getting truth table
```bash
$ python3 solve-logic-proposition.py truth-table
```

#### Evaluating proposition
Atom values are typed in stdin on the next line after proposition
```bash
$ python3 solve-logic-proposition.py evaluate
```

#### Check for tautology
```bash
$ python3 solve-logic-proposition.py is-tautology
```
Also you can inverse this function to check whether the proposition always return False
```bash
$ python3 solve-logic-proposition.py is-tautology --inverse
```

## Known issues
- When typing not operator ( code word like ! ) after other operator ( code like /\\ ) without space, solver will think that it is a single whole operator ( like /\\! ) and raise an exception
- There may be some problems with exceptions ( not tested )
