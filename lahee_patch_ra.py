#!/usr/bin/env python3
import os
import shutil

# Common paths for RetroArch on dArkOS/ArkOS
RA_PATHS = [
    "retroarch", # Check current directory (for testing/local)
    "retroarch32",
    "/usr/bin/retroarch",
    "/usr/local/bin/retroarch",
    "/opt/retroarch/bin/retroarch",
    "/opt/retroarch/bin/retroarch32"
]

TARGET_BASE = b"http://127.0.0.1:8000"
# Order matters: check longer patterns first to avoid partial matches
VARIATIONS = [
    b"https://retroachievements.org/",
    b"http://retroachievements.org/",
    b"https://retroachievements.org",
    b"http://retroachievements.org"
]

def patch_file(path):
    if not os.path.exists(path):
        return False
        
    print(f"Found retroarch at {path}")
    bak_path = path + ".bak"
    
    if not os.path.exists(bak_path):
        print(f"Creating backup at {bak_path}")
        shutil.copy2(path, bak_path)
    else:
        print("Backup already exists. Using existing backup.")
        
    with open(path, "rb") as f:
        data = f.read()
        
    any_replaced = False
    for url in VARIATIONS:
        if url in data:
            count = data.count(url)
            print(f"Found {count} instances of URL: {url.decode()}")
            
            # Determine target with trailing slash if needed
            target_url = TARGET_BASE
            if url.endswith(b"/"):
                target_url += b"/"
                
            # Pad with slashes instead of nulls. 
            # This is safer as multiple slashes are ignored by web servers
            # and it doesn't terminate the string if it's part of a longer path.
            padding_len = len(url) - len(target_url)
            if padding_len > 0:
                if target_url.endswith(b"/"):
                    padded_target = target_url[:-1] + b"/" * (padding_len + 1)
                else:
                    padded_target = target_url + b"/" * padding_len
            else:
                padded_target = target_url[:len(url)]
                
            print(f"Replacing with: {padded_target.decode()}")
            data = data.replace(url, padded_target)
            any_replaced = True
            
    if not any_replaced:
        if TARGET_BASE in data:
            print("File is already patched!")
        else:
            print("Could not find any variation of RetroAchievements URL in the binary.")
        return False
        
    with open(path, "wb") as f:
        f.write(data)
        
    # Ensure it's executable
    os.chmod(path, 0o755)
    print(f"Successfully patched {path}!")
    return True

def patch_retroarch():
    found_any = False
    for path in RA_PATHS:
        if patch_file(path):
            found_any = True
            
    if not found_any:
        print("No RetroArch binaries were patched. Check if they exist or are already patched.")

if __name__ == "__main__":
    patch_retroarch()
