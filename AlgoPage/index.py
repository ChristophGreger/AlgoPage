import reflex as rx


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
        align="center",
    )