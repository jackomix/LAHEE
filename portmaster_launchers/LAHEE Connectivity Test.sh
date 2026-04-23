#!/bin/bash

# Standard PortMaster path discovery
XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}

if [ -d "/opt/system/Tools/PortMaster/" ]; then
  controlfolder="/opt/system/Tools/PortMaster"
elif [ -d "/opt/tools/PortMaster/" ]; then
  controlfolder="/opt/tools/PortMaster"
elif [ -d "$XDG_DATA_HOME/PortMaster/" ]; then
  controlfolder="$XDG_DATA_HOME/PortMaster"
else
  controlfolder="/roms/ports/PortMaster"
fi

source $controlfolder/control.txt

GAMEDIR="/$directory/ports/LAHEE"
cd $GAMEDIR

# Use the terminal for output so the user can read it on the handheld
printf "\033c" >> /dev/tty1
echo "--- LAHEE CONNECTIVITY TEST ---" >> /dev/tty1
echo "Running diagnostics..." >> /dev/tty1

# Run the python script and redirect output to the terminal
$ESUDO python3 lahee_diag.py >> /dev/tty1 2>&1

echo "" >> /dev/tty1
echo "Test Complete." >> /dev/tty1
echo "Returning to menu in 10 seconds..." >> /dev/tty1
sleep 10
printf "\033c" >> /dev/tty1
