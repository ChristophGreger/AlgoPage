from AlgoPage.logicformulas import Subformula


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
        if self.element == "!":
            self.direct_subformulas = [Formula(self.directsubformula_strings[0])]
        elif self.element in {"&", "|", ">", "="}:
            self.direct_subformulas = [Formula(x) for x in self.directsubformula_strings]

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
    
    def evaluate(self) -> list[list[any]]:
        """Evaluates the formula for all models."""
        models = self.getallModels()
        solutions = []
        for model in models:
            value = self.evaluatehelper(model)
            solutions.append([model, value])
        return solutions

    def evaluatehelper(self, model):
        if self.element == "!" and len(self.direct_subformulas) == 1:
            return not self.direct_subformulas[0].evaluatehelper(model)
        elif self.element == "&" and len(self.direct_subformulas) == 2:
            return self.direct_subformulas[0].evaluatehelper(model) and self.direct_subformulas[1].evaluatehelper(model)
        elif self.element == "|" and len(self.direct_subformulas) == 2:
            return self.direct_subformulas[0].evaluatehelper(model) or self.direct_subformulas[1].evaluatehelper(model)
        elif self.element == ">" and len(self.direct_subformulas) == 2:
            return not self.direct_subformulas[0].evaluatehelper(model) or self.direct_subformulas[1].evaluatehelper(model)
        elif self.element == "=" and len(self.direct_subformulas) == 2:
            return self.direct_subformulas[0].evaluatehelper(model) == self.direct_subformulas[1].evaluatehelper(model)
        elif self.isvariable:
            return model[self.formula_string]
        else:
            # This case should never happen
            raise ValueError("Formel ist nicht korrekt")

    @staticmethod
    def bindsstrongerthan(element1: str, element2: str, leftchecking: bool = True) -> bool:
        operatorlist = ["v", "!", "&", "|", ">", "="]
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
        if self.isvariable:
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


if __name__ == "__main__":
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





