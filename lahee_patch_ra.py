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

# The "Golden" Padded IP and Port
# http://127.000.000.001:08000 is 28 characters
# https://retroachievements.org is 29 characters
# This allows for surgically perfect length matching

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
    
    # We define precise pairs to maintain exact length
    # No extra slashes or dots needed
    pairs = [
        (b"https://retroachievements.org/dorequest.php", b"http://127.000.000.001:08000/dorequest.php"),
        (b"http://retroachievements.org/dorequest.php",  b"http://127.000.000.001:08000/dorequest.php "), # Add a space if needed
        (b"https://retroachievements.org/",             b"http://127.000.000.001:08000//"),
        (b"http://retroachievements.org/",              b"http://127.000.000.001:08000/ "),
        (b"https://retroachievements.org",              b"http://127.000.000.001:08000/"),
        (b"http://retroachievements.org",               b"http://127.000.000.001:08000 "),
        (b"media.retroachievements.org",                b"127.000.000.001:08000/badge")
    ]
    
    for old, new in pairs:
        # Final length check to be safe
        if len(old) != len(new):
            # Dynamic padding for any missed cases
            if len(new) < len(old):
                new = new + (b"/" * (len(old) - len(new)))
            else:
                new = new[:len(old)]

        if old in new_data:
            count = new_data.count(old)
            print(f"  Found {count} instances of URL: {old.decode()}")
            print(f"  Replacing with: {new.decode()}")
            new_data = new_data.replace(old, new)
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
    print("LAHEE RetroArch Golden Patcher (v4 - Padded IP Mode) starting...")
    targets = find_targets()
    print(f"Found {len(targets)} potential binaries to check.")
    
    patched_count = 0
    for t in targets:
        if patch_file(t):
            patched_count += 1
            
    print(f"\nGolden Patch Complete. Total files patched: {patched_count}")
