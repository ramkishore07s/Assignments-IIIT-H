import copy
import random
from time import time
import traceback

class Team51:

###---------------------________________-init-________________________---------------------------

    def __init__(self):
        self.inf = 100000000000
        self.ninf = -100000000000
        self.ply = 0

        self.movestore = []

        self.free_move = 100
        self.max_small_board_cost = 100
        self.three_cons = 20
        self.two_cons = 4
        self.three_closed = -30
        self.two_closed = -7
        
        self.corner = 6
        self.middle = 3
        self.edge = 4
        self.strategy = 10
        
        self.b = [['-' for i in range(4)] for j in range(4)]
        self.b[0][0] = 'x'
        self.b[0][1] = 'x'
        self.b[1][0] = 'x'

        print self.scoring_places([0,0], self.b)
        print self.check(self.scoring_places([0,0], self.b))
        

    def scoring_places(self, mv, status):
        x = mv[0] - mv[0]%4
        y = mv[1] - mv[1]%4

        x1 = x+1
        x2 = x+2
        y1 = y+1
        y2 = y+2
        
        d1 = [status[x1+1][y1], status[x1-1][y1], status[x1][y1+1], status[x1][y1-1]]
        d2 = [status[x2+1][y1], status[x2-1][y1], status[x2][y1+1], status[x2][y1-1]]
        d3 = [status[x1+1][y2], status[x1-1][y2], status[x1][y2+1], status[x1][y2-1]]
        d4 = [status[x2+1][y1], status[x2-1][y1], status[x2][y1+1], status[x2][y1+1]]

        r = [[status[i][j] for i in range(x, x+4)] for j in range(y, y+4)]
        c = [[status[j][i] for i in range(x, x+4)] for j in range(y, y+4)]

        return d1, d2, d3, d4, r[0], r[1], r[2], r[3], c[0], c[1], c[2], c[3]
    
###---------------------__________Neutrality factor of a move________________-------------------------------
#
# Optimallity of a move locally determined to a depth of 1 ply(2 moves)
# Neutrality of a move = neutrality of second board
# A locally optimal move is one that gives the most for the player and lets the
#    opponent play in a less hostile area(a area where much damage cannot be done)
# Is calculated for the board where the subsequent play will be in.
#

    def neutrality_factor(self, board, mv, flg):
        next_mv = [mv[0]%4, mv[1]%4]
        if( board.block_status[next_mv[0]][next_mv[1]] != '-' ):
            return self.free_move
        return (self.max_small_board_cost - self.small_board_cost(board, mv, flg))/2


###---------------------_______________N_Greedy_moves_____________________--------------------------------
#
# Limits no of moves available based on local optimum and depth of the game
#
#

    def n_greedy_moves(self, board, moves, flg, cur_depth, max_depth):
        if self.ply < 80:
            values = [(self.neutrality_factor(board, mv, flg) +
                       abs(self.small_board_cost(board, mv, flg))) for mv in moves]
            if 12 - max_depth > 7:
                return [mv for _,mv in sorted(zip(values, moves))][:14 - max_depth]
            else:
                return [mv for _,mv in sorted(zip(values, moves))][:8]
        else:
            values = [(self.neutrality_factor(board, mv, flg) +
                       abs(self.small_board_cost(board, mv, flg))) for mv in moves]
            return [mv for _,mv in sorted(zip(values, moves))][:16]

###-----------------__________Implements iterative deepening_________________----------------------
#
# Iterative deepening from depth 3 to 100
# 
#
#

    def move(self, board, old_move, flag):
        self.ply += 1
        self.optimal_move = []
        self.move_store = []
        self.now = time()
        for max_depth in range(3,100):
            try:
                print "depth", max_depth
                self.fail_hard_ab(board, 0, max_depth, old_move, flag, self.ninf, self.inf)
                self.move_store.append(self.optimal_move)
            except Exception as error:
#                traceback.print_exc()
                print self.move_store
                if len(self.move_store) > 0:
                    return self.move_store[-1]
        if len(self.move_store) > 0:
            return self.move_store[-1]
        return board.find_valid_move_cells(old_move)[0]


###-----------------------________Aspiration search with Alpha Beta pruning__________---------------------------------
#
# Considers only n locally optimal moves as returned by n_greedy_moves(...) function
# Updates self.optimal_move for every iteration, so self.optimal_move always has the most optimal move found
# Assumptions: 1. A minimax algorithm with a heuristic that might not be admissible can be considered greedy.
#              2. So a minimax algorithm that can look only upto a depth of four or less will not make a locally
#                 unoptimal move unless it is unavoidable.
#
#
    
    def fail_hard_ab(self, board, cur_depth, max_depth, old_mv, flg, alpha, beta):
        if( cur_depth == max_depth ):
            return self.heuristic(board, old_mv, flg)

        if( time() - self.now > 15 ):
            print "timeout err"
            raise Exception('timeout')
        
        moves = self.n_greedy_moves(board, board.find_valid_move_cells(old_mv), flg, cur_depth, max_depth)
