from stemmer import Stemmer

if __name__ == '__main__':
    my_stemmer = Stemmer()
    my_text = "Təbii dilin emalı"
    my_words = my_text.lower().split()
    my_words = my_stemmer.stem_words(my_words)
    print(my_words)