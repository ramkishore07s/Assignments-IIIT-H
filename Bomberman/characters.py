from accessories import Bomb,Position

class Person(Position):
    def __init__(self,strength,x,y):
        self.strength = strength
        Position.__init__(self,x,y)

    def reduce_strength(self):
        self.strength -= 1
        
    
class Enemy(Person):
    identity = 'E'
    def __init__(self,strength,x,y):
        Person.__init__(self,strength,x,y)

class Bomberman(Person):
    identity = 'B'
    life = 4
    def __init__(self,strength,x,y):
        Person.__init__(self,strength,x,y)
        self.points = 0

    def action(self,key):
        print("class" + str(key))

    def drop_bomb(self,x,y):
        return Bomb(x,y)

    def red_life(self):
        self.life -= 1

            
        
    
    
