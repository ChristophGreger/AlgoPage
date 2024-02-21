from typing import List, Dict

import reflex as rx


class Tree(rx.Component):
    """A tree component"""
    library = "../public/myComponent.js"
    tag = "CenteredTree"
    lib_dependencies: list[str] = ["react-d3-tree"]

