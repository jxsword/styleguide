#!/usr/bin/env python3
"""把待翻译的上游文档按标题边界切分为片段，便于并行翻译后无损合并。

输出：.tools/parts/<doc-stem>/part-NN.md 与 .tools/parts/manifest.json
切分严格按行切片，片段顺序拼接后与源文件逐字节一致。
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARTS = ROOT / ".tools" / "parts"
MAX_ROWS = 1500

HEADING = re.compile(r"^#{1,3}\s")
FENCE = re.compile(r"^\s{0,3}(?:```|~~~)")


def heading_points(lines: list[str]) -> list[int]:
    points = [0]
    in_fence = False
    for i, line in enumerate(lines):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence and HEADING.match(line):
            points.append(i)
    points.append(len(lines))
    return sorted(set(points))


def cut(lines: list[str]) -> list[tuple[int, int]]:
    points = heading_points(lines)
    segments: list[tuple[int, int]] = []
    start = 0
    while start < len(lines):
        target = min(start + MAX_ROWS, len(lines))
        candidates = [p for p in points if start < p <= target]
        end = candidates[-1] if candidates else target
        if end <= start:
            end = target
        segments.append((start, end))
        start = end
    return segments


def main() -> None:
    import yaml

    state = yaml.safe_load((ROOT / "translation" / "state.yaml").read_text(encoding="utf-8"))
    pending = [k for k, v in state["files"].items() if v.get("status") != "done"]

    PARTS.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, list[dict]] = {}
    total_parts = 0

    for rel in pending:
        # 用二进制解码 + 二进制写出，避免 Windows 文本模式自动把 \n 转成 \r\n
        raw = (ROOT / rel).read_bytes().decode("utf-8")
        lines = raw.splitlines(keepends=True)
        segs = cut(lines)
        stem = rel.replace("/", "__").removesuffix(".md")
        outdir = PARTS / stem
        outdir.mkdir(parents=True, exist_ok=True)
        entries = []
        for n, (start, end) in enumerate(segs, 1):
            name = f"part-{n:02d}.md"
            (outdir / name).write_bytes("".join(lines[start:end]).encode("utf-8"))
            entries.append({"part": name, "dir": stem, "start": start, "end": end})
            total_parts += 1
        manifest[rel] = entries

    (PARTS / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"documents={len(pending)} parts={total_parts}")
    for rel, entries in manifest.items():
        print(f"  {rel:32s} {len(entries)} part(s)")


if __name__ == "__main__":
    main()
