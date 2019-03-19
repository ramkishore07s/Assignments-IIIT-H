import signal
import getch
import os
import time
import characters as c
import board
from termios import tcflush,TCIOFLUSH
from random import randint
import sys
import accessories
import graphic as g
import animations

b = board.Board()
strength = {'B':4,'E':5,'b':5,'r':5,' ':0,'W':100}
level = 1
bman = c.Bomberman(5,0,0)
enemies = []
bombs = []
explosions = []
bricks = []
disp = []
powerups = []

def game(b,strength,level,bman,enemies,bombs,explosions,bricks,disp,powerups):
    def calculate(key,x,y):
        if (key == 'a' or key == 'A'):
            if (y > 0):
                return {'x':x,'y':y-1,'can move':True}
            else:
                return {'x':x,'y':y,'can move':False}
        elif (key == 'd' or key == 'D'):
            if (y < 20):
                return {'x':x,'y':y+1,'can move':True}
            else:
                return {'x':x,'y':y,'can move':False}
        elif key == 'w' or key == 'W':
            if (x > 0):
                return {'x':x-1,'y':y,'can move':True}
            else:
                return {'x':x,'y':y,'can move':False}
        elif key == 's' or key == 'S':
            if (x < 20):
                return {'x':x+1,'y':y,'can move':True}
            else:
                return {'x':x,'y':y,'can move':False}
        else:
            return {'x':x,'y':y}
        
    def move(key,char):
        res_position = calculate(key,char.x,char.y)
        if b.occupant_at(res_position['x'], res_position['y']).strength <= char.strength:
            b.delete_occupant_at( char.x, char.y)
            char.change_pos(res_position['x'], res_position['y'])
            b.insert_at(char,res_position['x'], res_position['y'])
            if( res_position['x'] == bman.x and res_position['y'] == bman.y ):
                bman.red_life()
        

    move_key = ['w','s','a','d']
    def action(key,char):
        if key is 'p' or key is 'P':
            if len(powerups) is 0:
                kind = randint(0,1)
                if kind is 1:
                    powerups.append(accessories.Infinite(2*randint(2,9),2*randint(2,9)))
                else:
                    powerups.append(accessories.Slowdown(2*randint(2,9),2*randint(2,9)))
                b.insert_at(powerups[0],powerups[0].x,powerups[0].y)
                
        if key is 'q' or key is 'Q':
            exit()
        if (char.identity == 'B'):
            if ( key == 'b' or key == 'B' ):
                bombs.append( bman.drop_bomb(char.x,char.y) )
                b.insert_at(bombs[len(bombs) - 1],char.x,char.y)
            else:
                res_position = calculate(key,char.x,char.y)
                cur_occupant = b.occupant_at(char.x,char.y)
                if( cur_occupant.identity == 'E' ):
                    bman.red_life()
                if( b.occupant_at(res_position['x'],res_position['y']).identity not in ['W','b','k'] ):
                    char.change_pos(res_position['x'], res_position['y'])
                        #move(key,char)
                if( b.occupant_at(res_position['x'],res_position['y']).identity is 'p' ):
                    if b.occupant_at(res_position['x'],res_position['y']).name is 'SLOWDOWN':
                        b.insert_at(accessories.EmptySpace(),res_position['x'],res_position['y'])
                        return 1
                    else:
                        bman.life = 1000000
                    b.insert_at(accessories.EmptySpace(),res_position['x'],res_position['y'])
                    
        elif (char.identity == 'E'):
            if ( key == True ):
                move(move_key[randint(0,3)],char)
            



    disp = []
    for i in range(0,42):
        a = []
        for i in range(0,84):
            a.append(' ')
        disp.append(a)

    for i in range(1,(level + 6)*level):
        enemies.append(c.Enemy(bman.strength,2*randint(2,9),2*randint(2,9)))
        b.insert_at(enemies[i-1],enemies[i-1].x,enemies[i-1].y)
    for i in range(1,20*level):
        bricks.append(accessories.Brick( 2*randint(2,9) , 2*randint(2,8)+1 ))
        b.insert_at(bricks[i-1],bricks[i-1].x,bricks[i-1].y)
                  
    #b.insert_at(bman,0,0)
    g.disp(disp,b.board,bman,level)

    def inter(signum,frame):
        pass

    def explode(x,y):
        if calculate('w',x,y)['can move']:
            if( b.board[x-1][y].identity not in ['W','b'] ):
                b.board[x-1][y].strength = 0
                b.board[x-1][y] = accessories.Explosion(x-1,y)
                explosions.append(b.board[x-1][y])
                if bman.x is x-1 and bman.y is y:
                    bman.red_life()
        if calculate('s',x,y)['can move']:
            if( b.board[x+1][y].identity not in ['W','b'] ):
                b.board[x+1][y].strength = 0
                b.board[x+1][y] = accessories.Explosion(x+1,y)
                explosions.append(b.board[x+1][y])
                if bman.x is x+1 and bman.y is y:
                    bman.red_life()
        if calculate('a',x,y)['can move']:
            if( b.board[x][y-1].identity not in ['W','b'] ):
                b.board[x][y-1].strength = 0
                b.board[x][y-1] = accessories.Explosion(x,y-1)
                explosions.append(b.board[x][y-1])
                if bman.x is x and bman.y is y-1:
                    bman.red_life()
        if calculate('d',x,y)['can move']:
            if( b.board[x][y+1].identity not in ['W','b'] ):
                b.board[x][y+1].strength = 0
                b.board[x][y+1] = accessories.Explosion(x,y+1)
                explosions.append(b.board[x][y+1])
                if bman.x is x and bman.y is y+1:
                    bman.red_life()
        b.board[x][y] = accessories.Explosion(x,y)
        explosions.append(b.board[x][y])
        if bman.x is x and bman.y is y:
            bman.red_life()

    signal.signal(signal.SIGALRM, inter)

    slowdown = False
    time = True
    timecount = 0
    while bman.life > 0 and (len(enemies) is not 0):
        os.system('clear')
        g.disp(disp,b.board,bman,level)
        key = None
        signal.alarm(1)
        i = 0
        try:
            while True and i < 5:
                key = getch.getch()
                ret = action(key,bman)
                if ret is 1:
                    slowdown = True
                os.system('clear')
                g.disp(disp,b.board,bman,level)
                i = i+1
        except:
            pass
        signal.alarm(0)
        tcflush(sys.stdin,TCIOFLUSH)
        time = not time
        
        for i in enemies:
            if (i.strength is not 0):
                if slowdown and timecount < 100:
                    if time:
                        timecount = timecount + 1
                        action(time,i)
                else:
                    slowdown = False
                    timecount = 0
                    action(True,i)

        for i in explosions:
            b.insert_at(accessories.EmptySpace(),i.x,i.y)
        explosions = []

        remove = []
        for i in bombs:
            i.red_state_with_time()
            if( i.ret_state() == 0 ):
                explode(i.x,i.y)
                remove.append(i)
        for i in remove:
            bombs.remove(i)

        os.system('clear')
        g.disp(disp,b.board,bman,level)

    
        remove = []
        for i in enemies:
            if (i.strength == 0):
                remove.append(i)
        for i in remove:
            bman.points = bman.points + 100
            enemies.remove(i)

        remove = []
        for i in bricks:
            if (i.strength == 0):
                remove.append(i)
        for i in remove:
            bman.points = bman.points + 20
            bricks.remove(i)
    for i in explosions:
        b.insert_at(accessories.EmptySpace(),i.x,i.y)
    for i in bombs:
        b.insert_at(accessories.EmptySpace(),i.x,i.y)
    for i in bricks:
        b.insert_at(accessories.EmptySpace(),i.x,i.y)
    for i in powerups:
        b.insert_at(accessories.EmptySpace(),i.x,i.y)
    if bman.life > 0:
        return bman.points
    else:
        return 0
            
res = 1
while res is not 0:
    res = animations.start(level)
    if res is not 0:
        res = game(b,strength,level,bman,enemies,bombs,explosions,bricks,disp,powerups)
        if res is 0:
            animations.lose()
            time.sleep(2)
        else:
            level = level + 1
            animations.start(level)
            b = board.Board()
            strength = {'B':4,'E':5,'b':5,'r':5,' ':0,'W':100}
            bman = c.Bomberman(5,0,0)
            enemies = []
            bombs = []
            explosions = []
            bricks = []
            disp = []
            powerups = []
            
            game(b,strength,level,bman,enemies,bombs,explosions,bricks,disp,powerups)
    if res is 5:
        animations.win()
        break
            

