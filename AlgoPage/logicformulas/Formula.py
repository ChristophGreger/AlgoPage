import copy

from AlgoPage.logicformulas import Subformula
from typing import Self, Set, List
from AlgoPage.logicformulas import Colors


class Formula:

    # Wenn die Formel nicht syntaktisch korrekt ist, wird eine ValueError-Exception geworfen
    def __init__(self, formula: str):
        self.formula_string = Subformula.elminateuselessbraces(formula)
        self.bare_string = formula
        try:
            self.directsubformula_strings, self.element, self.position = Subformula.directsubformulas(formula)
        except ValueError:
            raise ValueError("The given formula is not a valid formula.")
        if self.element == "v":
            self.direct_subformulas = []
            self.isvariable = True
        else:
            self.isvariable = False
        if self.element == "p":
            self.direct_subformulas = []
        if self.element == "!":
            self.direct_subformulas = [Formula(self.directsubformula_strings[0])]
        elif self.element in {"&", "|", ">", "="}:
            self.direct_subformulas = [Formula(x) for x in self.directsubformula_strings]

        self.issatisfiable = False
        self.isvalid = False
        self.iscountersatisfiable = False
        self.isunsatisfiable = False

        self.color = "black"

    def negatedFormula(self) -> Self:
        """Returns the negated formula."""
        return Formula("!(" + self.withoutuselessbraces() + ")")

    def __eq__(self, other):
        return self.withoutuselessbraces() == other.withoutuselessbraces()

    def __hash__(self):
        return hash(self.withoutuselessbraces())

    def __str__(self):
        return self.formula_string

    def allunsortedVariables(self) -> set:
        """Returns all variables in the formula in an unordered set."""
        if self.isvariable:
            return {self.formula_string}
        else:
            return set().union(*[x.allunsortedVariables() for x in self.direct_subformulas])

    def allsortedVariables(self) -> list:
        """Returns all variables in the formula in an ordered list."""
        variables = list(self.allunsortedVariables())
        helper = []
        for var in variables:
            helper.append([var, self.formula_string.index(var)])
        helper.sort(key=lambda var2: var2[1])
        for i in range(len(helper)):
            variables[i] = helper[i][0]
        return variables

    def getallModels(self, variables=None) -> list:
        """Returns all models of the formula."""
        if variables is None:
            variables = self.allsortedVariables()
        if len(variables) == 0:
            return [{}]
        else:
            models = self.getallModels(variables[1:])
            return [{variables[0]: True, **model} for model in models] + [{variables[0]: False, **model} for model in
                                                                          models]

    def evaluate(self, showsubformulas: bool = False) -> list[list[any]]:
        """Evaluates the formula for all models."""
        models = self.getallModels()
        solutions = []

        for model in models:
            value = self.evaluatehelper(model)

            if showsubformulas:
                for subformula in self.getstrictSubformulas_sorted():
                    model[subformula.withoutuselessbraces()] = subformula.evaluatehelper(model)

            solutions.append([model, value])
            if value:
                self.issatisfiable = True
            else:
                self.iscountersatisfiable = True

        if not self.issatisfiable:
            self.isunsatisfiable = True
        if not self.iscountersatisfiable:
            self.isvalid = True
        return solutions

    def evaluatehelper(self, model) -> bool:
        if self.element == "!" and len(self.direct_subformulas) == 1:
            return not self.direct_subformulas[0].evaluatehelper(model)
        elif self.element == "&" and len(self.direct_subformulas) == 2:
            return self.direct_subformulas[0].evaluatehelper(model) and self.direct_subformulas[1].evaluatehelper(model)
        elif self.element == "|" and len(self.direct_subformulas) == 2:
            return self.direct_subformulas[0].evaluatehelper(model) or self.direct_subformulas[1].evaluatehelper(model)
        elif self.element == ">" and len(self.direct_subformulas) == 2:
            return not self.direct_subformulas[0].evaluatehelper(model) or self.direct_subformulas[1].evaluatehelper(
                model)
        elif self.element == "=" and len(self.direct_subformulas) == 2:
            return self.direct_subformulas[0].evaluatehelper(model) == self.direct_subformulas[1].evaluatehelper(model)
        elif self.isvariable:
            return model[self.formula_string]
        elif self.element == "p":
            if Subformula.elminateuselessbraces(self.formula_string).upper() == "TRUE":
                return True
            elif Subformula.elminateuselessbraces(self.formula_string).upper() == "FALSE":
                return False
        else:
            # This case should never happen
            raise ValueError("Formel ist nicht korrekt")

    @staticmethod
    def bindsstrongerthan(element1: str, element2: str, leftchecking: bool = True) -> bool:
        operatorlist = ["p", "v", "!", "&", "|", ">", "="]
        if leftchecking:
            return operatorlist.index(element1) <= operatorlist.index(element2)
        else:
            return operatorlist.index(element1) < operatorlist.index(element2)

    def withoutuselessbraces(self) -> str:
        """Returns the formula in a form that contains no unnecessary brackets.
        Does this by constructing the formula out of its tree"""
        # Die beiden Fälle, in denen die Formel eine Variable oder ein unary Operator (Negation) ist
        if self.element == "v":
            return self.formula_string

        if self.element == "p":
            if Subformula.elminateuselessbraces(self.formula_string.upper()) == "TRUE":
                return "True"
            return "False"

        sub1 = self.direct_subformulas[0]

        if self.element == "!" and len(self.direct_subformulas) == 1:
            if sub1.element == "v":
                return "!" + sub1.formula_string
            else:
                return "!(" + sub1.withoutuselessbraces() + ")"

        sub2 = self.direct_subformulas[1]
        toreturnright = ""
        toreturnleft = ""

        # Linkssassoziativer Fall
        if self.element in {"&", "|", "="}:
            if self.bindsstrongerthan(self.element, sub1.element, False):
                toreturnleft = "(" + sub1.withoutuselessbraces() + ")"
            else:
                toreturnleft = sub1.withoutuselessbraces()
            if self.bindsstrongerthan(self.element, sub2.element, True):
                toreturnright = "(" + sub2.withoutuselessbraces() + ")"
            else:
                toreturnright = sub2.withoutuselessbraces()

        # Rechtsassoziativer Fall
        if self.element in {">"}:
            if self.bindsstrongerthan(self.element, sub1.element, True):
                toreturnleft = "(" + sub1.withoutuselessbraces() + ")"
            else:
                toreturnleft = sub1.withoutuselessbraces()
            if self.bindsstrongerthan(self.element, sub2.element, False):
                toreturnright = "(" + sub2.withoutuselessbraces() + ")"
            else:
                toreturnright = sub2.withoutuselessbraces()

        return toreturnleft + self.element + toreturnright

    def isCNF(self, wasalreadydisj: bool = False) -> bool:
        """Check if the given formula is in CNF."""
        if self.isvariable or self.element == "p":
            return True
        if self.element == "!":
            return self.direct_subformulas[0].isCNF()
        if self.element not in {"&", "|"}:
            return False
        if self.element == "&":
            if wasalreadydisj:
                return False
            return self.direct_subformulas[0].isCNF() and self.direct_subformulas[1].isCNF()
        if self.element == "|":
            return self.direct_subformulas[0].isCNF(True) and self.direct_subformulas[1].isCNF(True)

    def getASTdata(self, recursiveCall: bool = False) -> dict or list[dict]:
        """Returns the data of the AST of the formula in a dictionary."""
        if self.isvariable or self.element == "p":
            return {"name": self.withoutuselessbraces(), "children": []} if recursiveCall else [
                {"name": self.formula_string, "children": []}]
        elif self.element == "!":
            if recursiveCall:
                return {"name": self.element, "children": [self.direct_subformulas[0].getASTdata(True)]}
            else:
                return [{"name": self.element, "children": [self.direct_subformulas[0].getASTdata(True)]}]
        else:
            if recursiveCall:
                return {"name": self.element, "children": [self.direct_subformulas[0].getASTdata(True),
                                                           self.direct_subformulas[1].getASTdata(True)]}
            else:
                return [{"name": self.element, "children": [self.direct_subformulas[0].getASTdata(True),
                                                            self.direct_subformulas[1].getASTdata(True)]}]

    # TODO: implement False and True als Variablen und somit dann auch als Knoten mit eigenen Regeln
    # In andtodo sind einfach nur Formeln, in ortodo sind 2er tupel von Formeln, oder 4er tuple (der Fall dass die Formel eine Äquivalenz enthält.
    def getTableauNode(self, alreadyintreeabove: Set = None, ortodo: List = None,
                       andtodo: List = None, alreadyusedcolors: Set = None):  # -> TableauTreeNode:
        """Returns the data of the Tableau as the first TableauTreeNode of its Tree."""

        if alreadyusedcolors is None:
            alreadyusedcolors = []

        # Import hier, um Circular Import zu vermeiden
        from AlgoPage.logicformulas import TableauTreeNode

        if alreadyintreeabove is None:
            alreadyintreeabove = set()
        if ortodo is None:
            ortodo = []
        if andtodo is None:
            andtodo = []

        # Der Fall, dass der Tableau Zweig geschlossen werden kann, weil !True oder False die Formel ist.
        if self.element == "p":
            if self.withoutuselessbraces() == "False":
                self.color = "red"
                if len(andtodo) % 2 == 0:
                    return TableauTreeNode.TableauTreeNode(self)
                # Fall dass ein andtodo muss noch zwingend bearbeitet werden muss
                elif len(andtodo) % 2 == 1:
                    nextformula = andtodo.pop(0)
                    return TableauTreeNode.TableauTreeNode(self, nextNode=TableauTreeNode.TableauTreeNode(nextformula))
        if self.element == "!":
            if self.direct_subformulas[0].element == "p":
                if self.direct_subformulas[0].withoutuselessbraces() == "True":
                    self.color = "red"
                    if len(andtodo) % 2 == 0:
                        return TableauTreeNode.TableauTreeNode(self)
                    # Fall dass ein andtodo muss noch zwingend bearbeitet werden muss
                    elif len(andtodo) % 2 == 1:
                        nextformula = andtodo.pop(0)
                        return TableauTreeNode.TableauTreeNode(self,
                                                               nextNode=TableauTreeNode.TableauTreeNode(nextformula))

        # Der Fall, dass der Tableau Zweig geschlossen werden kann
        for x in alreadyintreeabove:
            if x.negatedFormula() == self or x == self.negatedFormula():
                if x.color == "black":
                    newcolor = Colors.getColor(alreadyusedcolors)
                    x.color = newcolor
                    self.color = newcolor
                    alreadyusedcolors.append(newcolor)
                else:
                    self.color = x.color
                if len(andtodo) % 2 == 0:
                    return TableauTreeNode.TableauTreeNode(self)
                # Fall dass ein andtodo muss noch zwingend bearbeitet werden muss
                elif len(andtodo) % 2 == 1:
                    nextformula = andtodo.pop(0)
                    return TableauTreeNode.TableauTreeNode(self, nextNode=TableauTreeNode.TableauTreeNode(nextformula))

        # Jetzt kommen alle anderen Fälle
        alreadyintreeabove.add(self)

        # Hier passieren jetzt alle Tableau Proof Rules
        if self.element == "&":
            andtodo.append(self.direct_subformulas[0])
            andtodo.append(self.direct_subformulas[1])
        if self.element == "|":
            ortodo.append((self.direct_subformulas[0], self.direct_subformulas[1]))
        if self.element == ">":
            ortodo.append((self.direct_subformulas[0].negatedFormula(), self.direct_subformulas[1]))
        if self.element == "=":
            ortodo.append((self.direct_subformulas[0], self.direct_subformulas[1],
                           self.direct_subformulas[0].negatedFormula(), self.direct_subformulas[1].negatedFormula()))
        if self.element == "!":
            onlysubform = self.direct_subformulas[0]
            if onlysubform.element == "!":
                andtodo.append(onlysubform.direct_subformulas[0])
            elif onlysubform.element == "&":
                ortodo.append((onlysubform.direct_subformulas[0].negatedFormula(),
                               onlysubform.direct_subformulas[1].negatedFormula()))
            elif onlysubform.element == "|":
                andtodo.append(onlysubform.direct_subformulas[0].negatedFormula())
                andtodo.append(onlysubform.direct_subformulas[1].negatedFormula())
            elif onlysubform.element == ">":
                andtodo.append(onlysubform.direct_subformulas[0])
                andtodo.append(onlysubform.direct_subformulas[1].negatedFormula())
            elif onlysubform.element == "=":
                ortodo.append((onlysubform.direct_subformulas[0], onlysubform.direct_subformulas[1].negatedFormula(),
                               onlysubform.direct_subformulas[0].negatedFormula(),
                               onlysubform.direct_subformulas[1]))

        if len(andtodo) > 0:
            nextformula = andtodo.pop(0)
            return TableauTreeNode.TableauTreeNode(self, nextNode=nextformula.getTableauNode(alreadyintreeabove, ortodo,
                                                                                             andtodo,
                                                                                             alreadyusedcolors))
        elif len(ortodo) > 0:
            nextform = ortodo.pop(0)
            if len(nextform) == 2:
                nextformula1 = nextform[0]
                nextformula2 = nextform[1]
                newchildren = [
                    nextformula1.getTableauNode(alreadyintreeabove.copy(), copy.deepcopy(ortodo), None,
                                                alreadyusedcolors),
                    nextformula2.getTableauNode(alreadyintreeabove.copy(), copy.deepcopy(ortodo), None,
                                                alreadyusedcolors)
                ]
                return TableauTreeNode.TableauTreeNode(self, ListOfChildren=newchildren)
            else:
                nextformula1 = nextform[0]
                nextformula2 = nextform[1]
                nextformula3 = nextform[2]
                nextformula4 = nextform[3]
                firstandtodo = [nextformula2, ]
                secondandtodo = [nextformula4, ]
                newchildren = [
                    nextformula1.getTableauNode(alreadyintreeabove.copy(), copy.deepcopy(ortodo), firstandtodo,
                                                alreadyusedcolors),
                    nextformula3.getTableauNode(alreadyintreeabove.copy(), copy.deepcopy(ortodo), secondandtodo,
                                                alreadyusedcolors)
                ]
                return TableauTreeNode.TableauTreeNode(self, ListOfChildren=newchildren)
        else:
            return TableauTreeNode.TableauTreeNode(self)

    def getTableaudata(self, recursiveCall: bool = False, node=None) -> dict or list[dict]:
        if not recursiveCall:
            node = self.getTableauNode()
            mychildren = [self.getTableaudata(True, x) for x in node.children]
            return [{"name": self.withoutuselessbraces(), "attributes": {"color": node.formula.color},
                     "children": mychildren}]
        else:
            return {"name": node.formula.withoutuselessbraces(), "attributes": {"color": node.formula.color},
                    "children": [self.getTableaudata(True, x) for x in node.children]}

    def getstrictSubformulas(self, recursivecall: bool = False) -> set[Self]:
        """Returns all strict subformulas of the formula. Excluding the variables."""
        if not self.isvariable or self.element == "p":
            if recursivecall:
                return {self}.union(*[x.getstrictSubformulas(True) for x in self.direct_subformulas])
            else:
                return set().union(*[x.getstrictSubformulas(True) for x in self.direct_subformulas])
        else:
            return set()

    def __len__(self) -> int:
        """Returns the length of the formula."""
        if self.isvariable or self.element == "p":
            return 1
        else:
            return 1 + sum([len(x) for x in self.direct_subformulas])

    def getstrictSubformulas_sorted(self) -> list[Self]:
        """Returns all strict subformulas of the formula in a sorted list. Excluding the variables."""
        mylist = list(self.getstrictSubformulas())
        mylist.sort(key=lambda xy: len(xy))
        return mylist


if __name__ == "__main__":
    testinga = False
    if testinga:
        print(Formula("A&B|(C)>(A=B)").allsortedVariables())
        print(Formula("A&B|(C)>(A=B)").directsubformula_strings)
        x = Formula("A&B|(C)>(A=B)")
        print(x.evaluate())
        print("Ab jetzt CNF Testing")
        print(Formula("A&B").isCNF())
        print(Formula("A|B").isCNF())
        print(Formula("A").isCNF())
        print(Formula("!A").isCNF())
        print(Formula("A&B|C").isCNF())
        print(Formula("A&B&C").isCNF())
        print(Formula("A|B|C").isCNF())
        print(Formula("A|B&C").isCNF())
        print(Formula("A&(B|C)").isCNF())
        print(Formula("A>B&C").isCNF())
    Formula("(A|B)&B").getTableauNode().print()
