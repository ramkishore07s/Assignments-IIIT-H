"""parses input into a dictionary for the assignment"""

# --------------------------Converts each line of input into an array of floats-----------------
#
#

def get_input():
    """parses input into a array of floats"""
    try:
        line = raw_input()
    except EOFError:
        pass
    values = []
    for word in line.split():
        values.append(float(word))
    return values

# ------------------------------Read input and parse it to initialize MDP-----------------------

def read_input():
    """returns dict for an MDP"""

    # dimensions of the world
    output = get_input()
    dim_row, dim_col = output[0], output[1]

    # rewards for each state
    reward = []
    for _ in range(0, int(dim_row)):
        reward.append(get_input())

    # End states and Walls
    output = get_input()
    no_e, no_w = output[0], output[1]

    end_states = []
    walls = []

    for _ in range(0, int(no_e)):
        end_states.append(get_input())

    for _ in range(0, int(no_w)):
        walls.append(get_input())

    # start state and step reward
    start = get_input()
    step_reward = get_input()

    # returns dict used to initialize MDP
    return {"dim_row":int(dim_row), "dim_col":int(dim_col),
            "rewards":reward, "end_states":end_states,
            "walls":walls, "start":start, "step_reward":step_reward}


if __name__ == "__main__":
    print read_input()

# ----------------------------------------------------------------------------------------------
