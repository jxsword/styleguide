#!/usr/bin/env python3
"""分析 docs/ 译文中暴露给 Jekyll Liquid 解析、且未被 {% raw %} 保护的 {{ / {% 位置。"""
import re, glob, os

files = []
for f in glob.glob("docs/**/*.md", recursive=True):
    if os.path.basename(f) in ("_config.yml", "index.md"):
        continue
    files.append(f)

fence_re = re.compile(r"^\s*(```|~~~)")
raw_open_re = re.compile(r"{%\s*raw\s*%}")
raw_close_re = re.compile(r"{%\s*endraw\s*%}")
trigger_re = re.compile(r"\{\{|\{%")

for f in files:
    lines = open(f, encoding="utf-8").read().split("\n")
    raw_open = False
    in_fence = False
    exposed = []
    for i, ln in enumerate(lines, 1):
        if raw_open_re.search(ln):
            raw_open = True
            continue
        if raw_close_re.search(ln):
            raw_open = False
            continue
        m = fence_re.match(ln)
        if m:
            in_fence = not in_fence
            continue
        if trigger_re.search(ln) and not raw_open:
            exposed.append((i, "fence" if in_fence else "inline", ln.strip()[:95]))
    if exposed:
        print("### " + f.replace("docs/", ""))
        for i, kind, snip in exposed:
            print(f"   L{i:5d} [{kind}] {snip}")
