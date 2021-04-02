

from Garedami.Src.Annouce import *
from Garedami.Src.Problem import LittleCmd, Problem
from Garedami.Src import Config

from subprocess import Popen, PIPE, STDOUT

from os import path
import os
from time import sleep

def IsFloat(content:str):
    try:
        content = float(content)
        return content
    except:
        return False

def CheckFormat(judgeStr:str):
    #Output should be
    #verdict(1char);score(float);maxscore(float);time(float in ms);mem(float);comment(str)
    chunk = judgeStr.split(";")


    if len(chunk) < 6:
        return "Len in Judge should be 6"
    
    if len(chunk[0]) != 1:
        return "Verdict should be 1 character"
    
    res = IsFloat(chunk[1])
    if type(res) == bool and res == False:
        return "Score should be number :("
    
    res = IsFloat(chunk[2])
    if type(res) == bool and res == False:
        return "Max Score should be number :("
    
    res = IsFloat(chunk[3])
    if type(res) == bool and res == False:
        return "Time should be number :("
    
    res = IsFloat(chunk[4])
    if type(res) == bool and res == False:
        return "Memory should be number :("
    

    comment = ""
    for i in range(5,len(chunk)):
        comment += chunk[i] + ";"

    return chunk[0:5] + [comment[:-1]]

def JudgeRun(problemInfo:Problem,proLang:str,srcPath:str,problemDir:str,timeLimit:int,memoryLimit:int):
    
    otogVerdict = ""
    cfVerdict = "Accept"
    score = 0
    maxScore = 0
    comment = ""
    time = 0
    memory = 0

    try:
        
        printLog("Judge : "+f"""{problemInfo.judgingRun.main} {problemInfo.judgingRun.args}""")
        printLog("Compr : "+f"""{problemInfo.compareRun.main} {problemInfo.compareRun.args}""")
        printLog("runni : "+f"""{problemInfo.running[proLang].main} {problemInfo.running[proLang].args}""")

        for testCase in range(Config.configGrader["MAX_TEST_CASE"]):
            
            judgeArgsFile = path.join(problemDir,"JudgeArg.isl")

            with open(judgeArgsFile,"w") as f:
                f.write(f"{testCase + 1}\n" +
                f"{timeLimit}\n"+
                f"{memoryLimit}\n"+
                f"{problemDir}\n"+
                f"{srcPath}\n"+
                f"{problemInfo.compareRun.main}\n"+
                f"{problemInfo.compareRun.args}\n"+
                f"{problemInfo.running[proLang].main}\n"+
                f"{problemInfo.running[proLang].args}")

            sleep(0.09)


            p = Popen(f"""{problemInfo.judgingRun.main} {problemInfo.judgingRun.args} "{judgeArgsFile}" """, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
            (stdOut,stdErr) = p.communicate()
            stdOut = stdOut.decode()
            stdErr = stdErr.decode().replace(problemDir,"..\\")

            printLog(f"T{testCase+1} : "+stdOut)

            returnCode = p.returncode
            if returnCode != 0:
                return ("JudgeError",0,100,0,0,"Run judge not complely\n"+stdErr)
            

            chunk = CheckFormat(stdOut.strip())
            if type(chunk) != list:
                return ("JudgeError",0,100,0,0,chunk)
            
            

            if chunk[0].upper() == "E" :
                
                try:
                    os.remove(judgeArgsFile)
                except:
                    pass

                if testCase <= Config.configGrader["MAX_DISPLAY"]:
                    return (otogVerdict,score,maxScore,time,memory,comment)
                else:
                    return (cfVerdict,score,maxScore,time,memory,comment)

            if chunk[0].upper() == "P" :
                otogVerdict += "P"
            else:
                otogVerdict += chunk[0].upper()
                comment += f"Case {testCase} : {chunk[5]}\n"
                if cfVerdict == "Accept":
                    cfVerdict = Config.Verdict(chunk[0].upper())
                    
            

            score += IsFloat(chunk[1])
            maxScore += IsFloat(chunk[2])
            time += IsFloat(chunk[3])
            memory += IsFloat(chunk[4])
        

        if Config.configGrader["MAX_TEST_CASE"] <= Config.configGrader["MAX_DISPLAY"]:
            return (otogVerdict,score,maxScore,time,memory,comment)
        else:
            return (cfVerdict,score,maxScore,time,memory,comment)
    
    except:
        return ("JudgeError",0,100,0,0,"Error during Judge")



