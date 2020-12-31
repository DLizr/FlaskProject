import random

from src.simulation.data._InteractingBuilding import InteractingBuilding
from src.simulation.Field import Field
from src.util.pathfinding.SearchInRadius import SearchInRadius


class Cannon(InteractingBuilding):
    
    hp = 10
    reloadSpeed = 5
    damage = 5
    speed = 0.2
    attackRadius = 6
    
    def __init__(self, x: int, y: int):
        super().__init__(self.hp, x, y)
        self.__lastTarget: tuple = None
        self.__x = x
        self.__y = y
        self.__field = None
        
        self.__noTargets = False
        self.__reload = random.randint(0, 4)
        self.__targetFinder: SearchInRadius = None
        self.__hitQueue = []
    
    def setField(self, field: Field):
        self.__field = field
        self.__targetFinder = SearchInRadius(field, self.__x, self.__y)
        self.__targetFinder.setAttackingFunction(self.__canAttack)
        self.__targetFinder.setCellValidator(self.__isCellValid)
        self.__targetFinder.findTargets()
    
    def update(self):
        if (self.getHP() <= 0):
            return
        self.__handleQueue()
        if (self.__noTargets):
            return
        
        if (not (self.__lastTarget and self.__field.get(*self.__lastTarget))):
            self.__findTarget()
            if (not self.__lastTarget or not self.__field.get(*self.__lastTarget)):
                self.__noTargets = True
                return
        
        self.__shoot()
        
        if (self.__reload == 0):  # Just shot
            return "S:{}:{}:{}:{}".format(str(self.__x), str(self.__y), str(self.__lastTarget[0]), str(self.__lastTarget[1]))
    
    def __findTarget(self):
        target = self.__targetFinder.getNextTarget()
        if (target):
            self.__lastTarget = target
    
    def __isCellValid(self, x: int, y: int) -> bool:
        c = self.__field.get(x, y)
        return c != Field.TILE_INVALID
    
    def __canAttack(self, x: int, y: int) -> bool:
        if (abs(x - self.__x) + abs(y - self.__y) > self.attackRadius):
            return False
        c = self.__field.get(x, y)
        return c and c.getTeam() == self.DEFENDING
    
    def __shoot(self):
        if (self.__reloading()):
            return
        
        targetX, targetY = self.__lastTarget
        distance = ((targetX - self.__x) ** 2 + (targetY - self.__y) ** 2) ** 0.5
        time = distance // self.speed
        
        self.__hitQueue.append([self.__lastTarget, time])
            
    def __reloading(self):
        self.__reload += 1
        
        if (self.__reload == self.reloadSpeed):
            self.__reload = 0
            return False
        
        return True
        
    def __handleQueue(self):
        for i in range(len(self.__hitQueue)):
            coords = self.__hitQueue[i][0]
            self.__hitQueue[i][1] -= 1
            
            if (self.__hitQueue[i][1] <= 0):
                self.__hit(coords)
                self.__hitQueue.pop(i)
                break
    
    def __hit(self, coords):
        target = self.__field.get(*coords)
        if (not target):
            return
        target.dealDamage(self.damage)
        
        if (target.getHP() <= 0):
            self.__field.remove(*self.__lastTarget)
            if (target.__class__.__name__ == "Core"):
                self.__field.breakCore()
    
    def hasTarget(self):
        return not self.__noTargets or self.__hitQueue
    
    def getTeam(self):
        return self.ATTACKING
