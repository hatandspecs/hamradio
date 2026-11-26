#!/usr/bin/env python3
"""Parse the published tables, re-run the script, diff every cell."""
import importlib.util, io, re, subprocess, sys
spec = importlib.util.spec_from_file_location("c", "assets/code/choke_s2p.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
D = "assets/data/diy-common-mode-chokes/"
art = io.open("_articles/diy-transmit-grade-choke.md", encoding="utf-8").read()

def run(files, bands, avg):
    cmd = [sys.executable, "assets/code/choke_s2p.py",
           "--ref", D + "fixture-short-reference.s2p", "--bands", bands]
    if avg:
        cmd.append("--avg")
    cmd += [D + f for f in files]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    rows = {}
    for ln in out.splitlines():
        mm = re.match(r"\s+([\d.]+) MHz\s+(-?\d+)\s+([+-]\d+)\s+(\d+)\s+"
                      r"(-?[\d.]+)\s+(-?\d+)\s+(\S+ \S+|\S+)\s\s+(.+?)\s*$", ln)
        if mm:
            rows[mm.group(1)] = mm   # later blocks (the average) win
    return rows

def cells(row):
    return [c.strip().replace("**", "").replace("&#124;", "|")
            for c in row.strip().strip("|").split("|")]

fails = passes = 0
def chk(label, got, want):
    global fails, passes
    if str(got) == str(want):
        passes += 1
    else:
        fails += 1
        print(f"  MISMATCH {label}: article {want!r} vs script {got!r}")

print("Table 1: two sections, averaged")
r1 = run(["choke-two-sections-a.s2p", "choke-two-sections-b.s2p"],
         "1.9,3.5,7.2,10.1,14.3,18.1,21.2,24.9,28.4", True)
for line in art.splitlines():
    if re.match(r"\|\s*[\d.]+ MHz \|", line) and line.count("|") == 8:
        c = cells(line)
        band = c[0].replace(" MHz", "")
        if band not in r1:
            print("  no script row for", band); fails += 1; continue
        g = r1[band]
        chk(f"{band} R", g.group(2), c[1].replace(",", ""))
        chk(f"{band} X", g.group(3), c[2].replace(",", "").replace("+", "+"))
        chk(f"{band} |Z|", g.group(4), c[3].replace(",", ""))
        chk(f"{band} Rp", g.group(6), c[4].replace(",", ""))
        want = c[6]
        got = g.group(8)
        if want == "band-limited, X over R":
            want = "band-limited, X dominates"
        chk(f"{band} grade", got, want)

print("Table 2: one section")
r2 = run(["cmc-2026-11-08-one-section.s2p"], "3.5,7.2,14.3,21.2,28.4", False)
for line in art.splitlines():
    if re.match(r"\|\s*[\d.]+ MHz \|", line) and line.count("|") == 6:
        c = cells(line)
        band = c[0].replace(" MHz", "")
        if band not in r2:
            print("  no script row for", band); fails += 1; continue
        g = r2[band]
        chk(f"{band} R", g.group(2), c[1].replace(",", ""))
        chk(f"{band} X", g.group(3), c[2].replace(",", ""))
        chk(f"{band} |Z|", g.group(4), c[3].replace(",", ""))
        chk(f"{band} Rp", g.group(6), c[4].replace(",", ""))

print(f"\n{passes} cells match, {fails} differ")
sys.exit(1 if fails else 0)
