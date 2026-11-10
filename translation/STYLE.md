# 翻译规范（S2 全量翻译）

译文是 `google/styleguide` 最新代码的逐行对应中文版，文件名与目录结构与上游完全一致，统一放在 `docs/` 下。

## 必须原样保留，不得改写

- 代码块（围栏及其中全部内容）、内联代码及其中文本。
- 所有 HTML 标签、属性、`<div>` 块、`<a name="...">` 锚点、`<style>` 块。上游 30 份文档含约 1,798 个 `<div`、2,103 处内联标签，Jekyll/kramdown 依赖 `parse_block_html` 渲染。
- Markdown 链接目标、图片路径、引用式链接定义、锚点（`#...`）。
- 标题层级与顺序、列表符号与缩进、表格语法、分隔线。
- 文件头部的 HTML 注释（如 `<!--* toc_depth: 3 *-->`）。
- 命令、标识符、API 名称、语言关键字、URL。

## 只翻译

- 自然语言叙述：正文、标题、列表项文字、表格单元格中的自然语言、HTML 标签之间的文字。
- 代码注释中的自然语言可译，但不得改动代码结构。

## 术语

- 统一采用 `translation/GLOSSARY.md`。
- 专有名词不译：C++、Python、Abseil、RTTI、RAII、constexpr、lint、Google Style Guide 等。
- 少见术语首次出现可用「中文（English）」形式。

## 排版

- 中文与英文/数字之间加一个半角空格；中文标点用全角。
- 不新增、不删除、不合并段落；与上游逐段对应，便于后续 `git diff -U0` 做段落级增量重译。
- 不在译文内添加 front matter 或额外说明（版本对应关系由 `translation/state.yaml` 记录）。
- 保留上游页面内的 `<style>` 块与所有内联 CSS。
