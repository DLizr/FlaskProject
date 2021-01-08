from typing import Callable
from src.simulation.Field import Field


class PathFinding:
    def __init__(self, field: Field):
        self._field = field
        self._isCellValid = None
        self._canAttack = None
    
    def setCellValidator(self, cellValidator: Callable[[int, int], bool]):
        self._isCellValid = cellValidator
    
    def setAttackingFunction(self, attackCheck: Callable[[int, int], bool]):
        self._canAttack = attackCheck
