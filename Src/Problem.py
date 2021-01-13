
import json
import yaml
import os
import Config

CUR_DIR = os.path.dirname(__file__)


STD_FILE = os.path.abspath(os.path.join(CUR_DIR,"..","StandJudge","StdJudge.py"))


class LittleCmd:
    main = ""
    args = ""

    def __init__(self, mainCmd = "", argsCmd = ""):
        self.main = mainCmd
        self.args = argsCmd

    def __str__(self):
        return f"['{self.main}' , '{self.args}']"

class Problem:
    """
    Use to get problem info
    -----------
    
    timelimit : int
        in ms.
    
    memLimit : int
        in megabyte.
    
    judging : LittleCmd()
        in case of custom judge
    

    compiling : dict
        use for compile in each language
    
    running : dict
        same as compile but run

    """

    

    def reset(self):
        #Default goes here
        self.timeLimit = 1000
        self.memLimit = 256

        self.judging = LittleCmd("<<!Python:BIN_FILE>>",f"\"{STD_FILE}\"")

        self.compiling = {
            "C" : LittleCmd("<<!C:BIN_FILE>>","-O2 \"<<Cur_Src>>\" -o \"<<Cur_Bin>>\""),
            "Cpp" : LittleCmd("<<!Cpp:BIN_FILE>>","-O2 -std=c++17 \"<<Cur_Src>>\" -o \"<<Cur_Bin>>\""),
            "Python": LittleCmd("<<!Python:BIN_FILE>>","-m py_compile \"<<Cur_Src>>\""),
            "Java": LittleCmd(os.path.join("<<!Java:BIN_PATH>>","javac"),"\"<<Cur_Src>>\"")
        }

        self.runing = {
            "C" : LittleCmd("\"<<Cur_Bin>>\"",""),
            "Cpp" : LittleCmd("\"<<Cur_Bin>>\"",""),
            "Python": LittleCmd("<<!Python:BIN_FILE>>","\"<<Cur_Src>>\""),
            "Java": LittleCmd("<<!Java:BIN_FILE>>","\"<<Cur_Src>>\"")
        }

    def __init__(self, pbPath):
        
        self.reset()

        #New gen here
        if os.path.exists(os.path.join(pbPath, "Config.cfg")):
            
            try:
                
                with open(os.path.join(pbPath, "Config.cfg"),"r") as f:
                    data = f.read()
                
                data = yaml.load(data, Loader=yaml.FullLoader)

                if "timeLimit" in data and (type(data["timeLimit"]) == int or type(data["timeLimit"]) == float):
                    self.timeLimit = data["timeLimit"]
                
                if "memLimit" in data and (type(data["memLimit"]) == int or type(data["timeLimit"]) == float):
                    self.memLimit = data["memLimit"]
                
                if "judging" in data and type(data["judging"]) == list and len(data["judging"]) == 2:
                    self.judging = LittleCmd(data["judging"][0],data["judging"][1])

                if "compiling" in data and type(data["compiling"]) == dict:
                    
                    
                    self.compiling = dict()
                    
                    print(">>>>",data["compiling"],type(data["compiling"]),data["compiling"].keys())

                    for l in data["compiling"]:
                        if type(data["compiling"][l]) == list and len(data["compiling"][l]) == 2:
                            print(f"Adding {l}")
                            self.compiling[l] = LittleCmd(data["compiling"][l][0],data["compiling"][l][1])

                if "runing" in data and type(data["runing"]) == dict:
                    
                    self.runing = dict()
                    
                    for l in data["runing"]:
                        if type(data["runing"][l]) == list and len(data["runing"][l]) == 2:
                            self.runing[l] = LittleCmd(data["runing"][l][0],data["runing"][l][1])


            except:
                self.reset()
                return
        else:

            #Otog EXE method
            #TODO OTOG exe goes here
            pass
            




        #

    def __str__(self):
        sstr = ""

        sstr += f"Time : {self.timeLimit}\n"
        sstr += f"Mem : {self.memLimit}\n"
        sstr += f"Judge : {self.judging}\n"

        sstr += f"Compiling\n"
        for ss in self.compiling:
            sstr += f"\t{ss} : {self.compiling[ss]}\n"
        
        sstr += f"Running\n"
        for ss in self.runing:
            sstr += f"\t{ss} : {self.runing[ss]}\n"
        
        sstr+= "*End of Problem*\n"
            
        return sstr


if __name__ == "__main__":
    x = Problem("asd")
    print(x)