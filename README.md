# AASMA-2021
AASMA-2021 SmartCabs Multi-Agent System Project

# How to run the system

1. Open a command line and run the provided ```main.py``` file, doing so will start the system's starting configuration stage where you'll need to provide values for each of the requested parameters

# Starting configuration

1. Enter the **grid size**, that is the length of the environment's grid's edge. Since the developed system deals only with square grids, type only a single integer and it'll be used for horizontal and vertical length. The grid size needs to be **an even number between 6 and 16**. After this value is provided a new window will pop up showing the visual representation of the environment which will be constantly updated throughout the program's execution time.

2. Enter the **type of agent** that you wish to use. The different types of agent's are described by the system's output and numbered from 1 to 4, type the number corresponding to the one you wish to use.

3. Enter the **number of taxis**. This number must be **no more than 4 taxis per quadrant at maximum**. 

4. Enter each of the **taxi's coordinates**. Type two integers, the x coordinate and the y coordinate separated by a space. The only accepted values are integers within the range ***(0, grid_size - 1)***

5. Choose if you want **random client generation** or not.
    1. If you select the random client generation, you'll need to select which of the listed quadrants will have a higher concentration of new clients

6. Insert the **execution time**, an integer which is the number of timesteps you wish the program to run for.

# During execution time

1. The program will now start running, giving you the option to exit at each timestep. If you wish to exit the program, type **exit**, if not simply hit **ENTER** to continue to the next timestamp.

2. If the random generation option was not selected, you will be asked if you want to insert a new client or not, type **yes** or **no** accordingly. By choosing to insert a client, you will need to provide the client's pickup coordinates and destination coordinates in the same format as the taxi's coordinates.