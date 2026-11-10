# Google 风格指南（中文翻译）

本项目是 [google/styleguide](https://github.com/google/styleguide) 的**非官方中文翻译**，对应上游提交 `7237268`（2026-11-09）。规范以英文原文为准。

## 当前状态

- 已完成：仓库拓扑改造（`upstream` 指向 Google、`origin` 指向本 fork）、原生 Jekyll 站点骨架、侧边导航与站内搜索。
- 进行中：30 份文档的首次全量翻译（S2）。译文将按上游目录结构逐份加入，左侧导航与搜索索引会自动收录，无需手工维护清单。
- 左侧搜索框支持中文关键词，按标题与摘要模糊匹配。

## 文档范围

上游共 30 份 Markdown 文档、约 5.2 万行，覆盖 C++、C#、Go、Haskell、HTML/CSS、Java、JavaScript、JSON、Lisp、Objective-C、Python、R、Rust、Shell、TypeScript、Verilog、Vim script、XML，以及 Go 系列与文档指南系列。

## 许可与声明

- 原文文档由 Google LLC 以 [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/) 发布，代码示例为 Apache 2.0；本翻译沿用相同许可。
- 本项目非 Google 官方项目，仅供学习参考。
- 站内搜索使用自托管的 [Fuse.js](https://www.fusejs.io/) v7.1.0（Apache-2.0），许可文本见仓库 `docs/assets/js/FUSE-LICENSE.txt`。

## 相关决策

仓库 `docs/decision_log.md` 记录了 DR-1（仓库拓扑）与 DR-2（发布源与检索方案）。
