#
# raichu.py : Play the game of Raichu
#
# Jaya Sandeep, Ketha - jketha

# References:
# https://github.com/dimitrijekaranfilovic/checkers/blob/master/checkers.py
# https://github.com/njmarko/alpha-beta-pruning-minmax-checkers
# https://www.cs.huji.ac.il/w~ai/projects/old/English-Draughts.pdf
# https://www.hackerearth.com/blog/developers/minimax-algorithm-alpha-beta-pruning/

import sys
import time
import copy

# ----------------- Converting the board in string to a 2D matrix in board format --------------------------
def string_to_board(string_board, size):
    board = [list(string_board[i:i+size]) for i in range(0, size*size, size)]
    return board

# ----------------------------------- Move validator -------------------------------------------------------
def valid_move(row, column, N):
    return 0 <= row < N and 0 <= column < N

# ----------------------------------- Moves Defined --------------------------------------------------------
# -------------------------------- Moves for White Pichu ---------------------------------------------------
# ----------------------------- White Pichu ---> Left Diagonal ---------------------------------------------
def white_pichu_left_diag(current_state, row, column, N, successor_pichu):
    if 0 < column <= N and row <= N-1:
        new_state = copy.deepcopy(current_state)
        if current_state[row + 1][column - 1]==".":                     # If left diagonal position is empty
            if row == N - 1:                                        # If pichu at raichu promotion condition
                new_state[row + 1][column - 1] = '@'
            else:                                                         # If pichu at some middle position
                new_state[row + 1][column - 1] = 'w'
            
            new_state[row][column] = '.'
            successor_pichu.append(new_state)
              
        if  current_state[row + 1][column - 1] == "b" and (row <= N - 2 and column >= 2) and current_state[row + 2][column - 2]== ".":  # If opponentonent found
            if row == N - 2: # If jumping over an opponentonent in the left diagonal promotes the pichu to a raichu
                new_state[row + 2][column - 2] = '@'
            else:                                 # If an opponentonent is at the left diagonal but not at the edge
                new_state[row + 2][column - 2] = 'w'

            new_state[row][column] = '.'
            new_state[row + 1][column - 1] = '.'
            successor_pichu.append(new_state)

# ---------------------------- White Pichu ---> Right Diagonal ----------------------------------------------
def white_pichu_right_diag(current_state, row, column, N, successor_pichu):
    if valid_move(row, column, N) and current_state[row + 1][column + 1] == ".":    # Check if the move is valid and the immediate right diagonal position is empty
        new_state = copy.deepcopy(current_state)                                    # Create a copy of the current state
        if row == N - 1:                                                              # Check if the pichu reaches raichu promotion condition
            new_state[row + 1][column + 1] = '@'
        else:
            new_state[row + 1][column + 1] = 'w'
        
        new_state[row][column] = '.'
        successor_pichu.append(new_state)
                        
        if 0 <= column <= N - 2 and row <= N - 1:                                   # Check for opponent at the right diagonal and an empty cell after jumping
            new_state = copy.deepcopy(current_state)
            if current_state[row + 1][column + 1]==".":                             # If immediate next diagonal position is empty
                if row == N-1:                                                      # Raichu promotion condition
                    new_state[row + 1][column + 1] = '@'
                else:                                                               # Normal pichu movement
                    new_state[row + 1][column + 1] = 'w'     

                new_state[row][column] = '.'
                successor_pichu.append(new_state)
                            
            if  current_state[row + 1][column + 1]=="b" and (row <= N-2 and column <= N-2) and current_state[row + 2][column + 2]== "." :  # If there is an opponent and an empty cell after jumping
                if row == N - 2:                                                    # Raichu promotion after jumping opponent
                    new_state[row + 2][column + 2] = '@'
                else:                                                               # Jumping over opponent
                    new_state[row + 2][column + 2] = 'w'
                
                new_state[row][column] = '.'
                new_state[row + 1][column + 1] = '.' 
                successor_pichu.append(new_state)

# ----------------------------- Moves for Black pichu -------------------------------------------------------
# ---------------------------- Black Pichu ---> Left Diagonal -----------------------------------------------
def black_pichu_left_diag(current_state, row, column, N, successor_pichu):
    if 0 < column <= N:
        new_state = copy.deepcopy(current_state)               
        if current_state[row - 1][column - 1] == ".":                   # If the left diagonal is empty
            if row == 1:                                                # If in second-to-last position
                new_state[row - 1][column - 1] = '$'
            else:                                                       # If in a middle row
                new_state[row - 1][column - 1] = 'b'

            new_state[row][column] = '.'
            successor_pichu.append(new_state)
                        
        if  new_state[row - 1][column - 1] == "w" and (row >= 2 and column >= 2) and current_state[row - 2][column - 2] == '.' : # Opponent at immediate left diagonal
            if row == 2:
                new_state[row - 2][column - 2] = '$'
            else:
                new_state[row - 2][column - 2] = 'b'
            
            new_state[row][column] = '.'
            new_state[row - 1][column - 1] = '.'
            successor_pichu.append(new_state)

# ---------------------------- Black Pichu ---> Right Diagonal ----------------------------------------------
def black_pichu_right_diag(current_state, row, column, N, successor_pichu):
    if 0 <= column <= N-1:
        new_state = copy.deepcopy(current_state)
        if current_state[row - 1][column + 1]==".":                                     # Right diagonal empty 
            if row == 1:                                                                # Reached raichu condition
                new_state[row - 1][column + 1] = '$'
            else:                                                                       # No raichu promotion
                new_state[row - 1][column + 1] = 'b'
            
            new_state[row][column] = '.'
            successor_pichu.append(new_state)
            
        
        if  current_state[row - 1][column + 1] == "w" and (row >= 2 and column <= N-2) and current_state[row - 2][column + 2] == "." : # Opponent at immediate diagonal
            if row == 2:
                new_state[row - 2][column + 2] = '$'
            else:
                new_state[row - 2][column + 2] = 'b'
            
            new_state[row][column] = '.'
            new_state[row - 1][column + 1] = '.'
            successor_pichu.append(new_state)    

