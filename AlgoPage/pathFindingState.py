from typing import List, Tuple, Set

import reflex as rx
import asyncio


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
    distancematrix: List[List[int]] = [[100 for i in range(20)] for j in range(20)]
    distancematrix[start[0]][start[1]] = 0
    finished: Set[Tuple[int, int]] = set()
    currentlyopen: Set[Tuple[int, int]] = set()

    def resetGrid(self):
        self.start = (0, 0)
        self.end = (19, 19)
        self.startmatrix = [[False for i in range(20)] for j in range(20)]
        self.startmatrix[0][0] = True
        self.endmatrix = [[False for i in range(20)] for j in range(20)]
        self.endmatrix[19][19] = True
        self.searchmatrix = [[False for i in range(20)] for j in range(20)]
        self.pathmatrix = [[False for i in range(20)] for j in range(20)]
        self.currentlysetting = True
        self.distancematrix: List[List[int]] = [[100 for i in range(20)] for j in range(20)]
        self.distancematrix[self.start[0]][self.start[1]] = 0
        self.finished: Set[Tuple[int, int]] = set()
        self.currentlyopen: Set[Tuple[int, int]] = set()

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
        self.distancematrix[self.start[0]][self.start[1]] = 100
        self.start = (row, col)
        self.startmatrix[row][col] = True
        self.distancematrix[row][col] = 0

    def setEnding(self, row: int, col: int) -> None:
        self.endmatrix[self.end[0]][self.end[1]] = False
        self.end = (row, col)
        self.endmatrix[row][col] = True

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
                self.pathmatrix[x[0]][x[1]] = True
                yield
                yield from self.drawpathmatrix()
                return

    current: Tuple[int, int] = start
    justatuple: Tuple[int, int] = end

    async def solve(self) -> None:
        self.current = self.start
        print(self.current)
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
                self.searchmatrix[coordinate[0]][coordinate[1]] = True
        self.finished.add(self.current)
        if self.current == self.end:
            return
        if self.current in self.currentlyopen:
            self.currentlyopen.remove(self.current)
        self.current = self.getlowestdistanceopen()
        yield from self.solvehelp()
