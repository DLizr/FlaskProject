from src.simulation.data.Building import Building


class InvalidBuilding(Building):
    def __init__(self):
        pass
    
    # Override
    def getHP(self):
        raise ValueError("Trying to interact with an invalid building!")
    
    # Override
    def _setHP(self, newHP: int):
        raise ValueError("Trying to interact with an invalid building!")
    
    # Override
    def dealDamage(self, dmg: int):
        raise ValueError("Trying to interact with an invalid building!")
    
    # Override
    def getTeam(self):
        return 2
    
    # Override
    def __repr__(self):
        return self.__class__.__name__
