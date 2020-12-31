from src.simulation.data.Building import Building
from src.simulation.Field import Field


class InteractingBuilding(Building):
    def __init__(self, hp: int, x: int, y: int):
        super().__init__(hp)
    
    def setField(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError
    