#!/usr/bin/env python3
"""按 .tools/parts/manifest.json 把已翻译片段合并回 docs/<原路径>。

片段文件命名：part-NN.md -> part-NN.zh.md。使用二进制拼接，保留原始换行符。
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARTS = ROOT / ".tools" / "parts"


def main() -> None:
    manifest = json.loads((PARTS / "manifest.json").read_text(encoding="utf-8"))
    missing: list[str] = []
    merged = 0

    for rel, entries in manifest.items():
        chunks: list[bytes] = []
        for entry in entries:
            zh = PARTS / entry["dir"] / (entry["part"].removesuffix(".md") + ".zh.md")
            if not zh.exists():
                missing.append(str(zh.relative_to(ROOT)))
                break
            chunks.append(zh.read_bytes())
        if len(chunks) != len(entries):
            continue
        out = ROOT / "docs" / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(b"".join(chunks))
        merged += 1

    print(f"merged={merged}/{len(manifest)}")
    if missing:
        print(f"missing={len(missing)}")
        for item in missing:
            print("  " + item)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
