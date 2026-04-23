#!/usr/bin/env python3
import urllib.request
import os
import subprocess

def test_connection():
    print("Checking LAHEE Server (127.0.0.1:8000)...")
    try:
        # Test basic info endpoint
        url = "http://127.0.0.1:8000/dorequest.php?r=laheeinfo"
        response = urllib.request.urlopen(url, timeout=3)
        print(f"  [ OK ] Server found! Code: {response.getcode()}")
    except Exception as e:
        print(f"  [FAIL] Cannot reach server: {e}")
        print("  Tip: Is 'LAHEE Server' running?")

    print("\nChecking RetroArch Patch Status...")
    paths = [
        "/usr/bin/retroarch",
        "/opt/retroarch/bin/retroarch",
        "/opt/retroarch/bin/retroarch32",
        "retroarch"
    ]
    
    found_any = False
    for p in paths:
        if os.path.exists(p):
            found_any = True
            try:
                with open(p, 'rb') as f:
                    data = f.read()
                    if b"127.0.0.1:8000" in data:
                        print(f"  [ OK ] PATCHED: {p}")
                    elif b"retroachievements.org" in data:
                        print(f"  [ !! ] NOT PATCHED: {p}")
                    else:
                        # Check for older padding styles just in case
                        if b"localhost:8000" in data:
                            print(f"  [OLD] Patch uses localhost: {p}")
                        else:
                            print(f"  [??] Unknown State: {p}")
            except:
                print(f"  [ERR] Permission denied: {p}")

    if not found_any:
        print("  [ !! ] No RetroArch binaries found in standard paths.")

    print("\nChecking for active processes...")
    try:
        ps = subprocess.check_output(["ps", "aux"]).decode().lower()
        if "lahee" in ps:
            print("  [ OK ] LAHEE Server is RUNNING.")
        else:
            print("  [ !! ] LAHEE Server is NOT running.")
            
        if "retroarch" in ps:
            print("  [ OK ] RetroArch is currently RUNNING.")
    except:
        pass

if __name__ == "__main__":
    test_connection()
