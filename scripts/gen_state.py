#!/usr/bin/env python3
"""生成翻译基线元数据：

1. translation/state.yaml —— 基线提交 + 每份源文件的 blob 哈希（增量翻译依据）。
2. docs/_data/upstream.yml —— 供 Jekyll 页脚渲染的上游提交信息（本地与 GitHub Pages 构建一致读取）。
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "translation" / "state.yaml"
DATA_OUT = ROOT / "docs" / "_data" / "upstream.yml"
UPSTREAM_REPO_URL = "https://github.com/google/styleguide"

files = sorted(
    p.relative_to(ROOT).as_posix()
    for p in ROOT.glob("*.md")
) + sorted(
    p.relative_to(ROOT).as_posix()
    for d in ("go", "docguide")
    for p in (ROOT / d).glob("*.md")
)
files = [f for f in files if f not in ("CODE_OF_CONDUCT.md", "README.md")]

# 基线必须是上游 gh-pages 的提交，而不是本地 main 的 HEAD：
# 增量翻译要 diff 的是 upstream 的文档变化。
head = subprocess.check_output(
    ["git", "rev-parse", "upstream/gh-pages"], cwd=ROOT, text=True
).strip()
date = subprocess.check_output(
    ["git", "log", "-1", "--format=%ad", "--date=short", "upstream/gh-pages"],
    cwd=ROOT,
    text=True,
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

# 同步生成 Jekyll 数据文件：页脚“对应上游提交”随基线自动更新，
# 数据与模板分离，本地 build.rb 与 GitHub Pages legacy 构建读取同一份数据。
data_lines = [
    "# 由 scripts/gen_state.py 生成，勿手工编辑。",
    f"commit: {head}",
    f"short: {head[:7]}",
    f"date: {date}",
    f"url: {UPSTREAM_REPO_URL}/commit/{head}",
]
DATA_OUT.parent.mkdir(parents=True, exist_ok=True)
DATA_OUT.write_text("\n".join(data_lines) + "\n", encoding="utf-8")

print(
    f"state.yaml: {len(files)} files, baseline {head[:12]} ({date})"
    f" | docs/_data/upstream.yml updated"
)