# -------------------------------- Successors of pichu ---------------------------------------------------------
def pichu(current_state, player):
    successor_pichu = []
    N = len(current_state) - 1
    if player == "w":                                                                   # If the player is white
        for row in range(N):
               for column in range(len(current_state[0])):
                    if current_state[row][column] == 'w':
                        white_pichu_right_diag(current_state, row, column, N, successor_pichu)
                        white_pichu_left_diag(current_state, row, column, N, successor_pichu)               
                        
    else: 
        for row in range(len(current_state)):
            for column in range(len(current_state[0])):
                    if current_state[row][column] == 'b':
                        black_pichu_right_diag(current_state, row, column, N, successor_pichu)
                        black_pichu_left_diag(current_state, row, column, N, successor_pichu)                            
    return successor_pichu
                        
# -------------------------------- Moves for White Pichu ---------------------------------------------------
# -------------------------------- White Pikachu ---> Down--------------------------------------------------
def white_pikachu_down(current_state, row, column, N, successor_pikachu):             
        # Moving down, check if the immediate step below is empty
        if row <= N-1 and current_state[row + 1][column] == ".":
            new_state = copy.deepcopy(current_state)
            if row == N-1:                                              # When in the last row, promote Pikachu to Raichu
                new_state[row + 1][column] = '@'
            else:       # In a middle row
                new_state[row + 1][column] = 'W'
            new_state[row][column] = '.'
            successor_pikachu.append(new_state)
        
        # Jumping 2 steps when 2 steps below are empty
        if row <= N-2:                                                 
            if current_state[row + 1][column] == "." and current_state[row + 2][column] == "."  : 
                new_state = copy.deepcopy(current_state)   
                if row == N-2:      # In the 6th row, jumping 2 steps reaches last row (Raichu promotion) 
                    new_state[row + 2][column] = '@'                                   
                else:                                     # If in a middle row, move 2 steps forward
                    new_state[row + 2][column] = 'W'
                new_state[row][column] = '.'
                successor_pikachu.append(new_state)                               
                                                    
        # When the first step below is empty and the next is occupied by an opponent
        if row + 2 < N:
            if current_state[row + 1][column] == "." and (current_state[row + 2][column] in ["b","B","w","W"] ) : 
                if current_state[row + 2][column]=="b" or current_state[row + 2][column]=="B":
                    if row == N - 3 and current_state[row + 3][column] == ".": # if we are in 4th r
                        new_state = copy.deepcopy(current_state)
                        new_state[row + 3][column] = '@' # reached last r so convert to Raichu
                        new_state[row][column] = '.'     # updating our original location
                        new_state[row + 2][column] = '.'   # updating the opponents location
                        successor_pikachu.append(new_state)
                    elif row < N - 3 and current_state[row + 3][column] == ".":
                        new_state = copy.deepcopy(current_state)
                        new_state[row + 3][column] = 'W'
                        new_state[row + 2][column] = '.'
                        new_state[row][column] = '.'
                        successor_pikachu.append(new_state)          

    # Considering the case where the first step below is occupied while the second one is vacant.
        if (current_state[row + 1][column] in ["b","B","w","W"]) and current_state[row + 2][column] == "." : 
            if current_state[row + 1][column] == "b" or current_state[row + 1][column] == "B":
                new_state = copy.deepcopy(current_state)
                if row == N-2:
                    new_state[row + 2][column] = '@' # reached last r so convert to Raichu
                else:                             # if we are in some middle r 
                    new_state[row + 2][column] = 'W' 
                new_state[row][column] = '.'
                new_state[row + 1][column] = '.' 
                successor_pikachu.append(new_state)
    
    # Advancing when two consecutive steps are unoccupied.
        if row <= N-3 and (current_state[row + 1][column] in ["b","B","w","W"] ) and current_state[row + 2][column] == "." and current_state[row + 3][column] == "." : 
            if current_state[row+1][column] == "b" or current_state[row + 1][column] == "B":
                new_state = copy.deepcopy(current_state)
                if row == N-3:
                    new_state[row + 3][column] = '@' # reached last r so convert to Raichu
                else:                             # if we are in some middle ro
                    new_state = copy.deepcopy(current_state)
                    new_state[row + 3][column] = 'W' 
                new_state[row + 1][column] = '.'
                new_state[row][column] = '.'
                successor_pikachu.append(new_state)   

# -------------------------------- White Pikachu ---> Left--------------------------------------------------
def white_pikachu_left(current_state, row, column, N, successor_pikachu):
    # Handling all scenarios for moving Pikachu to the left.
    # When shifting one step to the left when it's unoccupied.
    if column >= 1 and current_state[row][column-1] == ".":
        new_state = copy.deepcopy(current_state)
        new_state[row][column-1] = 'W'
        new_state[row][column] = '.'
        successor_pikachu.append(new_state)
            
    if column >= 2:
        # when moving 2 step to the left when they are empty 
        if current_state[row][column - 1] == "." and current_state[row][column - 2] == "."  : 
            new_state = copy.deepcopy(current_state)
            new_state[row][column - 2] = 'W'
            new_state[row][column] = '.'
            successor_pikachu.append(new_state)
        
        # now considering first step in left empty and another is full
        if current_state[row][column - 1] == "." and (current_state[row][column - 2] in ["b","B","w","W"]) : 
            if column >= 3 and current_state[row][column - 3] == "." and current_state[row][column - 1] in 'bB':
                    new_state[row][column - 3] = 'W'
                    new_state[row][column - 2] = '.'
                    new_state[row][column] = '.'
                    successor_pikachu.append(new_state)
                
        # now considering first step full and another is empty 
        if (current_state[row][column - 1] in ["b","B","w","W"]) and current_state[row][column - 2] == "." : 
            if current_state[row][column - 1] == "b" or current_state[row][column - 1] == "B":
                new_state = copy.deepcopy(current_state)
                new_state[row][column - 2] = 'W' 
                new_state[row][column] = '.'
                new_state[row][column - 1] = '.' 
                successor_pikachu.append(new_state)
        
        # considering first step full and 2 steps are empty after that
        if column >= 3 and (current_state[row][column - 1] in ["b","B","w","W"]) and current_state[row][column - 2] == "." and current_state[row][column - 3] == "." : 
            if current_state[row][column - 1] == "b" or current_state[row][column - 1] == "B":    
                new_state = copy.deepcopy(current_state)
                new_state[row][column - 3] = 'W' 
                new_state[row][column - 1] = '.'
                new_state[row][column] = '.'
                successor_pikachu.append(new_state)

