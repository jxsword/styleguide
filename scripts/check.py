#!/usr/bin/env python3
"""校验译文与上游 Markdown 的结构一致性。

用法：python scripts/check.py [文件路径 ...]
不传参数时校验 state.yaml 中 status=done 的全部条目。
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT
TARGET = ROOT / "docs"

PATTERNS = {
    "headings": re.compile(r"^\s{0,3}#{1,6}\s", re.M),
    "fences": re.compile(r"^\s{0,3}(?:```|~~~)", re.M),
    "html_tags": re.compile(r"<[a-zA-Z/][^>]*>", re.M),
    "links": re.compile(r"\]\([^)]*\)", re.M),
    "link_defs": re.compile(r"^\s{0,3}\[[^\]]+\]:", re.M),
    "table_rows": re.compile(r"^\s*\|", re.M),
    "hr": re.compile(r"^\s{0,3}(?:---+|\*\*\*+|___+)\s*$", re.M),
}


def counts(text: str) -> dict[str, int]:
    return {k: len(p.findall(text)) for k, p in PATTERNS.items()}


def blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def check(rel: str) -> tuple[bool, str]:
    src, dst = SOURCE / rel, TARGET / rel
    if not src.exists():
        return False, f"{rel}: 上游源文件不存在"
    if not dst.exists():
        return False, f"{rel}: 译文缺失"
    a, b = counts(src.read_text(encoding="utf-8")), counts(dst.read_text(encoding="utf-8"))
    diffs = [f"{k} {a[k]}->{b[k]}" for k in a if a[k] != b[k]]
    if diffs:
        return False, f"{rel}: 结构不一致 " + ", ".join(diffs)
    return True, f"{rel}: OK (blob {blob_sha(src)[:12]})"


def main() -> int:
    if len(sys.argv) > 1:
        targets = sys.argv[1:]
    else:
        import yaml
        state = yaml.safe_load((ROOT / "translation" / "state.yaml").read_text(encoding="utf-8"))
        targets = [k for k, v in state["files"].items() if v.get("status") == "done"]

    failed = 0
    for rel in targets:
        ok, msg = check(rel)
        print(("  " if ok else "! ") + msg)
        failed += 0 if ok else 1
    print(f"\n{len(targets) - failed}/{len(targets)} 通过")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
