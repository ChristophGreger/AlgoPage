import reflex as rx


# This is the index page
def index() -> rx.Component:
    return rx.container(
        rx.link(
            rx.button("Sudoku"),
            href="/sudoku",
            color="rgb(107,99,246)",
            button=True,
        ),
        rx.link(
            rx.button("Path Finding"),
            href="/pathFinding",
            color="rgb(107,99,246)",
            button=True,
        ),
        rx.link(
            rx.button("Logic"),
            href="/logic",
            color="rgb(107,99,246)",
            button=True,
        ),
        align="center",
    )
