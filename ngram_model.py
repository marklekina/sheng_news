#!/bin/python
#
# ngram_model.py - builds the n-gram language model from the train set and tests it using the train set by:
# - computing the most frequent n-grams in the training set
# - calculating the perplexities of sentences from the test set
# - auto-generating text from the n-gram models
#
# Mark Lekina Rorat, Jun, July, Sept, Oct 2021

import textwrap

from nltk import word_tokenize, ngrams, FreqDist
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.lm import MLE

NGRAM = 3
NUM_WORDS = 100


# splits the words in a text file into separate tokens
def tokenize_text(filename):
    file = open(filename, 'r')
    text = file.read()
    tokenized_text = [word_tokenize(text)]
    return tokenized_text


# creates a maximum likelihood estimation model
def create_model(filename):
    # Preprocess the tokenized text for language modelling
    tokenized_text = tokenize_text(filename)
    train_data, padded_sentences = padded_everygram_pipeline(NGRAM, tokenized_text)

    # Train a n-gram MLE model.
    model = MLE(NGRAM)
    model.fit(train_data, padded_sentences)
    return model


# generates a finite number of words from a model
def generate_sequence(ngram):
    sequence = []
    model = create_model("processed_data/train.txt")
    for token in model.generate(num_words=NUM_WORDS):
        sequence.append(token)
    sequence = "\n".join(textwrap.wrap(TreebankWordDetokenizer().detokenize(sequence)))
    return sequence


# helper function for the perplexity function (see below)
def perplexity_helper(model, ngram, tokenized_text, test_sentences):
    dictionary = {}
    test_data = [ngrams(t, ngram, pad_right=False, pad_left=False) for t in tokenized_text]
    for i, test in enumerate(test_data):
        try:
            dictionary[test_sentences[i].strip()] = model.perplexity(test)
        except ZeroDivisionError:
            continue
    return dictionary


# calculates and prints the perplexities of test sentences using unigrams, bigrams and trigrams
def perplexity(model, source_file):
    test_sentences = open(source_file, 'r').readlines()
    tokenized_text = [list(map(str.lower, word_tokenize(sent))) for sent in test_sentences]

    unigram_scores = perplexity_helper(model, 1, tokenized_text, test_sentences)
    bigram_scores = perplexity_helper(model, 2, tokenized_text, test_sentences)
    trigram_scores = perplexity_helper(model, 3, tokenized_text, test_sentences)

    print("\nlowest unigram perplexities...\n")
    for key, value in sorted(unigram_scores.items(), key=lambda item: item[1])[:5]:
        if isinstance(value, float):
            print("Perplexity of ('{0}'):{1}".format(key, value))

    print("\nlowest bigram perplexities...\n")
    for key, value in sorted(bigram_scores.items(), key=lambda item: item[1])[:5]:
        if isinstance(value, float):
            print("Perplexity of ('{0}'):{1}".format(key, value))

    print("\nlowest trigram perplexities...\n")
    for key, value in sorted(trigram_scores.items(), key=lambda item: item[1])[:5]:
        if isinstance(value, float):
            print("Perplexity of ('{0}'):{1}".format(key, value))


# prints the n most common ngrams in a text sample
def most_frequent_ngrams(filename, ngram, n):
    # display the n most frequent ngrams
    tokenized_text = tokenize_text(filename)
    tokens = ngrams(tokenized_text[0], ngram)
    f_dist = FreqDist(tokens)
    for key, value in sorted(f_dist.items(), key=lambda item: item[1], reverse=True)[:n]:
        print(key, value)


# tests each function in this script
def test_model():
    # create model
    model = create_model("processed_data/train.txt")

    print("\nMost frequent unigrams...\n")
    most_frequent_ngrams("processed_data/train.txt", 1, 10)

    print("\nMost frequent bigrams...\n")
    most_frequent_ngrams("processed_data/train.txt", 2, 10)

    print("\nMost frequent trigrams...\n")
    most_frequent_ngrams("processed_data/train.txt", 3, 10)

    print()
    perplexity(model, "processed_data/test.txt")

    # print generated sequences
    print("\ngenerating text (unigrams)...\n")
    print(generate_sequence(1))
    print("\ngenerating text (bigrams)...\n")
    print(generate_sequence(2))
    print("\ngenerating text (trigrams)...\n")
    print(generate_sequence(3))
    print("\ngenerating text (four-grams)...\n")
    print(generate_sequence(4))


def main():
    test_model()


if __name__ == "__main__":
    main()
