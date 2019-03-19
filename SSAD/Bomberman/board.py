from accessories import Wall,EmptySpace

class Board:
    board = []
    def __init__(self):
        for j in range(0,10):
            a = []
            b = []
            for i in range(0,10):
                a.append(EmptySpace())
                a.append( Wall( 2*j + 1, 2*i+1) )
                b.append(EmptySpace())
                b.append(EmptySpace())
            a.append(EmptySpace())
            b.append(EmptySpace())
            self.board.append(b)
            self.board.append(a)

        b = []
        for i in range(0,10):
            b.append(EmptySpace())
            b.append(EmptySpace())
        b.append(EmptySpace())
        self.board.append(b)
            

    def occupant_at(self,x,y):
        return self.board[x][y]
    
    def insert_at(self,character,x,y):
        self.board[x][y] = character
        
    def delete_occupant_at(self,x,y):
        self.board[x][y] = EmptySpace()

    def display(self):
        for j in self.board:
            for g in j:
                if( g.identity == 'b' ):
                    print(g.state,end = ' ')
                else:
                    print(g.identity,end = ' ')
            print(' ')

       
            
