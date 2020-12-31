from src.simulation.data.Building import Building


class Core(Building):
    
    hp = 15
    
    def __init__(self):
        super().__init__(self.hp)
    
    def getTeam(self):
        return self.DEFENDING
