import reflex as rx
from reflex import Component

from . import pathFindingGrids

from .pathFindingState import PathFindingState, algorithms


# General Button
def abutton(row: int, col: int, color: str) -> rx.Component:
    return rx.chakra.button("", bg=color, button=True,
                            on_click=lambda: PathFindingState.setStartandEndandBarrier(row, col))


# Making a colored Button out of the fieldmatrix
def mybutton(row: int, col: int) -> rx.Component:
    return abutton(row, col, PathFindingState.fieldmatrix[row][col])


def allGridItems() -> rx.Component:
    return rx.fragment(*[mybutton(row, col) for row in range(0, 20) for col in range(0, 20)])


def presetButton(index: int) -> rx.Component:
    return rx.button("Preset " + str(index), on_click=PathFindingState.setGridwithConfiguration(index))


# Takes the presets and makes them into buttons
def allPresetButtons() -> list[Component]:
    return [presetButton(index) for index in range(len(pathFindingGrids.gridlist))]


def pathFinding() -> rx.Component:
    return rx.container(rx.grid(*[allGridItems()], columns="20", spacing_x="0", spacing_y="0", width="80%"),
                        rx.button("Setze Startpunkt", on_click=PathFindingState.setcurrentlysetting("start"),
                                  color="green"),
                        rx.button("Setze Endpunkt", on_click=PathFindingState.setcurrentlysetting("end"), color="red"),
                        rx.button("Setze Barriers", on_click=PathFindingState.setcurrentlysetting("barrier"),
                                  color="blue"),
                        rx.button("Solve", on_click=PathFindingState.solve()),
                        rx.button("Reset Solve", on_click=PathFindingState.resetSolve()),
                        rx.button("Reset", on_click=PathFindingState.resetGrid()),
                        rx.button("Print Grid", on_click=PathFindingState.printGrid()),
                        *allPresetButtons(),
                        rx.chakra.select(
                            algorithms,
                            on_change=PathFindingState.set_algorithm,
                            color_schemes="twitter",
                        ),
                        )
