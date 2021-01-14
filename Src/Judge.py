"""
    Not very done yet!
"""

import json
import os
from Problem import Problem
import TranferSrc
import Config

CUR_DIR = os.path.dirname(__file__)





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
    Outputwill out by tuple with 6 element
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


    # TODO:gathering problem info
    problemInfo = Problem(problemDir)

    if not (proLang in problemInfo.compiling) or not (proLang in problemInfo.compiling):
        return ("JudgeError",0,100,0,0,"Lang Error")
    
    srcDir = TranferSrc.CreateFileToCompileSpace(problemDir,proLang,src)

    if srcDir == False:
        return ("JudgeError",0,100,0,0,"Tranfer file failed.")

    # TODO:Change Tag <<>>

    # TODO:Compile






    # TODO:Run
