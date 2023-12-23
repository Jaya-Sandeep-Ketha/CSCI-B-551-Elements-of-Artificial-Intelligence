#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: Jaya Sandeep Ketha: jketha
# (Based on skeleton code by D. Crandall)
# References: https://www.ijrte.org/wp-content/uploads/papers/v7i4s2/Es2046017519.pdf
#             https://github.com/ssghule/Optical-Character-Recognition-using-Hidden-Markov-Models/tree/master
#             https://medium.com/@phylypo/nlp-text-segmentation-using-hidden-markov-model-f238743d87eb

from PIL import Image
import sys
import math
import numpy as np

CHARACTER_WIDTH = 14
CHARACTER_HEIGHT = 25
TRAIN_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
NUM_STATES = len(TRAIN_LETTERS)

def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    print(im.size)
    print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

#####
# main program
def calculate_initial_transition_probabilities(words_file_name):
    # Initialize initial probabilities and transition probabilities
    with open(words_file_name, 'r') as training_words:
        init_prob = {ch: 0 for ch in TRAIN_LETTERS} # Dictionary to store initial probabilities
        trans_prob = np.zeros(shape=(NUM_STATES, NUM_STATES)) # Matrix to store transition probabilities
        words = ''.join(training_words.readlines()) # Read all words from the file and concatenate
        
        # Calculate total number of words in the training set
        total_words = len(words.split())
        # Calculate initial probabilities for each letter in TRAIN_LETTERS
        for letter in TRAIN_LETTERS:
            # Add Laplace smoothing and calculate log probabilities for initial occurrences of each letter
            init_prob[letter] = math.log((words.count(letter) + 1) / (total_words + 2))

        # Calculate transition probabilities between consecutive letters
        for i in range(len(words) - 1):
            if words[i] in TRAIN_LETTERS and words[i+1] in TRAIN_LETTERS:
                # Increment transition count for the corresponding letter pair
                trans_prob[TRAIN_LETTERS.index(words[i]), TRAIN_LETTERS.index(words[i+1])] += 1

         # Calculate log probabilities for transition probabilities using Laplace smoothing
        for row in trans_prob:
            total = sum(row) # Calculate total occurrences for each row (current state)
            if total > 0:
                # Add Laplace smoothing and calculate log probabilities for each transition
                row[:] = [math.log((r + 1) / (total + 2)) for r in row]
        
        return init_prob, trans_prob  # Return the calculated initial and transition probabilities

def calculate_emission_probabilities(train_letters, test_letters):
    # Initialize emission_probabilities matrix
    emission_prob = np.zeros(shape=(NUM_STATES, len(test_letters)))
    # Iterate through each character in the training set
    for train_char, train_img in train_letters.items():
        # Compare the training image with each test image
        for j, test_img in enumerate(test_letters):
            hit = sum(train_img[y][x] == test_img[y][x] for x in range(CHARACTER_WIDTH) for y in range(CHARACTER_HEIGHT))
            miss = CHARACTER_WIDTH * CHARACTER_HEIGHT - hit

            # Calculate the probabilities for hit and miss events
            hit_prob = hit / (hit + miss)
            miss_prob = 1 - hit_prob

            # Calculate emission probability using the probabilities of hit and miss events
            prob = (hit_prob ** hit) * (miss_prob ** miss)
            # Handle edge case where prob is zero to avoid math domain errors
            emission_prob[TRAIN_LETTERS.index(train_char)][j] = math.log(10**(-6)) if prob == 0 else math.log(prob)
    return emission_prob

def simple_character_recognition(test_letters, emission_prob):
    # Get the indices of maximum probabilities for each column in emission_prob
    indices = np.argmax(emission_prob, axis=0)
    # Map the indices to corresponding letters in TRAIN_LETTERS and join them to form the recognized string
    return ''.join(TRAIN_LETTERS[i] for i in indices)

def hmm_character_recognition(test_letters, init_p, trans_p, emission_p):
    N = len(test_letters)
    Viterbi_matrix = np.zeros(shape=(NUM_STATES, N))
    backpointer_table = np.zeros(shape=(NUM_STATES, N), dtype=int)

    # Initialize Viterbi_matrix and backpointer_table with initial probabilities and emission probabilities
    for s in range(NUM_STATES):
        Viterbi_matrix[s, 0] = init_p[TRAIN_LETTERS[s]] + emission_p[s, 0]

    # Populate the tables using dynamic programming approach
    for i in range(1, N):
        for s in range(NUM_STATES):
            prev_state_scores = Viterbi_matrix[:, i - 1] + trans_p[:, s]  # Calculate scores for transitioning from previous states
            max_index = np.argmax(prev_state_scores)  # Find the index of the maximum score
            max_val = prev_state_scores[max_index]  # Get the maximum score
            Viterbi_matrix[s, i] = max_val + emission_p[s, i]  # Update the score for the current state
            backpointer_table[s, i] = max_index  # Store the index of the state that gave the maximum score

    # Backtrace to find the most likely decoded sequence of states
    decoded_sequence = [np.argmax(Viterbi_matrix[:, -1])]  # Start with the most likely decoded state at the last position

    for i in range(N - 1, 0, -1):
        decoded_sequence.insert(0, backpointer_table[decoded_sequence[0], i])  # Backtrace using the indices from backpointer_table

    return ''.join(TRAIN_LETTERS[i] for i in decoded_sequence)

#######################################################################################
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_chars = load_training_letters(train_img_fname)
test_chars = load_letters(test_img_fname)

init_prob, trans_prob = calculate_initial_transition_probabilities(train_txt_fname)
emission_probabilities = calculate_emission_probabilities(train_chars, test_chars)

simple_result = simple_character_recognition(test_chars, emission_probabilities)
hmm_result = hmm_character_recognition(test_chars, init_prob, trans_prob, emission_probabilities)

print("Simple: " + simple_result)
print("   HMM: " + hmm_result)
