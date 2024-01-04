import reflex as rx

from .pathFindingState import PathFindingState


def abutton(row: int, col: int, color: str) -> rx.Component:
    return rx.button("", bg=color, button=True, on_click=lambda: PathFindingState.setStartandEnd(row, col))


def mybutton(row: int, col: int) -> rx.Component:
    return abutton(row, col, PathFindingState.fieldmatrix[row][col])


def generateButtonsasGridItems(row: int, col: int) -> rx.Component:
    return rx.grid_item(mybutton(row, col), row=row, col=col)


def allGridItems() -> rx.Component:
    return rx.fragment(*[generateButtonsasGridItems(row, col) for row in range(0, 20) for col in range(0, 20)])


def pathFinding() -> rx.Component:
    return rx.container(rx.grid(*[allGridItems()], template_rows="repeat(20, 1fr)",
                                template_columns="repeat(20, 1fr)", gap=0),
                        rx.button("Setze Startpunkt", on_click=PathFindingState.setcurrentlysetting(True),
                                  color="green"),
                        rx.button("Setze Endpunkt", on_click=PathFindingState.setcurrentlysetting(False), color="red"),
                        rx.button("Solve", on_click=lambda: PathFindingState.solve()),
                        rx.button("Reset", on_click=lambda: PathFindingState.resetGrid())
                        )
