#!/bin/bash

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
source $controlfolder/device_info.txt

# Set directory
PORTDIR="/roms/ports/LAHEE"

cd $PORTDIR

# Execute the application.
# LAHEE is a console app, you might want to run it via gptokeyb so you can kill it with a button combo
$ESUDO chmod +x "$PORTDIR/LAHEE"

$ESUDO kill -9 $(pidof gptokeyb)
$controlfolder/gptokeyb "LAHEE" -c "./lahee.gptk" &
./LAHEE 2>&1 | tee /dev/tty0

$ESUDO kill -9 $(pidof gptokeyb)
$ESUDO systemctl restart oga_events &
printf "\033c" >> /dev/tty1
