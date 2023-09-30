# a0-release
## Question 1: Shortest path in a castle.
### Overview
This report is a summary of the Python program "mystical_castle.py," developed to navigate a castle provided through a text file. The program searches the castle using the **Breadth-First Search (BFS) algorithm** to discover the shortest route from a starting point indicated with the letter "p" to a magical portal (exit) marked with the symbol "@." The shortest path length and the series of steps needed to exit are then printed by the program.

## Program Structure
The `mystical_castle.py` program is structured as follows:

1. **Parsing the Map**: The program first reads the castle map from a text file given as a command-line parameter. It reads the castle layout, excluding the first three lines, and stores it as a 2D list.

2. **Validating Indices**: It defines a `valid_index` function to check if a given row and column index pair is within the bounds of the castle.

3. **Finding Possible Moves**: The `moves` function computes potential moves from a given position (row, col). It analyzes movements in four directions (up, down, left, and right) and only returns those inside the castle and through open areas ('.').

4. **Getting Direction**: The `get_direction` function compares the row and column coordinates of two locations to determine the direction of travel between them. It returns 'U' for upward, 'R' for right, 'D' for downward, 'L' for left, and an empty string for incorrect movements.

5. **Search Algorithm**: The `search` function uses the BFS algorithm to navigate the castle. It moves through the castle while keeping track of the distance traveled and the order of its movements. It begins at point 'p'. It keeps going until either the exit '@' is discovered or all options have been explored.

6. **Main Function**: The program's `main` section reads the castle from the provided file, starts the search, and prints the solution, along with the length of the shortest path and the order of the steps.

## Assumptions and Design Decisions
1. The program assumes that the castle is a grid with walls (represented by "#") or open spaces (represented by ".") in each cell. The goal to be located is marked with a "@," while the beginning position is marked with a "p."

2. It assumes that the castle has a single beginning point ('p') and a single goal ('@').

3. Diagonal movements are not taken into account by the program. Only movement in the four directions—up, down, left, and right—is permitted.

4. To determine the shortest path, the algorithm employs BFS. While this ensures that the shortest path will be found, it might not be the most time-effective strategy for big castles. However, BFS was selected due to its ease of use and assurance of accuracy.

## Innovative Aspects
The program solves castles using a conventional BFS methodology. However, the 'get_direction' function, is one interesting feature. It is developed to ascertain the direction of movement between two sites. This function makes it easier to keep track of movement patterns and helps construct the solution string.

## Challenges Faced
One challenge faced during the implementation was ensuring that the BFS algorithm correctly explored all possible paths while avoiding infinite loops. This was achieved by tracking visited positions in the `visited` set to prevent revisiting the same position.

## Conclusion
The `mystical_castle.py` program effectively solves castle puzzles using BFS, finding the shortest path from the starting position 'p' to the magical portal '@.' It adheres to the specified assumptions and design decisions while providing a clear and concise solution to the problem.

---

# Question 2: Turret Placement

## Overview
The `place_turrets.py` program is developed to solve the turret placement problem in a castle. The objective is to arrange a predetermined number of turrets in the castle so that none of them can engage in combat with one another. The program employs a backtracking approach to investigate potential turret placements and identify a viable solution, if any.

## Program Structure

1. **Parsing the Map**: The `parse_map` function reads the initial castle layout from a text file given as a command-line parameter. The castle contains empty spaces ('.'), walls ('#'), and initially placed turrets ('p').

2. **Counting Turrets**:  The `count_turrets` function counts the total number of turrets that have already been installed in the castle.

3. **Rendering the castle layout**: The `printable_castle_map` function transforms the castle layout for display in an easy-to-read format.

4. **Adding a Turret**: The `add_turret` function adds a turret to the current castle map at the specified position by taking the current castle map, row, and column as input.

5. **Generating Successors**:  The `successors` function creates a list of successor castle states by taking into account all potential locations to place turrets while making sure the placement requirements are satisfied.

6. **Goal State Check**: The `is_goal` function checks if the current castle configuration contains the required number of turrets without any conflicts.

7. **Condition Check**: The `check_conditions` function verifies if the placement of turrets adheres to the rules, ensuring that no turret can attack another. It checks rows, columns, and diagonals for potential conflicts.

8. **Solving the Problem**: The `solve` function initiates the backtracking search. It starts with the initial castle layout and iteratively explores successor states. If a valid solution is found, it returns the solution castle map/layout; otherwise, it returns "False."

9. **Main Function**: The program's `main` section reads the starting castle layout and the required number of turrets from the command-line inputs. After printing the initial castle layout and starting the search, it either prints the solution or "False" if there isn't one.

## Assumptions and Design Decisions
1. The program assumes that the input castle layout is a grid where each cell can be one of three types: empty space ('.'), wall ('#'), or a turret ('p').

2. It is assumed that the objective is to set up a certain number of turrets in the castle while preventing any two turrets from engaging in horizontal, vertical, or diagonal combat with one another.

3. The program uses the `check_conditions` function to make sure that no turrets can attack one another. It analyzes conflicts in terms of rows, columns, and both positive and negative diagonals.

4. The program uses a backtracking approach to explore possible turret placements. It incrementally adds turrets and checks the placement conditions. If a conflict is detected, it backtracks and explores other possibilities.

## Innovative Aspects
The program's implementation of the `check_conditions` function, which effectively checks for turret conflicts in rows, columns, and diagonals, is what makes it interesting and innovative. This function makes sure that the turret placement complies with the rules of the problem.

## Challenges Faced
Checking for diagonal conflicts in an efficient manner was one of the main implementation challenges. Careful indexing and management of diagonal checks were needed to guarantee accuracy and effectiveness.

## Conclusion
The backtracking approach used by the `place_turrets.py` program allows it to successfully solve the turret placement problem. It effectively checks for conflicts to provide a viable solution while adhering to the defined assumptions and design choices.
