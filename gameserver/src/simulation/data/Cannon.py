from src.simulation.data._InteractingBuilding import InteractingBuilding


class Cannon(InteractingBuilding):
    
    __hp = 10
    
    def getHP(self):
        return self.__hp
    
    def onDamageReceived(self, dmg: int):
        self.__hp -= dmg
    
    def update(self, field):
        return  # TODO: Find a target... Shoot it...
