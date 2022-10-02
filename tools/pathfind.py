"""Pathfinding for entities"""
#USING Pypi pathfinding
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

#1 is path, 0 obstacle
def pathfind(start_input,end_input,matrix_input):
    """Finds a path to end inside matrix of terrain, returning a list"""
    grid = Grid(matrix=matrix_input)
    #0=y 1=x
    start = grid.node(start_input[1], start_input[0])
    end = grid.node(end_input[1], end_input[0])
    #
    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path, runs = finder.find_path(start, end, grid)
    return path


