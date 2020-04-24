class Building:
    
    def getHP(self):
        raise NotImplementedError
    
    def onDamageReceived(self, dmg: int):
        raise NotImplementedError
