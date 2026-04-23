#!/usr/bin/env python3
import os
import shutil

# Targeted paths but also searching recursively in common locations
SEARCH_DIRS = [
    "/usr/bin",
    "/usr/local/bin",
    "/opt/retroarch",
    "/roms/tools",
    "/roms/bin",
    "."
]

TARGET_BASE = b"http://127.0.0.1:8000"
VARIATIONS = [
    b"https://retroachievements.org/",
    b"http://retroachievements.org/",
    b"https://retroachievements.org",
    b"http://retroachievements.org"
]

def find_targets():
    found = set()
    # Hardcoded known paths
    known = [
        "/usr/bin/retroarch",
        "/usr/bin/retroarch32",
        "/opt/retroarch/bin/retroarch",
        "/opt/retroarch/bin/retroarch32",
        "retroarch",
        "retroarch32"
    ]
    for k in known:
        if os.path.exists(k):
            found.add(k)
            
    # Search recursively
    for d in SEARCH_DIRS:
        if not os.path.exists(d):
            continue
        print(f"Searching for retroarch binaries in {d}...")
        for root, dirs, files in os.walk(d):
            # Prune directories to speed up search
            if "games" in dirs: dirs.remove("games")
            if "saves" in dirs: dirs.remove("saves")
            
            for file in files:
                if file.startswith("retroarch") and not file.endswith((".cfg", ".txt", ".sh", ".bak", ".lpl")):
                    found.add(os.path.join(root, file))
    return list(found)

def patch_file(path):
    print(f"Checking {path}...")
    try:
        with open(path, "rb") as f:
            data = f.read()
    except Exception as e:
        print(f"  Error reading file: {e}")
        return False
        
    any_replaced = False
    new_data = data
    
    for url in VARIATIONS:
        if url in new_data:
            count = new_data.count(url)
            print(f"  Found {count} instances of URL: {url.decode()}")
            
            target_url = TARGET_BASE
            if url.endswith(b"/"):
                target_url += b"/"
                
            padding_len = len(url) - len(target_url)
            if padding_len > 0:
                if target_url.endswith(b"/"):
                    padded_target = target_url[:-1] + b"/" * (padding_len + 1)
                else:
                    padded_target = target_url + b"/" * padding_len
            else:
                padded_target = target_url[:len(url)]
                
            print(f"  Replacing with: {padded_target.decode()}")
            new_data = new_data.replace(url, padded_target)
            any_replaced = True
            
    if any_replaced:
        bak_path = path + ".bak"
        if not os.path.exists(bak_path):
            print(f"  Creating backup at {bak_path}")
            shutil.copy2(path, bak_path)
            
        with open(path, "wb") as f:
            f.write(new_data)
        os.chmod(path, 0o755)
        print(f"  Successfully patched {path}!")
        return True
    
    if TARGET_BASE in data:
        print("  Already patched.")
    else:
        print("  No RetroAchievements patterns found.")
    return False

if __name__ == "__main__":
    print("LAHEE RetroArch Nuclear Patcher starting...")
    targets = find_targets()
    print(f"Found {len(targets)} potential binaries to check.")
    
    patched_count = 0
    for t in targets:
        if patch_file(t):
            patched_count += 1
            
    print(f"\nNuclear Patch Complete. Total files patched: {patched_count}")
