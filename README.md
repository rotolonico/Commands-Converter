# Datapack-Converter

Convert Minecraft datapack to command block chains!

## Installation

- Clone/Download the repo
- Open a command line at the folder
- You are all set!

## How to use

- Run `python3 commands_converter.py "datapack_path" x y z`

- Positional arguments:
    - **datapack_path:** Path of the Minecraft datapack to convert
    - **x:** X coordinate of location where command blocks will get placed
    - **y:** Y coordinate of location where command blocks will get placed
    - **z:** Z coordinate of location where command blocks will get placed
- Optional arguments:
    - **-h, --help:** show this help message and exit
    - **-ox OX, -ox OX:** Distance between two command block chains in the world on the X axis. 2 by default
    - **-oy OY, -offset-y OY:** Distance between two command block chains in the world on the Y axis. 2 by default
    - **-r, -commands-per-row:**  Number of command blocks in the same row. 8 by default
    - **-f, -force:** Overwrite existing datapack named 'converter_datapack'. False by default
    - **-d, -delete-datapack:** Automatically delete the converted datapack. Do NOT use this if the datapack contains
      stuff other than functions or you\'ll lose them. False by default
    - **-s, -segment-functions:** Creates a new chain after every function call. This removes race conditions problems
      but decreases code readability and makes chains after a function call run one tick later. False by default.

## How it works

- All functions in the tick.json tag file are converted to repeating always active chains
- All functions in the load.json tag file are converted to impulse always active chains
- All the other functions are converted to impulse needs redstone chains
- All impulse command block chains have `data merge block X Y Z {auto:0b}` at the end (to reset them for the next
  function call)
- Function calls are replaced with `data merge block X Y Z {auto:1b}` syntax
- If -s argument is used, it will also make any commands that come after a function call in a new chain. This is to
  mitigate the problem of function calls executing one tick later due to command blocks limitations.
- It will force load the necessary chunks to keep the commands always loaded

## Why it doesn't work

Unfortunately, in Minecraft, there's no way to remotely activate a command block chain in the same tick.
Using `data merge block X Y Z {auto:1b}`, the chain at X Y Z will be executed only next tick. This behaves differently
from function calls (that are instead executed instantly during the execution of the function caller)
This could create timing inconsistencies and lead to unexpected bugs in your map.
Therefore, this tool, unlike the [commands to datapack one](https://github.com/rotolonico/Datapack-Converter), was made
only for demonstration purposes and shouldn't be used for real projects.
The -s argument could be used to mitigate this problem, but it will have the side effect of making command execution
slower and therefore messing up timing in between separate chains.

## Looking for the opposite conversion?

Check out the [Datapack-Converter](https://github.com/rotolonico/Datapack-Converter) 
