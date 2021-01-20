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

DEFAULT_LANG = {
    "C" : {"BIN_PATH" : "", "BIN_FILE" : "gcc","TIME_FACTOR":1.0},
    "Cpp" : {"BIN_PATH" : "", "BIN_FILE" : "g++","TIME_FACTOR":1.0},
    "Python" : {"BIN_PATH" : "", "BIN_FILE" : "python","TIME_FACTOR":5.0},
    "Java" : {"BIN_PATH" : "", "BIN_FILE" : "java","TIME_FACTOR":1.5}
}

DEFAULT_GRADER = {
    "MAX_TEST_CASE" : 200,
    "COMPILE_TIME" : 5000,
    "JUDGE_TIME" : 5000,
    "MAX_DISPLAY" : 20
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

DEFAULT_DANGER_WORDS = ["Popen","popen","os.","import os","from os", "import subprocess", "from subprocess"]




configLang = dict()
configGrader = dict()
configVerdict = dict()
configDangerWord = []

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


def GetLangData(lang:str):

    data = GetYamlData(path.join(CONFIG_DIR_LANG, lang))

    if type(data) != dict:
        return data
    
    
    require = [("BIN_FILE",""),("BIN_PATH",""),("TIME_FACTOR",1.0)]

    for r in require:
        if not (r[0] in data):
            return f"{r[0]} not found in data."
        
        if type(data[r[0]]) != type(r[1]):
            return f"data in {r[0]} is not useable."
    
    return data

def ReloadConfig():

    global configLang
    global configGrader
    global configVerdict
    global configDangerWord


    configLang = dict()

    langs = [f for f in os.listdir(CONFIG_DIR_LANG) if path.isfile(path.join(CONFIG_DIR_LANG, f)) and f.endswith(".yaml")]
    
    for lang in langs:
        res = GetLangData(lang)

        if type(res) == str:
            printWarning(f"Config {lang} Error [{res}]")
        else:
            configLang[lang.replace(".yaml","")] = res
    

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

    if type(configDangerWord) != dict:
        printWarning(f"Config Danger word Error {configDangerWord}")
        configDangerWord = DEFAULT_DANGER_WORDS.copy()
    
        

def Verdict(vv:str)->str:
    vv = vv.upper()
    if not (vv in configVerdict) :
        vv = "?"
    return configVerdict[vv]

    
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


def getDangerWord():
    return configDangerWord
    