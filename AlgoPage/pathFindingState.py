from typing import List, Tuple, Set

import reflex as rx
import asyncio


class PathFindingState(rx.State):
    start: Tuple[int, int] = (0, 0)
    end: Tuple[int, int] = (19, 19)

    currentlysetting: bool = True  # True if setting start, False if setting end
    distancematrix: List[List[int]] = [[100 for i in range(20)] for j in range(20)]
    distancematrix[start[0]][start[1]] = 0
    finished: Set[Tuple[int, int]] = set()
    currentlyopen: Set[Tuple[int, int]] = set()

    fieldmatrix: List[List[str]] = [["grey" for i in range(20)] for j in range(
        20)]  # "grey", "red", "green", "blue", "yellow" für normalbutton, endingbutton, startingbutton, pathbutton, searchbutton
    fieldmatrix[start[0]][start[1]] = "green"
    fieldmatrix[end[0]][end[1]] = "red"

    def resetGrid(self):
        self.start = (0, 0)
        self.end = (19, 19)
        self.fieldmatrix: List[List[str]] = [["grey" for i in range(20)] for j in range(
            20)]  # "grey", "red", "green", "blue", "yellow" für normalbutton, endingbutton, startingbutton, pathbutton, searchbutton
        self.fieldmatrix[self.start[0]][self.start[1]] = "green"
        self.fieldmatrix[self.end[0]][self.end[1]] = "red"
        self.currentlysetting = True
        self.distancematrix: List[List[int]] = [[100 for i in range(20)] for j in range(20)]
        self.distancematrix[self.start[0]][self.start[1]] = 0
        self.finished: Set[Tuple[int, int]] = set()
        self.currentlyopen: Set[Tuple[int, int]] = set()

    def setcurrentlysetting(self, value: bool) -> None:
        self.currentlysetting = value

    def setStartandEnd(self, row: int, col: int) -> None:
        if self.currentlysetting:
            self.setStarting(row, col)
        else:
            self.setEnding(row, col)

    def setStarting(self, row: int, col: int) -> None:
        self.fieldmatrix[self.start[0]][self.start[1]] = "grey"
        self.distancematrix[self.start[0]][self.start[1]] = 100
        self.start = (row, col)
        self.fieldmatrix[row][col] = "green"
        self.distancematrix[row][col] = 0

    def setEnding(self, row: int, col: int) -> None:
        self.fieldmatrix[self.end[0]][self.end[1]] = "grey"
        self.end = (row, col)
        self.fieldmatrix[row][col] = "red"

    def getneighbors(self, pos: Tuple[int, int]) -> Set[Tuple[int, int]]:
        neighbors: Set[Tuple[int, int]] = set()
        if pos[0] > 0:
            neighbors.add((pos[0] - 1, pos[1]))
        if pos[0] < 19:
            neighbors.add((pos[0] + 1, pos[1]))
        if pos[1] > 0:
            neighbors.add((pos[0], pos[1] - 1))
        if pos[1] < 19:
            neighbors.add((pos[0], pos[1] + 1))
        if self.start in neighbors:
            neighbors.remove(self.start)
        return neighbors

    def getlowestdistanceopen(self) -> Tuple[int, int]:
        lowest: Tuple[int, int] = (0, 0)
        lowestdistance: int = 100
        for coordinate in self.currentlyopen:
            distance = self.distancematrix[coordinate[0]][coordinate[1]]
            if distance < lowestdistance:
                lowestdistance = distance
                lowest = coordinate
        return lowest

    def drawpathmatrix(self) -> None:
        for x in self.getneighbors(self.justatuple):
            if self.distancematrix[x[0]][x[1]] < self.distancematrix[self.justatuple[0]][self.justatuple[1]]:
                self.justatuple = x
                self.fieldmatrix[x[0]][x[1]] = "blue"
                yield
                yield from self.drawpathmatrix()
                return

    current: Tuple[int, int] = start
    justatuple: Tuple[int, int] = end

    async def solve(self) -> None:
        self.current = self.start
        self.justatuple = self.end
        for i in self.solvehelp():
            yield
        for i in self.drawpathmatrix():
            yield
            await asyncio.sleep(0.1)

    def solvehelp(self) -> None:
        currentdistance = self.distancematrix[self.current[0]][self.current[1]]
        for coordinate in self.getneighbors(self.current):
            coordinatedistance = self.distancematrix[coordinate[0]][coordinate[1]]
            if coordinatedistance > currentdistance + 1:  # Hier stand mal ein plus 1
                self.distancematrix[coordinate[0]][coordinate[1]] = currentdistance + 1
                self.currentlyopen.add(coordinate)
                yield
                if not self.fieldmatrix[coordinate[0]][coordinate[1]] == "red":
                    self.fieldmatrix[coordinate[0]][coordinate[1]] = "yellow"
        self.finished.add(self.current)
        if self.current == self.end:
            return
        if self.current in self.currentlyopen:
            self.currentlyopen.remove(self.current)
        self.current = self.getlowestdistanceopen()
        yield from self.solvehelp()
