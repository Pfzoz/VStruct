main.py includes a program designed to easily manipulate the VStruct object through commands
vstruct.py contains the main design of this project, the VStruct class, which handles directories structures with VHDL files.

howto ---
The program is defined around 6 commands:
path - asks for a input to a directory path that
leads to the folder with VHDL structuties
analyze - analyzes all .vhdl files encountered in the
path defined by 'path'
check - shows a current status of the .vhdl files found
the simulation path, currently default to the first
directory in 'path', and other informations.
tmp - enables temporary flag, making so that 'analyze' descards the path
it creates for the simulation. tmp is disabled during run
run - asks for the file to be ran through the ghdl -r command
and for its simulation time duration in ns
exit - exits
