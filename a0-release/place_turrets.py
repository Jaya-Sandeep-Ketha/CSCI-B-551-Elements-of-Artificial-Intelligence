#!/usr/local/bin/python3
#
# place_turrets.py : arrange turrets on a grid, avoiding conflicts
#
# Submitted by : Jaya Sandeep, Ketha (jketha)
#
# Based on skeleton code in CSCI B551, Fall 2022.
# References: https://youtu.be/xFv_Hl4B83A?feature=shared
#             https://www.geeksforgeeks.org/n-queen-problem-backtracking-3/
#             https://favtutor.com/blogs/n-queen-problem

import sys

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of turrets on castle_map
def count_turrets(castle_map):
    return sum([ row.count('p') for row in castle_map ] )

# Return a string with the castle_map rendered in a human-turretly format
def printable_castle_map(castle_map):
    return "\n".join(["".join(row) for row in castle_map])

# Add a turret to the castle_map at the given position, and return a new castle_map (doesn't change original)
def add_turret(castle_map, row, col):
    return castle_map[0:row] + [castle_map[row][0:col] + ['p',] + castle_map[row][col+1:]] + castle_map[row+1:]

# Get list of successors of given castle_map state
def successors(castle_map):
    return [
        add_turret(castle_map, r, c) for r in range(0, len(castle_map)) for c in range(0, len(castle_map[0]))
        if castle_map[r][c] == '.' and check_conditions(add_turret(castle_map, r, c))
    ]


# Check if castle_map is a goal state
def is_goal(castle_map, k):
    return count_turrets(castle_map) == k 

def check_conditions(castle_map):
    for row in range(0, len(castle_map)):
        for col in range(0,len(castle_map[0])):

            if castle_map[row][col] == "p":  
               
               # Check row 
                row_state = ""
                for i in range(col+1,len(castle_map[0])):
                    row_state += castle_map[row][i]

                    if castle_map[row][i] == "p":
                        if ("X" in row_state[:]) or ("@" in row_state[:]):
                            break
                        else:
                            return False
                
                # Check columns
                col_state = ""  
                for i in range(row+1,len(castle_map)):
                    col_state += castle_map[i][col]
                    
                    if castle_map[i][col] == "p":
                        if ("X" in col_state[:]) or ("@" in col_state[:]):
                            break
                        else:
                            return False
                        
                # Check upper half of positive diagonal
                up_pos_dia = ""
                up_row = row
                up_col = col
                while (up_row-1 in range(0,len(castle_map))) and (up_col+1 in range(0,len(castle_map[0]))):
                    up_row -= 1
                    up_col += 1
                    up_pos_dia += castle_map[up_row][up_col]
                    if castle_map[up_row][up_col] == "p":
                        if ("X" in up_pos_dia[:]) or ("@" in up_pos_dia[:]) :
                            break
                        else:
                            return False

                # Check lower half of the positive diagonal     
                low_pos_dia = ""
                row_down = row
                col_down = col
                while (row_down + 1 in range(len(castle_map)-1)) and (col_down-1 in range(len(castle_map[0]))):
                    row_down += 1
                    col_down -= 1
                    low_pos_dia += castle_map[row_down][col_down]
                    if castle_map[row_down][col_down] == "p":
                        if "X" in low_pos_dia[:] or ("@" in low_pos_dia[:]) :
                            break
                        else:
                            return False
               
                       
                # Check upper half of the negative diagonal
                up_neg_dia = ""
                up_row = row
                up_col = col
                while (up_row - 1 in range(len(castle_map))) and (up_col-1 in range(len(castle_map[0]))):
                    up_row -= 1
                    up_col -= 1
                    up_neg_dia += castle_map[up_row][up_col]
                    if castle_map[up_row][up_col]=="p":
                        if ("X" in up_neg_dia[:]) or ("@" in up_neg_dia[:]):
                            break
                        else:
                            return False

               # Check lower half of the negative diagonal
                
                down_neg_dia=""
                row_down=row
                col_down=col
                while (row_down+1 in range(len(castle_map)-1)) and (col_down+1 in range(len(castle_map[0]))):
                    row_down += 1
                    col_down += 1
                    down_neg_dia += castle_map[row_down][col_down]
                    if castle_map[row_down][col_down]=="p":
                        if ("X" in down_neg_dia[:]) or ("@" in down_neg_dia[:]):
                            break
                        else:
                            return False
       
    # it will return true if all the conditions have been met that is no "p" is able to see each other
    return True

def solve(initial_castle_map,k):
    fringe = [initial_castle_map]
    while len(fringe) > 0:
        for new_castle_map in successors(fringe.pop()):
            if is_goal(new_castle_map,k):
                return(new_castle_map,True)
            fringe.append(new_castle_map)
    return ("",False)

# Main Function
if __name__ == "__main__":
    castle_map=parse_map(sys.argv[1])
    # This is k, the number of turrets
    k = int(sys.argv[2])
    print ("Starting from initial castle map:\n" + printable_castle_map(castle_map) + "\n\nLooking for solution...\n")
    solution = solve(castle_map,k)
    print ("Here's what we found:")
    print (printable_castle_map(solution[0]) if solution[1] else "False")