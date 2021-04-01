"""
    Config
    ---------
    you can configulation here.
"""
from Garedami.Src.Annouce import *

import os
from os import path

import yaml

CUR_DIR = path.dirname(__file__)
CONFIG_DIR = path.abspath(path.join(CUR_DIR,"..","Config"))
CONFIG_DIR_LANG = path.join(CONFIG_DIR,"Langs")

DEFAULT_ALL_LANG = {"BIN_PATH" : "", "BIN_FILE" : "", "TIME_FACTOR":1.0, "MEM_FACTOR":1.0 , "DANGER_WORDS" : []}

DEFAULT_LANG = {
    "C" : {"BIN_PATH" : "", "BIN_FILE" : "gcc","TIME_FACTOR":1.0, "MEM_FACTOR":1.0, "DANGER_WORDS" : []},
    "Cpp" : {"BIN_PATH" : "", "BIN_FILE" : "g++","TIME_FACTOR":1.0, "MEM_FACTOR":1.0, "DANGER_WORDS" : []},
    "Python" : {"BIN_PATH" : "", "BIN_FILE" : "python","TIME_FACTOR":5.0, "MEM_FACTOR":1.0, "DANGER_WORDS" : ["import os","from os", "import subprocess", "from subprocess"]},
    "Java" : {"BIN_PATH" : "", "BIN_FILE" : "java","TIME_FACTOR":1.5, "MEM_FACTOR":1.0, "DANGER_WORDS" : ["import java.net"]}
}

DEFAULT_GRADER = {
    "MAX_TEST_CASE" : 200,
    "COMPILE_TIME" : 5000,
    "JUDGE_TIME" : 5000,
    "MAX_DISPLAY" : 20,
    "GLOBAL_TIME_FACTOR" : 1.0
}

DEFAULT_VERDICT = {
    "P" : "Accept",
    "-" : "Wrong Answer",
    "T" : "Time-Limit Exceed",
    "X" : "Runtime Error",
    "H" : "Partially correct",
    "S" : "Skip",

    "?" : "Undefined"
}

DEFAULT_DANGER_WORDS = ["Popen","popen"]

DEFAULT_CENSOR_WORD = ["Bruh"]#Just Example Don't mind that. 


configLang = dict()
configGrader = dict()
configVerdict = dict()
configDangerWord = []
configCensorWord = []

def init():
    #Creating important lang config if they don't exits

    if not path.exists(CONFIG_DIR):
        os.mkdir(CONFIG_DIR)

    if not path.exists(CONFIG_DIR_LANG):
        os.mkdir(CONFIG_DIR_LANG)
    
    #each lang
    for lang in DEFAULT_LANG:
        if not path.exists(path.join(CONFIG_DIR_LANG,f"{lang}.yaml")):
            print(f"{lang} config not found...",end="")
            try:
                with open(path.join(CONFIG_DIR_LANG,f"{lang}.yaml"),"w") as f:
                    f.write(yaml.dump(DEFAULT_LANG[lang]))
                    print("Created")
            except:
                print("\aError")

    #MainGrader
    if not path.exists(path.join(CONFIG_DIR,"Grader.yaml")):
        print("Grader config not found...",end="")
        try:
            with open(path.join(CONFIG_DIR,"Grader.yaml"),"w") as f:
                f.write(yaml.dump(DEFAULT_GRADER))
                print("Created")
        except:
            print("\aError")
    
    #verdict
    if not path.exists(path.join(CONFIG_DIR,"Verdict.yaml")):
        print("Verdict config not found...",end="")
        try:
            with open(path.join(CONFIG_DIR,"Verdict.yaml"),"w") as f:
                f.write(yaml.dump(DEFAULT_VERDICT))
                print("Created")
        except:
            print("\aError")
    

    #DangerWord
    if not path.exists(path.join(CONFIG_DIR,"DangerWord.yaml")):
        print("Danger word config not found...",end="")
        try:
            with open(path.join(CONFIG_DIR,"DangerWord.yaml"),"w") as f:
                f.write(yaml.dump(DEFAULT_DANGER_WORDS))
                print("Created")
        except:
            print("\aError")
        
    
    #Censor word
    if not path.exists(path.join(CONFIG_DIR,"Censors.yaml")):
        print("Censor word config not found...",end="")
        try:
            with open(path.join(CONFIG_DIR,"Censors.yaml"),"w") as f:
                f.write(yaml.dump(DEFAULT_CENSOR_WORD))
                print("Created")
        except:
            print("\aError")
    
    ReloadConfig()


