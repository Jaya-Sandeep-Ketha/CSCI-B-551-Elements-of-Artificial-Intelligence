#!/usr/local/bin/python3
#
# mystical_castle.py : a maze solver
#
# Submitted by : Jaya Sandeep, Ketha (jketha)
#
# Based on skeleton code provided in CSCI B551, Fall 2023.
# References: https://youtu.be/KiCBXu4P-2Y?feature=shared
#             https://towardsdatascience.com/graph-theory-bfs-shortest-path-problem-on-a-grid-1437d5cb4023
#             https://stackoverflow.com/questions/55316735/shortest-path-in-a-grid-using-bfs

import sys
from collections import deque

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))

        # Return only moves that are within the castle_map and legal (i.e. go through open space ".")
        return [ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]

# Determine the direction of the movements
def get_direction(previous_loction, next_location):
    if next_location[0] == previous_loction[0] - 1:
        return "U"
    elif next_location[1] == previous_loction[1] + 1:
        return "R"
    elif next_location[0] == previous_loction[0] + 1:
        return "D"
    elif next_location[1] == previous_loction[1] - 1:
        return "L"
    return ""  # movement is invalid

def search(castle_map):
        # Find current start position
        current_loc=[(row_i,col_i) for col_i in range(len(castle_map[0])) for row_i in range(len(castle_map)) if castle_map[row_i][col_i]=="p"][0]
        fringe = deque([(current_loc, 0, '')])  # Add an empty string to store the path
        visited = set()
        
        while fringe:
                (curr_move, curr_dist, move_string) = fringe.popleft()

                if curr_move in visited:
                       continue
                visited.add(curr_move)

                for move in moves(castle_map, *curr_move):
                        if castle_map[move[0]][move[1]]=="@":
                                return (curr_dist + 1, move_string + get_direction(curr_move, move))
                        else:
                               new_move_string = move_string + get_direction(curr_move, move)
                               fringe.append((move, curr_dist + 1, new_move_string))

        return (-1,'')

# Main Function
if __name__ == "__main__":
        castle_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution = search(castle_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + solution[1])

