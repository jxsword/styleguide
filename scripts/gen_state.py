#!/usr/bin/env python3
"""生成 translation/state.yaml：记录基线提交与每份源文件的 blob 哈希。"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "translation" / "state.yaml"

files = sorted(
    p.relative_to(ROOT).as_posix()
    for p in ROOT.glob("*.md")
) + sorted(
    p.relative_to(ROOT).as_posix()
    for d in ("go", "docguide")
    for p in (ROOT / d).glob("*.md")
)
files = [f for f in files if f not in ("CODE_OF_CONDUCT.md", "README.md")]

head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
date = subprocess.check_output(
    ["git", "log", "-1", "--format=%ad", "--date=short"], cwd=ROOT, text=True
).strip()

lines = [
    "# 翻译基线。由 scripts/gen_state.py 生成，勿手工编辑。",
    f"baseline: {head}",
    f"baseline_date: {date}",
    "source_root: .",
    "target_root: docs",
    "files:",
]
for rel in files:
    data = (ROOT / rel).read_bytes()
    sha = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    target = ROOT / "docs" / rel
    status = "done" if target.exists() else "pending"
    lines.append(f"  {rel}:")
    lines.append(f"    blob: {sha}")
    lines.append(f"    status: {status}")

OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"state.yaml: {len(files)} files, baseline {head[:12]} ({date})")
