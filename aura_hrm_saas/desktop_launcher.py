"""
AuraHR Enterprise — Native Desktop Window Launcher
Launches AuraHR in a dedicated standalone desktop app window (Chromium App Mode).
Includes automatic background server management and port readiness polling.
"""

import os
import sys
import time
import subprocess
import threading
import urllib.request
import webbrowser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_URL = "http://127.0.0.1:5000"


def is_server_running(url=APP_URL, timeout=1.0):
    try:
        req = urllib.request.Request(f"{url}/api/license/status")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status == 200
    except Exception:
        return False


def start_flask_backend():
    """Start Flask backend if not already listening."""
    if is_server_running():
        return None
    
    # Run app.py in a detached background subprocess
    app_script = os.path.join(BASE_DIR, "app.py")
    proc = subprocess.Popen(
        [sys.executable, app_script],
        cwd=BASE_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
    )
    return proc


def wait_for_server(timeout=15):
    """Wait until backend responds."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_server_running():
            return True
        time.sleep(0.4)
    return False


def find_browser_app_executable():
    """Find Microsoft Edge or Chrome executable for standalone app mode."""
    candidates = [
        # Microsoft Edge (Standard on Windows 10/11)
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"),
        # Google Chrome
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        # Brave Browser
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def launch_desktop_window():
    print("[AuraHR Desktop] Initializing AuraHR Enterprise...")
    backend_proc = start_flask_backend()

    print("[AuraHR Desktop] Waiting for local server to be ready...")
    ready = wait_for_server()
    if not ready:
        print("[AuraHR Desktop] Server took too long to start. Opening browser fallback...")

    browser_exe = find_browser_app_executable()

    if browser_exe:
        print(f"[AuraHR Desktop] Launching dedicated App Window via: {browser_exe}")
        # Launch dedicated app window without address bar / tabs
        app_args = [
            browser_exe,
            f"--app={APP_URL}",
            "--window-size=1366,850",
            "--window-position=50,50"
        ]
        try:
            window_proc = subprocess.Popen(app_args)
            window_proc.wait()
        except Exception as e:
            print(f"[AuraHR Desktop] Failed to launch window: {e}, falling back to default browser.")
            webbrowser.open(APP_URL)
    else:
        print("[AuraHR Desktop] Opening in default browser...")
        webbrowser.open(APP_URL)


if __name__ == "__main__":
    launch_desktop_window()
