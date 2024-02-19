import reflex as rx
from .logicState import LogicState
from AlgoPage.ownComponents.Tree import Tree


def logic() -> rx.Component:
    return rx.fragment(
        rx.text("Input your formula: "),
        rx.hstack(
            rx.chakra.input(
                type="text",
                value=LogicState.formula,
                on_change=LogicState.set_formula,
            ),
            rx.text("Formula without useless brackets: " + LogicState.bracketlessformula),
        ),
        rx.hstack(
            rx.button("Calculate Table", on_click=LogicState.submit),
            rx.button("Preset 1", on_click=LogicState.setPreset(1)),
            rx.button("Preset 2", on_click=LogicState.setPreset(2)),
            rx.text("'>': Implikation, '=': Äquivalenz, '&': Konjunktion, '|': Disjunktion, '!': Negation"),
        ),
        rx.chakra.tabs(
            rx.chakra.tab_list(
                rx.chakra.tab("Tabelle"),
                rx.chakra.tab("Abstract Syntax Tree"),
            ),
            rx.chakra.tab_panels(
                rx.chakra.tab_panel(
                    rx.chakra.table_container(
                        rx.chakra.table(
                            headers=LogicState.tableheaders,
                            rows=LogicState.tablerows,
                            variant="striped",
                        )
                    )
                ),
                rx.chakra.tab_panel(
                    rx.container(
                        rx.cond(LogicState.astdictlistisfilled,
                                rx.container(
                                    Tree(data=LogicState.astdictlist, height=3000),
                                    height=1000,
                                ),
                                rx.text("Du musst zuerst eine Formel eingeben und auf 'calculate Table' klicken!")),
                    ),
                ),
            ),
            bg="white",
            color="black",
            shadow="lg",
        ),
    )

