from src.simulation.data.Building import Building


class Wall(Building):
    
    hp = 20
    
    def __init__(self):
        super().__init__(self.hp)
    
    def getTeam(self):
        return self.DEFENDING
