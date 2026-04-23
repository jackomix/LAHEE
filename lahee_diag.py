#!/usr/bin/env python3
import urllib.request
import os
import subprocess

def test_connection():
    print("--- LAHEE DEEP DIAGNOSTIC ---")
    
    # 1. Check Interface Status
    print("\n[1/4] Checking Network Interfaces...")
    try:
        ifconfig = subprocess.check_output(["ifconfig"]).decode()
        if "lo:" in ifconfig or "lo " in ifconfig:
            if "UP" in ifconfig and "RUNNING" in ifconfig:
                print("  [ OK ] Internal Loopback (lo) is UP.")
            else:
                print("  [ !! ] Loopback (lo) is DOWN. This is why you get Connection Refused!")
        else:
            print("  [ !! ] Loopback interface not found!")
    except:
        print("  [ ?? ] Could not run ifconfig.")

    # 2. Check Process
    print("\n[2/4] Checking Processes...")
    server_proc = False
    try:
        ps = subprocess.check_output(["ps", "aux"]).decode().lower()
        if "lahee" in ps and "./lahee" in ps:
            print("  [ OK ] LAHEE Server process found.")
            server_proc = True
        else:
            print("  [ !! ] LAHEE Server process NOT found in memory.")
    except:
        print("  [ ?? ] Could not check process list.")

    # 3. Check Server Logs
    print("\n[3/4] Checking Server Logs (lahee.log)...")
    if os.path.exists("lahee.log"):
        try:
            with open("lahee.log", "r") as f:
                lines = f.readlines()
                # Look for bind errors
                found_start = False
                for line in lines[-20:]:
                    if "Starting webserver" in line:
                        print(f"  [ LOG ] {line.strip()}")
                        found_start = True
                    if "Address already in use" in line or "Permission denied" in line:
                        print(f"  [FAIL] BIND ERROR: {line.strip()}")
                if not found_start:
                    print("  [ !! ] No 'Starting webserver' message found in recent logs.")
        except:
            print("  [ ?? ] Could not read lahee.log")
    else:
        print("  [ !! ] lahee.log does not exist.")

    # 4. Connection Test
    print("\n[4/4] Final Connectivity Test...")
    try:
        url = "http://127.0.0.1:8000/dorequest.php?r=laheeinfo"
        response = urllib.request.urlopen(url, timeout=3)
        print(f"  [ SUCCESS ] Server responded! Code: {response.getcode()}")
    except Exception as e:
        print(f"  [ FAILED ] Connection failed: {e}")

    print("\n--- Diagnostic Complete ---")

if __name__ == "__main__":
    test_connection()