#        moves = board.find_valid_move_cells(old_mv)[:16]

        if( flg == 'x' ):
            value = self.ninf
            for move in moves:
                child_board = copy.deepcopy(board)
                child_board.update(old_mv, move, 'x')

                cur_value = self.fail_hard_ab(child_board, cur_depth+1, max_depth, move, 'o', alpha, beta)

                if( cur_value > value and cur_depth == 0 ):
                    self.optimal_move = move
                value = max(value, cur_value)
                if( value >= beta ):
                    return value
                alpha = max(value, alpha)
                
            return value

        else:
            value = self.inf
            for move in moves:
                child_board = copy.deepcopy(board)
                child_board.update(old_mv, move, 'o')

                cur_value = self.fail_hard_ab(child_board, cur_depth+1, max_depth, move, 'x', alpha, beta)
                
                if( cur_value < value and cur_depth == 0 ):
                    self.optimal_move = move
                    print "heur x", cur_value, move
                value = min(value, cur_value)
                if( value <= alpha ):
                    return value
                beta = min(value, beta)
                
            return value


###----------------------_______________Heuristics_____________________----------------------

    def check(self, what):
        x_3 = 0
        o_3 = 0
        x_2 = 0
        o_2 = 0
        closed_2x = 0
        closed_2o = 0
        closed_3x = 0
        closed_3o = 0
        
        for each in what:
            x = 0
            o = 0
            d = 0
            for cell in each:
                if cell == 'x':
                    x += 1
                elif cell == 'o':
                    o += 1
                elif cell == 'd':
                    d += 1

            if x == 4:
                return 0,0,0,0,self.max_small_board_cost
            if o == 4:
                return 0,0,0,0,-self.max_small_board_cost
        
            if x == 3:
                x_3 += 1
                if o == 1 or d == 1:
                    closed_3x += 1
            elif o == 3:
                o_3 += 1
                if x == 1 or d == 1:
                    closed_3o += 1

            if x == 2:
                x_2 += 1
                if o > 0 or d > 0:
                    closed_2x += 1
            if o == 2:
                o_2 += 1
                if x > 0 or d > 0:
                    closed_2o += 1


        cost = (x_3 - o_3) * self.three_cons + (x_2 - o_2) * self.two_cons
        cost += (closed_3x - closed_3o) * self.three_closed + (closed_2x - closed_2o) * self.two_closed
        return x_3 - closed_3x, o_3 - closed_3o, x_2 - closed_2x, o_2 - closed_2o, cost

    def small_board_cost(self, board, mv, flg):
        places = self.scoring_places(mv, board.board_status)
        x_3, o_3, x_2, o_2, cost = self.check(places)
        return cost

    def heuristic(self, board, old_mv, flg):
        cost = 0
        b = board.block_status
        places = self.scoring_places((0,0), b)
        # for x in range(0,4):
        #     for y in range(0,4):
        #         cost += self.small_board_cost(board, [x*4, y*4], flg)
                
        
        strategy1 = [b[0][2], b[1][0], b[3][1], b[2][3]]
        strategy2 = [b[0][1], b[2][0], b[3][2], b[1][3]]

        # for cell in strategy1:
        #     if cell == 'x':
        #         cost += 10
        #     elif cell == 'o':
        #         cost -= 10

        winnable_x = True
        winnable_o = True
        
        x_2 = [[None]*4]*4
        o_2 = [[None]*4]*4
        x_3 = [[None]*4]*4
        o_3 = [[None]*4]*4
        b_cost = [[None]*4]*4

        cur_cell = (old_mv[0]%4, old_mv[1]%4)
        
        for i in range(0,4):
            for j in range(0,4):
                place = self.scoring_places((i*4, j*4), board.board_status)
                x_3[i][j], o_3[i][j], x_2[i][j], o_2[i][j], b_cost[i][j] = self.check(place)
                cost += (x_3[i][j] - o_3[i][j]) * self.three_cons + (x_2[i][j] - o_2[i][j])*self.two_cons
                
        parasite_cost = 6 * (b_cost[0][3] + b_cost[0][0] + b_cost[3][0] + b_cost[3][3])
        parasite_cost += 4 * (b_cost[0][1] + b_cost[0][2] + b_cost[1][0] + b_cost[2][0] + b_cost[3][1] + b_cost[3][2] + b_cost[1][3] + b_cost[2][3])
        parasite_cost += 3 * (b_cost[1][1] + b_cost[2][2] + b_cost[2][1] + b_cost[1][2])
        
        a, b, c, d, e = self.check(places)

        cost = cost + (a-b)*1000 + (c-d)*100

        if (flg == 'x' and (not winnable_x)) or (flg == 'o' and (not winnable_o)):
            return parasite_cost
        
        return (cost + parasite_cost)
    
    
