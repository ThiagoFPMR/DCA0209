import os
import re
import nltk
from nltk.corpus import stopwords

from tree import AVLTree


def _corpus_parser(dir):
    """
    Yield each line of each file in a directory.

    Args:
        dir (str): The directory to parse.

    Yields:
        str: Each line of each file in the directory.
    """
    for filename in os.listdir(dir):
        if filename.endswith(".txt"):
            with open(os.path.join(dir, filename)) as file:
                for line in file:
                    print(filename)
                    yield line


def load_tokens_from_corpus(dir):
    """
    Load tokens from a corpus.

    Args:
        dir (str): The directory to parse.

    Returns:
        set: A set of tokens.
    """
    tokens = set()

    for line in _corpus_parser(dir):
        line = re.sub("[^A-Za-z0-9 ]+", "", line.lower())
        words = nltk.word_tokenize(line)
        tokens.update(words)

    # Remove stopwords
    tokens = tokens.difference(set(stopwords.words("english")))

    return tokens


if __name__ == "__main__":
    directory = "Modern Literature"
    token_tree = AVLTree()
    tokens = load_tokens_from_corpus(directory)
    for token in tokens:
        print(token)
        token_tree.add(token)
    print(len(tokens))
    print(token_tree.get_height())
