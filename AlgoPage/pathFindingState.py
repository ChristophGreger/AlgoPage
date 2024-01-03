from typing import List, Tuple

import reflex as rx


class PathFindingState(rx.State):
    start: Tuple[int, int] = (0, 0)
    end: Tuple[int, int] = (19, 19)
    startmatrix: List[List[bool]] = [[False for i in range(20)] for j in range(20)]
    startmatrix[0][0] = True
    endmatrix: List[List[bool]] = [[False for i in range(20)] for j in range(20)]
    endmatrix[19][19] = True
    searchmatrix: List[List[bool]] = [[False for i in range(20)] for j in range(20)]
    pathmatrix: List[List[bool]] = [[False for i in range(20)] for j in range(20)]
    currentlysetting: bool = True  # True if setting start, False if setting end

    def isStart(self, row: int, col: int) -> bool:
        return self.startmatrix[row][col]

    def isEnd(self, row: int, col: int) -> bool:
        return self.endmatrix[row][col]

    def setcurrentlysetting(self, value: bool) -> None:
        self.currentlysetting = value

    def setStartandEnd(self, row: int, col: int) -> None:
        if self.currentlysetting:
            self.setStarting(row, col)
        else:
            self.setEnding(row, col)

    def setStarting(self, row: int, col: int) -> None:
        self.startmatrix[self.start[0]][self.start[1]] = False
        self.start = (row, col)
        self.startmatrix[row][col] = True

    def setEnding(self, row: int, col: int) -> None:
        self.endmatrix[self.end[0]][self.end[1]] = False
        self.end = (row, col)
        self.endmatrix[row][col] = True

    def solve(self) -> None:
        pass
