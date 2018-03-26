import string
import csv
from stemmer import Stemmer

class Tagger:
    dictionary = {}
    punctuation = [',', '.', ':', ';']
    text = ''
    def __init__(self, file):
        self.load_dict()
        nstem = self.tag(file)
        stem = Stemmer().stem_words(nstem)
        tags = self.list_tags(stem)
        print(tags)
        # list of original words in the text
        list_of_words = self.text.split()
        print(list_of_words)

        self.save_to('cavab.txt', list_of_words, ["a", "b", "c", "e", "f", "g", "h", "i", "j"])

    def tag(self, file):
        with open(file, "r", encoding="utf8") as my_text:
            my_text = my_text.read()
        self.text = my_text
        print(self.text)

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
                tags.append((st, ['']))

        return tags

    def is_punctuation(self, symbol):
        for punct in self.punctuation:
            if symbol == punct:
                return True
        return False

    def save_to(self, filename, text, tags):
        file = open(filename, "w", encoding = 'utf8')
        for i in range(0, len(text)):
            if self.is_punctuation(text[i][-1]):
                file.write(text[i][:-1]+'{'+tags[i]+'}'+text[i][-1]+' ')
            else:
                file.write(text[i] + '{' + tags[i] + '} ')

        file.close()


tagi = Tagger('yoxla.txt')
