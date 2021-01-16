"""
    Not very done yet!
"""

import json
import os
from Problem import Problem
import TranferSrc
import Config
import Compile
import Run

CUR_DIR = os.path.dirname(__file__)

Config.init()



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

    Config.ReloadConfig()


    #gathering problem info
    problemInfo = Problem(problemDir)


    if not (proLang in problemInfo.compiling) or not (proLang in problemInfo.compiling):
        return ("JudgeError",0,100,0,0,"Lang Error")
    
    TranferSrc.CreateFromShadow(problemDir)

    srcDir = TranferSrc.CreateFileToCompileSpace(problemDir,proLang,src)

    if srcDir == False:
        return ("JudgeError",0,100,0,0,"Tranfer file failed.")

    if problemInfo.DoConvertDir(proLang,srcDir,problemDir) == False:
        return ("JudgeError",0,100,0,0,"Can't convert data")


    #Compile    
    res,compileMessage = Compile.DoCompile(problemInfo.compiling[proLang],problemDir)
    if res == 2:
        return ("Compile Failed",0,100,0,0,"NOT COMPILE ERROR!")
    elif res == 1:
        return ("Compile Error",0,100,0,0,compileMessage)

    #Run

    timeLimit = int(problemInfo.timeLimit * Config.getTimeFactor("lang"))

    res = Run.JudgeRun(problemInfo.judging,problemInfo.running[proLang],proLang,problemDir,timeLimit,int(problemInfo.memLimit))

    TranferSrc.DelFileInCompileSpace(problemDir,proLang,src)

    return res
