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

# Standard IP address
TARGET_HOST = b"http://127.0.0.1:8000"

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

    # v11: The "Slash-Padding" Method
    # Web servers treat http://127.0.0.1:8000////dorequest.php exactly the same
    # as http://127.0.0.1:8000/dorequest.php.
    
    # We replace the domain and pad with slashes to maintain exact character length.
    PATTERNS = [
        (b"https://retroachievements.org", b"http://127.0.0.1:8000////////"), # 29 -> 29
        (b"http://retroachievements.org",  b"http://127.0.0.1:8000///////"),  # 28 -> 28
        (b"media.retroachievements.org",   b"127.0.0.1:8000/badge//////")   # 27 -> 27
    ]
    
    for old, new in PATTERNS:
        if old in new_data:
            count = new_data.count(old)
            print(f"  Found {count} instances of: {old.decode()}")
            print(f"  Replacing with slash-padded: {new.decode()}")
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
    print("LAHEE RetroArch Nuclear Patcher (v11 - Slash Padding Mode) starting...")
    targets = find_targets()
    print(f"Found {len(targets)} potential binaries to check.")
    
    patched_count = 0
    for t in targets:
        if patch_file(t):
            patched_count += 1
            
    print(f"\nPatch Complete. Total files patched: {patched_count}")
