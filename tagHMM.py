#in this code we use results from training in hmm.py. If word is not found, we will look for in bostan.csv
import pickle, csv
from stemmer import Stemmer
from string import punctuation

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x',
               'y', 'z', 'ü', 'ö', 'ğ', 'ə', 'ç', 'ş', 'ı',
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'İ', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'X',
               'Y', 'Z', 'Ü', 'Ö', 'Ğ', 'Ə', 'Ç', 'Ş', 'I', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '%'
               ]

def low(word):
    word.replace("İ", "I")
    return word

def is_letter(x):
    for y in letters:
        if x == y:
            return True
    return False

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

tag_to_nums = {
    0: 'fel',
    1: 'zərf',
    2: 'qoşma',
    3: 'isim',
    4: 'əvəzlik',
    5: 'sifət',
    6: 'fsifət',
    7: 'ədat',
    8: 'nida',
    9: 'modal',
    10: 'say',
    11: 'bağlayıcı',
    12: 'hissəcik'
}


def upp(word):
    word = word.replace("i", "İ")
    word = word.replace("ı", "I")
    return word.upper()

def clean_word(word):
    try:
        word = "".join(c for c in word if (c not in punctuation) or (c == '-'))
        while is_letter(word[0]) == False:
            word = word[1:]

        while is_letter(word[-1]) == False:
            word = word[:-1]
        # print(word)
        return word
    except Exception:
        return ''

#we have to load "freq" and "tMatrix"
def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

class HmmTag:

    luget = {}
    freq = {}
    tMatrix = []

    def __init__(self, lug):
        self.freq = load_obj("freq")
        for i in self.freq:
            self.freq[low(i).lower()] = self.freq.pop(i)
        self.tMatrix = load_obj("tMatrix")
        self.read_luget(lug)

    # luget format
    # ZƏRƏRSİZLƏŞDİRİLMƏK []
    # ZƏRƏRSİZLƏŞMƏ ['fel', 'isim']

    def read_luget(self, lug):
        with open(lug, "r", encoding = "utf-8-sig") as temp:
            temp = csv.reader(temp)
            #temporary list for each word
            poss = []
            for t in temp:
                for i in range(2, 7):
                    if t[i] != '':
                        poss.append(t[i])
                self.luget[t[0]] = poss
                poss = []


    def tag_text(self, name, save_file):
        with open(name, "r", encoding="utf-8-sig") as text:
            text = text.read()

        text = text.split()
        sentences = []

        # split sentences, add them into the list of sentences
        sentence = []
        for word in text:
            sentence.append(word)
            if (word.find(".") != -1 or word.find("?") != -1 or word.find("!") != -1) and is_letter(word[-1]) == False:
                sentences.append(sentence)
                sentence = []


        #list of the same sentences with stemmed words
        stems = []
        stemmer = Stemmer()
        for ss in sentences:
            tmp = []
            for s in ss:
                ax = stemmer.stem_words([clean_word(s)])[0]
                tmp.append(ax)
                # print(ax)
            print(tmp)
            stems.append(tmp)

        #list all possible tags for each word in each sentence
        tags = []

        tags = []
        for ss in stems:
            snt = []
            for s in ss:
                wd = []
                try:
                    tmp = self.freq[low(s).lower()]
                    flag = 0
                    for i in range(0, 13):
                        if tmp[i] > 0.0:
                            flag += 1
                            wd.append(i)
                except Exception:
                    #create it in freq dictionary - kind of workaround
                    self.freq[low(s).lower()] = [1/13, 1/13, 1/13, 1/13, 1/13, 1/13, 1/13, 1/13, 1/13, 1/13, 1/13, 1/13, 1/13]
                    try:
                        z = self.luget[upp(s)]
                        for a in z:
                            wd.append(num_to_tags[a])
                    except Exception:
                        pass
                snt.append(wd)
            tags.append(snt)
        # print(tags)

        # Here we will apply HMM and put the final answer into final_tags
        final_tags = []
        #each sentence
        for i in range(0, len(tags)):
            # print(tags[i])
            cumle = []
            #each word
            #only first word
            if len(tags[i][0]) > 1:
                mx = -1
                ind = 0
                index = 0
                # print(stems[i])
                for x in self.freq[low(stems[i][0]).lower()]:
                    if x > mx:
                        mx = x
                        index = ind
                    ind += 1
                tags[i][0] = [index]

            #from second word
            for j in range(1, len(tags[i])):
                if len(tags[i][j]) < 2:
                    continue
                elif len(tags[i][j-1]) == 0:
                    mx = -1
                    ind = 0
                    index = 0
                    print(len(low(stems[i][j]).lower()))
                    print(tags[i][j])
                    for x in self.freq[low(stems[i][j]).lower()]:
                        if x > mx:
                            mx = x
                            index = ind
                        ind += 1
                    tags[i][j] = [index]

                else:
                    maximum = 0
                    ind_of_max = 0
                    #iterate over tags of the word
                    for e in tags[i][j]:
                        m = self.tMatrix[tags[i][j-1][0]][e] * self.freq[low(stems[i][j]).lower()][e]
                        if m > maximum:
                            maximum = m
                            ind_of_max = e

                    tags[i][j] = [ind_of_max]
        save(save_file, sentences, tags)
        # print(sentences)
        # print(tags)


def save(save_file, sentences, tags):
    file = open(save_file, "w", encoding='utf-8-sig')
    for i in range(0, len(sentences)):
        ss = sentences[i]
        for s in range(0, len(ss)):
            try:
                tg = tag_to_nums[tags[i][s][0]]
            except Exception:
                tg = ''

            if is_letter(ss[s][-1]):
                file.write(ss[s] + '{' + tg + '} ')
            else:
                for b in range(1, len(ss[s])):
                    if is_letter(ss[s][-b]):
                        file.write(ss[s][:-b+1] + '{' + tg + '}'+ss[s][-b+1:]+' ')
                        break

    file.close()



abc = HmmTag("fi.csv")
abc.tag_text("Rasim.txt", "Rasim_duzelt.txt")
