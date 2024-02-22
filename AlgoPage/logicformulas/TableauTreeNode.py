from typing import Self

from AlgoPage.logicformulas.Formula import Formula


class TableauTreeNode:
    def __init__(self, formula: Formula, nextNode: Self = None, ListOfChildren=None):
        if ListOfChildren is None:
            ListOfChildren = []
            if nextNode is not None:
                ListOfChildren.append(nextNode)
        self.formula = formula
        self.children = ListOfChildren

    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        return str(self.formula)

    def print(self):
        print(self.formula.withoutuselessbraces())
        for child in self.children:
            child.print()

