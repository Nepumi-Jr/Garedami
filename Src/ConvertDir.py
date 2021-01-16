import TranferSrc
import re
import Config

from os import path


def Converting(dirToConvert:str,srcDir:str,problemDir:str,lang:str):

    rDir = dirToConvert
    binName = path.join(problemDir,"CompileSpace",TranferSrc.GetBinName(lang,srcDir))

    rDir = rDir.replace("<<Cur_Src>>",srcDir)
    rDir = rDir.replace("<<Cur_Bin>>",binName)
    rDir = rDir.replace("<<Cur_Run_Exe>>",binName)

    graderPath = path.abspath(path.join(path.dirname(__file__),".."))
    
    rDir = rDir.replace("<<Std_Judge>>",path.join("<<Cur_Grader>>","StandardJudge","StdJudge.py"))
    rDir = rDir.replace("<<Cur_Grader>>",graderPath)
    rDir = rDir.replace("<<Cur_Problem>>",problemDir)

    #Otog EXE Context
    rDir = rDir.replace("<<Cur_Dir>>\\Compiler\\MinGW\\bin\\gcc.exe","<<!C:BIN_FILE>>")
    rDir = rDir.replace("<<Cur_Dir>>\\Compiler\\MinGW\\bin\\g++.exe","<<!Cpp:BIN_FILE>>")
    rDir = rDir.replace("<<Cur_Dir>>\\Compiler\\Python\\python.exe","<<!Python:BIN_FILE>>")
    rDir = rDir.replace("<<Cur_Dir>>\\Compiler\\Java\\bin\\javac.exe",f'"{path.join("<<!Java:BIN_PATH>>","javac")}"')
    rDir = rDir.replace("<<Cur_Dir>>\\Compiler\\Java\\bin\\java.exe","<<!Java:BIN_FILE>>")

    #Incase Java
    rDir = rDir.replace("<<JavaC>>",f'"{path.join("<<!Java:BIN_PATH>>","javac")}"')
    rDir = rDir.replace("<<Cur_JClass>>",binName.replace(".class","").replace(path.join(problemDir,"CompileSpace",""),""))

    reg = re.findall("<<![a-zA-Z]+:[a-zA-Z]+_[a-zA-Z]+>>", rDir)
    for e in reg:
        reLang = e.split(":")[0].replace("<<!","").strip()
        reWant = e.split(":")[1].replace(">>","").strip()


        res = ""

        if reWant == "BIN_FILE":
            res = Config.GetBinFile(reLang)
            if res == 1:
                return False
        elif reWant == "BIN_PATH":
            res = Config.GetBinPath(reLang)
            if res == 1:
                return False
        
        rDir = rDir.replace(e,res)
    
    pathSymbol = path.join("a","b").replace("a","").replace("b","")
    rDir = rDir.replace("\\",pathSymbol)
    

    return rDir



