class Stemmer:
    words = []
    suffixes = []

    def __init__(self):
        self.load_words()
        self.load_suffixes()

    def __del__(self):
        self.words.clear()
        self.suffixes.clear()

    def load_words(self):
        with open("words.txt", "r", encoding="utf8") as words_file:
            for word in words_file:
                self.words.append(word.strip())

    def load_suffixes(self):
        with open("suffix.txt", "r", encoding="utf8") as suffix_file:
            for suffix in suffix_file:
                self.suffixes.append(suffix.strip())

    def stem_word(self, word=""):
        if word in self.words:
            return word
        for suffix in self.suffixes:
            if word.endswith(suffix):
                new_word = word[:word.rfind(suffix)]
                if new_word in self.words:
                    return new_word
        return word

    def stem_words(self, list_of_words):
        for word_index in range(len(list_of_words)):
            list_of_words[word_index] = self.stem_word(list_of_words[word_index])
        return list_of_words
