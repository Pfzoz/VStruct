from cmath import e
from importlib.resources import path
from multiprocessing.context import ForkContext
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

    def __init__(self, v_path : str, sim_path=False): ### Initializion of a V Struct object
        self.v_path = v_path
        self.files = []
        self.a_ready = False
        self.sim_path = sim_path
        self.up_structure() 
        print("\n==(.vhdl) Files/Paths Found :", len(self.files))
        # --- Tries to set up simulation path (directory where the simulation will be runned).
        if not sim_path: 
            self.sim_path = v_path+"sim/"
            print("\n==Simulation path not defined, setting simulation path at structure's path [", self.sim_path, "].")
            
        else:
            if not os.path.exists(sim_path):
                print("\n==Warning: Given simulation path does not exist. Runs will fail.")
            self.sim_path = sim_path+"sim/"
            print("==Simulation path defined at", self.sim_path, "\n")

    def up_structure(self, *includes): ### Method that finds every .vhdl file in the current v_path.
        self.a_ready = False
        v_paths = loop_dir(self.v_path[:-1], "sim", "analysis")
        for path in v_paths:
            if (path.split(".")[-1] == "vhdl") and (not path in self.files):
                self.files.append(path)
            if includes and (not path in self.files):
                for inclusion in includes:
                    if inclusion in path:
                        print("==Included", path)
                        self.files.append(path)

    def analyze(self, tmp=False, save=True): ### Method that analyzes the VHDL structure through GHDL. TMP will not prevent the analysis file of being saved.
        originalPath = os.getcwd()
        if not os.path.exists(self.v_path+"analysis"): os.mkdir(self.v_path+"analysis")
        if os.path.exists(self.sim_path): shutil.rmtree(self.sim_path)
        os.chdir(self.v_path+"analysis")
        os.mkdir(self.sim_path)
        print("\n==Analyzing", self.v_path, "\n")
        for file in self.files:
            try:
                shutil.copy(file, self.sim_path)    
            except FileNotFoundError:
                print("\n==ERROR: Analyze-FileNotFoundError. (Simulation Path or Files Removed?)\n")
                os.chdir(originalPath)
            else:
                process = subprocess.Popen(f"ghdl -a {self.sim_path}*.vhdl", shell=True)
                process.wait()
                self.a_ready = True
        os.chdir(originalPath)
        if tmp: shutil.rmtree(self.sim_path)
        if not save: shutil.rmtree(self.v_path+"analysis")

    def run(self, time : int, *target_files, tmp=False, save=True, force=True):
        if not self.a_ready and force:
            self.analyze(tmp, save)
            self.a_ready = True
        elif not self.a_ready and not force:
            print("\n==Not Analsis Ready. Run not simulated. [FORCE->FALSE]\n")
        if not os.path.exists(self.sim_path) and force:
            self.analyze(tmp, save)
            self.a_ready = True
        for target_file in target_files:
            for file in self.files:
                if target_file in file:
                    if not os.path.exists(self.sim_path):
                        print("\n==Simulation dir missing...\n")
                        raise FileNotFoundError
                    else:
                        target_path = None
                        for file in os.listdir(self.sim_path):
                            if target_file in file:
                                target_path = file
                        originalPath = os.getcwd()
                        os.chdir(self.v_path+"analysis")
                        bashCommand = f"ghdl -r {target_path[:-5]} --wave=test_{target_file[:-5]}.ghw --stop-time={time}ns"
                        print(bashCommand)
                        process = subprocess.Popen(bashCommand, shell=True)
                        process.wait()
                        os.chdir(originalPath)
                        break

    def to_string(self, *args): ### Method that returns a string of the state of the current V Struct
        vreturn = "\n--Estrutura Atual--\n"
        if (len(args) == 0) or (args == "all") or ("all" in args):
            vreturn += "\nVHDL :\n"
            for i in self.files:
                if ".vhdl" in i:
                    vreturn += "-- " + i + "\n"
            vreturn += "\n\nINCLUDED :\n"
            for i in self.files:
                if not ".vhdl" in i:
                    vreturn += "-- " + i + "\n"
            vreturn += "\n\nSIM :\n-- " + self.sim_path
            vreturn += "\n"
        else:
            if ".vhdl" in [i.lower() for i in args]:
                vreturn += "\nVHDL :\n"
                for i in self.files:
                    if ".vhdl" in i:
                        vreturn += "-- " + i + "\n"
            if "included" in [i.lower() for i in args]:
                vreturn += "\nINCLUDED :\n"
                for i in self.files:
                    if not ".vhdl" in i:
                        vreturn += "-- " + i + "\n" 
        if "others" in args:
            vreturn += "\nFLAGS :\nANALYSIS_READY -> " + str(self.a_ready) + "\n"
        return vreturn
            

### Notes ###

#It is recommended to look at 'tmp' as a "private" variable. Calling and changing it directly from the object
#instance might lead to unpredictable results. Instead use the method change_tmp() to change its value