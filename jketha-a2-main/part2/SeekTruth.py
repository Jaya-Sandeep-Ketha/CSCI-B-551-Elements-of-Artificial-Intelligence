# SeekTruth.py : Classify text objects into two categories
#
# Jaya Sandeep, Ketha - jketha
#

import sys
import math

# Define a list of common filler words to remove
filler_words = ["a", "an", "the", "in", "on", "but", "to", "for", "I", "you", "My", "it", "have", "has", "do", "just", "even", "go", "two", "around", "asked", "by", "or", "did",
                "of", "we", "hotel", "that", "were", "with", "this", "had", "they", "but", "as", "there", "would", "so", "are", "one", "if", "like", "will", "about", "which"]

def load_file(filename):
    objects = []
    labels = []
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ', 1)
            labels.append(parsed[0] if len(parsed) > 0 else "")
            text = parsed[1] if len(parsed) > 1 else ""

            # Remove filler words and apply stemming
            text = remove_filler_words(text)
            
            objects.append(text)

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

def remove_filler_words(text):
    # Tokenize the text into words
    words = text.split()
    
    # Remove filler words and apply stemming
    words = [porter_stem(word) for word in words if word.lower() not in filler_words]
    
    # Reconstruct the text without filler words
    text_without_fillers = ' '.join(words)

    return text_without_fillers

def porter_stem(word):
    if word.endswith("ing"):
        word = word[:-3]
    elif word.endswith("ed"):
        word = word[:-2]
    
    return word

def classifier(train_data, test_data):
    # Initialize class counts and word counts
    class_counts = {train_data["classes"][0]: 0, train_data["classes"][1]: 0}
    word_counts = {}

    # Calculate class probabilities
    for label in train_data["labels"]:
        class_counts[label] += 1

    # Calculate word probabilities
    for i in range(len(train_data["objects"])):
        words = train_data["objects"][i].split()
        label = train_data["labels"][i]

        for word in words:
            if word not in word_counts:
                word_counts[word] = {train_data["classes"][0]: 0, train_data["classes"][1]: 0}
            word_counts[word][label] += 1

    # Classify test data
    results = []

    for text in test_data["objects"]:
        words = text.split()
        truth_prob = math.log(class_counts[train_data["classes"][0]] / len(train_data["labels"]))
        decpt_prob = math.log(class_counts[train_data["classes"][1]] / len(train_data["labels"]))

        for word in words:
            if word in word_counts:
                truth_prob += math.log((word_counts[word][train_data["classes"][0]] + 1) / (class_counts[train_data["classes"][0]] + len(word_counts)))
                decpt_prob += math.log((word_counts[word][train_data["classes"][1]] + 1) / (class_counts[train_data["classes"][1]] + len(word_counts)))

        if truth_prob > decpt_prob:
            results.append(train_data["classes"][0])
        else:
            results.append(train_data["classes"][1])

    return results

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    train_data = load_file(train_file)
    test_data = load_file(test_file)

    if sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2:
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}
    results = classifier(train_data, test_data_sanitized)

    correct_ct = sum([results[i] == test_data["labels"][i] for i in range(0, len(test_data["labels"]))])
    accuracy = 100.0 * correct_ct / len(test_data["labels"])
    print("Classification accuracy = %5.2f%%" % accuracy)
