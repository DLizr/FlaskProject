from src.player.Player import Player


class FakePlayer(Player):
    def __init__(self):
        pass
    
    def getAddress(self) -> str:
        return "0.0.0.0:00000"
    
    async def sendMessage(self, msg):
        return
    
    async def sendMessageSafe(self, msg):
        return
    
    async def disconnect(self):
        return
    
    def clearMessages(self):
        return
    
    def getMessageIfReceived(self):
        return
    
    async def ping(self):
        return
    
    def setId(self, ID):
        return
    
    def getId(self):
        return 0
