###################################
# CS B551 Fall 2023, Assignment #3
#
# Jaya Sandeep Ketha: jketha
# (Based on skeleton code by D. Crandall)

import random
import math

class Solver:
    base_val = 0.0000001234

    prob_emission = {} # Dictionary stores the probabilities of emitting or observing particular words given a specific part-of-speech tag.
    prob_transmission = {} # Dictionary stores the probabilities of transitioning between pairs of adjacent part-of-speech tags within sentences.
    word_tag_count = {} # Dictionary stores the different tags that can be assigned to individual words.
    tag_occurrence_count = {} # Dictionary keeps track of how many times each tag appears in the entire dataset.
    sentence_start_prob = {} # Dictionary contains probabilities associated with specific part-of-speech tags occurring at the beginning of sentences within the dataset.
    
    # To determine the posterior probability of a given sentence by computing its log
    def posterior(self, model, sentence, label):
        if model == "Simple":
            return self.simple_model_posterior(sentence, label)
        elif model == "HMM":
            return self.hmm_model_posterior(sentence, label)
        else:
            print("Unknown model!")
            return None

    def simple_model_posterior(self, sentence, label):
        posterior_prob = 0
        tag_count_sum = sum(self.tag_occurrence_count.values())

        for word_index in range(len(sentence)):
            current_word = sentence[word_index]
            if current_word in self.word_tag_count:
                current_label = label[word_index]
                if current_label in self.word_tag_count[current_word]:
                    prob_tag = self.tag_occurrence_count[current_label] / tag_count_sum
                    if current_word in self.prob_emission and current_label in self.prob_emission[current_word]:
                        posterior_prob += math.log(
                            self.prob_emission[current_word][current_label] * prob_tag, 10
                        )
                    else:
                        max_occuring_tag = max(self.tag_occurrence_count, key=self.tag_occurrence_count.get)
                        val = self.tag_occurrence_count[max_occuring_tag]
                        posterior_prob += math.log(val / tag_count_sum, 10)

        return posterior_prob

    def hmm_model_posterior(self, sentence, label):
        posterior_prob = 0

        if sentence[0] in self.prob_emission and label[0] in self.prob_emission[sentence[0]]:
            posterior_prob += math.log(
                self.sentence_start_prob[label[0]] * self.prob_emission[sentence[0]][label[0]], 10
            )
        else:
            posterior_prob += math.log(self.base_val * self.sentence_start_prob[label[0]], 10)

        tag_count_sum = sum(self.tag_occurrence_count.values())

        for i in range(1, len(sentence)):
            prob_tag = self.tag_occurrence_count[label[i]] / tag_count_sum

            if sentence[i] in self.prob_emission and label[i] in self.prob_emission[sentence[i]]:
                posterior_prob += math.log(self.prob_emission[sentence[i]][label[i]], 10)
            else:
                posterior_prob += math.log(self.base_val, 10)

            transition_key = (label[i], label[i - 1])

            if transition_key in self.prob_transmission:
                posterior_prob += math.log(
                    self.prob_transmission[transition_key] * prob_tag, 10
                )
            else:
                posterior_prob += math.log(self.base_val * prob_tag, 10)

        return posterior_prob

    def train(self, data):
        for sentence in data:
            words, sent_pos_tag = sentence

            start = sent_pos_tag[0]

            # Update sentence start probabilities
            if start in self.sentence_start_prob:
                self.sentence_start_prob[start] += 1
            else:
                self.sentence_start_prob[start] = 1

            # Update tag occurrences and transition probabilities
            for index, word in enumerate(words):
                tag = sent_pos_tag[index]

                if index + 1 < len(words):
                    next_tag = sent_pos_tag[index + 1]

                    if (next_tag, tag) in self.prob_transmission:
                        self.prob_transmission[(next_tag, tag)] += 1
                    else:
                        self.prob_transmission[(next_tag, tag)] = 1

                if word in self.word_tag_count:
                    if tag in self.word_tag_count[word]:
                        self.word_tag_count[word][tag] += 1
                    else:
                        self.word_tag_count[word][tag] = 1
                else:
                    self.word_tag_count[word] = {tag: 1}

                if tag in self.tag_occurrence_count:
                    self.tag_occurrence_count[tag] += 1
                else:
                    self.tag_occurrence_count[tag] = 1

        # Normalize probabilities
        total_sentences = len(data)
        for tag in self.sentence_start_prob:
            self.sentence_start_prob[tag] /= total_sentences

        for transition in self.prob_transmission:
            tag_count = self.tag_occurrence_count[transition[1]]
            self.prob_transmission[transition] /= tag_count

        for word in self.word_tag_count:
            for pos in self.word_tag_count[word]:
                self.prob_emission.setdefault(word, {})[pos] = self.word_tag_count[word][pos] / self.tag_occurrence_count[pos]

