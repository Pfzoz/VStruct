from cmath import e
from importlib.resources import path
import os
from re import sub
import shutil
import subprocess
# Function to loop through all files of a directory and its subdirectories.

def loop_dir(dir, *args):
    validPaths = []
    for path in os.listdir(dir):
        if os.path.isdir(dir+"/"+path):
            for i in loop_dir(dir+"/"+path, *args):
                validPaths.append(i)
        else:
            contains = False
            for i in args:
                if i in dir+"/"+path:
                    contains = True
            if not contains:
                validPaths.append(dir+"/"+path)
    return validPaths

# Class to handle VHDL projects-structured directories.

class VStruct:

    def __init__(self, v_path, sim_path=False, tmp=False): ### Initializion of a V Struct object
        self.v_path = v_path
        self.vhdl = []
        self.sim_path = sim_path
        self._tmp = tmp
        self.up_structure() 
        print("\n==(.vhdl) Files Found :", len(self.vhdl))
        # --- Tries to set up simulation path (directory where the simulation will be runned).
        if not tmp:
            if not sim_path: 
                print("\n==Simulation path not defined, setting simulation path at structure's path [", self.v_path, "].")
                if not os.path.exists(v_path + "sim"):
                    os.mkdir(v_path+"sim")
                self.sim_path = v_path+"sim/"
                print("==Simulation path defined successfully.\n")
            else:
                os.mkdir(sim_path+"sim")
                self.sim_path = sim_path+"sim/"
                print("==Simulation path defined successfully.\n")
        else:
            if not sim_path:
                print("\n==Simulation path not defined, setting simulation path at structure's path [", self.v_path, "]. -- TMP Enabled.")
                self.sim_path = v_path+"sim/"
            print("==Simulation path defined successfully.\n")

    def up_structure(self): ### Method that finds every .vhdl file in the current v_path.
        v_paths = loop_dir(self.v_path[:-1], "sim", "analysis")
        for path in v_paths:
            if path.split(".")[-1] == "vhdl":
                self.vhdl.append(path)

    def analyze(self, save=True): ### Method that analyzes the VHDL structure through GHDL. TMP will not prevent the analysis file of being saved.
        if not os.path.exists(self.v_path + "analysis"): os.mkdir(self.v_path + "analysis")
        os.chdir(self.v_path + "analysis")
        if not os.path.exists(self.sim_path):
            os.mkdir(self.sim_path)
        for file in self.vhdl:
            try:
                shutil.copy(file, self.sim_path)
            except FileNotFoundError:
                pass
            else:
                process = subprocess.Popen(f"ghdl -a {self.sim_path}*.vhdl", shell=True)
                process.wait()
                if self._tmp: shutil.rmtree(self.sim_path)

    def run(self, target_file, time):
        self.change_tmp(False)
        self.analyze()
        for vhdl in self.vhdl:
            if target_file in vhdl:
                if not os.path.exists(self.sim_path):
                    print("Simulation dir missing...")
                    raise FileNotFoundError
                else:
                    target_path = None
                    for file in os.listdir(self.sim_path):
                        if target_file in file:
                            target_path = file
                    bashCommand = f"ghdl -r {target_path[:-5]} --wave=test_{target_file[:-5]}.ghw --stop-time={time}ns"
                    print(bashCommand)
                    process = subprocess.Popen(bashCommand, shell=True)
                    process.wait()
                    break

    def change_tmp(self, val):
        self._tmp = val

    def to_string(self, *args): ### Method that returns a string of the state of the current V Struct
        vreturn = "\n--Estrutura Atual--\n"
        if (len(args) == 0) or (args == "all") or ("all" in args):
            vreturn += "\nVHDL :\n"
            for i in self.vhdl:
                vreturn += "-- " + i + "\n"
            vreturn += "\n\nSIM :\n-- " + self.sim_path
            vreturn += "\n"
        else:
            if ".vhdl" in [i.lower() for i in args]:
                vreturn += "\nVHDL :\n"
                for i in self.vhdl:
                    vreturn += "-- " + i + "\n"
        if "others" in args:
            vreturn += "\nFLAGS :\nTMP -> " + str(self._tmp) + "\n"
        return vreturn
            
