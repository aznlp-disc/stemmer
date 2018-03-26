import string
import csv
from stemmer import Stemmer

class Tagger:
    dictionary = {}
    def __init__(self, file):
        self.load_dict()
        nstem = self.tag(file)
        print(nstem)
        stem = Stemmer().stem_words(nstem)
        print(stem)
        self.list_tags(stem)

    def tag(self, file):
        with open(file, "r", encoding="utf8") as my_text:
            my_text = my_text.read()

        print(my_text)

        my_text = my_text.replace("İ", "I")
        my_text = my_text.replace("“", "")
        my_text = my_text.replace("”", "")
        my_text = my_text.replace("'", "")
        my_text = my_text.replace('"', "")
        my_words = my_text.translate(
            my_text.maketrans(string.punctuation, " " * len(string.punctuation))).lower().strip().split()
        return my_words

    def upp(self, word):
        word = word.replace("i", "İ")
        word = word.replace("ı", "I")
        return word

    def load_dict(self):
        with open("C:\\Users\\amustafali\\PycharmProjects\\Tikinti\\Bostan.csv", 'r', encoding = 'utf8') as temp:
            reader = csv.reader(temp)
            for row in reader:
                self.dictionary[row[0]] = row[2]

    def list_tags(self, stem):
        tags = []
        for st in stem:
            try:
                tags.append((st, str(self.dictionary[self.upp((str(st))).upper()]).split(';')))
            except Exception:
                tags.append((st, []))

        print(tags)


tagi = Tagger('yoxla.txt')
