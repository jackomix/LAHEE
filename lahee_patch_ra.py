#!/usr/bin/env python3
import os
import shutil

# Common paths for RetroArch on dArkOS/ArkOS
RA_PATHS = [
    "/usr/bin/retroarch",
    "/usr/local/bin/retroarch",
    "/opt/retroarch/bin/retroarch"
]

TARGET_URL = b"http://127.0.0.1:8000"
ORIGINAL_URL = b"https://retroachievements.org"

def patch_retroarch():
    ra_path = None
    for path in RA_PATHS:
        if os.path.exists(path):
            ra_path = path
            break
            
    if not ra_path:
        print("Could not find retroarch executable.")
        return
        
    print(f"Found retroarch at {ra_path}")
    bak_path = ra_path + ".bak"
    
    if not os.path.exists(bak_path):
        print(f"Creating backup at {bak_path}")
        shutil.copy2(ra_path, bak_path)
    else:
        print("Backup already exists. Using existing backup.")
        
    with open(ra_path, "rb") as f:
        data = f.read()
        
    if ORIGINAL_URL not in data:
        if TARGET_URL in data:
            print("RetroArch is already patched!")
        else:
            print("Could not find the RetroAchievements URL in the binary. Patching failed.")
        return
        
    # We must pad the target URL to exactly match the length of the original URL to prevent breaking the binary
    padded_target = TARGET_URL + b'\x00' * (len(ORIGINAL_URL) - len(TARGET_URL))
    
    # Replace all instances
    patched_data = data.replace(ORIGINAL_URL, padded_target)
    
    with open(ra_path, "wb") as f:
        f.write(patched_data)
        
    # Ensure it's executable
    os.chmod(ra_path, 0o755)
    print("RetroArch successfully patched to use LAHEE!")

if __name__ == "__main__":
    patch_retroarch()
