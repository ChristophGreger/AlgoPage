# This File is just for trying things out and testing stuff
from typing import List, Tuple, Set

start: Tuple[int, int] = (0, 0)
end: Tuple[int, int] = (19, 19)
searchmatrix: List[List[bool]] = [[False for i in range(20)] for j in range(20)]
pathmatrix: List[List[bool]] = [[False for i in range(20)] for j in range(20)]

distancematrix: List[List[int]] = [[100 for i in range(20)] for j in range(20)]
distancematrix[start[0]][start[1]] = 0

finished: Set[Tuple[int, int]] = set()

currentlyopen: Set[Tuple[int, int]] = set()


def getneighbors(pos: Tuple[int, int]) -> Set[Tuple[int, int]]:
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


def getlowestdistanceopen() -> Tuple[int, int]:
    lowest: Tuple[int, int] = (0, 0)
    lowestdistance: int = 100
    for coordinate in currentlyopen:
        distance = distancematrix[coordinate[0]][coordinate[1]]
        if distance < lowestdistance:
            lowestdistance = distance
            lowest = coordinate
    return lowest


current = start


def solve() -> None:
    global current
    currentdistance = distancematrix[current[0]][current[1]]
    for coordinate in getneighbors(current):
        coordinatedistance = distancematrix[coordinate[0]][coordinate[1]]
        if coordinatedistance > currentdistance + 1:
            distancematrix[coordinate[0]][coordinate[1]] = currentdistance + 1
            currentlyopen.add(coordinate)
    finished.add(current)
    if current == end:
        return
    if current in currentlyopen:
        currentlyopen.remove(current)
    current = getlowestdistanceopen()
    solve()


def drawpathmatrix() -> None:
    global justatuple
    for x in getneighbors(justatuple):
        if distancematrix[x[0]][x[1]] < distancematrix[justatuple[0]][justatuple[1]]:
            justatuple = x
            pathmatrix[x[0]][x[1]] = True
            drawpathmatrix()
            return


solve()
for x in distancematrix:
    print(x)

justatuple = end
drawpathmatrix()
for x in pathmatrix:
    print(x)
