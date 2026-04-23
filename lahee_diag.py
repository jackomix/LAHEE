#!/usr/bin/env python3
import urllib.request
import os
import subprocess

def test_connection():
    print("--- LAHEE Connectivity Diagnostic ---")
    
    # 1. Test Loopback Interface
    print("Testing internal network (127.0.0.1)...")
    try:
        url = "http://127.0.0.1:8000/dorequest.php?r=laheeinfo"
        response = urllib.request.urlopen(url, timeout=2)
        print(f"SUCCESS: Server responded with code {response.getcode()}")
    except Exception as e:
        print(f"FAILED: Could not reach LAHEE server. Error: {e}")
        print("Tip: Make sure the LAHEE Server is running!")

    # 2. Check for running RetroArch
    print("\nChecking for running RetroArch processes...")
    try:
        ps = subprocess.check_output(["ps", "aux"]).decode()
        ra_procs = [line for line in ps.split('\n') if 'retroarch' in line.lower()]
        if ra_procs:
            for p in ra_procs:
                print(f"FOUND: {p}")
        else:
            print("NONE: RetroArch is not currently running.")
    except:
        print("Could not check process list.")

    # 3. Verify Patch in common paths
    print("\nChecking patch status of binaries...")
    paths = ["/usr/bin/retroarch", "/opt/retroarch/bin/retroarch", "/roms/tools/retroarch", "retroarch"]
    for p in paths:
        if os.path.exists(p):
            try:
                with open(p, 'rb') as f:
                    data = f.read()
                    if b"127.0.0.1:8000" in data:
                        print(f"PATCHED: {p}")
                    elif b"retroachievements.org" in data:
                        print(f"NOT PATCHED: {p}")
                    else:
                        print(f"UNKNOWN: {p} (Binary looks modified or different)")
            except:
                print(f"ERROR: Could not read {p}")

    print("\n--- Diagnostic Complete ---")

if __name__ == "__main__":
    test_connection()
