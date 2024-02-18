from typing import List

from AlgoPage.logicformulas import Subformula


# Ein Model für die Auswertung einer Formel ist ein Dictionary, das Variablen auf Wahrheitswerte abbildet


# TODO Funktion überflüssig
def getallModels(variables):
    if len(variables) == 0:
        return [{}]
    else:
        models = getallModels(variables[1:])
        return [{variables[0]: True, **model} for model in models] + [{variables[0]: False, **model} for model in
                                                                      models]


# TODO Funktion überflüssig
def EvaluateForm(form: str) -> List[List[any]]:
    variables = Subformula.allvariables(form)
    models = getallModels(list(variables))
    solutions = []
    for model in models:
        value = evaluateformhelper(form, model)
        solutions.append([model, value])
    return solutions


# TODO Funktion überflüssig
def evaluateformhelper(form, model) -> bool:
    subs, element, position = Subformula.directsubformulas(form)
    if element == "!" and len(subs) == 1:
        return not evaluateformhelper(subs[0], model)
    elif element == "&" and len(subs) == 2:
        return evaluateformhelper(subs[0], model) and evaluateformhelper(subs[1], model)
    elif element == "|" and len(subs) == 2:
        return evaluateformhelper(subs[0], model) or evaluateformhelper(subs[1], model)
    elif element == ">" and len(subs) == 2:
        return not evaluateformhelper(subs[0], model) or evaluateformhelper(subs[1], model)
    elif element == "=" and len(subs) == 2:
        return evaluateformhelper(subs[0], model) == evaluateformhelper(subs[1], model)
    elif Subformula.isvariable(form):
        return model[form]
    else:
        raise ValueError("Formel ist nicht korrekt")


# TODO Funktion überflüssig
# Funktion, die eine Formel in eine Form umwandelt, die überhaupt keine unnötigen Klammern enthält
def eliminatealluselessbrackets(form: str) -> str:
    form = Subformula.elminateuselessbraces(form)

    # Hier wird gecheckt, ob die Formel syntaktisch korrekt ist
    evaluation = EvaluateForm(form)

    return eliminatealluselessbracketshelper(form)


# TODO Funktion überflüssig
def correctsyntax(form: str) -> bool:
    try:
        evaluation = EvaluateForm(form)
        return True
    except:
        return False


# TODO Funktion überflüssig
def eliminatealluselessbracketshelper(form: str) -> str:
    subs, element, position = Subformula.directsubformulas(form)

    # Die beiden Fälle, in denen die Formel eine Variable oder ein unary Operator (Negation) ist
    if element == "v":
        return Subformula.elminateuselessbraces(form)
    if element == "!" and len(subs) == 1:
        sub2, element2, position2 = Subformula.directsubformulas(subs[0])
        if element2 == "v":
            return "!" + Subformula.elminateuselessbraces(subs[0])
        else:
            return "!(" + eliminatealluselessbracketshelper(Subformula.elminateuselessbraces(subs[0])) + ")"

    subs2, element2, position2 = Subformula.directsubformulas(subs[0])
    subs3, element3, position3 = Subformula.directsubformulas(subs[1])
    toreturnright = ""
    toreturnleft = ""

    # Linkssassoziativer Fall
    if element in {"&", "|", "="}:
        if bindsstrongerthan(element, element2, False):
            toreturnleft = "(" + eliminatealluselessbracketshelper(subs[0]) + ")"
        else:
            toreturnleft = eliminatealluselessbracketshelper(subs[0])
        if bindsstrongerthan(element, element3, True):
            toreturnright = "(" + eliminatealluselessbracketshelper(subs[1]) + ")"
        else:
            toreturnright = eliminatealluselessbracketshelper(subs[1])

    # Rechtsassoziativer Fall
    if element in {">"}:
        if bindsstrongerthan(element, element2, True):
            toreturnleft = "(" + eliminatealluselessbracketshelper(subs[0]) + ")"
        else:
            toreturnleft = eliminatealluselessbracketshelper(subs[0])
        if bindsstrongerthan(element, element3, False):
            toreturnright = "(" + eliminatealluselessbracketshelper(subs[1]) + ")"
        else:
            toreturnright = eliminatealluselessbracketshelper(subs[1])

    return toreturnleft + element + toreturnright


# TODO Funktion überflüssig
def bindsstrongerthan(element1: str, element2: str, leftchecking: bool = True) -> bool:
    operatorlist = ["v", "!", "&", "|", ">", "="]
    if leftchecking:
        return operatorlist.index(element1) <= operatorlist.index(element2)
    else:
        return operatorlist.index(element1) < operatorlist.index(element2)


if __name__ == "__main__":
    formula = "A&B|(C)>(A=B)"
    print(eliminatealluselessbrackets(formula))
    formula = "A=(B=C)"
    print(eliminatealluselessbrackets(formula))
    formula = "(A=B)=C"
    print(eliminatealluselessbrackets(formula))
    formula = "(A&B)&C"
    print(eliminatealluselessbrackets(formula))
    formula = "A&(B&C)"
    print(eliminatealluselessbrackets(formula))
    formula = "A>(B>C)"
    print(eliminatealluselessbrackets(formula))
