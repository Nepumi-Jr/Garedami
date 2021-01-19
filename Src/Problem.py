
import json, yaml
import Garedami.Src.Config
import Garedami.Src.ConvertDir as CD
from os import path

CUR_DIR = path.dirname(__file__)
CONFIG_DIR = path.abspath(path.join(CUR_DIR,"..","Config"))


STD_FILE = path.abspath(path.join(CUR_DIR,"..","StandJudge","StdJudge.py"))


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

    timeLimit = 1000
    memLimit = 256
    judging = LittleCmd("<<!Python:BIN_FILE>>",f"\"{STD_FILE}\"")

    compiling = {
            "C" : LittleCmd("<<!C:BIN_FILE>>","-O2 \"<<Cur_Src>>\" -o \"<<Cur_Bin>>\""),
            "Cpp" : LittleCmd("<<!Cpp:BIN_FILE>>","-O2 -std=c++17 \"<<Cur_Src>>\" -o \"<<Cur_Bin>>\""),
            "Python": LittleCmd("<<!Python:BIN_FILE>>","-m py_compile \"<<Cur_Src>>\""),
            "Java": LittleCmd(path.join("<<!Java:BIN_PATH>>","javac"),"\"<<Cur_Src>>\"")
        }

    running = {
            "C" : LittleCmd("\"<<Cur_Bin>>\"",""),
            "Cpp" : LittleCmd("\"<<Cur_Bin>>\"",""),
            "Python": LittleCmd("<<!Python:BIN_FILE>>","\"<<Cur_Src>>\""),
            "Java": LittleCmd("<<!Java:BIN_FILE>>","\"<<Cur_Src>>\"")
        }



    def LoadYaml(self,pathLike):
        if path.exists(pathLike):
            
            try:
                with open(pathLike,"r") as f:
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

                    for l in data["compiling"]:
                        if type(data["compiling"][l]) == list and len(data["compiling"][l]) == 2:
                            self.compiling[l] = LittleCmd(data["compiling"][l][0],data["compiling"][l][1])

                if "running" in data and type(data["running"]) == dict:
                    
                    self.running = dict()
                    
                    for l in data["running"]:
                        if type(data["running"][l]) == list and len(data["running"][l]) == 2:
                            self.running[l] = LittleCmd(data["running"][l][0],data["running"][l][1])


            except:
                pass

    def __init__(self, pbPath):
        
        if not path.exists(path.join(CONFIG_DIR, "ProblemDefault.yaml")):
            CreateDefault()
        self.LoadYaml(path.join(CONFIG_DIR, "ProblemDefault.yaml"))
        

        
        #New gen here
        if path.exists(path.join(pbPath, "Config.yaml")):
            self.LoadYaml(path.join(pbPath, "Config.yaml"))

        else:
            #Otog Exe here
            if path.exists(path.join(pbPath, "Task_Com_Run.isl")):
                data = "meow"
                try:
                    with open(path.join(pbPath,"Task_Com_Run.isl"),"r") as f:
                        data = f.read()
                        data = json.loads(data)

                except:
                    pass
                
                if type(data) == dict: 
                    self.compiling = dict()
                    self.running = dict()

                    for lang in data:
                        if "Compiler" in data[lang] and "Runner" in data[lang]:
                            self.compiling[lang] = LittleCmd(data[lang]["Compiler"]["MainCMD"],
                            data[lang]["Compiler"]["ArgsCMD"])
                            self.running[lang] = LittleCmd(data[lang]["Runner"]["MainCMD"],
                            data[lang]["Runner"]["ArgsCMD"])
            

            if path.exists(path.join(pbPath, "Task_Info.isl")):
                data = "meow"
                try:
                    with open(path.join(pbPath,"Task_Info.isl"),"r") as f:
                        data = f.read()
                        data = json.loads(data)

                except:
                    pass
                

                if type(data) == dict: 
                    
                    if "TimeLimit" in data:
                        self.timeLimit = data["TimeLimit"]
                    
                    if "MemLimit" in data:
                        self.memLimit = data["MemLimit"]
            
            if path.exists(path.join(pbPath, "Task_Judge.isl")):
                data = "meow"
                try:
                    with open(path.join(pbPath,"Task_Judge.isl"),"r") as f:
                        data = f.read()
                        data = json.loads(data)

                except:
                    pass
                
                if type(data) == dict: 

                    if "MainCMD" in data and "ArgsCMD" in data:
                        self.judging = LittleCmd(data["MainCMD"],data["ArgsCMD"])

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
        for ss in self.running:
            sstr += f"\t{ss} : {self.running[ss]}\n"
        
        sstr+= "*End of Problem*\n"
            
        return sstr
    
    def DoConvertDir(self,lang:str,srcDir:str,proDir:str):

        ss = CD.Converting(self.judging.main,srcDir,proDir,lang)
        if ss == False:return False
        self.judging.main = ss

        ss = CD.Converting(self.judging.args,srcDir,proDir,lang)
        if ss == False:return False
        self.judging.args = ss


        ss = CD.Converting(self.compiling[lang].main,srcDir,proDir,lang)
        if ss == False:return False
        self.compiling[lang].main = ss

        ss = CD.Converting(self.compiling[lang].args,srcDir,proDir,lang)
        if ss == False:return False
        self.compiling[lang].args = ss


        ss = CD.Converting(self.running[lang].main,srcDir,proDir,lang)
        if ss == False:return False
        self.running[lang].main = ss

        ss = CD.Converting(self.running[lang].args,srcDir,proDir,lang)
        if ss == False:return False
        self.running[lang].args = ss


        return True



def CreateDefault():

    defData = {
        "timeLimit" : 1000,
        "memLimit" : 256,
        "judging" : ["<<!Python:BIN_FILE>>",f'"{path.join("<<Cur_Grader>>","StandardJudge","StdJudge.py")}"'],
        "compiling" : {
            "C" : ['"<<!C:BIN_FILE>>"','-O2 "<<Cur_Src>>" -o "<<Cur_Bin>>"'],
            "Cpp" : ['"<<!Cpp:BIN_FILE>>"','-O2 -std=c++17 "<<Cur_Src>>" -o "<<Cur_Bin>>"'],
            "Python": ['"<<!Python:BIN_FILE>>"','-m py_compile "<<Cur_Src>>"'],
            "Java": [f'"{path.join("<<!Java:BIN_PATH>>","javac")}"' ,f'-sourcepath "{path.join("<<Cur_Problem>>","CompileSpace")}" "<<Cur_Src>>"']
        },
        "running" : {
            "C" : ['"<<Cur_Bin>>"',''],
            "Cpp" : ['"<<Cur_Bin>>"',''],
            "Python": ['"<<!Python:BIN_FILE>>"','"<<Cur_Src>>"'],
            "Java": ['"<<!Java:BIN_FILE>>"',f'-cp "{path.join("<<Cur_Problem>>","CompileSpace")}" <<Cur_JClass>>']
        }
    }

    with open(path.join(CONFIG_DIR,"ProblemDefault.yaml"),"w") as f:
        f.write(yaml.dump(defData))

if __name__ == "__main__":
    x = Problem("asd")
    print(x)