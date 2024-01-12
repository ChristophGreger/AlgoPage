from typing import List, Tuple, Set

import reflex as rx
import asyncio
from .pathFindingGrids import getGridwithConfiguration


class PathFindingState(rx.State):
    _start: Tuple[int, int] = (0, 0)
    _end: Tuple[int, int] = (19, 19)

    _currentlysetting: str = "start"  # "start" if setting start, "end" if setting end, "barrier" if setting barrier
    _distancematrix: List[List[int]] = [[1000 for i in range(20)] for j in range(20)]
    _distancematrix[_start[0]][_start[1]] = 0
    _finished: Set[Tuple[int, int]] = set()
    _currentlyopen: Set[Tuple[int, int]] = set()

    fieldmatrix: List[List[str]] = [["grey" for i in range(20)] for j in range(
        20)]  # "grey", "red", "green", "blue", "yellow" für normalbutton, endingbutton, startingbutton, pathbutton, searchbutton
    fieldmatrix[_start[0]][_start[1]] = "green"
    fieldmatrix[_end[0]][_end[1]] = "red"

    def resetGrid(self):
        self._start = (0, 0)
        self._end = (19, 19)
        self.fieldmatrix: List[List[str]] = [["grey" for i in range(20)] for j in range(
            20)]  # "grey", "red", "green", "blue", "yellow" für normalbutton, endingbutton, startingbutton, pathbutton, searchbutton
        self.fieldmatrix[self._start[0]][self._start[1]] = "green"
        self.fieldmatrix[self._end[0]][self._end[1]] = "red"
        self._currentlysetting = "start"
        self._distancematrix: List[List[int]] = [[1000 for i in range(20)] for j in range(20)]
        self._distancematrix[self._start[0]][self._start[1]] = 0
        self._finished: Set[Tuple[int, int]] = set()
        self._currentlyopen: Set[Tuple[int, int]] = set()
        self.isnotsolvable = False

    def resetSolve(self):
        self._distancematrix: List[List[int]] = [[1000 for i in range(20)] for j in range(20)]
        self._distancematrix[self._start[0]][self._start[1]] = 0
        self._finished: Set[Tuple[int, int]] = set()
        self._currentlyopen: Set[Tuple[int, int]] = set()
        self.isnotsolvable = False
        for i in range(20):
            for j in range(20):
                if self.fieldmatrix[i][j] == "yellow":
                    self.fieldmatrix[i][j] = "grey"
                elif self.fieldmatrix[i][j] == "blue":
                    self.fieldmatrix[i][j] = "grey"

    def setcurrentlysetting(self, value: str) -> None:
        self._currentlysetting = value

    def setStartandEndandBarrier(self, row: int, col: int) -> None:
        if self._currentlysetting == "start":
            self.setStarting(row, col)
        elif self._currentlysetting == "end":
            self.setEnding(row, col)
        elif self._currentlysetting == "barrier":
            self.setBarrier(row, col)

    def setBarrier(self, row: int, col: int) -> None:
        if self.fieldmatrix[row][col] == "grey":
            self.fieldmatrix[row][col] = "black"
        elif self.fieldmatrix[row][col] == "black":
            self.fieldmatrix[row][col] = "grey"

    def setGridwithConfiguration(self, index: int) -> None:
        self._start, self._end, self.fieldmatrix = getGridwithConfiguration(index)
        self.resetSolve()

    def setStarting(self, row: int, col: int) -> None:
        self.fieldmatrix[self._start[0]][self._start[1]] = "grey"
        self._distancematrix[self._start[0]][self._start[1]] = 1000
        self._start = (row, col)
        self.fieldmatrix[row][col] = "green"
        self._distancematrix[row][col] = 0

    def setEnding(self, row: int, col: int) -> None:
        self.fieldmatrix[self._end[0]][self._end[1]] = "grey"
        self._end = (row, col)
        self.fieldmatrix[row][col] = "red"

    def getneighbors(self, pos: Tuple[int, int]) -> Set[Tuple[int, int]]:
        neighbors: Set[Tuple[int, int]] = set()
        if pos[0] > 0:
            if self.fieldmatrix[pos[0] - 1][pos[1]] != "black":
                neighbors.add((pos[0] - 1, pos[1]))
        if pos[0] < 19:
            if self.fieldmatrix[pos[0] + 1][pos[1]] != "black":
                neighbors.add((pos[0] + 1, pos[1]))
        if pos[1] > 0:
            if self.fieldmatrix[pos[0]][pos[1] - 1] != "black":
                neighbors.add((pos[0], pos[1] - 1))
        if pos[1] < 19:
            if self.fieldmatrix[pos[0]][pos[1] + 1] != "black":
                neighbors.add((pos[0], pos[1] + 1))
        if self._start in neighbors:
            neighbors.remove(self._start)
        return neighbors

    def getlowestdistanceopen(self) -> Tuple[int, int]:
        lowest: Tuple[int, int] = (0, 0)
        lowestdistance: int = 1000
        for coordinate in self._currentlyopen:
            distance = self._distancematrix[coordinate[0]][coordinate[1]]
            if distance < lowestdistance:
                lowestdistance = distance
                lowest = coordinate
        return lowest

    def drawpathmatrix(self) -> None:
        for x in self.getneighbors(self._justatuple):
            if self._distancematrix[x[0]][x[1]] < self._distancematrix[self._justatuple[0]][self._justatuple[1]]:
                self._justatuple = x
                self.fieldmatrix[x[0]][x[1]] = "blue"
                yield
                yield from self.drawpathmatrix()
                return

    _current: Tuple[int, int] = _start
    _justatuple: Tuple[int, int] = _end

    isnotsolvable: bool = False

    async def solve(self) -> None:
        self._current = self._start
        self._justatuple = self._end
        for i in self.solvehelp():
            yield
            await asyncio.sleep(0.02)
        if not self.isnotsolvable:
            for i in self.drawpathmatrix():
                yield
                await asyncio.sleep(0.1)
        else:
            yield rx.window_alert("Not solvable")
            print("Not solvable")
            self.resetSolve()

    def solvehelp(self) -> None:
        currentdistance = self._distancematrix[self._current[0]][self._current[1]]
        for coordinate in self.getneighbors(self._current):
            coordinatedistance = self._distancematrix[coordinate[0]][coordinate[1]]
            if coordinatedistance > currentdistance + 1:  # Hier stand mal ein plus 1
                self._distancematrix[coordinate[0]][coordinate[1]] = currentdistance + 1
                self._currentlyopen.add(coordinate)
                yield
                if not self.fieldmatrix[coordinate[0]][coordinate[1]] == "red":
                    self.fieldmatrix[coordinate[0]][coordinate[1]] = "yellow"
                if coordinate == self._end:
                    return
        self._finished.add(self._current)
        if self._current in self._currentlyopen:
            self._currentlyopen.remove(self._current)
        if self._currentlyopen == set():
            self.isnotsolvable = True
            return
        self._current = self.getlowestdistanceopen()
        yield from self.solvehelp()

    def printGrid(self) -> None:
        mymatrix = self.fieldmatrix.copy()
        for i in range(20):
            for j in range(20):
                if mymatrix[i][j] in ["yellow", "blue"]:
                    mymatrix[i][j] = "grey"
        print(mymatrix)
