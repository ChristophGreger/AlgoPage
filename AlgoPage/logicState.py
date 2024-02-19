from typing import List
import reflex as rx
from AlgoPage.logicformulas import Formula


class LogicState(rx.State):
    formula: str = ""
    tableheaders: List[str] = []
    tablerows: List[tuple] = []
    bracketlessformula: str = ""
    astdictlist: List[dict] = []
    astdictlistisfilled: bool = False

    def submit(self):
        try:
            classedformula = Formula.Formula(self.formula)
            self.bracketlessformula = classedformula.withoutuselessbraces()
            self.tableheaders = classedformula.allsortedVariables()
            self.tableheaders.append("RESULT")
            evaluationlist = classedformula.evaluate()
            self.tablerows.clear()
            for modelvaluecombo in evaluationlist:
                row = ()
                for variable in classedformula.allsortedVariables():
                    row += ("True" if modelvaluecombo[0][variable] else "False",)
                row += ("True" if modelvaluecombo[1] else "False",)
                self.tablerows.append(row)
        except Exception as e:
            return rx.window_alert(str(e))

    def setPreset(self, preset: int):
        if preset == 1:
            self.formula = "((A&B)|C)"
        elif preset == 2:
            self.formula = "((var1|var2)&var3)=var4&var3|var1>var2"
        self.submit()
