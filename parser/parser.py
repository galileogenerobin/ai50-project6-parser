import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> SubjP VP | S Conj S | S Conj VP
SubjP -> NP | Det PartP | Adj PartP
NP -> N | DetP | AdjP
DetP -> Det AdjP | Det N
AdjP -> Adj AdjP | Adj N
PartP -> P NP | NP P NP | AdjP P NP
VP -> V | V SubjP | VP PartP | VP Adv | Adv VP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Convert the sentence to lowercase and tokenize (i.e., split into list of words)
    words = nltk.tokenize.word_tokenize(sentence.lower())
    # Only retain the words that have at least one alphabetic character
    # For each word in words, we check each character; if any character is a letter, we keep that word in our list
    words = [w for w in words if any(c.isalpha() for c in w)]
    return words
    # raise NotImplementedError


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    output = []
    for subtree in tree.subtrees():
        # loop through each subtree amd check if NP
        if subtree.label() == "NP":
            output.append(subtree)

    return output
    # raise NotImplementedError


if __name__ == "__main__":
    main()
