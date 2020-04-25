class Building:
    
    DEFENDING = 0
    ATTACKING = 1
    
    def getHP(self):
        raise NotImplementedError
    
    def onDamageReceived(self, dmg: int):
        raise NotImplementedError
    
    def getTeam(self):
        raise NotImplementedError
    
    def __repr__(self):
        return self.__class__.__name__
