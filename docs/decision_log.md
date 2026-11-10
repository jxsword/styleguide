# 决策日志

## DR-1 2026-11-11 google/styleguide 中文翻译仓库拓扑 [状态:生效]
- 背景：需完整翻译上游最新代码（gh-pages `7237268`，2026-11-09）的 30 份 .md / 51,869 行；首次全量、后续仅翻增量，译文同样用 git 管理，google/styleguide 作为 upstream。经全网调研，无覆盖最新代码的完整中文版。
- 选项与权衡：
  - A 独立新仓库 + upstream 仅作 fetch：仓库最干净、只存译文；弃用——无 merge-base，基线追踪完全依赖 state.yaml，上游对象仍会进入 .git。
  - B 现有 clone 改造为 fork 模型：`origin` 改名 `upstream`、自有仓库设为 `origin`，`main` 保留上游历史，译文镜像到 `zh-cn/`；选用。
  - C 同路径覆盖根目录英文：路径最短；弃用——每次合并上游均全量冲突、原文丢失，增量不可持续。
- 结论：采用 B。
- 理由：上游关系、merge-base、增量 diff 均由 git 原生能力承担，元数据最轻，最贴合「添加为上游仓库」的要求。
- 影响：新增 `zh-cn/`、`translation/`、`scripts/`、`docs/`；`origin` 改指自有仓库，`upstream` 禁推送；本地 .git 含上游 705 次提交、约 5 MB；译文须遵守上游 CC BY 3.0 / Apache 2.0 并标注非官方翻译。
- 时间/会话：2026-11-11，本次调研与方案确认会话。
