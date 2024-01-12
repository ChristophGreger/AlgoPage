from typing import Tuple, List


def getGridwithConfiguration(index: int) -> Tuple[Tuple[int, int], Tuple[int, int], List[List[str]]]:  # start, end, fieldmatrix
    start = (0, 0)
    end = (19, 19)
    grid = gridlist[index].copy()
    for i in range(20):
        for j in range(20):
            if grid[i][j] == "green":
                start = (i, j)
            elif grid[i][j] == "red":
                end = (i, j)
    return start, end, grid


grid1 = [
    ['green', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey',
     'grey', 'black', 'grey', 'grey', 'grey', 'grey'],
    ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'grey', 'black', 'black', 'black', 'black',
     'black', 'black', 'black', 'black', 'black', 'black', 'grey'],
    ['grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey',
     'grey', 'grey', 'grey', 'grey', 'grey', 'grey'],
    ['grey', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black',
     'black', 'black', 'black', 'black', 'black', 'black', 'black'],
    ['grey', 'black', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'black', 'grey', 'grey', 'grey', 'grey', 'grey',
     'black', 'grey', 'grey', 'black', 'grey', 'grey'],
    ['grey', 'black', 'grey', 'black', 'grey', 'grey', 'black', 'grey', 'black', 'black', 'black', 'black', 'black',
     'grey', 'black', 'grey', 'grey', 'black', 'grey', 'grey'],
    ['grey', 'black', 'grey', 'black', 'grey', 'grey', 'black', 'grey', 'grey', 'grey', 'black', 'grey', 'grey', 'grey',
     'black', 'grey', 'black', 'black', 'black', 'black'],
    ['grey', 'black', 'black', 'black', 'grey', 'black', 'black', 'black', 'grey', 'grey', 'black', 'grey', 'grey',
     'grey', 'black', 'grey', 'grey', 'black', 'grey', 'grey'],
    ['grey', 'black', 'grey', 'grey', 'grey', 'grey', 'grey', 'black', 'grey', 'grey', 'black', 'grey', 'grey', 'grey',
     'grey', 'grey', 'grey', 'grey', 'grey', 'grey'],
    ['grey', 'black', 'grey', 'black', 'black', 'black', 'grey', 'black', 'black', 'grey', 'black', 'grey', 'black',
     'black', 'black', 'black', 'grey', 'black', 'black', 'black'],
    ['grey', 'black', 'grey', 'black', 'grey', 'grey', 'grey', 'grey', 'black', 'grey', 'grey', 'grey', 'grey', 'grey',
     'grey', 'black', 'grey', 'grey', 'grey', 'grey'],
    ['grey', 'black', 'grey', 'black', 'black', 'black', 'black', 'grey', 'black', 'grey', 'black', 'grey', 'black',
     'grey', 'grey', 'black', 'grey', 'black', 'black', 'grey'],
    ['grey', 'black', 'grey', 'grey', 'grey', 'grey', 'black', 'grey', 'black', 'grey', 'black', 'grey', 'black',
     'grey', 'grey', 'black', 'grey', 'black', 'black', 'grey'],
    ['grey', 'black', 'grey', 'black', 'grey', 'grey', 'black', 'grey', 'black', 'grey', 'black', 'grey', 'black',
     'grey', 'grey', 'black', 'grey', 'grey', 'grey', 'grey'],
    ['grey', 'black', 'grey', 'black', 'black', 'black', 'black', 'grey', 'black', 'grey', 'black', 'grey', 'black',
     'grey', 'grey', 'black', 'black', 'black', 'black', 'grey'],
    ['grey', 'black', 'grey', 'grey', 'grey', 'grey', 'black', 'grey', 'black', 'grey', 'black', 'grey', 'black',
     'black', 'grey', 'black', 'grey', 'grey', 'grey', 'grey'],
    ['grey', 'black', 'grey', 'black', 'black', 'grey', 'black', 'grey', 'black', 'grey', 'black', 'grey', 'grey',
     'grey', 'grey', 'black', 'grey', 'black', 'black', 'black'],
    ['grey', 'black', 'grey', 'grey', 'black', 'grey', 'black', 'grey', 'black', 'grey', 'black', 'grey', 'black',
     'grey', 'grey', 'black', 'grey', 'grey', 'grey', 'grey'],
    ['grey', 'black', 'black', 'black', 'black', 'grey', 'black', 'grey', 'black', 'grey', 'black', 'grey', 'black',
     'black', 'black', 'black', 'black', 'black', 'black', 'black'],
    ['grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'black', 'grey', 'grey', 'grey', 'black', 'grey', 'grey', 'grey',
     'grey', 'grey', 'grey', 'grey', 'grey', 'red']]

