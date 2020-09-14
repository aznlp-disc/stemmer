'''
    Subclasses the original Stemmer for additionaly functionality
'''
import os
from .stemmer import Stemmer

PARENT_DIR = os.path.dirname(os.path.realpath(__file__))

class StemmerV2(Stemmer):
    
    def __init__(self):
        super().__init__()
        self.words = self.words.union(self.__load_names())

    def __load_names(self):
        names_list = set()
        with open(os.path.join(PARENT_DIR,"names","male.txt"), "r", encoding="utf8") as names_male:
            with open(os.path.join(PARENT_DIR,"names","female.txt"), "r", encoding="utf8") as names_female:
                names_list = set(x.lower().strip() for x in names_male)
                names_list.union(set(x.lower().strip() for x in names_female))
        return names_list




    