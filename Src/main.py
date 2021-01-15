"""
    Example when try to use
"""

import Judge
from os import path

def GetSrc(namae):
    fileDir = path.join(path.dirname(__file__),"Test",namae)
    src = ""
    with open(fileDir,"r") as f:
        src = f.read()
    
    return src

def beautyJudge(somejudge,namae):
    print(f"------------{namae}------------")
    print(f"Result : {somejudge[0]}")
    print(f"Score : {somejudge[1]:.1f}/{somejudge[2]:.1f}")
    print(f"Time : {somejudge[3]} ms")
    print(f"Mem : {somejudge[4]} mb")
    print(f"-Comment-")
    print(somejudge[5])
    print("-End of Judge-\n\n")


if __name__ == "__main__":
    

    beautyJudge(Judge.judge("69","C",r"D:\TheCodeOfIsla\A lot Programing After Isla\Garademi\TestProblems\Pattern1",
    GetSrc("CPat1Error.c")),"-Test C Error-")

    beautyJudge(Judge.judge("69","C",r"D:\TheCodeOfIsla\A lot Programing After Isla\Garademi\TestProblems\Pattern1",
    GetSrc("CPat1Pass.c")),"-Test C-")

    beautyJudge(Judge.judge("69","C",r"D:\TheCodeOfIsla\A lot Programing After Isla\Garademi\TestProblems\Pattern1",
    GetSrc("CPat1NotPass.c")),"-Test C Not-")


    beautyJudge(Judge.judge("69","Cpp",r"D:\TheCodeOfIsla\A lot Programing After Isla\Garademi\TestProblems\Pattern1",
    GetSrc("CppPat1Error.cpp")),"-Test C++ Error-")

    beautyJudge(Judge.judge("69","Cpp",r"D:\TheCodeOfIsla\A lot Programing After Isla\Garademi\TestProblems\Pattern1",
    GetSrc("CppPat1Pass.cpp")),"-Test C++-")

    beautyJudge(Judge.judge("69","Cpp",r"D:\TheCodeOfIsla\A lot Programing After Isla\Garademi\TestProblems\Pattern1",
    GetSrc("CppPat1NotPass.cpp")),"-Test C++ Not-")


    beautyJudge(Judge.judge("69","Python",r"D:\TheCodeOfIsla\A lot Programing After Isla\Garademi\TestProblems\Pattern1",
    GetSrc("PyPat1Error.py")),"-Test Python Error-")

    beautyJudge(Judge.judge("69","Python",r"D:\TheCodeOfIsla\A lot Programing After Isla\Garademi\TestProblems\Pattern1",
    GetSrc("PyPat1Pass.py")),"-Test Python-")

    beautyJudge(Judge.judge("69","Python",r"D:\TheCodeOfIsla\A lot Programing After Isla\Garademi\TestProblems\Pattern1",
    GetSrc("PyPat1NotPass.py")),"-Test Python Not-")


    beautyJudge(Judge.judge("69","Java",r"D:\TheCodeOfIsla\A lot Programing After Isla\Garademi\TestProblems\Pattern1",
    GetSrc("JavaPat1Error.java")),"-Test Java Error-")



    