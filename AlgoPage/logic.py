import reflex as rx
from .logicState import LogicState


def logic() -> rx.Component:
    return rx.fragment(
        rx.text("Input your formula: "),
        rx.input(
            type="text",
            value=LogicState.formula,
            on_change=LogicState.set_formula,
        ),
        rx.button("Calculate Table", on_click=LogicState.submit),
        rx.table_container(
            rx.table(
                headers=LogicState.tableheaders,
                rows=LogicState.tablerows,
                variant="striped",
            )
        )
    )
