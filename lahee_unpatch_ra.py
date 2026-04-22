#!/usr/bin/env python3
import os
import shutil

RA_PATHS = [
    "/usr/bin/retroarch",
    "/usr/local/bin/retroarch",
    "/opt/retroarch/bin/retroarch"
]

def unpatch_retroarch():
    ra_path = None
    for path in RA_PATHS:
        if os.path.exists(path):
            ra_path = path
            break
            
    if not ra_path:
        print("Could not find retroarch executable.")
        return
        
    bak_path = ra_path + ".bak"
    
    if os.path.exists(bak_path):
        print(f"Restoring backup from {bak_path} to {ra_path}")
        shutil.copy2(bak_path, ra_path)
        os.chmod(ra_path, 0o755)
        print("RetroArch successfully unpatched!")
    else:
        print("No backup found. Cannot unpatch.")

if __name__ == "__main__":
    unpatch_retroarch()
