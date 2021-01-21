"""
    Input by 7 or more argument
    1 : test case
    2 : timeLimit in ms
    3 : memoryLimit in mb
    4 : PROBLEM_DIR
    5 : source path
    6 : cmp cmd
    7 : cmp args
    8 : run cmd
    9 : run args

    output will return by stdout in formating below
    {verdic};{score};{maxscore};{elapsed};{memory};{comment}
"""
from os import path
import os
import sys
from subprocess import Popen,TimeoutExpired,PIPE
import time
import signal

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

if(len(judgeArgs) < 9):
    print(f"!;0;1;0;0;Not Enough info to judge\nexpected 9 args got {len(judgeArgs)} args",end = "")
    exit(0)


testCase = judgeArgs[0] or ""
timeLimit = int(judgeArgs[1] or "")#In ms
memoryLimit = int(judgeArgs[2] or "")#mb
PROBLEM_DIR = judgeArgs[3] or ""

if(len(judgeArgs) < 6):
    print(f"!;0;1;0;0;Program not Found",end = "")
    exit(0)


srcPath = judgeArgs[4] or ""

cmpMain = judgeArgs[5] or ""
cmpArg = judgeArgs[6] or ""

outMain = judgeArgs[7]
outArg = judgeArgs[8]


inPath = path.join(PROBLEM_DIR,f"{testCase}.in")
outPath = path.join(PROBLEM_DIR,"output.txt")
errPath = path.join(PROBLEM_DIR,"errout.txt")
solPath = path.join(PROBLEM_DIR,f"{testCase}.sol")


def writeLog(text:str):
    with open(path.join(PROBLEM_DIR,f"{int(time.time())}LOG.txt"),"w") as f:
        f.write(text)

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

    isJava = outMain.find("java")

    if isJava != -1:
        start_time = time.time()
        runner = Popen(f'{outMain} -Xmx{int(memoryLimit)}M {outArg} < "{inPath}" > "{outPath}" 2> "{errPath}" ; exit', shell= True, preexec_fn=os.setsid)
    else:
        start_time = time.time()
        runner = Popen(f'ulimit -v {memoryLimit*1000};{outMain} {outArg} < "{inPath}" > "{outPath}" 2> "{errPath}" ; exit',shell= True, preexec_fn=os.setsid)

    try:
        runner.communicate(timeout=timeLimit/1000)
        returnCode = runner.returncode
    except TimeoutExpired:
        if os.path.exists("/proc/" + str(runner.pid)):
            os.killpg(os.getpgid(runner.pid), signal.SIGTERM)
        return timeLimit,0,"TIMELXC"

    if os.path.exists("/proc/" + str(runner.pid)):
        os.killpg(os.getpgid(runner.pid), signal.SIGTERM)

    elapsed = time.time() - start_time


    if returnCode != 0:
        return elapsed*1000,0,f"WTF M{returnCode}"
    else:
        return elapsed*1000,0,"OK"


def execute():
    if sys.platform == "linux" or sys.platform == "linux2":
        return execute_linux()
    else:
        return execute_Window()






def compare():

    if(not path.exists(outPath)):return "-","File not found :(\n"

    if sys.platform == "linux" or sys.platform == "linux2":
        runner = Popen(f'cd "{PROBLEM_DIR}"; {cmpMain} {cmpArg} "{solPath}" "{inPath}" "{srcPath}"', stdout=PIPE, stdin=PIPE, stderr=PIPE,shell= True)
    else:
        runner = Popen(f'cd /d "{PROBLEM_DIR}" & {cmpMain} {cmpArg} "{solPath}" "{inPath}" "{srcPath}"', stdout=PIPE, stdin=PIPE, stderr=PIPE,shell= True)
    
    #writeLog(f'cd /d "{PROBLEM_DIR}" & {cmpMain} {cmpArg} "{solPath}" "{inPath}" "{srcPath}"')

    runner.communicate()

    if not path.exists(path.join(PROBLEM_DIR,"grader_result.txt")):
        return "!","grader_result Not found"
    
    otogVerdict = ""
    with open(path.join(PROBLEM_DIR,"grader_result.txt"),"r") as f:
        otogVerdict = f.read()
    
    if otogVerdict != "P":
        return "-","WrongAnswer"

    return otogVerdict,"Test ok Yey!"

    


#This is from Kiyago's standard judge
def main():
    
    if not path.exists(inPath):
        print(f"E;0;0;0;0;End of Test",end = "")
        return
    elapsed, memory, comment = execute()

    score = 0
    maxscore = 1.0
    if comment == "OK":

        ver,comment = compare()
        verdic = ver
        score = 1.0 if ver == "P" else 0

    elif comment == "JUDGEER":
        verdic = "!"
        comment = "Judge_Error"

    elif comment == "TIMELXC":
        verdic = "T"
        comment = f"Time Limit Exceed\n\nYour program run {elapsed} ms."
    else:
        verdic = "X"
        comment += f"\nRuntime Error!\n============Error============\n"

        if path.exists(errPath):

            with open(errPath,"r") as f:
                comment += f.read()

    # Clean up tmp directory
    try:
        #if(path.exists(outPath)):os.remove(outPath)
        #if(path.exists(errPath)):os.remove(errPath)
        pass
    except:
        pass

    print(f"{verdic};{score};{maxscore};{elapsed:.2f};{memory};{comment}",end = "")

main()
