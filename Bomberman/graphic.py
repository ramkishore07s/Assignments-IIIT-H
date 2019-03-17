def animate(char):
    if char.identity is 'p':
        return [[char.name[0],char.name[1],char.name[2],char.name[3]],[char.name[4],char.name[5],char.name[6],char.name[7]]]
    elif char.identity is 'B' or char.identity is 'E':
        return [['[',char.identity,char.identity,']'],['[',char.identity,char.identity,']']]
    elif char.identity is 'k':
        return [['/','/','/','/'],['/','/','/','/']]
    elif char.identity is not 'b' and char.identity is not ' ':
        return [[char.identity,char.identity,char.identity,char.identity],[char.identity,char.identity,char.identity,char.identity]]
    elif char.identity is 'b':
        return [['[',char.state,char.state,']'],['[',char.state,char.state,']']]
    else:
        return [[' ',' ',' ',' '],[' ',' ',' ',' ']]

def insert(disp,char,x,y):
    pic = animate(char)
    disp[2*x][4*y] = pic[0][0]
    disp[2*x][4*y+1] = pic[0][1]
    disp[2*x][4*y+2] = pic[0][2]
    disp[2*x][4*y+3] = pic[0][3]
    disp[2*x+1][4*y] = pic[1][0]    
    disp[2*x+1][4*y+1] = pic[1][1]
    disp[2*x+1][4*y+2] = pic[1][2]
    disp[2*x+1][4*y+3] = pic[1][3]
    
def disp(disp,board,bman,level):
    for i in range(0,21):
        for j in range(0,21):
            insert(disp,board[i][j],i,j)
    insert(disp,bman,bman.x,bman.y)
    print("\n"*5)
    print(" "*55,end = '')
    for i in range(0,23):
        print("WWWW",end='')
    print('')

    print(" "*55,end='')
    for i in range(0,23):
        print("WWWW",end='')
    print('')


    for i in disp:
        print(" "*55,end='')
        print("WWWW",end='')
        for j in i:
            print(j,end='')
        print('WWWW',end='')
        print('')

    print(" "*55,end='')
    for i in range(0,23):
        print("WWWW",end='')
    print('')
    print(" "*55,end='')
    for i in range(0,23):
        print("WWWW",end='')

        
    print('')
    print("")
    print(" "*55,end='')
    print('   life : ',end = '')    
    print(bman.life, end = '                            ')
    print('points: ',end = '')   
    print(bman.points,end = '                           ')
    print('level :'+str(level))

