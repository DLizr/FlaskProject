from collections import deque

from src.simulation.Field import Field
from src.util.pathfinding.PathFinding import PathFinding


class SearchInRadius(PathFinding):
    def __init__(self, field: Field, x: int, y: int):
        super().__init__(field)
        self.__x = x
        self.__y = y
        self.__possibleTargets = deque()
    
    def findTargets(self):
        x, y = self.__x, self.__y

        distance = [[0 for j in range(self._field.getWidth())] for i in range(self._field.getHeight())]
        bfsQueue = deque()
        bfsQueue.appendleft((x, y))
        while (len(bfsQueue) > 0):
            tileX, tileY = bfsQueue.pop()
            if (self._canAttack(tileX, tileY)):
                self.__possibleTargets.appendleft((tileX, tileY))
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                if (self._isCellValid(tileX + dx, tileY + dy)):
                    if (distance[tileY + dy][tileX + dx] == 0):
                        distance[tileY + dy][tileX + dx] = distance[tileY][tileX] + 1
                        bfsQueue.appendleft((tileX + dx, tileY + dy))
    
    def getNextTarget(self) -> tuple:
        while (len(self.__possibleTargets) > 0):
            x, y = self.__possibleTargets.pop()
            if (self._canAttack(x, y)):
                return (x, y)
        return None
