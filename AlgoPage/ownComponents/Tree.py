from typing import List, Dict

import reflex as rx


class Tree(rx.Component):
    """A tree component"""
    library = "react-d3-tree"
    tag = "Tree"
    data: rx.Var[List[Dict]]
    orientation: str = "vertical"
    pathFunc: str = "straight"
    # nodeSize = {{x: 100, y: 100}}