# -------------------------------- White Pikachu ---> Right --------------------------------------------------
def white_pikachu_right(current_state, row, column, N, successor_pikachu):
    # All the cases when we are moving pikachu to right side
    # when moving 1 step to the right when its empty
    if column <= N - 1 and current_state[row][column + 1] == ".":
            new_state = copy.deepcopy(current_state)
            new_state[row][column + 1] = 'W'
            new_state[row][column] = '.'
            successor_pikachu.append(new_state)
            
    if column <= N - 2:                                    
         # considering when moving 2 steps to the right when they are empty 
        if current_state[row][column + 1]=="." and current_state[row][column + 2]=="."  :                                     
            new_state = copy.deepcopy(current_state)
            new_state[row][column + 2] = 'W'
            new_state[row][column] = '.'
            successor_pikachu.append(new_state)
        
        # now considering first step in right empty and another is full and after that there is an empty step
        # so we will jump to the last empty step. We could have jumped to the first empty step but that case 
        # we have already covered above when we to check any immediate empty step towards right
        if current_state[row][column + 1] == "." and (current_state[row][column + 2] in ["b","B","w","W"]) : 
            if current_state[row][column + 2]=="b" or current_state[row][column + 2] == "B":
                if column <= N - 3 and new_state[row][column + 3] == ".":
                    new_state = copy.deepcopy(current_state)
                    new_state[row][column + 3] = 'W'
                    new_state[row][column + 2] = '.'
                    new_state[row][column] = '.'
                    successor_pikachu.append(new_state)
                
        # now considering  first step full and another is empty 
        if (current_state[row][column + 1] in ["b","B","w","W"]) and current_state[row][column + 2]=="." : 
            if current_state[row][column + 1]=="b" or current_state[row][column + 1] == "B":
                new_state = copy.deepcopy(current_state)
                new_state[row][column + 2] = 'W' 
                new_state[row][column] = '.'
                new_state[row][column + 1] = '.' 
                successor_pikachu.append(new_state)
        
        # considering first step full and 2 steps empty to the right
        if column <= N - 3 and (current_state[row][column + 1] in ["b","B","w","W"]) and current_state[row][column + 2]=="." and current_state[row][column + 3]=="." : 
            if current_state[row][column + 1]=="b" or current_state[row][column + 1]=="B": 
                new_state = copy.deepcopy(current_state)
                new_state[row][column + 3] = 'W' 
                new_state[row][column + 1] = '.'
                new_state[row][column] = '.'
                successor_pikachu.append(new_state)  

# -------------------------------- Black Pikachu ---> Up --------------------------------------------------
def black_pikachu_up(current_state, row, column, N, successor_pikachu):           
                    # when moving up 
                    # consider to when 1 step is empty above
    if row >= 1 and current_state[row - 1][column] == ".":
        new_state = copy.deepcopy(current_state)
        if row == 1: # If we are in second r will get converted to Raichu
            new_state[row - 1][column] = '$'
        else:       # We are in some middle r
            new_state[row - 1][column] = 'B'
        new_state[row][column] = '.'
        successor_pikachu.append(new_state)
                                    
    if row >= 2:
    # considering when two steps above are empty
        if current_state[row - 1][column]=="." and current_state[row - 2][column]=="."  : 
            new_state = copy.deepcopy(current_state)
            if row == 2: # if we are in 2nd r and jumping 2 steps
                new_state[row - 2][column] = '$'                                   
            else: # if we are in some middle r and we move 2 position forward
                new_state[row - 2][column] = 'B'
            new_state[row][column] = '.'
            successor_pikachu.append(new_state)

    # now considering first step empty and another is full and then another step is empty 
    if current_state[row - 1][column]=="." and (current_state[row - 2][column] in ["w","W","b","B"]) : 
        if current_state[row - 2][column]=="w" or current_state[row - 2][column]=="W":                                
            if row == 3 and new_state[row - 3][column] == ".":
                new_state = copy.deepcopy(current_state)
                new_state[row - 3][column] = '$'
                new_state[row - 2][column] = '.'
                new_state[row][column] = '.'
                successor_pikachu.append(new_state)            
            elif row > 3 and new_state[row - 3][column] == ".":
                new_state = copy.deepcopy(current_state)
                new_state[row - 3][column] = 'B'
                new_state[row - 2][column] = '.'
                new_state[row][column] = '.'
                successor_pikachu.append(new_state)
       
    # now considering  first step full and another is empty 
    if (current_state[row - 1][column] in ["w","W","b","B"]) and current_state[row - 2][column]=="." : 
        if current_state[row - 1][column]=="w" or current_state[row - 1][column]=="W":
            new_state = copy.deepcopy(current_state)
            if row == 2: # if we are in 2nd r 
                new_state[row - 2][column] = '$' # will reach last r therefore raichu
            else: # if we are in some middle r
                new_state[row - 2][column] = 'B' 
            new_state[row][column] = '.'
            new_state[row - 1][column] = '.' 
            successor_pikachu.append(new_state)

    # considering first step full and then 2 steps are empty
    if row >= 3 and (current_state[row - 1][column] in ["w","W","b","B"]) and current_state[row - 2][column]=="." and current_state[row - 3][column] == "." : 
        if current_state[row - 1][column]=="w" or current_state[row - 1][column]=="W":
            new_state = copy.deepcopy(current_state)
            if row == 3: # if in 3rd r than will be converted to Raichu
                new_state[row - 3][column] = '$' 
            else: # We are in some middle r
                new_state[row - 3][column] = 'B' 
            new_state[row - 1][column] = '.'
            new_state[row][column] = '.'
            successor_pikachu.append(new_state)

