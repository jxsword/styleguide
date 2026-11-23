# Google 的 R 风格指南

R 是一种主要用于统计计算和图形的
高级编程语言。R 编程风格指南的目标是让我们的 R 代码
更易于阅读、共享和验证。

Google R 风格指南是 Hadley Wickham 所著
[Tidyverse 风格指南](https://style.tidyverse.org/) 的一个分支（fork），
[许可证](https://creativecommons.org/licenses/by-sa/2.0/)。Google 的修改
是与内部 R 用户社区协作完成的。本文档其余部分
说明 Google 与 Tidyverse 指南的主要差异，
以及存在这些差异的原因。

Google 对每个签入的文件都使用 [styler](https://github.com/r-lib/styler) 包，
以确保代码一致性，并帮助评审者专注于更
重要的问题。

<!-- mdformat off -->
* TOC
{:toc}
<!-- mdformat on -->

## 语法

### 命名约定

Google 倾向于用 `BigCamelCase` 标识函数，以便清楚地
将它们与其他对象区分开来。

<div class='goodcode'></div>

```r
DoNothing <- function() {
  return(invisible(NULL))
}
```

私有函数的名称应以点开头。这有助于说明
函数的来源及其预期用途。

<div class='goodcode'></div>

```r
.DoNothingPrivately <- function() {
  return(invisible(NULL))
}
```

我们此前曾推荐用 `dot.case` 命名对象。现在我们正逐步放弃
这一做法，因为它会与 S3 方法产生混淆。

### 不要使用 attach()

使用 `attach()` 时，产生错误的可能性非常多。

## 管道

### 右向赋值

我们不支持使用右向赋值。

<div class='badcode'></div>

```r
iris %>%
  dplyr::summarize(max_petal = max(Petal.Width)) -> results
```

这一约定与其他语言中的实践有显著差别，
并且让人更难在代码中看出对象是在哪里定义的。例如，搜索
`foo <-` 比同时搜索 `foo <-` 和 `-> foo`（可能跨行
拆分）更容易。

### 使用显式返回

不要依赖 R 的隐式返回特性。最好明确表达你
要 `return()` 一个对象的意图。

<div class='goodcode'></div>

```r
AddValues <- function(x, y) {
  return(x + y)
}
```

<div class='badcode'></div>

```r
AddValues <- function(x, y) {
  x + y
}
```

### 限定命名空间

用户应对所有外部函数显式限定命名空间。

<div class='goodcode'></div>

```r
purrr::map()
```

我们不鼓励使用 `@import` Roxygen 标签把所有函数引入
NAMESPACE。Google 拥有非常庞大的 R 代码库，导入所有函数
会带来过大的名称冲突风险。

虽然使用 `::` 会有轻微的性能开销，但它能让人更容易
理解代码中的依赖关系。这条规则有一些例外。

*   中缀函数（`%name%`）始终需要被导入。
*   某些 `rlang` 代词，尤其是 `.data`，需要被导入。
*   来自 R 默认包的函数，包括 `datasets`、`utils`、
    `grDevices`、`graphics`、`stats` 和 `methods`。如有需要，可以用 `@import`
    导入整个包。

导入函数时，把 `@importFrom` 标签放在 Roxygen 头部中，
位于使用外部依赖的函数的上方。

## 文档

### 包级文档

所有包都应有一个包文档文件，放在
`packagename-package.R` 文件中。

## 错误

### 项目符号的使用

在生成错误信息时，相比 unicode，我们更偏好 ASCII 风格的项目符号（`*`）。
