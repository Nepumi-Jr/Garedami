"""
    Config
    ---------
    you can configulation here.
"""
from Annouce import *

import os
from os import path

import yaml

CUR_DIR = path.dirname(__file__)
CONFIG_DIR = path.abspath(path.join(CUR_DIR,"..","Config","Langs"))

configData = dict()

def init():
    #Creating important lang config if they don't exits

    if not path.exists(CONFIG_DIR):
        os.mkdir(CONFIG_DIR)

    #C
    if not path.exists(path.join(CONFIG_DIR,"C.yaml")):
        print("C config not found...",end="")
        try:
            with open(path.join(CONFIG_DIR,"C.yaml"),"w") as f:
                f.write(yaml.dump({"BIN_PATH" : "", 
                "BIN_FILE" : "gcc","TIME_FACTOR":1.0}))
                print("Created")
        except:
            print("\aError")
    

    #Cpp
    if not path.exists(path.join(CONFIG_DIR,"Cpp.yaml")):
        print("Cpp config not found...",end="")
        try:
            with open(path.join(CONFIG_DIR,"Cpp.yaml"),"w") as f:
                f.write(yaml.dump({"BIN_PATH" : "", 
                "BIN_FILE" : "g++","TIME_FACTOR":1.0}))
                print("Created")
        except:
            print("\aError")
    

    #Python
    if not path.exists(path.join(CONFIG_DIR,"Python.yaml")):
        print("Python config not found...",end="")
        try:
            with open(path.join(CONFIG_DIR,"Python.yaml"),"w") as f:
                f.write(yaml.dump({"BIN_PATH" : "", 
                "BIN_FILE" : "python","TIME_FACTOR":5.0}))
                print("Created")
        except:
            print("\aError")
    

    #Java
    if not path.exists(path.join(CONFIG_DIR,"Java.yaml")):
        print("Java config not found...",end="")
        try:
            with open(path.join(CONFIG_DIR,"Java.yaml"),"w") as f:
                f.write(yaml.dump({"BIN_PATH" : "", 
                "BIN_FILE" : "java","TIME_FACTOR":1.5}))
                print("Created")
        except:
            print("\aError")
    
    ReloadConfig()

def ReloadConfig():

    configData = dict()

    langs = [f for f in os.listdir(CONFIG_DIR) if path.isfile(path.join(CONFIG_DIR, f)) and f.endswith(".yaml")]
    
    for lang in langs:
        res = GetData(lang)

        if type(res) == str:
            printWarning(f"Config {lang} Error [{res}]")
        else:
            configData[lang.replace(".yaml","")] = res




def GetData(lang:str):

    try:
        with open(path.join(CONFIG_DIR, lang)) as f:
            data = f.read()
    except:
        return "Can't read file!"
    

    try:
        data = yaml.load(data, Loader=yaml.FullLoader)
    except:
        return "Can't read yaml file!!"
    
    
    require = [("BIN_FILE",""),("BIN_PATH",""),("TIME_FACTOR",1.0)]

    for r in require:
        if not (r[0] in data):
            return f"{r[0]} not found in data."
        
        if type(data[r[0]]) != type(r[1]):
            return f"data in {r[0]} is not useable."
    
    return data

    
def GetBinPath(lang:str):
    """
    Get binary path

    return 1 is Path not found
    """
    if not (lang in configData):
        return 1
    return configData[lang]["BIN_PATH"]

def GetBinFile(lang:str):
    """
    Get binary file(eg. gcc.exe)

    return 1 is File not found
    """
    if not (lang in configData):
        return 1
    return configData[lang]["BIN_FILE"]

def getTimeFactor(lang:str):
    """
    Get time factor for that lang..

    return 1 is File not found
    """
    if not (lang in configData):
        return 1
    return configData[lang]["TIME_FACTOR"]
    

init()