from typing import List
import reflex as rx
from AlgoPage.logicformulas import Subformula
from AlgoPage.logicformulas import evaluateformulas


class LogicState(rx.State):
    formula: str = ""
    tableheaders: List[str] = []
    tablerows: List[tuple] = []

    def submit(self):
        try:
            subs = Subformula.allvariables(self.formula)
            self.tableheaders = subs.copy()
            self.tableheaders.append("RESULT")
            evaluationlist = evaluateformulas.EvaluateForm(self.formula)
            self.tablerows.clear()
            for modelvaluecombo in evaluationlist:
                row = ()
                for variable in subs:
                    row += ("True" if modelvaluecombo[0][variable] else "False",)
                row += ("True" if modelvaluecombo[1] else "False",)
                self.tablerows.append(row)
        except ValueError as e:
            return rx.window_alert(str(e))



