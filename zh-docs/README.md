# Google 风格指南中文翻译 — 工作手册

Google Style Guides 非官方中文翻译，站点：<https://jxsword.github.io/styleguide/>。
本文件是完整工作手册：任何 AI 编码助手或维护者凭本仓库即可独立完成**依赖安装、上游增量翻译、本地预览、部署验证**，不依赖任何历史会话。所有路径均为相对仓库根的相对路径。

## 仓库结构

| 路径 | 内容 |
|---|---|
| `/`（根目录 `*.md`、`go/`、`docguide/`） | 上游英文原文（同步目标，勿手改） |
| `zh-docs/` | 中文译文 + Jekyll 站点源（本目录即发布源） |
| `zh-docs/decision_log.md` | 决策日志（DR-1 起） |
| `translation/` | 翻译规范（STYLE.md、GLOSSARY.md）与基线（state.yaml） |
| `scripts/` | 校验与辅助脚本（check.py、gen_state.py 等） |
| `.github/workflows/zh-pages-deploy.yml` | 站点部署流水线（GitHub Actions） |
| `.tools/`（不入库） | 本地构建工具链（Ruby 便携版等），见「依赖安装」 |
| `project-memory/` | 项目记忆（任何 agent 会话开始先读，见该目录 README） |
| `.site-local/`（不入库） | 本地构建产物 |

## 依赖安装

### 1. Ruby 3.3.4（Jekyll 构建）

使用 RubyInstaller 3.3.4-1 便携版（`.7z` 免安装），与 GitHub Pages 的 Ruby 3.3.4 对齐。两种安装方式任选：

**方式 A：全局安装（推荐，多项目共享）**

1. 下载：<https://rubyinstaller.org/downloads/> → `RubyInstaller-3.3.4-1-x64.7z`（或直接用 `.tools/rubyinstaller-3.3.4-1-x64.7z` 存档）。
2. 解压到全局目录，例如 `C:\Users\ysm\tools\rubyinstaller-3.3.4-1-x64\`。
3. 在项目的 `.tools/` 下建 junction 指回全局（免管理员权限，PowerShell）：

   ```powershell
   New-Item -ItemType Junction -Path "<项目>\.tools\rubyinstaller-3.3.4-1-x64" -Target "C:\Users\ysm\tools\rubyinstaller-3.3.4-1-x64"
   ```

**方式 B：项目局部安装**：解压 `.7z` 直接到 `.tools/rubyinstaller-3.3.4-1-x64/`（体积约 162MB，仅本机有效）。

**安装 gem**（构建脚本按 `$LOAD_PATH` 加载，无需 Bundler）。优先常规安装（新机器缺编译工具链时可能因 native 扩展失败，此时用下面的快照恢复）：

```bash
# 用解压目录内的 gem（bash 中 PATH 未含 ruby 时需经 ruby -S 调用）
.tools/rubyinstaller-3.3.4-1-x64/bin/ruby \
  .tools/rubyinstaller-3.3.4-1-x64/bin/gem install \
  jekyll:3.10.0 jekyll-theme-primer jekyll-optional-front-matter \
  jekyll-relative-links jekyll-default-layout jekyll-titles-from-headings \
  jekyll-readme-index jekyll-seo-tag --no-document
```

失败时的确定性恢复（逐 gem `--ignore-dependencies`，规避 MSYS2 native 编译；清单与当前环境一致，共 49 个）：

```bash
# gems.lock 每行形如 "name (version)"，逐行转 install
sed -E 's/^([a-zA-Z0-9_.-]+) \(([^ )]+).*/\1 -v \2/' gems.lock | while read -r n v; do
  .tools/rubyinstaller-3.3.4-1-x64/bin/ruby \
    .tools/rubyinstaller-3.3.4-1-x64/bin/gem install "$n" -v "$v" --ignore-dependencies --no-document
