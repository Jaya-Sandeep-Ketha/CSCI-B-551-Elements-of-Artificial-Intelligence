# jketha-a2
## Part 1
## Report on "Raichu.py" 

## Problem Formulation:
The problem can be formulated with given details as to create a AI based strategy board game which contains 3 different types of pieces: Pichu, Pikachu and Raichu. The goal of the AI is to estimate an optimal/best move by considering the future states and improving the chances of winning.

### AI Decision-Making:
The main difficulty lies in making AI understnad the right move for a particular board state to maximize its chances of winning. This can be achieved through MiniMax Algorithm, this analyzes the future states of the game, using an evaluation function which calculates the scores of the moves and then suggests the best move.

### Successor States:
This program generates successor positions for both the players (black and white) for each piece type (Pichu, Pikachu, Raichu).

### Evaluation Function:
Every board position is given a value by an evaluation function that takes into account the kinds and quantities of pieces that each player has, as well as possible moves in the future.

## Program Description:
The program works as follows:

1. It defines various functions to handle different aspects of the game:
  - `string_to_board` function converts a string representation of a game board into a 2D list.
  - `valid_move` function checks if a given row and column are within the boundaries of the board.
The code defines various functions for different types of moves (e.g., `white_pichu_left_diag`, `white_pikachu_down`) for white and black pieces (Pichu, Pikachu and Raichu).
   - These move functions generate successor states by creating copies of the current state and applying the specified moves.
   - `raichu`, `pichu`, `pikachu` generate successor positions for each piece type based on their movement rules.
   - `successor_evaluation_list` calculates the successor positions for the current player and assigns an evaluation values to each of them.
   - `evaluation_function` calculates the evaluation value for a given board position, considering the number and types of pieces.
   - `all_moves` counts the total remaining Pichus and Pikachus for a player.
   - `board_to_string` converts the game board back into a string for easier processing.
   - `final_state` checks for a winning condition based on the state of the game board.

2. The `max_value` and `min_value` functions are used to implement the Minimax algorithm, which maximizes and minimizes players to that extent.

3. The program uses `minimax_algorithm` to determine the best/optimal move. The highest value of the evaluation function for successor states is selected by sorteing them based on the values of evaluation function.

4. `find_best_move` is used to find the best move for a given player within a time limit.

## Challenges Faced:
1. **Complexity:** Implementing a Minimax algorithm for a complex board game has been challenging, especially in this case as there are multiple piece types and many possible moves.

2. **Performance:** AI performance is significantly influenced by the quality of the evaluation function. It was challenging to create an efficient evaluation function. Despite the fact that the ideal evaluation function is still unknown.

3. **Time Limit:** When the search space is large, it was difficult to manage the program's time limit for making decisions.

## Assumptions, Simplifications, and Design Decisions:
1. All of the game's rules, including the movement guidelines for every kind of piece, are assumed to be well-defined in the code.

2. The code employs a weighted linear combination of different factors as the evaluation function. The AI's performance may be enhanced by adjusting the weights and other components in the evaluation function, which is an important decision.

3. In order to avoid endless searches, the code uses depth limits. Since the depth limit of five is hard-coded, a dynamic depth limit adjustment might be taken into consideration if this isn't enough for complicated games.

4. The AI thinking time is controlled by the code using a simple time limit, which might not always result in the optimal move in games with intricate and deep search trees. One could think about using more sophisticated methods like iterative deepening.

Overall, the code serves as a foundation for implementing an AI for the described board game. Further refinement, optimization, and testing are necessary to make it a competitive and reliable game-playing AI.

------------------------------------------------------------------------------------------------------------------------------------------------------
## Part2
## Report on "SeekTruth.py" Text Classification Program

## 1. Problem Formulation:

The problem addressed by the "SeekTruth.py" program is the classification of text objects into two categories based on a training dataset. Specifically, the goals are:

- To build a text classification model that can accurately classify text objects into one of two predefined classes.
- To develop a solution that removes common filler words and applies a basic stemming operation to improve the accuracy of classification.
- To compute and report the accuracy of the classification model.

## 2. Program Description:

The "SeekTruth.py" program is designed to achieve these goals using the following key components and procedures:

### - Data Preprocessing:
  - The program loads training and test data from text files, extracting labels and text objects. During this process, common filler words are removed from the text data, and a basic stemming operation is applied to reduce word variations.

### - Classifier Function:
  - The main classification logic is implemented in the `classifier` function.
  - Class probabilities are calculated based on the training data. Word probabilities are also computed, considering the frequency of words in each class.
  - The classification is performed for each text object in the test data by comparing the log probabilities for both classes.
  - The class with higher log probability is assigned as the predicted class for the text object.
  
### - Accuracy Calculation:
  - The program calculates the accuracy of the classification by comparing the predicted labels with the true labels in the test data.

### - Output:
  - The program reports the classification accuracy as a percentage.

## 3. Discussion of Problems, Assumptions, and Design Decisions:

During the development of "SeekTruth.py," several difficulties were encountered, and various assumptions and design decisions were made. Here is a more detailed discussion of these aspects, including the challenges faced:

### - Assumption of Binary Classification:
  - The program assumes a binary classification problem, where text objects are classified into one of two predefined classes. This assumption is reflected in the code, and the classifier is designed accordingly.

### - Filler Word Removal:
  - One key design decision is to remove common filler words from the text data. While this can improve classification accuracy by reducing noise, the list of filler words used is limited and may not be exhaustive. Further customization of the list may be necessary for specific applications.

### - Stemming:
  - The program applies a basic stemming operation by removing common word suffixes like "ing" and "ed." This is a simplification of the stemming process, and more advanced stemming algorithms could be used for improved accuracy.

### - Smoothing:
  - Laplace smoothing (add-one smoothing) is applied when computing word probabilities. This is a common technique to prevent zero probabilities, but there are other smoothing methods that could be explored for better results.

### - Simplistic Word Probability Calculation:
  - The word probability calculation is based on simple frequency counts. More advanced techniques like TF-IDF or word embeddings could enhance the model's performance. But implementing those rresulted in decreased accuracy.

### - Data Quality and Quantity:
  - The program does not address issues related to data quality, such as handling misspellings or outliers, which can impact classification accuracy. Moreover, the program may not perform well with very limited training data.

### - Hyperparameter Tuning:
  - The program does not offer options for hyperparameter tuning or model selection. The choice of classifier, features, and smoothing techniques are fixed in the code.

In conclusion, "SeekTruth.py" provides a preliminary solution for binary text classification but may not deliver state-of-the-art performance. It serves as a starting point for text classification tasks and can be improved by incorporating more advanced techniques, expanding the list of filler words, and considering additional preprocessing steps and model enhancements.
