from Garedami.Src import Config
from Garedami.Src.Annouce import *


def IsDanger(srcStr:str):

    danger = Config.getDangerWord()

    # TODO: It's better to use Suffix array!

    for word in danger:
        if srcStr.find(word):
            printError("fFound Danger word!{word}")
            return word
    
    return False









