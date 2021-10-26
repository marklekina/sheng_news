# sheng news

## Description
An initial Sheng corpus compiled from the People's Daily (Kenya) newspaper articles and an n-gram model trained from the corpus.
The goal of the project was to capture common use of written Sheng and construct a computational representation of the language.
This model can be evaluated by testing for common n-grams, computing the perplexity of the model and auto-generating text samples from it.

## Modules
``file_converter.py`` - handles the conversion of news article files (.pdf files) to text files.

``text_processor.py`` - cleans the converted news article files (.txt files), compiles the text in each of the files into two separate files: a training and a testing set, and standardizes both sets.

``ngram_model.py``- builds the n-gram language model from the train set and tests it using the train set by:
- computing the most frequent n-grams in the training set;
- calculating the perplexities of sentences from the test set;
- auto-generating text from the n-gram models.