
from Problem import LittleCmd

from subprocess import Popen, PIPE, STDOUT
import subprocess
import signal
import os
import time

def DoCompile(comCMD:LittleCmd,problemDir:str):
    
    print(comCMD.main+" "+comCMD.args)

    try:

        p = Popen(comCMD.main+" "+comCMD.args, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        (stdOut,stdErr) = p.communicate()
        stdOut = stdOut.decode().replace(problemDir,"..\\")
        stdErr = stdErr.decode().replace(problemDir,"..\\")


        returnCode = p.returncode
        if returnCode!= 0:
            return 1,stdOut+"\n"+stdErr
        return 0,""
    except:
        return 2,""
