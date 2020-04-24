from src.simulation.data._Building import Building


class Wall(Building):
    
    __hp = 20
    
    def getHP(self):
        return self.__hp
    
    def onDamageReceived(self, dmg: int):
        self.__hp -= dmg
