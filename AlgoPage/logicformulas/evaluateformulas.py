from typing import List

from AlgoPage.logicformulas import Subformula


# Ein Model für die Auswertung einer Formel ist ein Dictionary, das Variablen auf Wahrheitswerte abbildet


def getallModels(variables):
    if len(variables) == 0:
        return [{}]
    else:
        models = getallModels(variables[1:])
        return [{variables[0]: True, **model} for model in models] + [{variables[0]: False, **model} for model in
                                                                      models]


def EvaluateForm(form: str) -> List[List[any]]:
    variables = Subformula.allvariables(form)
    models = getallModels(list(variables))
    solutions = []
    for model in models:
        value = evaluateformhelper(form, model)
        solutions.append([model, value])
    return solutions


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


if __name__ == "__main__":
    formula = "((A&B)|C)"
    EvaluateForm(formula)
