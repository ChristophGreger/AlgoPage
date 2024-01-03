from typing import List
import reflex as rx
import asyncio


class SudokuState(rx.State):
    sudoku: List[List[int]] = [
        [3, 0, 0, 6, 0, 0, 0, 9, 0],
        [0, 4, 0, 0, 2, 0, 0, 5, 0],
        [0, 8, 0, 0, 7, 0, 1, 6, 0],
        [9, 0, 0, 3, 0, 4, 7, 0, 0],
        [0, 5, 0, 0, 8, 0, 0, 2, 0],
        [0, 0, 1, 9, 0, 0, 0, 0, 6],
        [0, 2, 7, 0, 3, 0, 0, 4, 0],
        [0, 9, 0, 0, 6, 0, 0, 1, 0],
        [0, 3, 0, 0, 0, 5, 0, 0, 8],
    ]

    notsolvable: bool = False

    def setNumber(self, row: int, col: int, value: int) -> None:
        try:
            value = int(value)
            if 0 <= value <= 9:
                self.sudoku[row][col] = value
            else:
                return
        except:
            self.sudoku[row][col] = 0

    def issolution(self) -> bool:
        for row in range(0, 9):
            for col in range(0, 9):
                if self.sudoku[row][col] == 0:
                    return False
        return True

    def check(self, row: int, col: int, value: int) -> bool:
        for i in range(0, 9):
            if self.sudoku[row][i] == value:
                return False
            if self.sudoku[i][col] == value:
                return False
        row0 = (row // 3) * 3
        col0 = (col // 3) * 3
        for i in range(0, 3):
            for j in range(0, 3):
                if self.sudoku[row0 + i][col0 + j] == value:
                    return False
        return True

    async def solvehelp(self):
        for i in self.solve():
            yield
            await asyncio.sleep(0.2)

    def solve(self) -> None:
        if self.issolution():
            return
        for row in range(0, 9):
            for col in range(0, 9):
                if self.sudoku[row][col] == 0:
                    for value in range(1, 10):
                        if self.check(row, col, value):
                            self.sudoku[row][col] = value
                            yield
                            yield from self.solve()
                            if self.issolution():
                                return
                            else:
                                self.sudoku[row][col] = 0
                    return