def GetYamlData(dir:str):

    data = ""
    try:
        with open(dir) as f:
            data = f.read()
    except:
        return "Can't read file!"
    

    try:
        data = yaml.load(data, Loader=yaml.FullLoader)
    except:
        return "Can't read yaml file!!"
    
    return data


def GetLangData(langFile:str):

    lang = langFile.replace(".yaml","")

    if lang in DEFAULT_LANG:
        res = DEFAULT_LANG[lang].copy()
    else:
        res = DEFAULT_ALL_LANG.copy()

    try:
        data = GetYamlData(path.join(CONFIG_DIR_LANG, langFile))
    except:
        printWarning(f"LANG {lang} Can't read data :(")
        return res

    if type(data) != type(dict()):
        printWarning(f"LANG {lang} not useable :(")
        return res

    for r in res:
        if not (r in data):
            printWarning(f"LANG {lang} : {r} not found in data.")
        elif type(data[r]) != type(res[r]):
            printWarning(f"LANG {lang} : data in {r} is not useable.")
        else:
            res[r] = data[r]
    
    return res

def ReloadConfig():

    global configLang
    global configGrader
    global configVerdict
    global configDangerWord
    global configCensorWord


    configLang = dict()

    langs = [f for f in os.listdir(CONFIG_DIR_LANG) if path.isfile(path.join(CONFIG_DIR_LANG, f)) and f.endswith(".yaml")]
    
    for langFile in langs:
        res = GetLangData(langFile)
        configLang[langFile.replace(".yaml","")] = res

        try:
            with open(path.join(CONFIG_DIR_LANG,langFile),"w") as f:
                f.write(yaml.dump(res))
        except:
            printWarning(f"Can't save config {langFile}")
    

    configGrader = GetYamlData(path.join(CONFIG_DIR,"Grader.yaml"))

    if type(configGrader) != dict:
        printWarning(f"Config Grader Error {configGrader}")
        configGrader = DEFAULT_GRADER.copy()
    else:
        for config in DEFAULT_GRADER:
            if not (config in configGrader):
                configGrader[config] = DEFAULT_GRADER[config]
    

    configVerdict = GetYamlData(path.join(CONFIG_DIR,"Verdict.yaml"))

    if type(configVerdict) != dict:
        printWarning(f"Config Verdict Error {configVerdict}")
        configVerdict = DEFAULT_VERDICT.copy()
    else:
        for config in DEFAULT_VERDICT:
            if not (config in configVerdict):
                configVerdict[config] = DEFAULT_VERDICT[config]
    

    configDangerWord = GetYamlData(path.join(CONFIG_DIR,"DangerWord.yaml"))

    if type(configDangerWord) != list:
        printWarning(f"Config Danger word Error {configDangerWord}")
        configDangerWord = DEFAULT_DANGER_WORDS.copy()


    configCensorWord = GetYamlData(path.join(CONFIG_DIR,"Censors.yaml"))

    if type(configDangerWord) != list:
        printWarning(f"Config Danger word Error {configDangerWord}")
        configCensorWord = DEFAULT_DANGER_WORDS.copy()
    
    

def Verdict(vv:str)->str:
    vv = vv.upper()
    if not (vv in configVerdict) :
        vv = "?"
    return configVerdict[vv]

def IsLangExist(lang:str):
    return (lang in configLang)
    
def GetBinPath(lang:str):
    global configLang
    """
    Get binary path

    return 1 is Path not found
    """
    if not (lang in configLang):
        return 1
    return configLang[lang]["BIN_PATH"]

def GetBinFile(lang:str):
    global configLang
    """
    Get binary file(eg. gcc.exe)

    return 1 is File not found
    """

    if not (lang in configLang):
        return 1
    return configLang[lang]["BIN_FILE"]

def getTimeFactor(lang:str):
    global configLang
    """
    Get time factor for that lang..

    return 1 is File not found
    """
    if not (lang in configLang):
        return 1
    return configLang[lang]["TIME_FACTOR"]

def getMemFactor(lang:str):
    global configLang
    if not (lang in configLang):
        return 1
    return configLang[lang]["MEM_FACTOR"]

def getGlobalTimeFactor():
    global configGrader

    if "GLOBAL_TIME_FACTOR" in configGrader:
        return configGrader["GLOBAL_TIME_FACTOR"]

    return 1


def getDangerWord():
    global configDangerWord
    return configDangerWord

def getDangerWordByLang(lang:str):
    global configLang

    if "DANGER_WORDS" in configLang[lang]:
        return configLang[lang]["DANGER_WORDS"]
    
    return []

def getCensorWords(lang:str):
    global configCensorWord
    return configCensorWord


    