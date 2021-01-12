from collections import deque

from src.simulation.Field import Field
from src.util.pathfinding.PathFinding import PathFinding


class SearchInCross(PathFinding):
    def __init__(self, field: Field, x: int, y: int):
        super().__init__(field)
        self.__x = x
        self.__y = y
        self.__possibleTargets = deque()

    def findTargets(self):
        x, y = self.__x, self.__y

        bfsQueue = deque()
        bfsQueue.appendleft((x, y))
        for d in range(self._field.getWidth()):
            if (self._isCellValid(x, d)):
                bfsQueue.appendleft((x, d))
        for d in range(self._field.getHeight()):
            if (self._isCellValid(d, y)):
                bfsQueue.appendleft((d, y))
        while (len(bfsQueue) > 0):
            tileX, tileY = bfsQueue.pop()
            if (self._canAttack(tileX, tileY)):
                self.__possibleTargets.appendleft((tileX, tileY))

    def getNextTarget(self) -> tuple:
        while (len(self.__possibleTargets) > 0):
            x, y = self.__possibleTargets.pop()
            if (self._canAttack(x, y)):
                return (x, y)
        return None
