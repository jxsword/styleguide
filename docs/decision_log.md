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

## DR-2 2026-11-11 中文站点发布源与检索方案 [状态:生效]
- 背景：翻译后需用 GitHub Pages 发布中文站；`gh-pages` 分支已作上游原文镜像，且上游渲染依赖 Pages 原生 Jekyll 的隐式主题与默认插件（30 份 .md 均无 front matter）。
- 选项与权衡（发布源）：MkDocs+Actions 弃用——自装构建丢失隐式环境，Material 标注 2027-05-05 EOL；D2 新建 `gh-zh-pages` 弃用——Pages 支持任意分支 `/docs` 源，额外分支徒增跨分支同步；D3 `main:/(root)` 弃用——英文原文会一并发布且 exclude 需随增量维护；D1 `main:/docs` 选用。
- 选项与权衡（检索）：F2 Just the Docs 弃用——主题不在 Pages 白名单且中文搜索弱；F3 Pagefind 弃用——需构建后索引 CLI，回到 Actions 路线；F0 保持原样弃用——无搜索与侧栏；F1 Fuse.js 自建选用。
- 更正：此前「145 个站内 .html 链接需重映射」判断有误，实测站内 0 个（全部为外链）。
- 结论：采用 D1 + F1，即原生 Jekyll / Deploy from a branch → `main:/docs`，配 Fuse.js v7.1.0 自托管与 Liquid 生成的侧栏、搜索索引。
- 理由：零新生成器、零构建脚本、零插件、零新分支；1,798 个 `<div>` 由 kramdown 原生渲染；搜索与侧栏由 Jekyll 内置 defaults/layout/Liquid 补齐。
- 影响：S1 译文目录由 `zh-cn/` 调整为 `docs/`（DR-1 拓扑结论仍生效，仅目录名变更）；新增 `docs/_config.yml`、`_layouts/`、`_includes/`、`assets/` 及上游静态资源副本，S3 需比对上游 `_config.yml` 变更；Pages 设置（Source = Deploy from a branch → main /docs）待确认后启用。
- 时间/会话：2026-11-11，本次调研与方案确认会话。
