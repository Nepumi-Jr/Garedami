"""
    Input by 7 or more argument
    1 : test case
    2 : timeLimit in ms
    3 : memoryLimit in mb
    4 : PROBLEM_DIR
    5 : source path
    6 : run cmd
    7 : run args (opional)

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

if(len(judgeArgs) < 4):
    print(f"!;0;1;0;0;Not Enough info to judge",end = "")
    exit(0)


testCase = judgeArgs[0] or ""
timeLimit = int(judgeArgs[1] or "")#In ms
memoryLimit = int(judgeArgs[2] or "")#mb
PROBLEM_DIR = judgeArgs[3] or ""

if(len(judgeArgs) < 6):
    print(f"!;0;1;0;0;Program not Found",end = "")
    exit(0)


srcPath = judgeArgs[4] or ""
outMain = judgeArgs[5] or ""

outArg = ""

for i in range(6,len(judgeArgs)):
    outArg += judgeArgs[i] + " "



inPath = path.join(PROBLEM_DIR,f"{testCase}.in")
outPath = path.join(PROBLEM_DIR,"output.txt")
errPath = path.join(PROBLEM_DIR,"errout.txt")
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
        runner.terminate()
        runner.kill()
        if os.path.exists("/proc/" + str(runner.pid)):
            os.killpg(os.getpgid(runner.pid), signal.SIGTERM)
        return timeLimit,0,"TIMELXC"

    runner.terminate()
    runner.kill()
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


def OtogCompare(langCheck,checkPath):

    mainCmd = "Nani"

    if langCheck == "Cpp":
        mainCmd = "g++"

    if mainCmd == "Nani":
        return False,"OTOG_!"

    runner = Popen(f'{mainCmd} "{checkPath}" -o "{path.join(PROBLEM_DIR,"BinCheck")}"', stdout=PIPE, stdin=PIPE, stderr=PIPE,shell= True)
    runner.communicate()

    if sys.platform == "linux" or sys.platform == "linux2":
        runner = Popen(f'cd  "{PROBLEM_DIR}"; "{path.join(PROBLEM_DIR,"BinCheck")}" "{solPath}" "{inPath}" "{srcPath}"', stdout=PIPE, stdin=PIPE, stderr=PIPE,shell= True)
    else:
        runner = Popen(f'cd /d "{PROBLEM_DIR}" & "{path.join(PROBLEM_DIR,"BinCheck")}" "{solPath}" "{inPath}" "{srcPath}"', stdout=PIPE, stdin=PIPE, stderr=PIPE,shell= True)
    
    runner.communicate()

    if not path.exists(path.join(PROBLEM_DIR,"grader_result.txt")):
        return False,"OTOG_!"
    
    otogVerdict = ""
    with open(path.join(PROBLEM_DIR,"grader_result.txt"),"r") as f:
        otogVerdict = f.read()
    
    return True,"OTOG_"+otogVerdict


def compare_equal():
    with open(solPath,"r") as solFile:
        solContent = solFile.read().strip().split("\n")

    with open(outPath,"r") as Out_File:
        outContent = Out_File.read().strip().split("\n")

    if len(solContent)!=len(outContent):
        return False,f"Expected {len(solContent)} line(s) but you got {len(outContent)} lines\n"
    
    for i in range(len(outContent)):
        if (solContent[i].strip())!=(outContent[i].strip()):
            return False,f"Answer Not right in line {i+1}\n"
    
    return True,"Test OK"



def compare():

    if(not path.exists(outPath)):return False,"File not found :(\n"

    if path.exists(path.join(PROBLEM_DIR,"check.cpp")):
        return OtogCompare("Cpp",path.join(PROBLEM_DIR,"check.cpp"))

    return compare_equal()

    


#This is from Kiyago's standard judge
def main():
    
    if not path.exists(inPath):
        print(f"E;0;0;0;0;End of Test",end = "")
        return
    elapsed, memory, comment = execute()

    score = 0
    maxscore = 1.0
    if comment == "OK":
        res,comment = compare()
        s = "ss"

        verdic = "P" if res else "-"
        score = 1.0 if res else 0

        if comment.startswith("OTOG_"):
            if comment == "OTOG_!":
                verdic = "!"
                score = 0.0
                comment = "Compare_Error"
            elif comment == "OTOG_P":
                verdic = "P"
                score = 1.0
                comment = "Test Ok!"
            else:
                verdic = "-"
                score = 0.0
                comment = "Test Ok!"
        

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
        if(path.exists(outPath)):os.remove(outPath)
        if(path.exists(errPath)):os.remove(errPath)
    except:
        pass

    print(f"{verdic};{score};{maxscore};{elapsed:.2f};{memory};{comment}",end = "")

main()
