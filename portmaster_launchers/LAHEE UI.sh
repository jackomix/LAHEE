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
[ -f "${controlfolder}/mod_${CFW_NAME}.txt" ] && source "${controlfolder}/mod_${CFW_NAME}.txt"
get_controls

GAMEDIR="/$directory/ports/LAHEE"
cd $GAMEDIR

# Set SDL variables for R36S/ArkOS
export SDL_VIDEODRIVER=kmsdrm
export SDL_VIDEO_GL_DRIVER=/usr/lib/libGL.so.1
export SDL_VIDEO_EGL_DRIVER=/usr/lib/libEGL.so.1

# Run the UI script using python3
$ESUDO python3 lahee_ui.py > lahee_ui_sh.log 2>&1

$ESUDO systemctl restart oga_events &
printf "\033c" >> /dev/tty1
