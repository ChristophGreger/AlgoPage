import reflex as rx
from .sudoku import sudoku
from .index import index
from .pathFinding import pathFinding


# Every page is registered here
app = rx.App()
app.add_page(sudoku(), "/sudoku")
app.add_page(index(), "/")
app.add_page(pathFinding(), "/pathFinding")
app.compile()