grid2 = [['green', 'grey', 'grey', 'black', 'grey', 'grey', 'grey', 'black', 'grey', 'grey', 'grey', 'black', 'black',
          'grey', 'grey', 'grey', 'black', 'grey', 'black', 'grey'],
         ['grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'black', 'grey', 'grey', 'black', 'grey', 'grey', 'grey',
          'grey', 'black', 'grey', 'grey', 'black', 'grey', 'grey'],
         ['grey', 'grey', 'black', 'grey', 'black', 'black', 'grey', 'black', 'black', 'grey', 'black', 'grey', 'black',
          'grey', 'grey', 'grey', 'black', 'grey', 'grey', 'grey'],
         ['grey', 'black', 'grey', 'grey', 'black', 'grey', 'grey', 'grey', 'grey', 'black', 'grey', 'black', 'grey',
          'grey', 'black', 'grey', 'grey', 'grey', 'black', 'grey'],
         ['black', 'grey', 'grey', 'black', 'grey', 'grey', 'black', 'grey', 'black', 'grey', 'grey', 'grey', 'grey',
          'black', 'grey', 'black', 'black', 'grey', 'black', 'grey'],
         ['grey', 'grey', 'grey', 'black', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'black', 'grey', 'black',
          'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey'],
         ['grey', 'black', 'grey', 'grey', 'grey', 'black', 'grey', 'grey', 'grey', 'black', 'grey', 'grey', 'grey',
          'black', 'grey', 'black', 'grey', 'black', 'black', 'grey'],
         ['grey', 'grey', 'grey', 'black', 'grey', 'grey', 'grey', 'black', 'grey', 'grey', 'grey', 'black', 'grey',
          'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey'],
         ['grey', 'black', 'grey', 'grey', 'grey', 'black', 'grey', 'grey', 'grey', 'black', 'grey', 'grey', 'black',
          'grey', 'black', 'grey', 'black', 'grey', 'black', 'grey'],
         ['grey', 'grey', 'grey', 'grey', 'black', 'grey', 'grey', 'black', 'black', 'grey', 'black', 'grey', 'grey',
          'black', 'grey', 'grey', 'grey', 'black', 'grey', 'grey'],
         ['grey', 'grey', 'black', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'black', 'grey',
          'grey', 'grey', 'black', 'grey', 'grey', 'black', 'grey'],
         ['grey', 'grey', 'grey', 'black', 'grey', 'black', 'grey', 'black', 'grey', 'grey', 'grey', 'black', 'grey',
          'black', 'grey', 'grey', 'grey', 'black', 'grey', 'grey'],
         ['grey', 'black', 'grey', 'grey', 'black', 'grey', 'grey', 'grey', 'grey', 'black', 'grey', 'grey', 'grey',
          'grey', 'black', 'grey', 'grey', 'grey', 'grey', 'black'],
         ['grey', 'black', 'grey', 'black', 'grey', 'black', 'grey', 'black', 'black', 'grey', 'grey', 'black', 'grey',
          'grey', 'grey', 'black', 'grey', 'black', 'grey', 'grey'],
         ['grey', 'grey', 'grey', 'grey', 'grey', 'black', 'grey', 'black', 'grey', 'grey', 'black', 'grey', 'grey',
          'black', 'grey', 'black', 'grey', 'grey', 'grey', 'grey'],
         ['grey', 'black', 'grey', 'grey', 'black', 'grey', 'grey', 'grey', 'grey', 'black', 'grey', 'grey', 'grey',
          'grey', 'black', 'grey', 'grey', 'grey', 'black', 'grey'],
         ['grey', 'grey', 'black', 'grey', 'grey', 'grey', 'black', 'grey', 'grey', 'black', 'black', 'grey', 'black',
          'grey', 'grey', 'grey', 'grey', 'black', 'grey', 'grey'],
         ['grey', 'black', 'grey', 'grey', 'black', 'grey', 'black', 'black', 'grey', 'grey', 'grey', 'grey', 'grey',
          'grey', 'grey', 'black', 'grey', 'black', 'grey', 'grey'],
         ['grey', 'grey', 'black', 'black', 'grey', 'grey', 'grey', 'grey', 'black', 'grey', 'black', 'black', 'black',
          'black', 'black', 'grey', 'black', 'grey', 'grey', 'grey'],
         ['grey', 'grey', 'grey', 'grey', 'grey', 'black', 'grey', 'grey', 'grey', 'black', 'grey', 'grey', 'grey',
          'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'red']]

gridlist = [grid1, grid2]
