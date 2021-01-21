
import json, yaml

from Garedami.Src import Config
from Garedami.Src import ConvertDir as CD
from os import path

CUR_DIR = path.dirname(__file__)
CONFIG_DIR = path.abspath(path.join(CUR_DIR,"..","Config"))


STD_FILE = path.abspath(path.join(CUR_DIR,"..","StandardJudge","StdJudge.py"))
STD_CMP = path.abspath(path.join(CUR_DIR,"..","StandardJudge","StdCMP.cpp"))

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
    
    
    judgingCompile : LittleCmd()
    judgingRun : LittleCmd()
        in case of custom judge

    compareCompile
    compareRun : LittleCmd()
        in case of custom compare
    

    compiling : dict
        use for compile in each language
    
    running : dict
        same as compile but run

    """
    judgingCompile = LittleCmd('<<!Python:BIN_FILE>>',f'-m py_compile "{STD_FILE}"')
    judgingRun = LittleCmd('<<!Python:BIN_FILE>>',f'"{STD_FILE}"')
    
    compareCompile = LittleCmd('<<!Cpp:BIN_FILE>>',f'-O2 -std=c++17 "{STD_CMP}" -o {path.abspath(path.join(CUR_DIR,"..","StandJudge","StdCheckBin"))}')
    compareRun = LittleCmd(f'cd {path.abspath(path.join(CUR_DIR,"..","StandJudge"))} ; {path.abspath(path.join(CUR_DIR,"..","StandJudge","StdCheckBin"))}',f'')

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
                
                if "judgingCompile" in data and type(data["judgingCompile"]) == list and len(data["judgingCompile"]) == 2:
                    self.judgingCompile = LittleCmd(data["judgingCompile"][0],data["judgingCompile"][1])

                if "judgingRun" in data and type(data["judgingRun"]) == list and len(data["judgingRun"]) == 2:
                    self.judgingRun = LittleCmd(data["judgingRun"][0],data["judgingRun"][1])


                if "compareCompile" in data and type(data["compareCompile"]) == list and len(data["compareCompile"]) == 2:
                    self.compareCompile = LittleCmd(data["compareCompile"][0],data["compareCompile"][1])

                if "compareRun" in data and type(data["compareRun"]) == list and len(data["compareRun"]) == 2:
                    self.compareRun = LittleCmd(data["compareRun"][0],data["compareRun"][1])



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


    def __str__(self):
        sstr = ""

        sstr += f"judgingCompile : {self.judgingCompile}\n"
        sstr += f"judgingRun : {self.judgingRun}\n"
        sstr += f"compareCompile : {self.compareCompile}\n"
        sstr += f"compareRun : {self.compareRun}\n"

        sstr += f"Compiling\n"
        for ss in self.compiling:
            sstr += f"\t{ss} : {self.compiling[ss]}\n"
        
        sstr += f"Running\n"
        for ss in self.running:
            sstr += f"\t{ss} : {self.running[ss]}\n"
        
        sstr+= "*End of Problem*\n"
            
        return sstr
    
    def DoConvertDir(self,lang:str,srcDir:str,proDir:str):

        ss = CD.Converting(self.judgingCompile.main,srcDir,proDir,lang)
        if ss == False:return False
        self.judgingCompile.main = ss

        ss = CD.Converting(self.judgingCompile.args,srcDir,proDir,lang)
        if ss == False:return False
        self.judgingCompile.args = ss

        ss = CD.Converting(self.judgingRun.main,srcDir,proDir,lang)
        if ss == False:return False
        self.judgingRun.main = ss

        ss = CD.Converting(self.judgingRun.args,srcDir,proDir,lang)
        if ss == False:return False
        self.judgingRun.args = ss

        
        ss = CD.Converting(self.compareCompile.main,srcDir,proDir,lang)
        if ss == False:return False
        self.compareCompile.main = ss

        ss = CD.Converting(self.compareCompile.args,srcDir,proDir,lang)
        if ss == False:return False
        self.compareCompile.args = ss

        ss = CD.Converting(self.compareRun.main,srcDir,proDir,lang)
        if ss == False:return False
        self.compareRun.main = ss

        ss = CD.Converting(self.compareRun.args,srcDir,proDir,lang)
        if ss == False:return False
        self.compareRun.args = ss


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
        "judgingCompile" : ["<<!Python:BIN_FILE>>",f'-m py_compile "{STD_FILE}"'],
        "judgingRun" : ["<<!Python:BIN_FILE>>",f'"{STD_FILE}"'],

        "compareCompile" : ['<<!Cpp:BIN_FILE>>',f'-O2 -std=c++17 "{STD_CMP}" -o "{path.join("<<Cur_Problem>>","StdCheckBin")}"'],
        "compareRun" : [f'"{path.join("<<Cur_Problem>>","StdCheckBin")}"',f''],

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