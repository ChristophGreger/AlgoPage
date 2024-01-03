import reflex as rx
from .sudoku import sudoku
from .index import index


# Add state and page to the app.
app = rx.App()
app.add_page(sudoku(), "/sudoku")
app.add_page(index(), "/")
app.compile()
