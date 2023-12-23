#!/usr/local/bin/python3
# solve_fairies.py : Fairy puzzle solver
#
# Code by: Gautam, Kataria (gkataria)
#          Jaya Sandeep, Ketha (jketha)
#          Wenqian, Chen (wenqchen)
#
# Based on skeleton code by B551 course staff, Fall 2023
#
# N fairies stand in a row on a wire, each adorned with a magical symbol from 1 to N.
# In a single step, two adjacent fairies can swap places. How can
# they rearrange themselves to be in order from 1 to N in the fewest
# possible steps?

# !/usr/bin/env python3
import sys
import queue

N = 5

# THE ABSTRACTION:
#
# Initial state:

# Goal state:
# Given a state, returns True or False to indicate if it is the goal state
def is_goal(state):
    return state == list(range(1, N + 1))

# Successor function:
# Given a state, return a list of successor states
def successors(state):
    return [state[0:n] + [state[n + 1], ] + [state[n], ] + state[n + 2:] for n in range(0, N - 1)]

# Heuristic: Total Displacement from goal state
def total_displacement(s):
    return sum(abs(i - (fairy - 1)) for i, fairy in enumerate(s))

def solve(initial_state):
    visited = set()
    pq = queue.PriorityQueue()

    # Push the initial state into the priority queue with priority
    pq.put((0 + total_displacement(initial_state), (initial_state, 0)))

    path = {tuple(initial_state): [initial_state.copy()]}  # Use lists instead of tuples for the path

    while not pq.empty():
        priority, (state, cost) = pq.get()
        tuple_state = tuple(state)
        if tuple_state in visited:
            continue
        visited.add(tuple_state)

        if is_goal(state):
            return path[tuple_state]  # Return the path to the goal state

        for neighbor in successors(state):
            if tuple(neighbor) not in visited:
                new_cost = cost + 1
                new_priority_value = total_displacement(neighbor)  # Compute the priority value
                # Push the neighbor into the priority queue with updated priority
                pq.put((new_cost + new_priority_value, (neighbor, new_cost)))
                # Update the path with a copy of the neighbor state as a list
                path[tuple(neighbor)] = path[tuple_state] + [neighbor.copy()]

    return []  # Return an empty path if no solution is found

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a test case filename"))

    test_cases = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            test_cases.append([ int(i) for i in line.split() ])
    for initial_state in test_cases:
        	print('From state ' + str(initial_state) + " found goal state by taking path: " + str(solve(initial_state)))

    
