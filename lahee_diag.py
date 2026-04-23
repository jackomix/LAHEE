#!/usr/bin/env python3
import urllib.request
import os
import subprocess

def test_url(name, url):
    print(f"  Testing {name}...")
    try:
        # We add a dummy parameter to verify it can still parse query strings
        full_url = f"{url}?r=laheeinfo"
        response = urllib.request.urlopen(full_url, timeout=2)
        code = response.getcode()
        if code == 200:
            print(f"    [ OK ] Success (200)")
            return True
        else:
            print(f"    [ !! ] Failed with code: {code}")
    except Exception as e:
        print(f"    [FAIL] Error: {e}")
    return False

def test_connection():
    print("--- LAHEE PADDING COMPATIBILITY TEST ---")
    
    # 1. Basic Process Check
    try:
        ps = subprocess.check_output(["ps", "aux"]).decode().lower()
        if "lahee" not in ps:
            print("\n[!!] WARNING: LAHEE Server process not detected in memory.")
            print("     Please start the server before running this test.\n")
    except:
        pass

    # 2. Test Variations
    print("\nChecking which padding methods the server accepts:")
    
    base = "http://127.0.0.1:8000"
    methods = [
        ("Standard",      f"{base}/dorequest.php"),
        ("Slash Padding", f"{base}////dorequest.php"),
        ("Dot Padding",   f"{base}/./././dorequest.php"),
        ("Zero Port",     "http://127.0.0.1:00000008000/dorequest.php"),
        ("Zero IP",       "http://127.000.000.001:8000/dorequest.php"),
        ("Mangled Path",  f"{base}/././././dorequest.php")
    ]

    results = []
    for name, url in methods:
        results.append(test_url(name, url))

    print("\n--- Summary ---")
    for i in range(len(methods)):
        status = "[ PASS ]" if results[i] else "[ FAIL ]"
        print(f"{status} {methods[i][0]}")

    print("\n--- Diagnostic Complete ---")
    print("Use the method that says [ PASS ] for the best results.")

if __name__ == "__main__":
    test_connection()
