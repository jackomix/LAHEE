#!/usr/bin/env python3
import os
import shutil

# Common paths for RetroArch on dArkOS/ArkOS
RA_PATHS = [
    "/usr/bin/retroarch",
    "/usr/local/bin/retroarch",
    "/opt/retroarch/bin/retroarch"
]

TARGET_BASE = b"http://127.0.0.1:8000"
VARIATIONS = [
    b"https://retroachievements.org/",
    b"http://retroachievements.org/",
    b"https://retroachievements.org",
    b"http://retroachievements.org"
]

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
        
    found_url = None
    for url in VARIATIONS:
        if url in data:
            found_url = url
            break
            
    if not found_url:
        if TARGET_BASE in data:
            print("RetroArch is already patched!")
        else:
            print("Could not find any variation of RetroAchievements URL in the binary. Patching failed.")
            print("Try checking if your RetroArch version uses a different URL or is already patched.")
        return
        
    print(f"Found URL: {found_url.decode()}")
    
    # Determine the target URL based on whether the original had a trailing slash
    target_url = TARGET_BASE
    if found_url.endswith(b"/"):
        target_url += b"/"
        
    # We must pad the target URL to exactly match the length of the original URL to prevent breaking the binary
    padded_target = target_url + b'\x00' * (len(found_url) - len(target_url))
    
    # Replace all instances
    patched_data = data.replace(found_url, padded_target)
    
    with open(ra_path, "wb") as f:
        f.write(patched_data)
        
    # Ensure it's executable
    os.chmod(ra_path, 0o755)
    print("RetroArch successfully patched to use LAHEE!")

if __name__ == "__main__":
    patch_retroarch()