# -------------------------------- Black Pikachu ---> Left --------------------------------------------------
def black_pikachu_left(current_state, row, column, N, successor_pikachu):
    # now doing all the things when moving left side
    # when first step towards left is empty            
    if column >= 1 and current_state[row][column - 1]==".":
            new_state = copy.deepcopy(current_state)
            new_state[row][column - 1] = 'B'
            new_state[row][column] = '.'
            successor_pikachu.append(new_state)
                
    if column >= 2:
        # considering when left 2 steps are empty and we jump 2 steps left 
        if current_state[row][column - 1]=="." and current_state[row][column - 2]=="."  : 
            new_state = copy.deepcopy(current_state)
            new_state[row][column - 2] = 'B'
            new_state[row][column] = '.'
            successor_pikachu.append(new_state)
        
        # now considering first step in left empty and another is full and there is another empty step after that
        if current_state[row][column - 1]=="." and (current_state[row][column - 2] in ["w","W","b","B"]) : 
            if current_state[row][column - 2]=="w" or current_state[row][column - 2] == "W":
                if column >= 3 and new_state[row][column - 3] == ".": # we will jump to last empty step
                    new_state = copy.deepcopy(current_state)
                    new_state[row][column - 3] = 'B'
                    new_state[row][column - 2] = '.'
                    new_state[row][column] = '.'
                    successor_pikachu.append(new_state)
            
        # now considering first step full and another is empty 
        if (current_state[row][column - 1] in ["w","W","b","B"]) and current_state[row][column - 2] == "." : 
            if current_state[row][column - 1]=="w" or current_state[row][column - 1]=="W":                                    
                new_state = copy.deepcopy(current_state)
                new_state[row][column - 2] = 'B' 
                new_state[row][column] = '.'
                new_state[row][column - 1] = '.' 
                successor_pikachu.append(new_state)
        
        # considering first step full and then 2 steps empty and jumped on last empty slot 
        if column >= 3 and (current_state[row][column - 1] in ["w","W","b","B"]) and current_state[row][column - 2]=="." and current_state[row][column - 3]=="." : 
            if current_state[row][column - 1]=="w" or current_state[row][column - 1]=="W":
                new_state = copy.deepcopy(current_state)
                new_state[row][column - 3] = 'B' 
                new_state[row][column - 1] = '.'
                new_state[row][column] = '.'
                successor_pikachu.append(new_state)

# -------------------------------- Black Pikachu ---> Right --------------------------------------------------
def black_pikachu_right(current_state, row, column, N,successor_pikachu):
    # cases in which we are moving right
    # one step is empty  
    if column <= N-1 and current_state[row][column + 1]==".":
            new_state = copy.deepcopy(current_state)
            new_state[row][column + 1] = 'B'
            new_state[row][column] = '.'
            successor_pikachu.append(new_state)
        
    if column <= N-2:
         # considering when 2 steps are empty on the right and we jump 2 steps right 
        if current_state[row][column + 1]=="." and current_state[row][column + 2]=="."  :                                     
            new_state = copy.deepcopy(current_state)
            new_state[row][column + 2] = 'B'
            new_state[row][column] = '.'
            successor_pikachu.append(new_state)
        
        # now considering first step in right empty and another is full and another empty step after that
        if current_state[row][column + 1]=="." and (current_state[row][column + 2] in ["w","W","b","B"]) : 
            if current_state[row][column + 2]=="w" or current_state[row][column + 2]=="W":
                if column <= N-3 and new_state[row][column + 3]==".":
                    new_state = copy.deepcopy(current_state)
                    new_state[row][column + 3] = 'B'
                    new_state[row][column + 2] = '.'
                    new_state[row][column] = '.'
                    successor_pikachu.append(new_state)
        
        # now considering first step full and another is empty 
        if (current_state[row][column + 1] in ["w","W","b","B"]) and current_state[row][column + 2]=="." : 
            if current_state[row][column + 1]=="w" or current_state[row][column + 1]=="W":
                new_state = copy.deepcopy(current_state)
                new_state[row][column + 2] = 'B' 
                new_state[row][column] = '.'
                new_state[row][column + 1] = '.' 
                successor_pikachu.append(new_state)
        
        # considering first step full and then 2 steps are empty
        if column <= N - 3 and (current_state[row][column + 1] in ["w","W","b","B"]) and current_state[row][column + 2]=="." and current_state[row][column + 3]=="." : 
            if current_state[row][column + 1]=="w" or current_state[row][column + 1]=="W":
                new_state = copy.deepcopy(current_state)
                new_state[row][column + 3] = 'B' 
                new_state[row][column + 1] = '.'
                new_state[row][column] = '.'
                successor_pikachu.append(new_state)   


# Generating all the successors of pikachu
def pikachu(current_state, player):
    successor_pikachu=[]
    N = len(current_state)-1
    if player == "w": # if the current player is white 
        for row in range(N):
               for column in range(len(current_state[0])):
                    if current_state[row][column] == 'W': 
                        white_pikachu_down(current_state, row, column, N, successor_pikachu)
                        white_pikachu_left(current_state, row, column, N, successor_pikachu)
                        white_pikachu_right(current_state, row, column, N, successor_pikachu)

    else: #covered all the cases of black pikachu
         if player == "b": # all the moves if the current player is Black 
            for row in range(len(current_state)):
               for column in range(len(current_state[0])):
                    if current_state[row][column] == 'B': 
                        black_pikachu_up(current_state, row, column, N, successor_pikachu)
                        black_pikachu_left(current_state, row, column, N, successor_pikachu)
                        black_pikachu_right(current_state, row, column, N, successor_pikachu)   
                        
    return successor_pikachu                            

# Generating all the successors of raichu
# -------------------------------- White Raichu ---> Below --------------------------------------------------
def white_raichu_below(current_state, row, column, N, successor_raichu):
    # Initialize variables to keep track of the opponent, opponent's position, and captured piece's position
    opponent = 0
    row_value = 0
    col_value = 0
    # Generate successor states for Raichu moving below the current position
    for i in range(row + 1, len(current_state)):
        # If we find the same player's piece, stop searching in this direction 
        if current_state[i][column] in ['w', 'W', '@'] :
            break
        # If we find an opponent's piece, save its position and continue searching
        # If we have already found an opponent's piece and encounter another one, stop (Raichu can capture one opponent per move)
        if current_state[i][column] in ['b','B','$']:
            if opponent == 0:
                opponent = 1  
                row_value = i
                col_value = column
                continue
            else: break
        # If an empty location is found, generate a new state for Raichu's move
        # If an empty location is found after capturing an opponent's piece, remove the opponent's piece from the board
        if current_state[i][column]==".":
            new_state = copy.deepcopy(current_state)
            new_state[i][column] = '@'
            new_state[row][column] = '.'
            if opponent == 1:
                new_state[row_value][col_value] = "."
            successor_raichu.append(new_state)
                        
