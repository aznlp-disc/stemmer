# Import the Stemmer class from stemmer.py file.
from stemmer import Stemmer
# Import string.
import string

# Program starts here.
if __name__ == '__main__':
    # Instantiate Stemmer object.
    my_stemmer = Stemmer()
    # Generate your text.
    with open("text.txt", 'r', encoding="utf-8-sig") as text:
        my_text = text.read()
    # Preprocess your text: remove punctuation, lowercase the letters, trim the spaces and newlines, and split the text by space/s.
    my_text=my_text.replace("İ", "I")
    my_text=my_text.replace("“", "")
    my_text=my_text.replace("”", "")
    my_text=my_text.replace("'", "")
    my_text=my_text.replace('"', "")
    my_words = my_text.translate(my_text.maketrans(string.punctuation, " " * len(string.punctuation))).lower().strip().split()
    # Print the generated array of words (not stemmed yet).
    print(my_words)
    # Apply stemming to the list of words.
    my_words = my_stemmer.stem_words(my_words)
    # Print the generated array of words (already stemmed words).
    print(my_words)