done
```

<details>
<summary>gems.lock（当前环境已装 gem 快照，点击展开）</summary>

```text
addressable (2.8.7)
colorator (1.1.0)
concurrent-ruby (1.3.8)
debug (1.9.1)
ffi (1.17.4 x64-mingw-ucrt)
forwardable-extended (2.6.0)
i18n (1.15.2)
jekyll (3.10.0)
jekyll-default-layout (0.1.5)
jekyll-optional-front-matter (0.3.2)
jekyll-readme-index (0.3.0)
jekyll-relative-links (0.6.1)
jekyll-sass-converter (1.5.2)
jekyll-seo-tag (2.8.0)
jekyll-theme-primer (0.6.0)
jekyll-titles-from-headings (0.5.3)
jekyll-watch (2.2.1)
kramdown (2.4.0)
kramdown-parser-gfm (1.1.0)
liquid (4.0.4)
listen (3.10.1)
matrix (0.4.2)
mercenary (0.3.6)
minitest (5.20.0)
net-ftp (0.3.4)
net-imap (0.4.9.1)
net-pop (0.1.2)
net-smtp (0.4.0.1)
nokogiri (1.19.7 x64-mingw-ucrt)
pathutil (0.16.2)
power_assert (2.0.3)
prime (0.1.2)
public_suffix (6.0.2)
racc (1.7.3)
rake (13.1.0)
rb-fsevent (0.11.2)
rb-inotify (0.11.1)
rbs (3.4.0)
rexml (3.2.8)
rouge (3.30.0)
rss (0.3.0)
safe_yaml (1.0.5)
sass (3.7.4)
sass-listen (4.0.0)
terminal-table (1.8.0)
test-unit (3.6.1)
typeprof (0.21.9)
unicode-display_width (1.8.0)
webrick (1.9.2)
```

</details>

### `.tools/Gemfile` 来源与用途

**来源**：手工创建，记录本地构建的**顶层直接依赖**（非完整依赖树）：

```ruby
source 'https://rubygems.org'
gem 'github-pages', '232', group: :jekyll_plugins
```

**用途**：
- 给 **Bundler** 用（`bundle install`），但本项目**未使用 Bundler**——`build.rb` 通过 `$LOAD_PATH` 直接把已解压 gem 的 `lib/` 加载到 Ruby 进程，完全绕过 Bundler。
- 保留它的唯一价值：**作为“需安装哪些 gem 的清单”存档**。README「依赖安装」节的 `gem install …` 命令行清单，就是从此 Gemfile 推导而来（展开 `github-pages:232` 的运行时依赖后去重，得到 49 个 gem 的快照）。
- **不删除也可**；若以后改用 `bundle install --path vendor/bundle` 标准流程，它就是入口文件。

### 2. Python 3 + PyYAML（校验与基线脚本）

```bash
python -m pip install pyyaml
python scripts/check.py   # 验证：输出 28/28 通过
```

### 3. git 与 gh CLI

- git：常规安装。
- gh CLI：<https://cli.github.com/>。**注意**：本仓库有 `origin`（jxsword/styleguide）与 `upstream`（google/styleguide，仅 fetch）两个远程，gh 会把基准仓库误解析为上游，**所有 gh 命令必须显式加 `-R jxsword/styleguide`**。

### 4. `.tools/` 重建附录（构建脚本不在仓库中）

`.tools/` 整体被 `.gitignore` 排除，换机器或项目路径变化后需重建。除 Ruby 与 gem 外，还需以下两个文件（全文如下，复制即可）。

`.tools/build.rb`：

```ruby
# Windows 原生本地构建：与 GitHub Pages 的 Jekyll 3.10.0 环境对齐。
# 通过 $LOAD_PATH 直接加载 gem，绕开仅 jekyll serve 需要的 native 依赖
# (http_parser.rb 需要 MSYS2 编译，便携版 Ruby 无开发工具链)。
# 该脚本只用于本地验证，不随仓库发布。

root = File.expand_path("..", __dir__)
ruby_dir = Dir.glob(File.join(root, ".tools", "rubyinstaller-*-x64")).first
gems_dir = File.join(ruby_dir, "lib", "ruby", "gems", "3.3.0", "gems")

Dir.glob(File.join(gems_dir, "*", "lib")).each do |lib|
  $LOAD_PATH.unshift(lib)
end

require "jekyll"
require "jekyll/commands/build"

# Pages 构建器通过 Bundler 的 :jekyll_plugins 组隐式加载这些默认插件。
# 本地用 $LOAD_PATH 加载时需显式 require，否则无 front matter 的 .md 不会被渲染。
%w[
  jekyll-optional-front-matter
  jekyll-relative-links
  jekyll-default-layout
  jekyll-titles-from-headings
  jekyll-readme-index
  jekyll-seo-tag
].each do |name|
  require name
end

# primer 主题的 default.html 使用 jekyll-github-metadata 提供的 github_edit_link 标签。
# 本地验证不加载该插件（需 GitHub API），注册空实现以完成 layout 解析。
class LocalGithubEditLink < Liquid::Tag
  def render(_context)
    ""
  end