# -------------------------------- White Raichu ---> Above --------------------------------------------------                      
def white_raichu_above(current_state, row, column, N, successor_raichu):
    opponent = 0
    row_value = 0
    col_value = 0
    for i in range(row - 1, -1, -1):
        if current_state[i][column] in ['w', 'W', '@']:
            break
        if current_state[i][column] in ['b','B','$']:  
            if opponent==0:
                opponent=1  
                row_value=i
                col_value=column
                continue
            else: break
        if current_state[i][column]==".":
            new_state = copy.deepcopy(current_state)
            new_state[i][column] = '@'
            new_state[row][column] = '.'
            if opponent==1:
                new_state[row_value][col_value]="."
            successor_raichu.append(new_state)
                        
# -------------------------------- White Raichu ---> Right --------------------------------------------------
def white_raichu_right(current_state, row, column, N, successor_raichu):
    opponent = 0
    row_value = 0
    col_value = 0
    for i in range(column + 1, len(current_state[0])):
        if current_state[row][i] in ['w', 'W', '@']:
            break
        if current_state[row][i] in ['b','B','$']:  
            if opponent == 0:
                opponent = 1  
                row_value = row
                col_value = i
                continue
            else: break
        if current_state[row][i]==".":
            new_state = copy.deepcopy(current_state)
            new_state[row][i] = '@'
            new_state[row][column] = '.'
            if opponent==1:
                new_state[row_value][col_value]="."
            successor_raichu.append(new_state)
                        
# -------------------------------- White Raichu ---> Left --------------------------------------------------
def white_raichu_left(current_state, row, column, N, successor_raichu):
    opponent = 0
    row_value = 0
    col_value = 0   
    for i in range(column - 1, -1, -1):
        if current_state[row][i] in ['w', 'W', '@']:
            break
        if current_state[row][i] in ['b','B','$'] :  
            if opponent == 0:
                opponent = 1  
                row_value = row
                col_value = i
                continue
            else: 
                break
        if current_state[row][i]==".":
            new_state = copy.deepcopy(current_state)
            new_state[row][i] = '@'
            new_state[row][column] = '.'
            if opponent == 1:
                new_state[row_value][col_value]="."
            successor_raichu.append(new_state)
                        
# -------------------------------- White Raichu ---> Positive Diagonal --------------------------------------------------
def white_raichu_pos_diag(current_state, row, column, N, successor_raichu):
    row_up_val = row
    col_up_val = column
    opponent = 0
    row_value = 0
    col_value = 0   
    while (row_up_val - 1 in range(0, len(current_state))) and (col_up_val + 1 in range(0, len(current_state[0]))):
        row_up_val -= 1
        col_up_val += 1
        if current_state[row_up_val][col_up_val] in ['w', 'W', '@'] :
            break
        if current_state[row_up_val][col_up_val] in ['b','B','$']:  
            if opponent==0:
                opponent=1  
                row_value=row_up_val
                col_value=col_up_val
                continue
            else: break
        if current_state[row_up_val][col_up_val]==".":
            new_state = copy.deepcopy(current_state)
            new_state[row_up_val][col_up_val] = '@'
            new_state[row][column] = '.'
            if opponent==1:
                new_state[row_value][col_value]="."
            successor_raichu.append(new_state)
                                
    # Lower half negetive diagonal
    row_up_val = row
    col_up_val = column
    opponent = 0
    row_value = 0
    col_value = 0   
    while (row_up_val+1 in range(0, len(current_state))) and (col_up_val - 1 in range(0, len(current_state[0]))):
        row_up_val += 1
        col_up_val -= 1
        if current_state[row_up_val][col_up_val] in ['w', 'W', '@']:
            break
        if current_state[row_up_val][col_up_val] in ['b','B','$']:  
            if opponent == 0:
                opponent = 1  
                row_value = row_up_val
                col_value = col_up_val
                continue
            else: 
                break
        if current_state[row_up_val][col_up_val] == ".":
            new_state = copy.deepcopy(current_state)
            new_state[row_up_val][col_up_val] = '@'
            new_state[row][column] = '.'
            if opponent==1:
                new_state[row_value][col_value]="."
            successor_raichu.append(new_state)
                        
# -------------------------------- White Raichu ---> Positive Diagonal --------------------------------------------------
def white_raichu_neg_diag(current_state, row, column, N, successor_raichu):
 # Upper half negetive diagonal
    row_up_val = row
    col_up_val = column
    opponent = 0
    row_value = 0
    col_value = 0   
    while (row_up_val - 1 in range(0, len(current_state))) and (col_up_val - 1 in range(0, len(current_state[0]))):
        row_up_val -= 1
        col_up_val -= 1
        if current_state[row_up_val][col_up_val] in ['w', 'W', '@']:
            break
        if current_state[row_up_val][col_up_val] in ['b','B','$']: 
            if opponent==0:
                opponent=1  
                row_value=row_up_val
                col_value=col_up_val
                continue
            else: break
        if current_state[row_up_val][col_up_val]==".":
            new_state = copy.deepcopy(current_state)
            new_state[row_up_val][col_up_val] = '@'
            new_state[row][column] = '.'
            if opponent==1:
                new_state[row_value][col_value]="."
            successor_raichu.append(new_state)
                                
# Lower half negative diagonal traversal
    row_up_val = row
    col_up_val = column
    opponent = 0
    row_value = 0
    col_value = 0   
    while (row_up_val + 1 in range(0, len(current_state))) and (col_up_val + 1 in range(0, len(current_state[0]))):
        row_up_val += 1
        col_up_val += 1
        if current_state[row_up_val][col_up_val] in ['w', 'W', '@']:
            break
        if current_state[row_up_val][col_up_val] in ['b','B','$']:  
            if opponent == 0:
                opponent = 1  
                row_value = row_up_val
                col_value = col_up_val
                continue
            else: 
                break
        if current_state[row_up_val][col_up_val]==".":
            new_state = copy.deepcopy(current_state)
            new_state[row_up_val][col_up_val] = '@'
            new_state[row][column] = '.'
            if opponent==1:
                new_state[row_value][col_value]="."
            successor_raichu.append(new_state)
    
