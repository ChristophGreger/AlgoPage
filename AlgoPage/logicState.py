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

    issatisfiable: bool = False
    isunsatisfiable: bool = False
    isvalid: bool = False
    iscountersatisfiable: bool = False

    showsubformulas: bool = False

    tableaudictlist: List[dict] = []
    tableaudictlistisfilled: bool = False

    def submit(self):
        if not self.formula:
            return rx.window_alert("Please enter a formula.")
        try:
            classedformula = Formula.Formula(self.formula)
            self.bracketlessformula = classedformula.withoutuselessbraces()
            self.tableheaders = classedformula.allsortedVariables()

            if self.showsubformulas:
                for subformula in classedformula.getstrictSubformulas_sorted():
                    self.tableheaders.append(subformula.withoutuselessbraces())

            self.tableheaders.append(classedformula.withoutuselessbraces())
            evaluationlist = classedformula.evaluate(self.showsubformulas)
            self.tablerows.clear()

            for modelvaluecombo in evaluationlist:
                row = ()
                for variable in classedformula.allsortedVariables():
                    row += ("True" if modelvaluecombo[0][variable] else "False",)

                if self.showsubformulas:
                    for subformula in classedformula.getstrictSubformulas_sorted():
                        row += ("True" if modelvaluecombo[0][subformula.withoutuselessbraces()] else "False",)

                row += ("True" if modelvaluecombo[1] else "False",)
                self.tablerows.append(row)
            self.astdictlist = classedformula.getASTdata()
            self.astdictlistisfilled = True

            self.iscountersatisfiable = classedformula.iscountersatisfiable
            self.issatisfiable = classedformula.issatisfiable
            self.isunsatisfiable = classedformula.isunsatisfiable
            self.isvalid = classedformula.isvalid

        except Exception as e:
            return rx.window_alert(str(e))

    def setPreset(self, preset: int):
        if preset == 1:
            self.formula = "((A&B)|C)"
        elif preset == 2:
            self.formula = "((var1|var2)&var3)=var4&var3|var1>var2"
        self.submit()
