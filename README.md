# VStruct - Folder system for VHDL compilation


# VStruct
VStruct is a personal quickly-made program and object created with the purpose of facilitating project organization within VHDL projects.

VStruct is also completely dependent on commands from the powerful open-source analyzer, compiler and simulator GHDL, which can be found here https://github.com/ghdl/ghdl.


<img src="./images/vhdl7.jpg">

## How to use? (main.py)
<code>python3 ./src/main.py</code>
The program is defined around 6 commands:

1. cd - basic path navigating command
2. mount - incorporates a specific directory to create the V (VHDL) Structure. Parameters: [-c | mounts the current path] [-p | mounts a path based on a given string Ex; -p "/home/user/work/vhdl/"] Flags: [-i | includes words/strings/extensions to be included when looking for paths to incorporate with the V Struct (certain applications require the use of other files such as .mem files, etc) Ex; -i ".mem" ".txt"]
3. analyze - analyzes all the .vhdl files within the mounted structure by creating a simulation directory. Flags: [-tmp | 'temporary' flag; removes the simulation path after analysis] [-save | by default the analysis folder is kept; adding this flag will remove the analysis directory after analysis]
4. run - runs specific file(s) specified through strings. Ex; [run tb_neander.vhdl tb_ula.vhdl -f -time 280]. Flags: [-time | specifies time in ns (default is 20)] [-f | forces the running of the simulation by automatically analyzing regardless of the case, and only not doing so if exatcly not necessary. This is useful to avoid unlikely outcomes such as simulation directory being deleted after a user-done analysis. Its use is always recommended overall.]
5. status - displays the different features of the current mounted V structure. Flags: [-vhdl | shows .vhdl] [-included | shows included files] [-others | shows other minor characteristics]. Displays the whole structure if no flags are specified.
6. exit - exits the program.

## Documentation (vstruct.py)

[WIP]

I currently see no use for VStruct (vstruct.py) as it is - such as a module as an instance - , and probably none for the near future, hence you can use it at your will, but its solutions are still very one-problem-specific-oriented.


