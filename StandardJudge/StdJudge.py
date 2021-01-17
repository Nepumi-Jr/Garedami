"""
    Input by 6 argument
    1 : test case
    2 : timeLimit in ms
    3 : memoryLimit in mb
    4 : PROBLEM_DIR
    5 : run cmd
    6 : run args (opional)

    output will return by stdout in formating below
    {verdic};{score};{maxscore};{elapsed};{memory};{comment}
"""
from os import path
import os
import sys
from subprocess import Popen,TimeoutExpired
import time

judgeArgs = sys.argv[-1]
if not path.exists(judgeArgs):
    print(f"!;0;1;0;0;Judge args not found :(",end = "")
    exit(0)

try:
    with open(judgeArgs,"r") as f:
        judgeArgs = f.read().split("\n")

except:
    print(f"!;0;1;0;0;Can't read Judge args:(",end = "")
    exit(0)

if(len(judgeArgs) < 5):
    print(f"!;0;1;0;0;Not Enough info to judge",end = "")
    exit(0)


testCase = judgeArgs[0] or ""
timeLimit = int(judgeArgs[1] or "")#In ms
memoryLimit = int(judgeArgs[2] or "")#mb
PROBLEM_DIR = judgeArgs[3] or ""

if(len(judgeArgs) < 5):
    print(f"!;0;1;0;0;Program not Found",end = "")
    exit(0)

outMain = judgeArgs[4] or ""

outArg = ""

for i in range(5,len(judgeArgs)):
    outArg += judgeArgs[i] + " "






inPath = path.join(PROBLEM_DIR,f"{testCase}.in")
outPath = path.join(PROBLEM_DIR,"Out.txt")
errPath = path.join(PROBLEM_DIR,"Err.txt")
solPath = path.join(PROBLEM_DIR,f"{testCase}.sol")


def execute_Window():
    start_time = time.time()
    runner = Popen(f'{outMain} {outArg}  < "{inPath}" > "{outPath}" 2> "{errPath}"',shell= True)

    try:
        runner.communicate(timeout=timeLimit/1000)
        returnCode = runner.returncode
    except TimeoutExpired:
        runner.terminate()
        runner.kill()
        return timeLimit,0,"TIMELXC"

    runner.terminate()
    runner.kill()

    elapsed = time.time() - start_time


    if returnCode != 0:
        return elapsed*1000,0,f"WTF M{returnCode}"
    else:
        return elapsed*1000,0,"OK"

def execute_linux():
    # TODO:linux version()
    return execute_Window()


def execute():
    if sys.platform == "linux" or sys.platform == "linux2":
        return execute_linux()
    else:
        return execute_Window()

def compareCustom():
    pass

def compare_equal(outStr:str, solStr:str):
    with open(solStr,"r") as solFile:
        solContent = solFile.read().strip().split("\n")

    with open(outStr,"r") as Out_File:
        outContent = Out_File.read().strip().split("\n")

    if len(solContent)!=len(outContent):
        return False,f"Expected {len(solContent)} line(s) but you got {len(outContent)} lines\n"
    
    for i in range(len(outContent)):
        if (solContent[i].strip())!=(outContent[i].strip()):
            return False,f"Answer Not right in line {i+1}\n"
    
    return True,"Test OK"



def compare(outStr:str, solStr:str):

    if(not path.exists(outStr)):return False,"File not found :(\n"

    # TODO:Support old friend (Otog.org)

    return compare_equal(outStr,solStr)

    


#This is from Kiyago's standard judge
def main():
    
    if not path.exists(inPath):
        print(f"E;0;0;0;0;End of Test",end = "")
        return
    elapsed, memory, comment = execute()

    score = 0
    maxscore = 1.0
    if comment == "OK":
        res,comment = compare_equal(outPath,solPath)
        verdic = "P" if res else "-"
        score = 1.0 if res else 0

    elif comment == "JUDGEER":
        verdic = "!"
        comment = "Judge_Error"

    elif comment == "TIMELXC":
        verdic = "T"
        comment = f"Time Limit Exceed\n\nYour program run {elapsed} ms."
    else:
        verdic = "X"
        comment = f"Runtime Error!\n============Error============\n"

        with open(errPath,"r") as f:
            comment += f.read()

    # Clean up tmp directory
    try:
        if(path.exists(outPath)):os.remove(outPath)
        if(path.exists(errPath)):os.remove(errPath)
    except:
        pass

    print(f"{verdic};{score};{maxscore};{elapsed:.2f};{memory};{comment}",end = "")

main()