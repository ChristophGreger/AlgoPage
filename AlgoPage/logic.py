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
        ),
        rx.hstack(
            rx.button("Calculate Table", on_click=LogicState.submit),
            rx.button("Preset 1", on_click=LogicState.setPreset(1)),
            rx.button("Preset 2", on_click=LogicState.setPreset(2)),
            rx.checkbox(
                "Show Subformulas in Table",
                default_checked=False,
                on_change=LogicState.set_showsubformulas,
            ),
            rx.text("'>': Implikation, '=': Äquivalenz, '&': Konjunktion, '|': Disjunktion, '!': Negation"),
        ),
        rx.chakra.tabs(
            rx.chakra.tab_list(
                rx.chakra.tab("Tabelle"),
                rx.chakra.tab("Abstract Syntax Tree"),
                rx.chakra.tab("Tableau Calculus"),
                rx.chakra.tab("Further Information on the Formula"),
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
                    rx.fragment(
                        rx.cond(LogicState.astdictlistisfilled,
                                rx.fragment(
                                    Tree(data=LogicState.astdictlist, style={"height": "100%", "width": "100%", "margin": "auto"}),
                                ),
                                rx.text("Du musst zuerst eine Formel eingeben und auf 'calculate Table' klicken!")),
                    ),
                    height=1000,
                ),
                rx.chakra.tab_panel(
                    rx.fragment(
                        rx.cond(LogicState.astdictlistisfilled,
                                rx.fragment(
                                    Tree(data=LogicState.astdictlist,
                                         style={"height": "100%", "width": "100%", "margin": "auto"}),
                                ),
                                rx.text("Du musst zuerst eine Formel eingeben und auf 'calculate Table' klicken!")),
                    ),
                    height=1000,
                ),
                rx.chakra.tab_panel(
                    rx.text("Formula without useless brackets: " + LogicState.bracketlessformula.to_string()),
                    rx.text("Formula is satisfiable: " + LogicState.issatisfiable.to_string()),
                    rx.text("Formula is valid: " + LogicState.isvalid.to_string()),
                    rx.text("Formula is countersatisfiable: " + LogicState.iscountersatisfiable.to_string()),
                    rx.text("Formula is unsatisfiable: " + LogicState.isunsatisfiable.to_string()),
                ),
            ),
            bg="white",
            color="black",
            shadow="lg",
        ),
    )

