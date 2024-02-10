from typing import List
import reflex as rx
import asyncio
from . import logicformulas


class LogicState(rx.State):
    formula: str = ""
    tableheaders: List[str] = []
    tablerows: List[tuple] = []

    def submit(self):
        pass

