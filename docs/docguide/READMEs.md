# README 文件

README 是对某个目录内容的简短概述。当你查看该目录的
内容时，文件内容会显示在 GitHub 和 Gitiles 中。
README 文件为浏览你代码的人提供关键信息，尤其是初次
使用的用户。

本文档介绍如何创建便于以 markdown 阅读的 README 文件。

<!-- mdformat off -->
* TOC
{:toc}
<!-- mdformat on -->

## 可读的 README 文件

**README 文件必须命名为 `README.md`。** 文件名 *必须* 以
`.md` 扩展名结尾，且区分大小写。

例如，查看包含 /README.md 的目录内容时，该文件
会被渲染：

https://github.com/google/styleguide/tree/gh-pages

此外，Gitiles 在显示仓库索引时也会渲染 `README.md`
（`HEAD` 引用处）：

https://gerrit.googlesource.com/gitiles/

## README 应放在哪里

与所有其他 Markdown 文件不同，`README.md` 文件不应放在
你的产品或库的文档目录内。`README.md` 文件应
位于你的产品或库的实际代码库的
顶层目录中。

代码包的所有顶层目录都应保有最新的
`README.md` 文件。对于为其他团队提供接口的包目录，
这一点尤其重要。

## README 中应写什么

至少，你的 `README.md` 文件应包含一个指向面向用户
和/或团队的文档的链接。

每个包级的 `README.md` 都应包含或指向以下
信息：

1.  这个包或库中包含什么，以及它的用途。
1.  联系人。
1.  该包或库是否已被弃用，或是否不适用于
    普遍发布等状态。
1.  如何使用该包或库。示例包括示例代码、可复制的
    `bazel` 命令等。
1.  指向相关文档的链接。
