from AlgoPage.logicformulas import Subformula
from AlgoPage.logicformulas import evaluateformulas


def isCNF(form: str, wasalreadydisj: bool = False) -> bool:
    """Check if the given formula is in CNF."""
    if not evaluateformulas.correctsyntax(form):
        return False
    form = Subformula.elminateuselessbraces(form)
    if Subformula.isvariable(form):
        return True
    if Subformula.isnegation(form):
        return Subformula.isvariable(Subformula.elminateuselessbraces(form[1:]))
    subs, element, position = Subformula.directsubformulas(form)
    if element not in {"&", "|"}:
        return False
    if element == "&":
        if wasalreadydisj:
            return False
        return isCNF(subs[0]) and isCNF(subs[1])
    if element == "|":
        return isCNF(subs[0], True) and isCNF(subs[1], True)


if __name__ == "__main__":
    print(isCNF("A&B"))
    print(isCNF("A|B"))
    print(isCNF("A"))
    print(isCNF("!A"))
    print(isCNF("A&B|C"))
    print(isCNF("A&B&C"))
    print(isCNF("A|B|C"))
    print(isCNF("A|B&C"))
    print(isCNF("A&(B|C)"))
    print(isCNF("A>B&C"))