# -------------------------------- Black Raichu ---> Below --------------------------------------------------
def black_raichu_below(current_state, row, column, N, successor_raichu):
    opponent = 0
    row_value = 0
    col_value = 0
    # for rs that are below the current current_stateition
    for i in range(row + 1, len(current_state)):
        if current_state[i][column] in ['b','B','$']:
            break
        if current_state[i][column] in ['w', 'W', '@']:
            if opponent == 0:
                opponent = 1  
                row_value = i
                col_value = column
                continue
            else: 
                break
        if current_state[i][column] == ".":
            new_state = copy.deepcopy(current_state)
            new_state[i][column] = '$'
            new_state[row][column] = '.'
            if opponent==1:
                new_state[row_value][col_value]="."
            successor_raichu.append(new_state)
                        
# -------------------------------- Black Raichu ---> Above --------------------------------------------------
def black_raichu_above(current_state, row, column, N, successor_raichu):
    opponent = 0
    row_value = 0
    col_value = 0
    for i in range(row - 1, -1, -1):
        if current_state[i][column] in ['b','B','$']:
            break
        if current_state[i][column] in ['w', 'W', '@']:  
            if opponent == 0:
                opponent = 1  
                row_value = i
                col_value = column
                continue
            else: 
                break
        if current_state[i][column] == ".":
            new_state = copy.deepcopy(current_state)
            new_state[i][column] = '$'
            new_state[row][column] = '.'
            if opponent==1:
                new_state[row_value][col_value]="."
            successor_raichu.append(new_state)

# -------------------------------- Black Raichu ---> Right --------------------------------------------------   
def black_raichu_right(current_state, row, column, N, successor_raichu):
    for i in range(column + 1, len(current_state[0])):
        if current_state[row][i] == '.':
            # Check if all squares between the start and end are empty
            all_empty = all(current_state[row][j] == '.' for j in range(column + 1, i))
            if all_empty:
                new_state = copy.deepcopy(current_state)
                new_state[row][i] = '$'  # Move "Black_raichu" to the right
                new_state[row][column] = '.'  # Remove "Black_raichu" from the current cell
                successor_raichu.append(new_state)
        elif current_state[row][i] in ['w', 'W', '@']:
            # Check if there's a piece of the opposite color to jump over
            if i + 1 < N and current_state[row][i + 1] == '.':
                # Check if there are no blocking items between "$" and "W"
                has_blocking_item = any(current_state[row][j] in ['b', 'B', '$'] for j in range(column + 1, i))
                if not has_blocking_item:
                    new_state = copy.deepcopy(current_state)
                    new_state[row][i + 1] = '$'  # Move "Black_raichu" to the right
                    new_state[row][column] = '.'  # Remove "Black_raichu" from the current cell
                    # Remove the captured piece
                    new_state[row][i] = '.'
                    successor_raichu.append(new_state)
                break  # Break the loop since no more jumping can occur in this direction
            else:
                break  # Break the loop if there's a blocking piece

# -------------------------------- Black Raichu ---> Left --------------------------------------------------   
def black_raichu_left(current_state, row, column, N, successor_raichu):
    for i in range(column - 1, -1, -1):
        if current_state[row][i] == '.':
            # Check if all squares between the start and end are empty
            all_empty = all(current_state[row][j] == '.' for j in range(i + 1, column))
            if all_empty:
                new_state = copy.deepcopy(current_state)
                new_state[row][i] = '$'  # Move "Black_raichu" to the right
                new_state[row][column] = '.'  # Remove "Black_raichu" from the current cell
                successor_raichu.append(new_state)
        elif current_state[row][i] in ['w', 'W', '@']:
            # Check if there's a piece of the opposite color to jump over
            if i - 1 >=0 and current_state[row][i - 1] == '.':
                # Check if there are no blocking items between "$" and "W"
                has_blocking_item = any(current_state[row][j] in ['b', 'B', '$'] for j in range(i + 1, column))
                if not has_blocking_item:
                    new_state = copy.deepcopy(current_state)
                    new_state[row][i - 1] = '$'  # Move "Black_raichu" to the right
                    new_state[row][column] = '.'  # Remove "Black_raichu" from the current cell
                    # Remove the captured piece
                    new_state[row][i] = '.'
                    successor_raichu.append(new_state)
                break  # Break the loop since no more jumping can occur in this direction
            else:
                break  # Break the loop if there's a blocking piece

