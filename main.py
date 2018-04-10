from stemmer import Stemmer
from string import punctuation

# Program starts here.
if __name__ == '__main__':
    # Instantiate Stemmer object
    my_stemmer = Stemmer()
    # Generate your text
    with open("test1.txt", 'r', encoding="utf-8-sig") as text:
        my_text = text.read()
    # Preprocess your text: remove punctuation, lowercase the letters, trim the spaces and newlines, and split the text by space/s
    my_text=my_text.replace("İ", "I")
    my_text=my_text.replace("“", "")
    my_text=my_text.replace("”", "")
    my_text=my_text.replace("'", "")
    my_text=my_text.replace('"', "")
    my_text=my_text.split()
    my_words=[]
    for word in my_text:
        my_words.append(''.join(c for c in word if (c not in punctuation) or (c == '-')))
    # Print words before stemming
    print(my_words)
    # Apply stemming to the list of words
    my_words = my_stemmer.stem_words(my_words)
    # Print words after stemming
    print(my_words)
