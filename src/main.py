import os
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
        pass

    


exit(0)
print("V Structer: Insira uma opção:\n1 - path\n2 - analyze\n3 - check\n4 - tmp\n5 - run\n6 - exit")
while option != "exit":
    option = input("> ")
    if option == "path":
        arg = valid_path(input("\nInsira o path da estrutura vhdl:\n>"))
        if (arg != False) and (os.path.isdir(arg)):
            vStructure = VStruct(arg, tmp=False)
            print("\nCurrent path:", arg)
        else:
            print("\nCaminho não existente ou não é um diretório válido.")
    elif option == "analyze":
        if vStructure != None:
            vStructure.analyze()
        else:
            print("\nNenhuma estrutura foi especificada. Utilize 'path' para especificar um diretório com uma estrutura de arquivos VHDL.")
    elif option == "check":
        if vStructure != None:
            print(vStructure.to_string("all", "others"))
        else:
            print("\nNenhuma estrutura foi especificada. Utilize 'path' para especificar um diretório com uma estrutura de arquivos VHDL.")
    elif option == "tmp":
        if vStructure != None:
            tmp = not tmp
            vStructure.change_tmp(tmp)
            print("\nTMP Flag changed to:", tmp)
        else:
            print("\nNenhuma estrutura foi especificada. Utilize 'path' para especificar um diretório com uma estrutura de arquivos VHDL.")
    elif option == "run":
        if vStructure != None:
            target_file = input("Insira o arquivo que deseja simular: ")
            time = input("Insira o tempo em ns da simulação: ")
            vStructure.run(target_file, time)
        else:
            print("\nNenhuma estrutura foi especificada. Utilize 'path' para especificar um diretório com uma estrutura de arquivos VHDL.")
    if not option in ["path", "analyze", "check", "tmp", "run", "exit"]:
        print("\n-> Opção inválida")
    else:
        print("\nV Structer: Insira uma opção:\n1 - path\n2 - analyze\n3 - check\n4 - tmp\n5 - run\n6 - exit")
        