# -------------------------------- Black Raichu ---> Positive Diagonal --------------------------------------------------                        
def black_raichu_pos_diag(current_state, row, column, N, successor_raichu):
    # Positive half of the upper diagonal states
    # Initialize variables to keep track of the position, opponent, and capture information
    row_up_val = row
    col_up_val = column
    opponent = 0
    row_value = 0
    col_value = 0   
    # Loop to traverse the positive half of the upper diagonal
    while (row_up_val - 1 in range(0, len(current_state))) and (col_up_val + 1 in range(0, len(current_state[0]))):
        row_up_val -= 1
        col_up_val += 1
        # Check if there's an opponent piece in the diagonal
        if current_state[row_up_val][col_up_val] in ['b','B','$'] :
            break
        # Check if there's a white piece in the diagonal
        if current_state[row_up_val][col_up_val] in ['w', 'W', '@']:  
            if opponent==0:
                opponent=1  
                row_value=row_up_val
                col_value=col_up_val
                continue
            else: 
                break
        # Check if the position is empty (no piece)
        if current_state[row_up_val][col_up_val]==".":
            # Create a new state with the Raichu moving to this empty position and update the board
            new_state = copy.deepcopy(current_state)
            new_state[row_up_val][col_up_val] = '$'
            new_state[row][column] = '.'
            # If there was an opponent piece, remove it from the board
            if opponent==1:
                new_state[row_value][col_value]="."
            # Add the new state to the list of successor positions
            successor_raichu.append(new_state)
            
    # For states lower half diagonal
    row_up_val = row
    col_up_val = column
    opponent = 0
    row_value = 0
    col_value = 0  
    # Loop to traverse the lower half of the diagonal 
    while (row_up_val + 1 in range(0, len(current_state))) and (col_up_val - 1 in range(0, len(current_state[0]))):
        row_up_val += 1
        col_up_val -= 1
        # Check if there's an opponent piece in the diagonal
        if current_state[row_up_val][col_up_val] in ['b','B','$'] :
            break
        # Check if there's a white piece in the diagonal
        if current_state[row_up_val][col_up_val] in ['w', 'W', '@']:  
            if opponent == 0:
                opponent = 1  
                row_value = row_up_val
                col_value = col_up_val
                continue
            else: 
                break
        # Check if the position is empty (no piece)
        if current_state[row_up_val][col_up_val]==".":
            # Create a new state with the Raichu moving to this empty position and update the board
            new_state = copy.deepcopy(current_state)
            new_state[row_up_val][col_up_val] = '$'
            new_state[row][column] = '.'
            # If there was an opponent piece, remove it from the board
            if opponent==1:
                new_state[row_value][col_value]="."
            # Add the new state to the list of successor positions
            successor_raichu.append(new_state)

    # Upper half negetive diagonal traversal
    row_up_val = row
    col_up_val = column
    opponent = 0
    row_value = 0
    col_value = 0   
    # Loop to traverse the upper half of the negative diagonal
    while (row_up_val - 1 in range(0, len(current_state))) and (col_up_val - 1 in range(0, len(current_state[0]))):
        row_up_val -= 1
        col_up_val -= 1
        # Check if there's an opponent piece in the diagonal
        if current_state[row_up_val][col_up_val] in ['b','B','$']:
            break
        # Check if there's a white piece in the diagonal
        if current_state[row_up_val][col_up_val] in ['w', 'W', '@']:  
            if opponent == 0:
                opponent = 1  
                row_value = row_up_val
                col_value = col_up_val
                continue
            else: 
                break
        # Check if the position is empty (no piece)
        if current_state[row_up_val][col_up_val]==".":
            # Create a new state with the Raichu moving to this empty position and update the board
            new_state = copy.deepcopy(current_state)
            new_state[row_up_val][col_up_val] = '$'
            new_state[row][column] = '.'
            # If there was an opponent piece, remove it from the board
            if opponent == 1:
                new_state[row_value][col_value]="."
            # Add the new state to the list of successor positions
            successor_raichu.append(new_state)
                                
 # -------------------------------- Black Raichu ---> Negative Diagonal --------------------------------------------------
def black_raichu_neg_diag(current_state, row, column, N, successor_raichu):
    # Lower half diagonal traversal
    # Initialize variables to keep track of the position, opponent, and capture information
    row_up_val = row
    col_up_val = column
    opponent = 0
    row_value = 0
    col_value = 0   
    # Loop to traverse the lower half of the diagonal
    while (row_up_val + 1 in range(0, len(current_state))) and (col_up_val + 1 in range(0, len(current_state[0]))):
        row_up_val += 1
        col_up_val += 1
        # Check if there's an opponent piece in the diagonal
        if current_state[row_up_val][col_up_val] in ['b','B','$']:
            break
        # Check if there's a white piece in the diagonal
        if current_state[row_up_val][col_up_val] in ['w', 'W', '@']:  
            if opponent==0:
                opponent=1  
                row_value=row_up_val
                col_value=col_up_val
                continue
            else: 
                break
        # Check if the position is empty (no piece)
        if current_state[row_up_val][col_up_val]==".":
            # Create a new state with the Raichu moving to this empty position and update the board
            new_state = copy.deepcopy(current_state)
            new_state[row_up_val][col_up_val] = '$'
            new_state[row][column] = '.'
            # If there was an opponent piece, remove it from the board
            if opponent == 1:
                new_state[row_value][col_value] = "."
            # Add the new state to the list of successor positions
            successor_raichu.append(new_state)   

# -------------------------------------- Defining Raichu states ------------------------------------------- 
def raichu(current_state, player):
    # Initialize a list to store successor positions for Raichu
    successor_raichu=[]
    if player == "w": # If the current player is white 
        for row in range(len(current_state)):
               for column in range(len(current_state[0])):
                    if current_state[row][column] == '@': # If there is a white Raichu in this position
                        # Generate successor positions for white Raichu
                       white_raichu_below(current_state, row, column, N, successor_raichu) 
                       white_raichu_above(current_state, row, column, N, successor_raichu)
                       white_raichu_right(current_state, row, column, N, successor_raichu)
                       white_raichu_left(current_state, row, column, N, successor_raichu)
                       white_raichu_pos_diag(current_state, row, column, N, successor_raichu)
                       white_raichu_neg_diag(current_state, row, column, N, successor_raichu)

    if player == "b": # If the current player is black
        for row in range(len(current_state)):
               for column in range(len(current_state[0])):
                    if current_state[row][column] == '$': # If there is a black Raichu in this position
                        # Generate successor positions for black Raichu
                        black_raichu_below(current_state, row, column, N, successor_raichu)
                        black_raichu_above(current_state, row, column, N, successor_raichu)
                        black_raichu_right(current_state, row, column, N, successor_raichu)
                        black_raichu_left(current_state, row, column, N, successor_raichu)
                        black_raichu_pos_diag(current_state, row, column, N, successor_raichu)
                        black_raichu_neg_diag(current_state, row, column, N, successor_raichu)

    return  successor_raichu

