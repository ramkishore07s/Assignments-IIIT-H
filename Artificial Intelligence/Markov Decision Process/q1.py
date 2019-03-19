"""value iteration algorithm for assignment 1"""

# ---------------------------Value Iteration for MDP-------------------------------------------
# Files required: q1.py          =>  value iteration algorithm and helper functions for given MDP
#                 mdp.py         =>  MDP class with rewards, transitions_table etc.
#                 stdin_input.py =>  Parsing input
#
# run as: python q1.py < input
# pep8 standards have benn adhered to.
#

import copy
from stdin_input import read_input
from mdp import MDP as CREATE_MDP

# ------------------------------Initialize MDP and other constants-----------------------------

MDP_VALS = read_input()
MDP = CREATE_MDP(MDP_VALS)
START_STATE = MDP_VALS["start"]
EPSILON = 0.01
GAMMA = 1.0
MAX_CHANGE_TOLERANCE = EPSILON * (1 - GAMMA)/GAMMA
U = [0 for _ in range(0, MDP_VALS["dim_row"] * MDP_VALS["dim_col"])]

# --------------------------------------Helper functions---------------------------------------
#
# Functions used by Value iteration algorithm
#

def state_name(row, col):
    """calculate state name for given coords"""
    return row * MDP_VALS["dim_row"] + col

def utility(state, action):
    """calculate one look ahead utility"""
    utility_value = 0.0
    outcomes = MDP.transition_table[state][action]

    for outcome in outcomes:
        outcome_state = outcome["result"]["row"] * (MDP.max_col + 1) + outcome["result"]["col"]
        utility_value += U[outcome_state] * outcome["prob"]

    return utility_value + MDP_VALS["step_reward"][0]

def max_utility(state):
    """max one look ahead utility for all possible actions"""
    u_list = []
    actions = ["left", "right", "up", "down"]
    for action in actions:
        u_list.append(utility(state, action))

    if MDP.endstate(state) or MDP.walls(state):
        return 0
    return max(u_list)

# ---------------------------------Max norm for comparing utilities-----------------------------
#
# 1. Norm used: maximum of difference between corresponding elements in current and
#    previous utilities
# 2. Artificial Intelligence: A Modern Approach by Russel and Norvig provides proof
#    for the validity of norm used
#

def change(u_temp, u_prev):
    """max norm"""
    diff = []
    for _, (temp_val, prev_val) in enumerate(zip(u_temp, u_prev)):
        diff.append(abs(temp_val - prev_val))

    return max(diff)

# ----------------------------------Draw policies-----------------------------------------------

P = [0 for _ in range(0, MDP_VALS["dim_row"] * MDP_VALS["dim_col"])]
SYMBOL = {"left":'<', "right":'>', "up":'^', "down":'v'}

def draw_policies():
    """draws policies if policy change is observed"""
    prev_p = copy.deepcopy(P)

    for state in range(0, MDP_VALS["dim_row"] * MDP_VALS["dim_col"]):
        actions = ["left", "right", "up", "down"]
        prev_util = -100000000
        req_action = ""

        for action in actions:
            util = utility(state, action)
            if util > prev_util:
                req_action = action
                prev_util = util

        if not MDP.walls(state) and not MDP.endstate(state):
            P[state] = SYMBOL[req_action]
        else:
            P[state] = '*'
    if not prev_p == P:
        count = 0
        for each_one in P:
            count += 1
            print each_one,
            if count % MDP_VALS["dim_col"] == 0:
                print ""

    return not prev_p == P


# --------------------------------The value iteration algorithm---------------------------------

def value_iteration():
    """the value iteration algorithm"""
    no_iterations = 0
    global U

    while True:
        no_iterations += 1
        u_temp = copy.deepcopy(U)
        max_change = 0

        for state in range(0, MDP_VALS["dim_row"] * MDP_VALS["dim_col"]):
            u_temp[state] = MDP.reward(state) +  GAMMA * max_utility(state)
            if change(u_temp, U) > max_change:
                max_change = change(u_temp, U)

        if max_change <= 0:
            return u_temp
        U = u_temp

        # if draw_policies():
        #     print ""
        #     count = 0
        #     for each in U:
        #         count += 1
        #         print '%.3f' % (each,),
        #         if count % MDP_VALS["dim_col"] == 0:
        #             print ""
        #     print ""
        #     print ""


U = value_iteration()

# --------------------------------formatted output----------------------------------------------

COUNT = 0
for each in U:
    COUNT += 1
    print '%.3f' % (each,),
    if COUNT % MDP_VALS["dim_col"] == 0:
        print ""

# ----------------------------------------------------------------------------------------------


# draw_policies()
