#!/usr/bin/env python3

import platform
import os
import shutil
import subprocess
from colorama import Fore, init # for text coloring
init(autoreset=True) 

cyan = Fore.CYAN

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True).strip()
    except Exception:
        return ""

def get_distro():
    paths = ["/etc/os-release", "/usr/lib/os-release"]
    for p in paths:
        if os.path.exists(p):
            data = {}
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if not line or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    v = v.strip().strip('"').strip("'")
                    data[k] = v
            name = data.get("NAME", "")
            ver = data.get("VERSION", "")
            pretty = data.get("PRETTY_NAME", "")
            if pretty:
                return pretty
            if name and ver:
                return f"{name} {ver}"
            if name:
                return name
    return ""

def get_kernel():
    return platform.release()

def get_uptime():
    if os.path.exists("/proc/uptime"):
        try:
            with open("/proc/uptime", "r", encoding="utf-8") as f:
                seconds = float(f.read().split()[0])
            seconds = int(seconds)
            days, rem = divmod(seconds, 86400)
            hours, rem = divmod(rem, 3600)
            minutes, _ = divmod(rem, 60)
            if days > 0:
                return f"{days}d {hours}h"
            return f"{hours}h {minutes}m"
        except Exception:
            pass
    if shutil.which("uptime"):
        out = run_cmd(["uptime", "-p"])
        if out:
            return out
    return ""

def get_shell():
    return os.environ.get("SHELL", "")

def get_cpu():
    if os.path.exists("/proc/cpuinfo"):
        try:
            with open("/proc/cpuinfo", "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if line.lower().startswith("model name"):
                        return line.split(":", 1)[1].strip()
        except Exception:
            pass
    return platform.processor() or ""

def get_ram():
    if os.path.exists("/proc/meminfo"):
        try:
            with open("/proc/meminfo", "r", encoding="utf-8", errors="ignore") as f:
                mem_total_kb = None
                mem_avail_kb = None
                for line in f:
                    if line.startswith("MemTotal:"):
                        mem_total_kb = int(line.split()[1])
                    elif line.startswith("MemAvailable:"):
                        mem_avail_kb = int(line.split()[1])
                    if mem_total_kb is not None and mem_avail_kb is not None:
                        break
            if mem_total_kb is not None and mem_avail_kb is not None:
                total_gb = mem_total_kb / (1024 * 1024)
                avail_gb = mem_avail_kb / (1024 * 1024)
                return f"{total_gb:.2f} GB total, {avail_gb:.2f} GB available"
        except Exception:
            pass
    return ""

def main():

    print()
    print(f"{cyan}Hostname{Fore.RESET}: {platform.node()}")
    print(f"{cyan}OS{Fore.RESET}: {get_distro() or (platform.system() + ' ' + platform.version())}")
    print(f"{cyan}Kernel{Fore.RESET}: {get_kernel()}")
    print(f"{cyan}Uptime{Fore.RESET}: {get_uptime() or 'Unknown'}")
    print(f"{cyan}CPU{Fore.RESET}: {get_cpu() or 'Unknown'}")
    print(f"{cyan}RAM{Fore.RESET}: {get_ram() or 'Unknown'}")
    print(f"{cyan}Shell{Fore.RESET}: {get_shell() or 'Unknown'}")

    xdg_session = os.environ.get("XDG_SESSION_TYPE", "")
    desktop = os.environ.get("XDG_CURRENT_DESKTOP", "")
    if xdg_session or desktop:
        print(f"{cyan}Session{Fore.RESET}: {xdg_session} {desktop}".strip())

    print()

if __name__ == "__main__":
    main()