# ------------------------- Function for Simple - Bayes Net -------------------------------------------------------
    def simplified(self, sentence):
            assigned_tags = []
            
            for word in sentence:
                max_probability = 0
                assigned_tag = ''

                if word not in self.word_tag_count:
                    assigned_tag = max(self.tag_occurrence_count, key=self.tag_occurrence_count.get)
                else:
                    tags_for_word = self.word_tag_count[word]
                    total_occurrences = sum(tags_for_word.values())
                    
                    for pos, count in tags_for_word.items():
                        probability = count / total_occurrences
                        if probability > max_probability:
                            max_probability = probability
                            assigned_tag = pos
                
                assigned_tags.append(assigned_tag)
            
            return assigned_tags

# ------------------------------------------ Function for HMM ------------------------------------------------------------
    def hmm_viterbi(self, sentence):
        POS_tag_sentence = [] # Final POS tags for the sentence.
        viterbi = [] # List of dictionaries for each word containing probabilities of all the POS for that word
        temp = {}

        Start_prob_val = 9.303335340e-14
        
        # Getting the most probable tag for the first word in the sentence
        for tag in self.tag_occurrence_count:
            if sentence[0] in self.prob_emission:
                if tag in self.prob_emission[sentence[0]]:
                    temp[tag] = (self.prob_emission[sentence[0]][tag] * self.sentence_start_prob[tag], tag)
                else:
                    # Start_prob_val is the lower limit of a floating point number
                    temp[tag] = (Start_prob_val, tag)
            else:
                temp[tag] = (Start_prob_val, tag)
        viterbi.append(temp)
        
        # Traversing through rest of the words in the sentence to get most probable tag for each
        for i in range(1, len(sentence)):
            temp_dict = {}
            tag_prev = viterbi[i-1]
            for tag1 in self.tag_occurrence_count:
                max_probability = 0
                current = tag1
                for tag2 in self.tag_occurrence_count:
                    value = 0
                    if (tag1,tag2) in self.prob_transmission:
                        value = self.prob_transmission[(tag1,tag2)] * tag_prev[tag2][0]
                    else:
                        value = Start_prob_val * tag_prev[tag2][0]
                    if value > max_probability:
                        max_probability = value 
                        current = tag2
                if max_probability == 0:
                    max_probability = Start_prob_val
                if sentence[i] in self.prob_emission and tag1 in self.prob_emission[sentence[i]]:
                    temp_dict[tag1] = self.prob_emission[sentence[i]][tag1] * max_probability, current
                else:
                    temp_dict[tag1] = (Start_prob_val * max_probability, current)
            viterbi.append(temp_dict)
        
        # Getting the tag of the last word having maximum probability
        max_probability = 0
        previous_tag = ''
        end = ''
        last_col = viterbi[len(sentence)-1]
        for tag in last_col:
            probability, previous = last_col[tag]
            if probability > max_probability:
                max_probability = probability
                previous_tag = previous
                end = tag
        if len(sentence) > 1:
            POS_tag_sentence.append(end)
        POS_tag_sentence.append(previous_tag)
        
        #Backtracking to get rest of the tags assigned to the words in the sentence
        for i in range(len(sentence)-2,0,-1):
            col = viterbi[i]
            probability, previous= col[previous_tag]
            POS_tag_sentence.append(previous)
            previous_tag = previous
        
        POS_tag_sentence.reverse()

        return POS_tag_sentence

    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        else:
            print("Unknown algo!")

