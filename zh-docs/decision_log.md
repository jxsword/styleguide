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

## DR-3 2026-11-23 页脚上游提交信息自动生成 [状态:生效]
- 背景：`docs/_layouts/docs.html` 页脚原为硬编码「对应上游提交 7237268（2026-11-09）」，上游同步后须手工改页脚与 state.yaml 两处，易漏易漂移。
- 选项与权衡：A `gen_state.py` 顺带生成 `docs/_data/upstream.yml`、页脚模板读 `site.data.upstream` —— 本地与 Pages 构建一致、数据与模板分离，选用；B 脚本字符串改写布局文件 —— 生成内容混入手工维护模板，易被后续编辑覆盖，弃用；C 运行时由 git 元数据推导（`site.github`）—— Pages 构建环境无 upstream 远端，`build_revision` 是本仓库提交而非上游，语义不可行，弃用。
- 结论：采用 A。数据文件含 commit/short/date/url 四字段；页脚改 Liquid 读取，数据文件缺失时兜底提示运行 `scripts/gen_state.py`。
- 理由：同步流程零新增步骤（`gen_state.py` 本就是第 4 步）；Pages legacy Jekyll 原生支持 `_data/`；页脚哈希顺带变为上游 commit 直链。
- 影响：新增 `docs/_data/` 目录（Jekyll 保留目录，不入 `site.pages`，侧栏无变化）；`translation/state.yaml` 再生成时补回脚本注释头一行。
- 时间/会话：2026-11-23，本次方案确认会话。

## DR-4 2026-11-23 译文目录更名 zh-docs 并切换 Actions 部署 [状态:生效 替代 DR-2 发布源结论]
- 背景：`docs/` 与上游未来可能在根目录新增的同名目录存在碰撞风险；而 Pages legacy 发布目录仅允许 `/` 或 `/docs`（配置文档与 REST API `source.path` 双重限制，官方文档原文），故更名必须伴随发布方式切换。
- 选项与权衡：A 更名 + GitHub Actions（官方 `actions/jekyll-build-pages`，与 legacy 同用 pages-gem，渲染一致）选用；B 保持 `docs/` 不动——碰撞风险仅延迟不消除，弃用；C git 符号链接 `docs → zh-docs` 保 legacy——官方文档明确 legacy 构建不支持符号链接，排除；D 源改 `/`(root) + 维护 exclude——DR-2 已弃用的同路线，排除。
- CI 冲突顾虑消解：上游同步为路径限定式（仅 `*.md`，见 STYLE.md 成文约定），上游 workflow 文件不会进入本仓库；Actions 只执行本仓库分支内的 workflow；workflow 防御性命名 `zh-pages-deploy.yml`。
- 结论：目录 `docs/` → `zh-docs/`（git mv 保留历史，48 文件）；新增 `.github/workflows/zh-pages-deploy.yml`（source_dir 探测式兼容旧目录，切换全程零中断）；更新 check/gen_state/merge_translations/analyze_liquid/build.rb/STYLE.md/index.md 共 7 文件路径引用。
- 理由：`zh-docs` 命名与上游目录空间隔离，消除碰撞隐患；Actions 部署换来源目录自由度与未来构建扩展通道；渲染器与 legacy 同源，行为漂移风险最小。
- 影响：DR-2 的「Deploy from a branch → main:/docs」结论被替代；构建时长约 1 → 2 分钟；线上 URL（baseurl `/styleguide`）不变；本仓库 gh 命令须显式 `-R jxsword/styleguide`（双远程下 gh 会误选 upstream）。
- 时间/会话：2026-11-23，本次方案确认会话。

## DR-5 2026-11-23 工作手册入仓（zh-docs/README.md）与项目记忆持久化 [状态:生效]
- 背景：增量翻译/部署/预览流程此前仅存于 agent 私有记忆（`.workbuddy/memory/`，被 gitignore）与历史对话，换 agent 或换机器即不可恢复；`.tools/`（162MB Ruby 及 49 个用户 gem）同样不入库，项目路径变化即构建能力丢失。
- 选项与权衡（手册位置）：放 `zh-docs/README.md`（用户指定；exclude 防发布）选用；放仓库根其他名字弃用——偏离用户要求。记忆位置：新增仓库根 `project-memory/` 选用（仓库为权威、双写同步）；并入 `zh-docs/` 弃用——发布源不放内部资料；仅留 `.workbuddy/` 弃用——agent 绑定且不入库。
- 依赖全局化：RubyInstaller 3.3.4-1 整体移至 `C:\Users\ysm\tools\`，`.tools/` 原位建 junction（`New-Item -ItemType Junction`，免管理员）指回；`build.rb` 的 `Dir.glob` 穿透 junction 实测有效。过程坑：跨卷 Move-Item 中途失败产生半移动状态，`robocopy /MOVE` 又因长路径/文件占用残留 `share/` 文档（对构建无用），最终删除残留后建 junction 成功。
- 结论：新增 `zh-docs/README.md`（依赖安装含 gem 快照与 build.rb/_config.local.yml 全文、增量翻译、预览、部署、新会话提示词附录）；新增 `project-memory/`（README 约定 + 日志副本，任何 agent 通用）；`zh-docs/_config.yml` exclude 增 `README.md`；`.tools/_config.local.yml` 增 `baseurl: ""` 简化本地预览。
- 影响：`.gitignore` 无变更；线上站点无变化（README 被 exclude）；任何 agent 凭仓库文件可独立完成全流程；本地预览免符号链接（`http://localhost:8124/<页面>`）。
- 时间/会话：2026-11-23，本次方案确认会话。
