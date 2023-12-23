#!/usr/local/bin/python3
# solver2023.py : 2023 Sliding tile puzzle solver
#
# Code by:  Gautam, Kataria (gkataria)
#           Jaya Sandeep, ketha (jketha)
#           Wenqian, Chen (wenqchen)
#
# Based on skeleton code by B551 Staff, Fall 2023

import sys
import heapq

ROWS=5
COLS=5

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]

# ------------Get the row and column values from the given index----------------------
def index_pos(index):
    return (int(index/5), index % 5)

# ------------- Outer Elements Rotation --------------
# Outer clockwise rotation
def OC(board):
    return (tuple([board[5]]) + tuple(board[0:4]) + tuple([board[10]]) + tuple(board[6:9]) + tuple([board[4]]) + tuple([board[15]]) + tuple(board[11:14]) + tuple([board[9]]) + tuple([board[20]]) + tuple(board[16:19]) + tuple([board[14]]) + tuple([board[21]]) + tuple(board[22:25]) + tuple([board[19]]))

# Outer counter-clockwise rotation
def OCC(board):
    return (tuple([board[1]]) + tuple(board[2:5]) + tuple([board[9]]) + tuple([board[0]]) + tuple(board[6:9]) + tuple([board[14]]) + tuple([board[5]]) + tuple(board[11:14]) + tuple([board[19]]) + tuple([board[10]]) + tuple(board[16:19]) + tuple([board[24]]) + tuple([board[15]]) + tuple(board[20:23]) + tuple([board[23]]))

# -------------- Inner Elements Rotation ----------------
# Inner clockwise rotation
def IC(board):
    return (tuple(board[0:6]) + tuple([board[11]]) + tuple(board[6:8]) + tuple(board[9:11]) + tuple([board[16]]) + tuple([board[12]]) + tuple([board[8]]) + tuple(board[14:16]) + tuple(board[17:19]) + tuple([board[13]]) + tuple(board[19:]))

# Inner counter-clockwise rotation
def ICC(board):
    return (tuple(board[0:6]) + tuple(board[7:9]) + tuple([board[13]]) + tuple(board[9:11]) + tuple([board[6]]) + tuple([board[12]]) + tuple([board[18]]) + tuple(board[14:16]) + tuple([board[11]]) + tuple(board[16:18]) + tuple(board[19:]))

# ------------ Row Rotation ----------------
# Perform a row rotation towards the right
def row_right(row):
    return row[-1:] + row[0:-1]

# Perform a row rotation towards the left
def row_left(row):
    return row[1:] + row[0:1]

# ----------- Row Successors -----------------
# Get successors of a row by rotating it towards the right
def row_right_succ(board, row):
    right_rot = row_right(board[row*5:(row*5)+5])
    return (tuple(board[0:row*5] + right_rot + board[(row*5)+5:]))

# Get successors of a row by rotating it towards the left
def row_left_succ(board, row):
    left_rot = row_left(board[row*5:(row*5)+5])
    return (tuple(board[0:row*5] + left_rot + board[(row*5)+5:]))

# ----------- Column Rotation ----------------
# Perform a column rotation upwards
def column_up(col):
    return col[1:] + col[0:1]

# Perform a column rotation downwards
def column_down(col):
    return col[-1:] + col[0:-1]

# ------------ Column Successors ---------------
# Get successors of a column by rotating it upwards
def column_up_succ(board, col):
    up_rot = column_up(board[col:col+21:5])
    return (tuple(board[0:col] + tuple([up_rot[0]])) + board[col+1:col+5] + tuple([up_rot[1]]) + board[col+6:col+10] + tuple([up_rot[2]]) + board[col+11:col+15] + tuple([up_rot[3]]) + board[col+16:col+20] + tuple([up_rot[4]]) + board[col+21:])

