###################################
# CS B551 Fall 2023, Assignment #3
#
# Jaya Sandeep Ketha: jketha
# (Based on skeleton code by D. Crandall)

# References: https://github.com/gurjaspalbedi/parts-of-speech-tagging/blob/master/pos_solver.py
#             https://github.com/harshars/Artificial-Intelligence-POS-tagging-Decryption-Naive-Bayes-Text-Classification
#             https://web.stanford.edu/~jurafsky/slp3/old_oct19/8.pdf

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
        total_tag_count = sum(self.tag_occurrence_count.values())

        for word, pos_label in zip(sentence, label):
            if word in self.word_tag_count:
                prob_tag = self.tag_occurrence_count.get(pos_label, 0) / total_tag_count

                word_tag_prob = self.prob_emission.get(word, {}).get(pos_label, None)
                if word_tag_prob is not None:
                    posterior_prob += math.log(word_tag_prob * prob_tag, 10)
                else:
                    max_occurring_tag = max(self.tag_occurrence_count, key=self.tag_occurrence_count.get)
                    fallback_prob = self.tag_occurrence_count[max_occurring_tag] / total_tag_count
                    posterior_prob += math.log(fallback_prob, 10)

        return posterior_prob


    def hmm_model_posterior(self, sentence, label):
        posterior_prob = 0

        for i, (word, pos_label) in enumerate(zip(sentence, label)):
            if i == 0:
                start_prob = self.sentence_start_prob.get(pos_label, 0)
                emission_prob = self.prob_emission.get(word, {}).get(pos_label, None)

                if emission_prob is not None:
                    posterior_prob += math.log(start_prob * emission_prob, 10)
                else:
                    posterior_prob += math.log(self.base_val * start_prob, 10)
            else:
                prob_tag = self.tag_occurrence_count.get(pos_label, 0) / sum(self.tag_occurrence_count.values())

                emission_prob = self.prob_emission.get(word, {}).get(pos_label, None)
                if emission_prob is not None:
                    posterior_prob += math.log(emission_prob, 10)
                else:
                    posterior_prob += math.log(self.base_val, 10)

                transition_key = (pos_label, label[i - 1])
                transition_prob = self.prob_transmission.get(transition_key, None)

                if transition_prob is not None:
                    posterior_prob += math.log(transition_prob * prob_tag, 10)
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
            if word in self.word_tag_count:
                tags_for_word = self.word_tag_count[word]
                max_tag = max(tags_for_word, key=tags_for_word.get)
                assigned_tags.append(max_tag)
            else:
                max_occuring_tag = max(self.tag_occurrence_count, key=self.tag_occurrence_count.get)
                assigned_tags.append(max_occuring_tag)

        return assigned_tags

# ------------------------------------------ Function for HMM ------------------------------------------------------------
    def hmm_viterbi(self, sentence):
        POS_tag_sequence = []  # Final POS tags for the sentence
        viterbi_matrix = []  # Matrix for storing probabilities
        backpointer = []  # Matrix for storing backpointers

        # Initializing the viterbi matrix and backpointer matrix
        for i in range(len(sentence)):
            viterbi_matrix.append({})
            backpointer.append({})

        Start_prob_val = 9.303335340e-14

        # Initialization step for the first word in the sentence
        for tag in self.tag_occurrence_count:
            temp = Start_prob_val
            if sentence[0] in self.prob_emission and tag in self.prob_emission[sentence[0]]:
                temp = self.prob_emission[sentence[0]][tag] * self.sentence_start_prob.get(tag, Start_prob_val)
            viterbi_matrix[0][tag] = temp
            backpointer[0][tag] = None

        # Iterating through the rest of the words in the sentence
        for i in range(1, len(sentence)):
            for current_tag in self.tag_occurrence_count:
                max_prob, max_tag = max(
                    ((viterbi_matrix[i - 1][prev_tag] * self.prob_transmission.get((current_tag, prev_tag), Start_prob_val)), prev_tag)
                    for prev_tag in self.tag_occurrence_count
                )
                max_prob *= self.prob_emission.get(sentence[i], {}).get(current_tag, Start_prob_val)
                viterbi_matrix[i][current_tag] = max_prob
                backpointer[i][current_tag] = max_tag

        # Backtracking to get the POS tags sequence
        final_tag = max(viterbi_matrix[-1], key=viterbi_matrix[-1].get)
        POS_tag_sequence.append(final_tag)
        
        for i in range(len(sentence) - 1, 0, -1):
            final_tag = backpointer[i][final_tag]
            POS_tag_sequence.append(final_tag)

        POS_tag_sequence.reverse()
        return POS_tag_sequence


    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        else:
            print("Unknown algo!")