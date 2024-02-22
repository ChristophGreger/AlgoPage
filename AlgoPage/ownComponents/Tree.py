from typing import List, Dict

import reflex as rx


class Tree(rx.Component):
    """A tree component"""
    library = "../public/myTree.js"
    tag = "CenteredTree"
    lib_dependencies: list[str] = ["react-d3-tree"]
    data: rx.Var[List[Dict]]
    orientation: str = "vertical"
    pathFunc: str = "straight"
    draggable: bool = True
    zoomable: bool = True
