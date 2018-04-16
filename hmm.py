import pickle
from stemmer import Stemmer

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x',
               'y', 'z', 'ü', 'ö', 'ğ', 'ə', 'ç', 'ş', 'ı',
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'İ', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'X',
               'Y', 'Z', 'Ü', 'Ö', 'Ğ', 'Ə', 'Ç', 'Ş', 'I', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
               ]


def is_letter(x):
    for y in letters:
        if x == y:
            return True
    return False


# . ? !

#cleans the word of the tag
def pure_tag(word):
    i = word.find('{')
    return word[i:]

dirnaqlar = {'”', '“', '"'}

#cleans the word from the left and tag from the right, returns the word and its tag in a list
def word_and_tag(word):
    while is_letter(word[0]) == False:
        word = word[1:]

    while word[len(word)-1] != '}':
        word = word[:-1]

    i = word.find("{")

    # print(word[:i], word[i:])
    return [word[:i], word[i:]]

#when it is not the end of sentence - exceptions
def disregard(symbol):
    for i in dirnaqlar:
        if symbol == i:
            return True
    return False

class Matrix:
    freq = {}
    num_to_tags = {
        'fel': 0,
        'zərf': 1,
        'qoşma': 2,
        'isim': 3,
        'əvəzlik': 4,
        'sifət': 5,
        'fsifət': 6,
        'ədat': 7,
        'nida': 8,
        'modal': 9,
        'say': 10,
        'bağlayıcı': 11,
        'hissəcik': 12,
    }

    #the matrix is created and printed automatically. initialize as Matrix(corpus.txt)
    tags = []

    # fel, zərf, qoşma, isim, əvəzlik, sifət, fsifət, ədat, nida, modal, say, bağlayıcı, hissəcik - tag frequency
    cTag = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    tMatrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    # returns a dictionary with words with frequency for each of 13 tags
    def first_step(self, text):
        st = Stemmer()
        dic = {}
        for t in text:
            x = word_and_tag(t)
            x[0] = st.stem_words([x[0]])[0]
            try:
                dic[x[0]][self.num_to_tags[x[1][1:-1]]] += 1
            except Exception:
                dic[x[0]] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                dic[x[0]][self.num_to_tags[x[1][1:-1]]] += 1

        for i, j in dic.items():
            for x in range(0, 13):
                if self.cTag[x] != 0:
                    j[x] /= self.cTag[x]
                else:
                    j[x] = 0.0

        return dic

    def __init__(self, filename):
        with open(filename, "r", encoding = "utf-8-sig") as text:
            text = text.read()

        text = text.split()
        temp = []

        #we get list of skeletons, i.e. sentences without words and puncutation. Each sentence is just a list of ordered tags.
        for t in text:
            if disregard(t[-1]):
                x = t[::-1]
                x = x[x.find("}"):]
                temp.append(pure_tag(x[::-1]))
            elif t[-1] != '}':
                x = t[::-1]
                x = x[x.find("}"):]
                temp.append(pure_tag(x[::-1]))
                self.tags.append(temp)
                temp = []
            else:
                temp.append(pure_tag(t))

        # print(self.tags)

        #count all tags
        for s in self.tags:
            for t in s:
                try:
                    self.cTag[self.num_to_tags[t[1:-1]]] += 1
                except Exception:
                    pass

        # print(self.cTag)

        #count all binary relations in each sentence

        for s in self.tags:
            left = ''
            right = ''
            for t in s:
                left = right
                right = t
                try:
                    self.tMatrix[self.num_to_tags[left[1:-1]]][self.num_to_tags[right[1:-1]]] += 1
                except Exception:
                    pass

        # print(self.tMatrix)

        #get the transition matrix by dividing every element in tMatix by cTag of the row

        for i in range(0, 13):
            for j in range(0, 13):
                try:
                    self.tMatrix[i][j] = self.tMatrix[i][j]/self.cTag[i]
                except Exception:
                    self.tMatrix[i][j] = 0.0

        # print(self.tMatrix)

        self.freq = self.first_step(text)


        stemmer = Stemmer()
        # for i, j in self.freq.items():
        #     print('second ', i, j)
        tmp = {}
        for i in self.freq:
            tmp[stemmer.stem_words([i.lower()])[0]] = self.freq[i]
        self.freq = tmp

        for i, j in self.freq.items():
            print('second ',i, j)

        save_obj(self.freq, "freq")
        save_obj(self.tMatrix, "tMatrix")



def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


temp = Matrix("korpusumuz.txt")
for i in temp.tMatrix:
    print(i)