# ---------------- Creating a comprehensive list of successors and their corresponding evaluation function values ----------------
def successor_evaluation_list(current_position, player_color):
    # Initialize an empty list to store the successors
    successors = [] 
    # Determine the player's color and generate possible successor positions
    if player_color == 'w':
        steps_pichu = pichu(current_position, 'w')
        steps_pikachu = pikachu(current_position, 'w')
        steps_raichu = raichu(current_position, 'w')

        # For each successor position, calculate its evaluation using the evaluation function and add it to the list
        for i in steps_pichu:
            successors.append([evaluation_function(i,'w', N), i])
        for i in steps_pikachu:
            successors.append([evaluation_function(i,'w', N), i])
        for i in steps_raichu:
            successors.append([evaluation_function(i,'w', N), i])

    else:
        steps_pichu = pichu(current_position, 'b')
        steps_pikachu = pikachu(current_position, 'b')
        steps_raichu = raichu(current_position, 'b')
        # For each successor position, calculate its evaluation using the evaluation function and add it to the list
        for i in steps_pichu:
            successors.append([evaluation_function(i,'b', N), i])
        for i in steps_pikachu:
            successors.append([evaluation_function(i,'b', N), i])
        for i in steps_raichu:
            successors.append([evaluation_function(i,'b', N), i])
    # Sort the successors in descending order of their evaluation scores
    sorted_successors = sorted(successors, reverse= True)
    return sorted_successors

# ------------------- Evaluation Function ------------------------------------------------------------------------------------------------
def evaluation_function(current_position, player, N):
    # Initialize counters for different pieces
    black_pichu = 0
    black_pikachu = 0
    black_raichu = 0
    white_pichu = 0
    white_pikachu = 0
    white_raichu = 0
    # Count the number of each piece type for both players
    for piece in current_position:
        # Pichu counts
        black_pichu += piece.count('b')
        white_pichu += piece.count('w')

        # Pikachu counts
        black_pikachu += piece.count('B')
        white_pikachu += piece.count('W')

        # Raichu counts
        black_raichu += piece.count('$')
        white_raichu += piece.count('@')
    
    # Calculate the total number of possible moves
    number_moves = (N-1)*(N-1)*(N-1)
    
    if player=='w':    
        # Evaluate the position for the white player
        evaluated_value = number_moves * (white_raichu - black_raichu) + 9 * (white_pikachu - black_pikachu)+ 2 * (white_pichu - black_pichu)
        evaluated_value += 0.1 * ((all_moves(current_position,'w') - all_moves(current_position,'b')))
        return evaluated_value
    else:
        # Evaluate the position for the black player
        evaluated_value = number_moves * (black_raichu - white_raichu)+ 9 * (black_pikachu - white_pikachu)+ 2 * (black_pichu - white_pichu)
        evaluated_value += 0.1 * ((all_moves(current_position,'b') - all_moves(current_position,'w'))) 
        return evaluated_value
    
# ---------------------------- Retrieve the count of remaining Pichus and Pikachus ---------------------------
def all_moves(current_pos, player):
    return len(pichu(current_pos,player)) + len(pikachu(current_pos,player))

# Converting the board back to string
def board_to_string(board, N):
    string = ''
    for i in range(0, len(board)):
        for j in board[i][0:N]:
            string += j
    return string

# ------------------------------------- Checking if there is a winner ----------------------------------------
def final_state(current_board):
    # Convert the game board to a string for easier processing
    stringBoard=board_to_string(current_board, N)
    # Define lists of pieces for black and white players
    black_pieces = ["b", "B", "$"]
    white_pieces = ["w", "W", "@"]
    # Check if no black pieces or no white pieces remain on the board
    if any(piece in black_pieces for piece in stringBoard) == False or any(piece in white_pieces for piece in stringBoard) == False:
        # If either player has no pieces left, it's a final state
        return True
    
    elif any(piece in black_pieces[:1] for piece in stringBoard) == False or any(piece in white_pieces[:1] for piece in stringBoard) == False:
        return True
    return False
    
start_time = time.time()

# ----------------------------------------- Max Value of States ----------------------------------------------
def max_value(current_board, player_color, depth, start_time, timelimit):
    N = len(current_board)
    # Check termination conditions: final state, depth limit, or time limit reached
    if final_state(current_board) or depth > 5 or (time.time() - start_time) >= timelimit:
        return evaluation_function(current_board, player_color, N)
    # Initialize the maximum evaluation to negative infinity
    max_eval = float('-inf')

    # Iterate through the successor states and find the maximum evaluation
    for state in successor_evaluation_list(current_board, player_color):
        max_eval = max(max_eval, min_value(state[1], player_color, depth + 1, start_time, timelimit))
    
    return max_eval

# ------------------------------------------ Min Value of States ------------------------------------------------
def min_value(current_board, player_color, depth, start_time, timelimit):
    N = len(current_board)
    # Switch player's color for the next level of the tree (minimizing player becomes maximizing player and vice versa)
    if player_color == 'b':
        player_color = 'w'
    else:
        player_color = 'b'

    # Check termination conditions: final state, depth limit, or time limit reached
    if final_state(current_board) or depth > 5 or (time.time() - start_time) >= timelimit:
        return evaluation_function(current_board, player_color, N)

    # Initialize the minimum evaluation to positive infinity
    min_eval = float('inf')

    # Iterate through the successor states and find the minimum evaluation
    for state in successor_evaluation_list(current_board, player_color):
        min_eval = min(min_eval, max_value(state[1], player_color, depth + 1, start_time, timelimit))
    
    return min_eval

# -------------------------------------------- MiniMax Algorithm ---------------------------------------------------
def minimax_algorithm(board_state, player_color):
    successor = successor_evaluation_list(board_state, player_color)
    max_val = -float('inf')  # Initialize max_val with negative infinity
    max_action = None

    # Sort successor states based on your evaluation function
    successor.sort(key=lambda state: evaluation_function(state[1], player_color, len(board_state)), reverse=True)

    for state in successor:
        value = max_value(state[1], player_color, 0, start_time, timelimit - 0.5)
        if value > max_val:
            max_val = value
            max_action = state[1]

    return max_action

# ------------------------------ Finding Best Move -----------------------------------------------------------------
def find_best_move(board, N, player, timelimit):
    board_mat = string_to_board(board,N)
    minimax_ans = minimax_algorithm(board_mat, player)
    return [board_to_string(minimax_ans,N)]

# ----------------------------- Main Function ------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))

    start_time = time.time()  # Record the start time
    best_moves = find_best_move(board, N, player, timelimit)
    end_time = time.time()  # Record the end time

    print("Time taken:", end_time - start_time, "seconds")
    print("Here's what I decided:")
    for new_board in best_moves:
        print(new_board)
    # print("Here's what I decided:")
    # for new_board in find_best_move(board, N, player, timelimit):
    #     print(new_board)
