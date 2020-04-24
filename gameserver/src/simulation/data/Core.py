from src.simulation.data._Building import Building


class Core(Building):
    
    __hp = 15
    
    def getHP(self):
        return self.__hp
    
    def onDamageReceived(self, dmg: int):
        self.__hp -= dmg
