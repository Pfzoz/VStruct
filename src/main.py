import os
from xml.sax.handler import feature_external_ges
from vstruct import VStruct

# Function that returns a directory path if its valid, or returns False if it's invalid or doesn't exist. Valid paths strings have '/' at the end and returns True
# with os.path.exists

def valid_path(path):
    if os.path.exists(path) and path[-1] == "/":
        return path
    elif os.path.exists(path):
        return path + "/"
    else:
        return False

# Pre-Defined Variables

tmp = False
cmd = None
vStructure = None
path = os.getcwd()
modified = True
# Program

while cmd != "exit":
    print(path)
    cmd = input("VStruct >>> ")
    arguments = cmd.split(" ")
    if arguments == []:
        continue
    # Commands
    op = arguments[0]
    if op == "cd": # Path Manipulation
        try:
            if len(arguments) > 1:
                os.chdir(arguments[1])
            else:
                print("! No Argument Given.\n")
        except FileNotFoundError:
            print("! File/Directory Not Found.\n")
        else:
            path = os.getcwd()
            print("")
    elif op == "mount": # Mount the V Struct.
        parameters = arguments[1:]
        if "-c" in parameters:
            vStructure = VStruct(valid_path(path))
        elif "-p" in parameters:
            if len(parameters) > parameters.index("-p")+1:
                if os.path.exists(parameters[parameters.index("-p")+1]):
                    vStructure = VStruct(valid_path(parameters[parameters.index("-p")+1]))
                else:
                    print("! Invalid Given Path\n")
        if "-i" in parameters and len(parameters)-parameters.index("-i")+1 != 0:
            if vStructure:
                inclusions = []
                for i in range(parameters.index("-i")+1, len(parameters)):
                    if parameters[i][0] != "-":
                        inclusions.append(parameters[i])
                vStructure.up_structure(*inclusions)
                print("")
            else:
                print("! Tried Inclusion when V Struct wasn't mounted.\n")                 
    elif op == "analyze": # Analyze the Mounted V Struct.
        if vStructure != None:
            parameters = arguments[1:]
            passers = []
            if "-tmp" in parameters and "-save" in parameters:
                vStructure.analyze(True, False)
            elif "-save" in parameters:
                vStructure.analyze(save=False)
            elif "-tmp" in parameters:
                vStructure.analyze(True)
            else:
                vStructure.analyze()
        else:
            print("! Tried Analyzing when V Struct wasn't mounted.\n")
    elif op == "run": # Run the Mounted V Struct.
        parameters = arguments[1:]
        if vStructure != None:
            target_files = []
            time = None
            force = False
            for parameter in parameters:
                if parameter == "-time":
                    time = parameters[parameters.index(parameter)+1]
                    time = int(time)
                if parameter == "-f":
                    force = True
            for parameter in parameters:
                if parameter[0] != "-":
                    target_files.append(parameter)
                else:
                    break
            if not time:
                time = 20
            vStructure.run(time, *target_files, force=force)
        else:
            print("! Tried Running when V Struct wasn't mounted.\n")
    elif op == "status": # Check the current structure.
        parameters = arguments[1:]
        if len(parameters) != 0:
            passes = []
            if "-vhdl" in parameters: passes.append(".vhdl")
            if "-included" in parameters: passes.append("included")
            if "-others" in parameters: passes.append("others")
            print("passes")
            print(vStructure.to_string(*passes))
        else:
            print(vStructure.to_string())

exit(0)