# Get successors of a column by rotating it downwards
def column_down_succ(board,col):
    down_rot = column_down(board[col:col + 21:5])
    return (tuple(board[0:col] + tuple([down_rot[0]])) + board[col + 1:col + 5] + tuple([down_rot[1]]) + board[col + 6:col + 10] + tuple([down_rot[2]]) + board[col + 11:col + 15] + tuple([down_rot[3]]) + board[col + 16:col + 20] + tuple([down_rot[4]]) + board[col + 21:])

# -------------- Heuristic Function -----------------
# Calculate the Manhattan distance heuristic for the board

def manhatten_distance(board):
    # Define the goal state for the 5x5 board
    goal_state = [
        1, 2, 3, 4, 5,
        6, 7, 8, 9, 10,
        11, 12, 13, 14, 15,
        16, 17, 18, 19, 20,
        21, 22, 23, 24, 25
    ]

    # Initialize the Manhattan distance heuristic to 0
    heuristic = 0

    # Calculate the Manhattan distance for each tile and accumulate the total heuristic value
    for tile in range(1, 26):
        current_pos = board.index(tile)
        goal_pos = goal_state.index(tile)
        current_row, current_col = index_pos(current_pos)
        goal_row, goal_col = index_pos(goal_pos)
        heuristic += abs(current_row - goal_row) + abs(current_col - goal_col)

    return heuristic//5

# Generate a list of possible successor states for the given state
def successors(state):
    succ = []
    # First, check all rotations and append them to the successor list
    succ.append([(OC(state)), 'Oc', manhatten_distance(OC(state))])
    succ.append([(OCC(state)), 'Occ', manhatten_distance(OCC(state))])
    succ.append([(IC(state)), 'Ic', manhatten_distance(IC(state))])
    succ.append([(ICC(state)), 'Icc', manhatten_distance(ICC(state))])
    
    # Then, check and compute the column and row rotations and find their Manhattan distances in parallel.
    for ele in range(1,6):
        # Append row left rotation
        succ.append(
            [(row_left_succ(state, ele-1)), 'L' + str(ele), manhatten_distance(row_left_succ(state, ele-1))])
        # Append row right rotation
        succ.append(
            [(row_right_succ(state, ele-1)), 'R' + str(ele), manhatten_distance(row_right_succ(state, ele-1))])
        # Append column up rotation
        succ.append(
            [(column_up_succ(state, ele-1)), 'U' + str(ele), manhatten_distance(column_up_succ(state, ele-1))])
        # Append column down rotation
        succ.append(
            [(column_down_succ(state, ele-1)), 'D' + str(ele), manhatten_distance(column_down_succ(state, ele-1))])
    # Return all the computed successors
    return succ

# ----------------------------------- Goal State Comparison ----------------------------------------------
# Check if the current state is the goal state
def is_goal(state):
    dest = list(range(1, ROWS*COLS+1))
    return dest == list(state)

# Solve the puzzle using A* search
def solve(initial_board):
    # Create a set to keep track of visited states
    traversed = set()
    # Create a priority queue for the fringe of states to explore
    fringe = []
    # Initialize the current path and cost
    current_path = []
    current_cost = 0

    # Push the initial state onto the fringe with its heuristic value
    heapq.heappush(fringe, (manhatten_distance(initial_board), (initial_board, current_cost, current_path)))

    while fringe:
        _, (state, current_cost, current_path) = heapq.heappop(fringe)
        # Check if the current state is the goal state
        if is_goal(state):
            return current_path
        # Skip states that have already been visited
        if state in traversed:
            continue
        # Mark the current state as visited
        traversed.add(state)
        # Generate successors and add them to the fringe
        for (next_state, move, manhattan_cost) in successors(state):
            # Skip states that have already been visited
            if next_state not in traversed:
                heuristic_val = current_cost + 1 + manhattan_cost
                heapq.heappush(fringe, (heuristic_val, (next_state, current_cost + 1, current_path + [move])))


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
