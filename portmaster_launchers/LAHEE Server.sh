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

GAMEDIR="/$directory/ports/LAHEE"
cd $GAMEDIR

# Ensure loopback interface is up for offline play
$ESUDO ip link set lo up
$ESUDO ifconfig lo 127.0.0.1 up > /dev/null 2>&1

# Flush potential firewall blocks for port 8000
$ESUDO iptables -I INPUT -p tcp --dport 8000 -j ACCEPT 2>/dev/null

# Give execute permissions
$ESUDO chmod +x "$GAMEDIR/LAHEE"

# Kill existing instance if running
$ESUDO killall -9 LAHEE 2>/dev/null

# Start in background, send output to a log file
$ESUDO nohup ./LAHEE > lahee.log 2>&1 &

# Brief message on screen
printf "\033c" >> /dev/tty1
echo "LAHEE Server started in background." >> /dev/tty1
sleep 2
printf "\033c" >> /dev/tty1
