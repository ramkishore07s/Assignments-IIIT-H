class Position:
    def __init__(self,x,y):
        self.x,self.y = x,y

    def change_pos(self,x,y):
        self.x = x
        self.y = y

    def return_pos():
        return {'x':x,'y':y}

class Bomb(Position):
    identity = 'b'
    strength = 10
    def __init__(self,x,y):
        Position.__init__(self,x,y)
        self.state = 3

    def red_state_with_time(self):
        self.state -= 1

    def ret_state(self):
        return self.state

class Wall(Position):
    identity = 'W'
    strength = 1000
    def __init__(self,x,y):
        Position.__init__(self,x,y)
        

class EmptySpace:
    identity = ' '
    strength = 0

class Explosion(Position):
    identity = 'x'
    strength = 0
    def __init__(self,x,y):
        Position.__init__(self,x,y)
        
class Brick(Position):
    identity = 'k'
    strength = 10
    def __init__(self,x,y):
        Position.__init__(self,x,y)

class Powerup(Position):
    identity = 'p'
    strength = 200
    def __init__(self,x,y):
        Position.__init__(self,x,y)

class Slowdown(Powerup):
    name = 'SLOWDOWN'
    def __init__(self,x,y):
        Powerup.__init__(self,x,y)

class Infinite(Powerup):
    name = 'INFINITE'
    def __init__(self,x,y):
        Powerup.__init__(self,x,y)
