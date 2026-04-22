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

# Try to find a python environment with pygame
# Default to system python
PYTHON_EXE="python3"

# List of potential PortMaster runtimes to check
# Checking both /roms/ports and /opt paths
RUNTIMES=(
    "/roms/ports/PortMaster/runtimes/python3.11/bin/python3"
    "/roms/ports/PortMaster/runtimes/python3.10/bin/python3"
    "/roms/ports/PortMaster/runtimes/python3.9/bin/python3"
    "/opt/system/Tools/PortMaster/runtimes/python3.11/bin/python3"
    "/opt/tools/PortMaster/runtimes/python3.11/bin/python3"
    "$controlfolder/runtimes/python3.11/bin/python3"
    "$controlfolder/runtimes/python3.10/bin/python3"
    "$controlfolder/runtimes/python3.9/bin/python3"
)

for runtime in "${RUNTIMES[@]}"; do
  if [ -f "$runtime" ]; then
    echo "Checking runtime: $runtime" >> lahee_ui_sh.log
    if "$runtime" -c "import pygame" > /dev/null 2>&1; then
      PYTHON_EXE="$runtime"
      echo "Found pygame in: $PYTHON_EXE" >> lahee_ui_sh.log
      export LD_LIBRARY_PATH="$(dirname "$runtime")/../lib:$LD_LIBRARY_PATH"
      break
    fi
  fi
done

if [ "$PYTHON_EXE" == "python3" ]; then
    echo "Warning: Using system python3, pygame might be missing." >> lahee_ui_sh.log
fi

# Run the UI script
$ESUDO "$PYTHON_EXE" lahee_ui.py >> lahee_ui_sh.log 2>&1

$ESUDO systemctl restart oga_events &
printf "\033c" >> /dev/tty1
