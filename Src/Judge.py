"""
    Not very done yet!
"""

from Annouce import *
import json
import os
from Problem import Problem
import TranferSrc
import Config
import Compile
import Run
import time

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



def judge(idTask:int,proLang:str,problemDir:str,src:str) -> tuple():
    """
    This is main function that use for judging user

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
        return ("JudgeError",0,100,0,0,"Are you joking to me?")

    Config.ReloadConfig()


    #gathering problem info
    problemInfo = Problem(problemDir)

    printLog("Checking lang")
    if not (proLang in problemInfo.compiling) or not (proLang in problemInfo.compiling):
        beautyJudge(("JudgeError",0,100,0,0,"Lang Error"))
        return ("JudgeError",0,100,0,0,"Lang Error")
    
    TranferSrc.CreateFromShadow(problemDir)

    srcDir = TranferSrc.CreateFileToCompileSpace(problemDir,proLang,src)

    if srcDir == False:
        beautyJudge(("JudgeError",0,100,0,0,"Tranfer file failed."))
        return ("JudgeError",0,100,0,0,"Tranfer file failed.")

    if problemInfo.DoConvertDir(proLang,srcDir,problemDir) == False:
        beautyJudge(("JudgeError",0,100,0,0,"Can't convert data"))
        return ("JudgeError",0,100,0,0,"Can't convert data")



    printAnnou("Compiling...")

    #Compile    
    res,compileMessage = Compile.DoCompile(problemInfo.compiling[proLang],problemDir)
    if res == 2:
        beautyJudge(("Compile Failed",0,100,0,0,"NOT COMPILE ERROR!"))
        return ("Compile Failed",0,100,0,0,"NOT COMPILE ERROR!")
    elif res == 1:
        beautyJudge(("Compile Error",0,100,0,0,compileMessage))
        return ("Compile Error",0,100,0,0,compileMessage)


    printAnnou("Running...")
    #Run

    timeLimit = int(problemInfo.timeLimit * Config.getTimeFactor("lang"))

    res = Run.JudgeRun(problemInfo.judging,problemInfo.running[proLang],proLang,problemDir,timeLimit,int(problemInfo.memLimit))

    time.sleep(0.2)

    try:
        TranferSrc.DelFileInCompileSpace(problemDir,proLang,src)
    except:
        printWarning("Can't Delete Src and Bin")

    beautyJudge(res)

    return res