end
Liquid::Template.register_tag("github_edit_link", LocalGithubEditLink)

options = {
  "source"      => File.join(root, "zh-docs"),
  "destination" => File.join(root, ".site-local"),
  "config"      => [
    File.join(root, "zh-docs", "_config.yml"),
    File.join(root, ".tools", "_config.local.yml"),
  ],
  "safe"        => true,
  "incremental" => false,
}

puts "Ruby   #{RUBY_VERSION}"
puts "Jekyll #{Jekyll::VERSION}"
puts "Source #{options["source"]}"
puts "-" * 60

Jekyll::Commands::Build.process(Jekyll.configuration(options))
puts "-" * 60
puts "Build finished."
```

`.tools/_config.local.yml`：

```yaml
# 本地构建专用：模拟 GitHub Pages 构建器隐式注入的默认主题。
# 正式 zh-docs/_config.yml 不写 theme，与上游保持一致。
theme: jekyll-theme-primer

# GitHub Pages 构建器隐式启用的默认插件，本地需显式列出
plugins:
  - jekyll-optional-front-matter
  - jekyll-relative-links
  - jekyll-default-layout
  - jekyll-titles-from-headings
  - jekyll-readme-index
  - jekyll-seo-tag

# 本地预览简化：baseurl 置空后产物为根路径，直接 `python -m http.server --directory .site-local`
# 打开 http://localhost:8124/cppguide.html 即可，无需符号链接。
# 仅本地生效；线上 baseurl 由 zh-docs/_config.yml（/styleguide）控制。
baseurl: ""
url: ""
```

另需空桩目录 `.tools/msys2/usr/bin/`（内放空的 `msys-2.0.dll` 文件即可）与 `.tools/parts/`（仅翻译分片时用，见下文）。

#### `msys-2.0.dll`（空文件）的真实作用

**位置**：`.tools/msys2/usr/bin/msys-2.0.dll`（0 字节空文件）。

**作用**：**欺骗 `http_parser.rb` 等 native gem 的运行时探测，使其误以为 MSYS2 已安装，从而跳过“加载 `msys-2.0.dll` 失败 → 尝试编译 native 扩展”的分支。**

背景：
- RubyInstaller 便携版不带 MSYS2 工具链，无法编译 C 扩展。
- `http_parser.rb`（jekyll 依赖链中）在 `require` 时会 `FindLibrary('msys-2.0.dll')`；找不到就回退到“编译 native extension”，导致 `gem install` 或 `require` 报错。
- 因为我们用 `$LOAD_PATH` 直接加载**已预编译好的 gem**（gem 包里已含 `x64-mingw-ucrt` 预编译二进制），根本不需要 MSYS2 编译。放一个空桩文件，让探测“找到文件”（Windows `LoadLibrary` 只检查文件存在性，不校验内容），从而跳过编译分支，直接用预编译二进制。

**验证**：删掉该文件后跑 `build.rb`，会在 `require 'http_parser'` 时抛 `LoadError: cannot load such file -- msys-2.0.dll` 或触发编译尝试失败。**此文件必须保留。**

### `.tools/parts/` 目录：来源、现状与后续处理

**来源**：初次全量翻译时，`scripts/split_for_translation.py` 将超 1700 行的大文件按逻辑块切片生成。每个大文件产生：
- 英文切片：`part-01.md`、`part-02.md` …（原文分段）
- 中文切片：`part-01.zh.md`、`part-02.zh.md` …（并行翻译产出）
- 清单：`manifest.json`（记录每文件的切片边界 `start`/`end` 行号与目录映射）

现状（实测）：**90 个文件、3.2 MB**，包含 `cppguide`（5 片）、`go/best-practices`（3 片）、`go/decisions`（1 片）、`docguide/style`（1 片）等的中英切片。**所有译文已通过 `merge_translations.py` 无损合并回 `zh-docs/`**（如 `cppguide.md` 5949 行 = 5 片之和），译文完整无缺。

**下次增量翻译是否需要**：
- **不需要**。现有文件的增量修改直接对已合并的 `zh-docs/<文件>.md` 做 diff 落笔，完全不依赖 `.tools/parts/`。
- **上游新增大文件**（>1700 行）时：重新运行 `split_for_translation.py` 会**自动重建**目录结构与切片，覆盖旧内容（或先手动 `rm -rf .tools/parts` 再跑）。
- `manifest.json` 仅在**合并阶段**被 `merge_translations.py` 读取，合并完成后即无用。

**可删除吗**：**可删除**（`rm -rf .tools/parts`），不影响任何后续流程。保留也无害，仅占 3.2 MB 磁盘。

## 上游增量同步流程

### 1. 拉取上游并定位变化

```bash
git fetch upstream
# 基线取 translation/state.yaml 的 baseline 字段，<baseline> 替换为该值
git diff --name-status <baseline> upstream/gh-pages -- '*.md' 'go/*.md' 'docguide/*.md'
```

输出中 `M`=修改（增量翻译）、`A`=新增（全篇翻译）、`D`=删除（下线页面）。
**同步范围仅限上述 `*.md`**；上游的 `.github/`、`assets/`、`include/` 等其他文件一律不拉取（防止误引入上游 CI 等，见 `translation/STYLE.md`）。

### 2. 更新英文源文件

```bash
# M/A 文件：
git checkout upstream/gh-pages -- <文件...>
# D 文件：
git rm <英文文件> zh-docs/<同名译文>
```

### 3. 增量翻译

- 用 `git diff <baseline> upstream/gh-pages -- <文件>` 查看英文改动，把同等改动落到 `zh-docs/` 同名译文。
- 遵守 `translation/STYLE.md`（与上游逐段对应、代码块与 HTML 原样保留、中英文间距等）与 `translation/GLOSSARY.md`（术语表）。
- **Liquid 冲突**：改动段落中出现 `{{` 或 `{%` 的内容（尤其代码块）必须用 `{% raw %}…{% endraw %}` 包裹，否则 Jekyll 会当作模板标签解析并丢弃内容；注意 `{% raw %}` 不可嵌套。可用 `python scripts/analyze_liquid.py` 复查。
- 大文件新增可切片并行：`python scripts/split_for_translation.py` 切片 → 翻译 → `python scripts/merge_translations.py` 合并（清单在 `.tools/parts/manifest.json`）。
- 侧栏导航（`zh-docs/_includes/sidebar.html` 读 `site.pages` 自动生成）与页脚上游提交（读 `zh-docs/_data/upstream.yml`）均自动更新，无需手改。
- **特例**：上游若新增根目录/`go/`/`docguide/` 之外的 `.md` 目录，需把该目录加进 `scripts/gen_state.py` 的扫描列表；上游若改动其 `_config.yml`，需比对 `zh-docs/_config.yml`。

### 4. 校验、更新基线、部署

```bash
python scripts/check.py        # 结构一致性校验，必须全部通过
python scripts/gen_state.py    # 再生成基线 state.yaml 与 zh-docs/_data/upstream.yml
git add -A
git commit -m "translate: sync upstream <上游短哈希>"
git push origin main           # Actions（zh-pages-deploy.yml）自动构建部署，约 2 分钟
```

部署验证：

```bash
gh run list --workflow=zh-pages-deploy.yml -R jxsword/styleguide --limit 3
curl -s -o /dev/null -w "%{http_code}\n" https://jxsword.github.io/styleguide/cppguide.html
```

## 本地预览

```bash
# 构建（Ruby 在全局时，把前半段替换为全局 ruby 路径）
.tools/rubyinstaller-3.3.4-1-x64/bin/ruby .tools/build.rb

# 预览（本地构建配置 baseurl 为空，产物为根路径）
python -m http.server 8124 --directory .site-local
# 浏览器打开 http://localhost:8124/cppguide.html
```

- **禁止直接双击（`file://`）打开产物**：页面资源为根绝对路径，`file://` 下 CSS/JS 全部 404，`site.js` 不执行，侧栏/搜索/行号/复制按钮/主题切换全部失效。
- 线上地址带 `/styleguide` 前缀（`zh-docs/_config.yml` 的 `baseurl: /styleguide`），本地预览不带——差异仅来自本地叠加配置 `.tools/_config.local.yml`（`baseurl: ""`），不影响部署。
- 若本地配置未含 `baseurl: ""`（旧环境）：建符号链接后在仓库根起服务——`ln -sfn "$(pwd)/.site-local" styleguide && python -m http.server 8124`，访问 `http://localhost:8124/styleguide/cppguide.html`。

## 部署机制

- GitHub Pages 设置：**Source = GitHub Actions**（`build_type: workflow`；2026-11 起替代早期 legacy `/docs` 模式，因 legacy 发布目录仅允许 `/` 或 `/docs`，无法使用自定义目录名 `zh-docs`）。
- 流水线 `.github/workflows/zh-pages-deploy.yml`：push 到 `main` 或手动触发 → `actions/jekyll-build-pages`（与 legacy 同用 pages-gem，渲染一致；源目录探测式：存在 `zh-docs` 用之）→ upload/deploy-pages。
- 线上 URL 恒为 `https://jxsword.github.io/styleguide/`（URL 由 `zh-docs/_config.yml` 的 `baseurl` 决定，与发布方式无关）。

## 项目记忆与决策

- **任何 agent 会话开始先读 `project-memory/`**（约定见其 README）；完成工作后按约定追加当日日志并同步回本目录。
- 重大决策（含背景/选项/结论）见 `zh-docs/decision_log.md`：DR-1 仓库拓扑、DR-2 发布源与检索、DR-3 页脚自动化、DR-4 目录更名与 Actions 部署、DR-5 本手册与记忆持久化。

## 附录：新会话执行增量翻译的提示词

将下述提示词整段发给任何 AI 编码助手即可执行一次上游增量同步（提示词自包含，配合本仓库文件即可工作）：

```text
你在仓库 jxsword/styleguide 的本地工作区内，执行「Google 风格指南中文翻译」的上游增量同步任务。
工作区结构：仓库根是上游英文源（*.md、go/、docguide/）；zh-docs/ 是中文译文 + Jekyll 站点源；
translation/ 是规范（STYLE.md、GLOSSARY.md）与基线（state.yaml）；scripts/ 是校验与工具脚本；
.github/workflows/zh-pages-deploy.yml 是站点部署流水线。完整手册见 zh-docs/README.md。

开始前先读 zh-docs/README.md 与 translation/state.yaml，并做依赖自检（缺失则按 README「依赖安装」节处理）：
- Ruby 3.3.4 便携版（.tools/rubyinstaller-3.3.4-1-x64/bin/ruby，或其全局安装处的 junction）
- python3 且 import yaml 可用（pip install pyyaml）
- git、gh CLI。注意：本仓库有 origin 与 upstream 双远程，gh 会误选上游仓库，
  所有 gh 命令必须显式带 -R jxsword/styleguide。

执行步骤：
1. git fetch upstream
2. 读 translation/state.yaml 的 baseline 值，运行
   git diff --name-status <baseline> upstream/gh-pages -- '*.md' 'go/*.md' 'docguide/*.md'
   输出中 M=修改、A=新增、D=删除。同步范围仅限这些 .md；严禁拉取上游 .github/、assets/、include/ 等其他文件。
3. M/A 文件：git checkout upstream/gh-pages -- <文件...>；D 文件：git rm 根目录英文文件与 zh-docs/ 同名译文。
4. 增量翻译：用 git diff <baseline> upstream/gh-pages -- <文件> 查看英文改动，把同等改动落到 zh-docs/ 同名译文。
   遵守 translation/STYLE.md（与上游逐段对应、代码块与 HTML 原样保留、中英文之间加半角空格）
   与 translation/GLOSSARY.md（术语表）。
   关键规则：改动段落中出现 {{ 或 {% 的内容（尤其代码块）必须用 {% raw %}…{% endraw %} 包裹，
   否则 Jekyll 会当作 Liquid 模板丢弃内容；{% raw %} 不可嵌套。
   大文件新增可先 python scripts/split_for_translation.py 切片翻译，再 python scripts/merge_translations.py 合并。
5. python scripts/check.py 必须全部通过（结构一致性校验）。
6. python scripts/gen_state.py —— 更新基线 state.yaml 与 zh-docs/_data/upstream.yml（页脚自动更新）。
   若上游新增了根目录/go/docguide 之外的 .md 目录，先把该目录加入 scripts/gen_state.py 的扫描列表再执行本步。
7. git add -A && git commit -m "translate: sync upstream <上游短哈希>" && git push origin main
   push 后 Actions 自动构建部署（约 2 分钟）。
8. 验证：gh run list --workflow=zh-pages-deploy.yml -R jxsword/styleguide --limit 3 查看构建状态；
   curl -s -o /dev/null -w "%{http_code}" https://jxsword.github.io/styleguide/<变更页面> 应为 200。

补充约定：全程不要 merge upstream 分支（只做路径限定 checkout）；改动重大配置前先读
zh-docs/decision_log.md 与 project-memory/；本地预览方法见 README「本地预览」节。
```
