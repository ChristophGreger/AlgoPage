from typing import List
import reflex as rx
from AlgoPage.logicformulas import Subformula
from AlgoPage.logicformulas import evaluateformulas


class LogicState(rx.State):
    formula: str = ""
    tableheaders: List[str] = []
    tablerows: List[tuple] = []

    def submit(self):
        subs = Subformula.allvariables(self.formula)
        self.tableheaders = subs.copy()
        self.tableheaders.append("RESULT")
        evaluationlist = evaluateformulas.EvaluateForm(self.formula)
        for modelvaluecombo in evaluationlist:
            row = ()
            for variable in subs:
                row += ("True" if modelvaluecombo[0][variable] else "False",)
            row += ("True" if modelvaluecombo[1] else "False",)
            self.tablerows.append(row)



