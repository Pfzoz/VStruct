# VStruct - Folder system for VHDL compilation


# VStruct
VStruct is a personal quickly-made program and object created with the purpose of facilitating project organization within VHDL projects.

For now, VStruct.run() does not completely integrates itself with VStruct.analyze() + tmp functionality. Overall tmp is for now only details and not completely functional.
Enabling tmp is not recommended overall.
VStruct.run() also runs .analyze() itself, being completly dependent on it.

VStruct is also completely dependent on commands from the open-source analyzer, compiler and simulator GHDL, which can be found here https://github.com/ghdl/ghdl


<img src="./images/vhdl7.jpg">

## How to use?
<code>python3 ./src/main.py</code>
The program is defined around 6 commands:

1. path - asks for a input to a directory path that
2. leads to the folder with VHDL structuties
3. analyze - analyzes all .vhdl files encountered in the
4. path defined by 'path'
5. check - shows a current status of the .vhdl files found the simulation path, currently default to the first directory in 'path', and other informations.
6. tmp - enables temporary flag, making so that 'analyze' descards the path it creates for the simulation. tmp is disabled during run
7. run - asks for the file to be ran through the ghdl -r command and for its simulation time duration in ns
8. exit - exits

## Documentation

<b>main.py</b> includes a program designed to easily manipulate the VStruct object through commands
vstruct.py contains the main design of this project, the VStruct class, which handles directories structures with VHDL files.


