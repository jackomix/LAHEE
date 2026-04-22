#!/bin/bash
# Start LAHEE in the background

XDG_DATA_HOME=${XDG_DATA_HOME:-$HOME/.local/share}

PORTDIR="/roms/ports/LAHEE"
cd $PORTDIR

# Give execute permissions
chmod +x "$PORTDIR/LAHEE"

# Kill existing instance if running
killall -9 LAHEE 2>/dev/null

# Start in background, send output to a log file
nohup ./LAHEE > lahee.log 2>&1 &

echo "LAHEE Server started in background."
sleep 2
