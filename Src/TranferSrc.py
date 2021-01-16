

from os import path
import os,shutil

def GetJavaPublicClass(src:str):
    #public class <Name> {
    pc = src.find("public class")
    if pc == -1:
        return False
    
    op = src.find("{",pc)
    if pc == -1:
        return False
    
    if pc+12 > op:
        return False
    
    if src[pc+12:op] == "":
        return False
    
    return src[pc+12:op].strip()

def GetNameForSrc(lang:str,src:str):
    fileName = "Src"

    if lang == "C":
        fileName += ".c"
    elif lang == "Cpp":
        fileName += ".cpp"
    elif lang == "Python":
        fileName += ".py"
    elif lang == "Java":
        
        className = GetJavaPublicClass(src)
        if className == False:
            return False
        fileName = f"{className}.java"
    
    return fileName

def CreateFileToCompileSpace(problemDir:str,lang:str,src:str):


    fileName = GetNameForSrc(lang,src)

    if fileName == False:
        return False
    
    with open(path.join(problemDir,"CompileSpace",fileName),"w") as f:
        f.write(src)
    
    return path.join(problemDir,"CompileSpace",fileName)

def GetBinName(lang:str,srcDir:str)->str:

    if lang == "Java" and path.exists(srcDir):

        src = ""

        with open(srcDir,"r") as f:
            src = f.read()

        return GetJavaPublicClass(src).replace(".java","")

    return "BIN"



def DelFileInCompileSpace(problemDir:str,lang:str,src:str):

    fileName = GetNameForSrc(lang,src)

    if fileName == False:
        return False

    if path.exists(path.join(problemDir,"CompileSpace",fileName)):
        os.remove(path.join(problemDir,"CompileSpace",fileName))
    
    BinName = GetBinName(lang,src)

    if path.exists(path.join(problemDir,"CompileSpace",BinName)):
        os.remove(path.join(problemDir,"CompileSpace",BinName))
    
    if path.exists(path.join(problemDir,"CompileSpace",BinName + ".exe")):
        os.remove(path.join(problemDir,"CompileSpace",BinName + ".exe"))
    
    if lang == "Java" and GetJavaPublicClass(src) != False and path.exists(path.join(problemDir,"CompileSpace",GetJavaPublicClass(src)+".class")):
        os.remove(path.join(problemDir,"CompileSpace",GetJavaPublicClass(src)+".class"))


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def CreateFromShadow(problemDir:str):
    if path.exists(path.join(problemDir,"Shadow")):
        copytree(path.join(problemDir,"Shadow"),path.join(problemDir,"CompileSpace"))
    else:
        if not path.exists(path.join(problemDir,"CompileSpace")):
            os.mkdir(path.join(problemDir,"CompileSpace"))
