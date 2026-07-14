#!/usr/bin/env python3
"""Probe constitution source for exact section-header character offsets and section text."""
import re
from pathlib import Path

src = Path(r"C:\Users\krist\AppData\Local\hermes\cache\web\www.gutenberg.org-48ab8abb9a.md")
text = src.read_text(encoding="utf-8", errors="ignore")

patterns = [
    ("Preamble", re.compile(r"^We the people of the United States", re.MULTILINE)),
    ("Article I", re.compile(r"^Article\s+(I|1)$", re.MULTILINE)),
    ("Article I Section 1", re.compile(r"^Section\s+1\.\s+(.*)$", re.MULTILINE)),
    ("Article I Section 8", re.compile(r"^Section\s+8\.\s+(.*)$", re.MULTILINE)),
    ("Article I Section 9", re.compile(r"^Section\s+9\.\s+(.*)$", re.MULTILINE)),
    ("Article I Section 10", re.compile(r"^Section\s+10\.\s+(.*)$", re.MULTILINE)),
    ("Article II", re.compile(r"^Article\s+(II|2)$", re.MULTILINE)),
    ("Article III", re.compile(r"^Article\s+(III|3)$", re.MULTILINE)),
    ("Article IV", re.compile(r"^Article\s+(IV|4)$", re.MULTILINE)),
    ("Article V", re.compile(r"^Article\s+(V|5)$", re.MULTILINE)),
    ("Article VI", re.compile(r"^Article\s+(VI|6)$", re.MULTILINE)),
    ("Article VII", re.compile(r"^Article\s+(VII|7)$", re.MULTILINE)),
]

found = {}
for name, pat in patterns:
    m = pat.search(text)
    if m:
        start = m.start()
        snippet = text[max(0, start-40):start+100].replace("\n", "↵")
        found[name] = {"start": start, "end": m.end(), "snippet": snippet}
        print(f"{name:25} offset={start:6} snippet={snippet!r}")
    else:
        print(f"{name:25} NOT FOUND")

print("\n--- First 120 chars of Preamble context ---")
for name, info in found.items():
    if name.startswith("Preamble"):
        print(text[info["start"]:info["start"]+120].replace("\n", "↵"))
