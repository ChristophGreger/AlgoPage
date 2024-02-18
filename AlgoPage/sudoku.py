import reflex as rx
from .sudokuState import SudokuState


def cell(row: int, col: int) -> rx.Component:
    return rx.chakra.number_input(
        value=SudokuState.sudoku[row][col],
        on_change=lambda value: SudokuState.setNumber(row, col, value),
        width="5%",
    )


def wholerow(row: int) -> rx.Component:
    return rx.hstack(*[cell(row, col) for col in range(0, 9)])


def sudoku() -> rx.Component:
    return rx.fragment(
        rx.center(rx.vstack(*[wholerow(row) for row in range(0, 9)]), align="center"),
        rx.button("Solve", on_click=lambda: SudokuState.solvehelp()),
        rx.cond(SudokuState.notsolvable, rx.text("Not solvable")),
    )
