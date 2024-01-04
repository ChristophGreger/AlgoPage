from typing import List

import reflex as rx
from reflex import Component

from . import pathFindingGrids

from .pathFindingState import PathFindingState


def abutton(row: int, col: int, color: str) -> rx.Component:
    return rx.button("", bg=color, button=True, on_click=lambda: PathFindingState.setStartandEndandBarrier(row, col))


def mybutton(row: int, col: int) -> rx.Component:
    return abutton(row, col, PathFindingState.fieldmatrix[row][col])


def generateButtonsasGridItems(row: int, col: int) -> rx.Component:
    return rx.grid_item(mybutton(row, col), row=row, col=col)


def allGridItems() -> rx.Component:
    return rx.fragment(*[generateButtonsasGridItems(row, col) for row in range(0, 20) for col in range(0, 20)])


def presetButton(index: int) -> rx.Component:
    return rx.button("Preset " + str(index), on_click=PathFindingState.setGridwithConfiguration(index))


def allPresetButtons() -> list[Component]:
    return [presetButton(index) for index in range(len(pathFindingGrids.gridlist))]


def pathFinding() -> rx.Component:
    return rx.container(rx.grid(*[allGridItems()], template_rows="repeat(20, 1fr)",
                                template_columns="repeat(20, 1fr)", gap=0),
                        rx.button("Setze Startpunkt", on_click=PathFindingState.setcurrentlysetting("start"),
                                  color="green"),
                        rx.button("Setze Endpunkt", on_click=PathFindingState.setcurrentlysetting("end"), color="red"),
                        rx.button("Setze Barriers", on_click=PathFindingState.setcurrentlysetting("barrier"),
                                  color="blue"),
                        rx.button("Solve", on_click=PathFindingState.solve()),
                        rx.button("Reset Solve", on_click=PathFindingState.resetSolve()),
                        rx.button("Reset", on_click=PathFindingState.resetGrid()),
                        rx.button("Print Grid", on_click=PathFindingState.printGrid()),
                        *allPresetButtons()
                        )
