class Building:
    
    DEFENDING = 0
    ATTACKING = 1
    
    def __init__(self, hp: int):
        self.__hp = hp
    
    def getHP(self) -> int:
        return self.__hp
    
    def _setHP(self, newHP: int):
        self.__hp = newHP
    
    def dealDamage(self, dmg: int):
        self.__hp -= dmg
    
    def getTeam(self) -> int:
        raise NotImplementedError
    
    def __repr__(self):
        return self.__class__.__name__
