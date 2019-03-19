"""mdp with states, rewards, actions, transition table"""

# ----------------------------------Markov Decision Process----------------------------------
# Requires stdin_input.py for run as python script
#
# States:                    0 to MDP.max_row * MDP.max_col
# Rewards:                   MDP.rewards
# Transition table:          MDP.transition_table
# Actions:                   up, down, left, right (for all valid states)
#

class MDP(object):
    """mdp with states, rewards, actions, transition table"""

    def __init__(self, values):
        """init"""
        self.rewards = values["rewards"]
        self.max_row = values["dim_row"] - 1
        self.max_col = values["dim_col"] - 1
        self.step_reward = values["step_reward"]
        self.end_state = []
        self.wall = []
        self.transition_table = {}

        for row in range(0, self.max_row + 1):
            end_row = []
            wall_row = []
            for col in range(0, self.max_col + 1):
                if [row, col] in values["end_states"]:
                    end_row.append(True)
                else:
                    end_row.append(False)

                if [row, col] in values["walls"]:
                    wall_row.append(True)
                else:
                    wall_row.append(False)
            self.end_state.append(end_row)
            self.wall.append(wall_row)

        self.construct_transition_table()

# --------------------------------Construct transition table---------------------------------
# 1. Each outcome(row, column) from each state by performing each action can be accessed by :
#    row         :      MDP.transition_table[state][action][index]["result"]["row"]
#    col         :      MDP.transition_table[state][action][index]["result"]["col"]
#
# 2. And the corresponding probability by:
#    probability : MDP.transition_table[state][action][index]["prob"]
#

    def construct_transition_table(self):
        """constructs transition table self.transition_table[state][action]"""
        max_col = self.max_col + 1
        for row in range(0, self.max_row + 1):
            for col in range(0, self.max_col + 1):
                self.transition_table[row * max_col + col] = self.transition_table_row(row, col)

# -------------------------------Valid adjacent states---------------------------------------

# Valid adjacent states when an agent executes a move succesfully and got the desired output
#

    def adjacent_states(self, row, col):
        """returns possible adjacent states that are valid"""
        current_state = {"row":row, "col":col}
        state_to_the = {}
        if col == 0:
            state_to_the["left"] = current_state
        elif self.wall[row][col - 1]:
            state_to_the["left"] = current_state
        else:
            state_to_the["left"] = {"row":row, "col":col-1}

        if col == self.max_col:
            state_to_the["right"] = current_state
        elif self.wall[row][col + 1]:
            state_to_the["right"] = current_state
        else:
            state_to_the["right"] = {"row":row, "col":col+1}

        if row == 0:
            state_to_the["up"] = current_state
        elif self.wall[row-1][col]:
            state_to_the["up"] = current_state
        else:
            state_to_the["up"] = {"row":row - 1, "col":col}

        if row == self.max_row:
            state_to_the["down"] = current_state
        elif self.wall[row+1][col]:
            state_to_the["down"] = current_state
        else:
            state_to_the["down"] = {"row":row + 1, "col":col}

        return state_to_the

# --------------------------------Row of each transition table------------------------------
#
# correspondes to each of the valid states in the given MDP
#
#

    def transition_table_row(self, row, col):
        """returns rows corresponding to a single state"""
        table_row = {}
        actions = ["left", "right", "up", "down"]
        for action in actions:
            table_row[action] = []
        state_to_the = self.adjacent_states(row, col)


        # moved correctly
        table_row["left"].append({"result":state_to_the["left"], "prob":0.8})
        table_row["right"].append({"result":state_to_the["right"], "prob":0.8})
        table_row["up"].append({"result":state_to_the["up"], "prob":0.8})
        table_row["down"].append({"result":state_to_the["down"], "prob":0.8})

        # moved perpendicularly
        table_row["left"].append({"result":state_to_the["up"], "prob":0.1})
        table_row["left"].append({"result":state_to_the["down"], "prob":0.1})

        table_row["right"].append({"result":state_to_the["up"], "prob":0.1})
        table_row["right"].append({"result":state_to_the["down"], "prob":0.1})

        table_row["up"].append({"result":state_to_the["left"], "prob":0.1})
        table_row["up"].append({"result":state_to_the["right"], "prob":0.1})

        table_row["down"].append({"result":state_to_the["left"], "prob":0.1})
        table_row["down"].append({"result":state_to_the["right"], "prob":0.1})

        return table_row

# ---------------------------------Helper functions-----------------------------------------

    def reward(self, state):
        """return reward of state given state name"""
        row = state / (self.max_col + 1)
        col = state % (self.max_col + 1)
        return self.rewards[row][col]

    def endstate(self, state):
        """returns true if state given is endstate"""
        row = state / (self.max_col + 1)
        col = state % (self.max_col + 1)
        return self.end_state[row][col]

    def walls(self, state):
        """returns true if state is blocked"""
        row = state / (self.max_col + 1)
        col = state % (self.max_col + 1)
        return self.wall[row][col]

# ----------------------------------for testing---------------------------------------------
if __name__ == "__main__":

    from stdin_input import read_input

    TEST = MDP(read_input())
    print TEST.rewards
    print TEST.end_state
    print TEST.wall

    print TEST.transition_table[0]["up"]
    print ""
    print TEST.transition_table[10]["right"]

    print TEST.wall[1][2]

# -----------------------------------------------------------------------------------------
