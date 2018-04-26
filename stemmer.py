# Stemmer class definition
class Stemmer:
    # Stores the words loaded from the words.txt file
    words = set()
    # Stores the suffixes loaded from the suffix.txt file
    suffixes = []
    # Stores all possible stems of a word
    stems = []

    # Constructor of the Stemmer class
    def __init__(self):
        # Loads words from the words.txt file
        self.__load_words()
        # Loads suffixes from the suffix.txt file
        self.__load_suffixes()

    # Destructor of the Stemmer class
    def __del__(self):
        # Clear both lists to free the memory space
        self.words.clear()
        self.suffixes.clear()

    # Loads the words from the word.txt file into memory
    def __load_words(self):
        # Open words.txt file in read mode with utf-8 encoding.
        with open("words.txt", "r", encoding="utf8") as words_file:
            # Iterate over each line in the words.txt file
            for word in words_file:
                # Trim the spaces and newline characters from the string before adding to the list
                self.words.add(word.strip())

    # Loads the suffixes from the suffix.txt file into memory
    def __load_suffixes(self):
        # Open suffix.txt file in read mode with utf-8 encoding
        with open("suffix.txt", "r", encoding="utf8") as suffix_file:
            # Iterate over each line in the suffix.txt file
            for suffix in suffix_file:
                # Trim the spaces and newline characters from the string before adding to the list
                self.suffixes.append(suffix.strip())

    # Removes one suffix at a time
    def suffix(self, word):
        for suffix in self.suffixes:
            # If the word ends with the particular suffix, create a new word by removing that suffix
            if word.endswith(suffix) and (word[:word.rfind(suffix)] in self.words):
                word = word[:word.rfind(suffix)]
                return word
        # Iterate over the suffixes
        for suffix in self.suffixes:
            # If the word ends with the particular suffix, create a new word by removing that suffix
            if word.endswith(suffix):
                word = word[:word.rfind(suffix)]
                return word
        return word

    # Converts changed suffixes and roots to their original forms
    def converter(self, word):
        if word.endswith('lığ') or word.endswith('luğ') or word.endswith('lağ') or word.endswith('cığ'):
            l=list(word); l[-1]='q'; return "".join(l)
        if word.endswith('liy') or word.endswith('lüy'):
            l=list(word); l[-1]='k'; return "".join(l)
        if word.endswith('cağ'):
            l=list(word); l[-1]='q'; return "".join(l)
        if word.endswith('cəy'):
            l=list(word); l[-1]='k'; return "".join(l)
        if word.endswith('ığ') or word.endswith('uğ') or word.endswith('ağ'):
            l=list(word); l[-1]='q'; return "".join(l)
        if word.endswith('iy') or word.endswith('üy') or word.endswith('əy'):
            l=list(word); l[-1]='k'; return "".join(l)
        if word == 'ed':
            l=list(word); l[1]='t'; return "".join(l)
        if word == 'ged':
            l=list(word); l[2]='t'; return "".join(l)
        return word
        
    # Returns the stemmed version of word
    def stem_word(self, word):
        # Change the word to lowercase.
        word = word.lower()
        # Convert if the word has changed root or suffix
        word = self.converter(word)
        # If word is already in the list, append it to stems list
        if word.isnumeric():
                self.stems.append(word)
        else: 
            if word in self.words:
                self.stems.append(word)
        # Iterate through suffixes
        for suffix in self.suffixes:
                # If word ends with current suffix, remove the suffix and stem again
                if word.endswith(suffix):
                    self.stem_word(word[:word.rfind(suffix)])
                
    # Returns the stemmed versions of the given words
    def stem_words(self, list_of_words):
        # Iterate over the range of word indexes
        list_of_stems = []
        for word in list_of_words:
            # Empty the stems list for each word
            self.stems = []
            # Apply stemming to each word in the list.
            self.stem_word(word)
            selected_stem = ""
            # Choose the stem with the maximum length
            for stem in self.stems:
                if len(stem) > len(selected_stem): selected_stem = stem
            # If there is no selected stem for word, append the word itself
            if selected_stem == "":
                selected_stem = word
            # Append the stem of the current word to the list of stems
            list_of_stems.append(selected_stem)
            
        # Return the updated list.
        return list_of_stems
