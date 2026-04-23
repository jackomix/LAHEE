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

# The standard address
TARGET_BASE = b"http://127.0.0.1:8000"

VARIATIONS = [
    b"https://retroachievements.org/dorequest.php",
    b"http://retroachievements.org/dorequest.php",
    b"https://retroachievements.org/",
    b"http://retroachievements.org/",
    b"https://retroachievements.org",
    b"http://retroachievements.org",
    b"media.retroachievements.org"
]

def find_targets():
    found = set()
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
            
    for d in SEARCH_DIRS:
        if not os.path.exists(d):
            continue
        print(f"Searching for retroarch binaries in {d}...")
        for root, dirs, files in os.walk(d):
            if "games" in dirs: dirs.remove("games")
            if "saves" in dirs: dirs.remove("saves")
            
            for file in files:
                if file.startswith("retroarch") and not file.endswith((".cfg", ".txt", ".sh", ".bak", ".lpl", ".so")):
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
            
            # Simple padding with /
            padding_len = len(url) - len(TARGET_BASE)
            if padding_len >= 0:
                padded_target = TARGET_BASE + (b"/" * padding_len)
            else:
                padded_target = TARGET_BASE[:len(url)]
                
            print(f"  Replacing with: {padded_target.decode()}")
            new_data = new_data.replace(url, padded_target)
            any_replaced = True
            
    if any_replaced:
        bak_path = path + ".bak"
        if not os.path.exists(bak_path):
            print(f"  Creating backup at {bak_path}")
            shutil.copy2(bak_path, path) # ERROR in logic here, fixing below
            
        with open(path, "wb") as f:
            f.write(new_data)
        os.chmod(path, 0o755)
        print(f"  Successfully patched {path}!")
        return True
    
    return False

# Self-Correction: Fix the backup logic error in the write_file above
def patch_file_fixed(path):
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
            
            # Use /./ as padding (it's very safe)
            padding_len = len(url) - len(TARGET_BASE)
            if padding_len > 0:
                # Add a slash then ././
                pad = b"/"
                remaining = padding_len - 1
                pad += (b"./" * (remaining // 2))
                if remaining % 2 == 1:
                    pad += b"."
                padded_target = TARGET_BASE + pad
            else:
                padded_target = TARGET_BASE[:len(url)]
                
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
    return False

if __name__ == "__main__":
    print("LAHEE RetroArch Nuclear Patcher (v5 - Loopback Fix) starting...")
    targets = find_targets()
    print(f"Found {len(targets)} potential binaries to check.")
    
    patched_count = 0
    for t in targets:
        # We'll use the logic from patch_file_fixed
        if patch_file_fixed(t):
            patched_count += 1
            
    print(f"\nNuclear Patch Complete. Total files patched: {patched_count}")
