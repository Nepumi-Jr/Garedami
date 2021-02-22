"""
    Judge
    ---------
    To use it you must call judge()

    for argument and output from this function
    you can look at judge()
"""

from Garedami.Src.Annouce import *
import json, os, time
from Garedami.Src.Problem import Problem
from Garedami.Src import TranferSrc, Config, Compile, Run, DangerSrc

CUR_DIR = os.path.dirname(__file__)

Config.init()

def beautyJudge(somejudge):
    printAnnou(f"------------Complete------------")
    print(f"Result : {somejudge[0]}")
    print(f"Score : {somejudge[1]:.1f}/{somejudge[2]:.1f}")
    print(f"Time : {somejudge[3]} ms")
    print(f"Mem : {somejudge[4]} mb")
    print(f"-Comment-")
    print(somejudge[5])
    print("-End of Judge-\n\n")



def judge(idTask:int,proLang:str,problemDir:str,src:str,timeJudge:int = 1000,memJudge:int = 64) -> tuple():
    """
    This is *main* function that use for judging user

    Input
    ----------
    idTask : str
        ... self-explanatory but we don't use them much.
    proLang : str
        is programming language that user what to compile
    problemDir : str 
        is Directory of that problem.
    src : str
        is source code that user want to judge
    time : int in ms
        time for Judging
    memory : int in mb
        meory for judging

    Output 
    ----------
    Output will out by tuple with 6 element
    1.Result : str
        is result from judge :)
    2.score : float
    3.maxScore :float
        max score in this problem
    4.Time : int
        is the sum of all testcases
    5.Memory : int
        is maximum memories that use in program
    6.Comment : str
        is useful for find the problem when Judge-side Error
    """
    printAnnou("JudgeRunning")

    printLog("Checking problem directory")
    if not os.path.exists(problemDir):
        printError("Really? problemDir not found :(")
        return ("JudgeError",0,100,0,0,"F**k admin!")

    Config.ReloadConfig()


    #gathering problem info
    problemInfo = Problem(problemDir)

    printLog("Checking lang")
    if not (proLang in problemInfo.compiling) or not (proLang in problemInfo.compiling):
        beautyJudge(("Compile Error?",0,100,0,0,f"{proLang} is not allowed"))
        return ("Compile Error?",0,100,0,0,f"{proLang} is not allowed")
    
    if Config.IsLangExist(proLang) == False:
        beautyJudge(("Judge Error",0,100,0,0,f"{proLang} config not found!!!"))
        return ("Judge Error",0,100,0,0,f"{proLang} config not found!!!")


    printLog("Checking source")
    danger = DangerSrc.IsDanger(src, proLang)
    if danger != False:
        beautyJudge(("SrcError",0,100,0,0,f"Found Danger word '{danger}'"))
        return ("SrcError",0,100,0,0,f"Found Danger word '{danger}'")


    TranferSrc.CreateFromShadow(problemDir)

    srcDir = TranferSrc.CreateFileToCompileSpace(problemDir,proLang,src)

    if srcDir == False:
        beautyJudge(("JudgeError",0,100,0,0,"Tranfer file failed."))
        return ("JudgeError",0,100,0,0,"Tranfer file failed.")
    elif srcDir == "Java Class Not Found :((":
        beautyJudge(("Compile Error",0,100,0,0,"Class not found :("))
        return ("Compile Error",0,100,0,0,"Class not found :(")
        

    if problemInfo.DoConvertDir(proLang,srcDir,problemDir) == False:
        beautyJudge(("JudgeError",0,100,0,0,"Can't convert data"))
        return ("JudgeError",0,100,0,0,"Can't convert data")


    #Compile judge  
    printAnnou("Compiling Judge...")
    res,compileMessage = Compile.DoCompile(problemInfo.judgingCompile,problemDir)
    if res == 2:
        beautyJudge(("Judge Compile Failed",0,100,0,0,"IMPOSSIBLE"))
        return ("Judge Compile Failed",0,100,0,0,"IMPOSSIBLE")
    elif res == 1:
        beautyJudge(("Judge Compile Error",0,100,0,0,compileMessage))
        return ("Judge Compile Error",0,100,0,0,compileMessage)


    #Compile Cmp  
    printAnnou("Compiling Cmp...")
    res,compileMessage = Compile.DoCompile(problemInfo.compareCompile,problemDir)
    if res == 2:
        beautyJudge(("Cmp Compile Failed",0,100,0,0,"IMPOSSIBLE"))
        return ("Cmp Compile Failed",0,100,0,0,"IMPOSSIBLE")
    elif res == 1:
        beautyJudge(("Cmp Compile Error",0,100,0,0,compileMessage))
        return ("Cmp Compile Error",0,100,0,0,compileMessage)

    

    #Compile src
    printAnnou("Compiling...")
    res,compileMessage = Compile.DoCompile(problemInfo.compiling[proLang],problemDir)
    if res == 2:
        beautyJudge(("Compile Failed",0,100,0,0,"Maybe you have some mystery alphabet."))
        return ("Compile Failed",0,100,0,0,"Maybe you have some mystery alphabet.")
    elif res == 1:
        beautyJudge(("Compile Error",0,100,0,0,compileMessage))
        return ("Compile Error",0,100,0,0,compileMessage)


    
    #Run
    printAnnou("Running...")
    timeLimit = int(timeJudge * Config.getTimeFactor(proLang) * Config.getGlobalTimeFactor())
    memLimit = int(memJudge * Config.getMemFactor(proLang))

    res = Run.JudgeRun(problemInfo, proLang, srcDir, problemDir, timeLimit, memLimit)

    time.sleep(0.2)

    try:
        TranferSrc.DelFileInCompileSpace(problemDir,proLang,src)
    except:
        printWarning("Can't Delete Src and Bin")

    beautyJudge(res)

    return res
