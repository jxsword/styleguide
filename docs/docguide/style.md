# Markdown 风格指南

Markdown 令人耳目一新之处，很大程度上在于能够书写纯文本并由此获得出色的格式化
输出。为了让下一位作者接手时是一片干净的石板，你的 Markdown 应当尽量保持简洁，
并与整个语料库保持一致，
只要有可能。

我们力求在三个目标之间取得平衡：

1.  *源文本可读且可移植。*
2.  *Markdown 语料库可长期、跨团队维护。*
3.  *语法简单且易于记忆。*

<!-- mdformat off -->
* TOC
{:toc}
<!-- mdformat on -->

<a id="min_doc"></a>

## 最小可行文档

一小批新鲜而准确的文档，胜过一大堆松散、
处于各种失修状态的「文档」集合。

**Markdown 之道** 鼓励工程师对自己的文档负起责任，并怀着与我们维护测试时同样的
热忱让它们保持更新。
请以此为目标。

*   明确你真正需要什么：发布文档、API 文档、测试指南。
*   经常性地、以小批量方式删除无用内容。

<a id="better_best"></a>

## 「更好」胜过「最好」

内部文档评审的标准不同于代码评审的标准。
评审者应当要求改进，但总体而言，
作者应当始终能够援引「更好/最好规则」。

快速迭代是你的朋友。为了获得长期改进，**作者在进行短期改进时必须保持高效**。
为每次 CL 设定更低的标准，这样**才会有更多这样的 CL**
出现。

作为文档 CL 的评审者：

1.  在合理的情况下，立即 LGTM，并相信评论会得到
    妥善的处理。
2.  倾向于建议一种替代方案，而不是留下含糊的评论。
3.  对于重大改动，不如自己发起一个后续 CL。尤其要避免形如
    「你*也*应该……」的评论。
4.  极少数情况下，如果该 CL 确实让文档变得更糟，可暂缓
    提交。要求作者回退也是可以的。

作为作者：

1.  避免在无谓的争论中浪费精力。尽早让步，继续前进。
2.  按需随时引用「更好/最好规则」。

## 大小写

使用产品、工具和二进制文件的原名，保留其
大小写。例如：

```markdown
# Markdown style guide

`Markdown` is a dead-simple platform for internal engineering documentation.
```

而非

<div class='badcode'></div>

```markdown
# markdown bad style guide example

`markdown` is a dead-simple platform for internal engineering documentation.
```

<a id="layout"></a>

## 文档布局

一般来说，文档从下列布局的某种变体中受益：

<div class='goodcode'></div>

```markdown
# Document Title

Short introduction.

[TOC]

## Topic

Content.

## See also

* https://link-to-more-info
```

1.  `# Document title`：第一个标题应当是一级标题，理想情况下
    与文件名相同或几乎相同。第一个一级标题会被用作
    页面的 `<title>`。

2.  `author`：*可选*。如果你想声明对文档的所有权，或者
    你为它感到非常自豪，可以在标题下方加上自己。不过，
    修订历史通常已经足够。

3.  `Short introduction.` 提供该主题高层概述的 1–3 句话。想象
    你自己是一个完全的新手，偶然点开你的「扩展 Foo」文档，
    却不知道你视为理所当然的那些最基本的信息。
    「Foo 是什么？我为什么要扩展它？」

4.  `[TOC]`：如果你使用的托管服务支持目录（例如
    Gitiles），请在简短介绍之后放置 `[TOC]`。参见
    [`[TOC]` 文档][TOC-docs]。

5.  `## Topic`：其余的标题应当从二级开始。

6.  `## See also`：把杂项链接放在底部，供想要了解更多
    或没找到所需内容的用户使用。

<a id="toc"></a>

## 目录

### 使用 `[TOC]` 指令

除非你在笔记本电脑上所有内容都位于「折叠线之上」[^above]，否则请使用
    [`[TOC]` 指令][TOC-docs]。

[TOC-docs]: https://gerrit.googlesource.com/gitiles/+/HEAD/Documentation/markdown.md#Table-of-contents
[^above]: 如果内容在页面首次显示时即可见，则称其位于「折叠线之上」。如果内容
    被隐藏，直到用户在电脑上向下滚动页面，或字面意义上
    展开（如报纸）一份文档时才出现，则称其位于
    「折叠线之下」。

### 将 `[TOC]` 指令置于介绍之后

将 `[TOC]` 指令放在页面介绍之后、第一个
H2 标题之前。例如：

<div class='goodcode'></div>

```markdown
# My Page

This is my introduction **before** the TOC.

[TOC]

## My first H2
```

<div class='badcode'></div>

```markdown
# My Page

[TOC]

This is my introduction **after** the TOC where it should not be.

## My first H2
```

对于以视觉方式阅读你文档的用户来说，`[TOC]` 指令放在何处无关紧要，因为
    Markdown 总是将目录显示在页面顶部
    靠右的位置。然而，当涉及屏幕阅读器或
    键盘控制时，`[TOC]` 的放置位置就很重要了。

这是因为 `[TOC]` 会把目录的 HTML 插入到你 Markdown 文件中包含该
    指令之处的 DOM 里。例如，如果你把指令放在
    文件最底部，屏幕阅读器要读到文档
    末尾才会读到它。

<a id="80"></a>

## 80 字符行宽限制

Markdown 内容遵循 80 字符行宽的残留约定。
为什么？因为这是我们大多数人写代码时的做法。

*   **工具集成**：我们所有的工具都围绕代码设计，因此文档越是按照
    相似规则格式化，这些工具就越好用。例如，
    Code Search 不会软换行。

*   **质量**。工程师在创建和编辑 Markdown 内容时越是沿用他们
    习以为常的编码习惯，质量就越好。Markdown
    利用了我们已有的优秀评审文化。

<a id="80_exceptions"></a>

### 例外

80 字符规则的例外包括：

*   链接
*   表格
*   标题
*   代码块

这意味着包含链接的行可以延伸到第 80 列之外，
    连同相关的标点符号一起：

<div class='goodcode'></div>

```markdown
*   See the
    [foo docs](https://gerrit.googlesource.com/gitiles/+/HEAD/Documentation/markdown.md)
    and find the logfile.
```

不过，请注意链接前后的文本会被换行。

表格也可能很长。不过，有一些
[创建简短、易读表格的最佳实践](#tables)。

<div class='goodcode'></div>

```markdown
Foo                                                                           | Bar | Baz
----------------------------------------------------------------------------- | --- | ---
Somehow-unavoidable-long-cell-filled-with-content-that-simply-refuses-to-wrap | Foo | Bar
```

<a id="trailing"></a>

## 行尾空白

不要使用行尾空白。使用行尾反斜杠来换行。

[CommonMark 规范](http://spec.commonmark.org/0.20/#hard-line-breaks) 规定，
    行尾的两个空格应当插入一个 `<br />` 标签。然而，许多
    目录都有针对行尾空白的预提交检查，而且许多
    IDE 无论如何都会清理它。

请谨慎地使用行尾反斜杠：

<div class='goodcode'></div>

```markdown
For some reason I just really want a break here,\
though it's probably not necessary.
```

最佳实践是根本避免对 `<br />` 的需求。一对换行符
    会创建一个段落标签；请习惯这一点。

<a id="headings"></a>

## 标题

<a id="atx"></a>

### ATX 风格标题

<div class='goodcode'></div>

```markdown
# Heading 1

## Heading 2
```

带有 `=` 或 `-` 下划线的标题维护起来可能令人厌烦，并且
    与其余标题语法不相符。编辑器不得不问：`---` 指的是
    H1 还是 H2？

<div class='badcode'></div>

```markdown
Heading - do you remember what level?
---------
```

### 为标题使用唯一、完整的名称

为每个标题（即使是子节）使用唯一且描述充分的名称。由于
    链接锚点由标题构成，这有助于确保自动生成的
    锚点链接直观且清晰。

例如，不要这样：

<div class='badcode'></div>

```markdown
## Foo
### Summary
### Example
## Bar
### Summary
### Example
```

而应该这样：

<div class='goodcode'></div>

```markdown
## Foo
### Foo summary
### Foo example
## Bar
### Bar summary
### Bar example
```

<a id="heading_spacing"></a>

### 为标题添加间距

建议在 `#` 之后加空格，并在其前后加空行：

<div class='goodcode'></div>

```markdown
...text before.

## Heading 2

Text after...
```

缺少空格会让源代码稍难阅读：

<div class='badcode'></div>

```markdown
...text before.

##Heading 2
Text after...
```

<a id="h1"></a>

### 使用单个 H1 标题

使用单个 H1 标题作为文档的标题。其后的标题应当是
    H2 或更深层。更多信息参见 [文档布局](#layout)。

### 标题与表头的大小写

遵循
[大小写](https://developers.google.com/style/capitalization#capitalization-in-titles-and-headings)
    在
[Google 开发者文档风格指南](https://developers.google.com/style/) 中的指引。

<a id="lists"></a>

## 列表

<a id="numbered-lists"></a>


Markdown 足够智能，能让生成 HTML 正确渲染你的有序列表。对于
    可能变动、尤其是冗长嵌套的有序列表，请使用
    「惰性」编号：

<div class='goodcode'></div>

```markdown
1.  Foo.
1.  Bar.
    1.  Foofoo.
    1.  Barbar.
1.  Baz.
```

不过，如果列表较小且你不打算改动它，则倾向于使用完整的
    编号列表，因为这样在源文件中更易读：

<div class='badcode'></div>

```markdown
1.  Foo.
2.  Bar.
3.  Baz.
```

<a id="nested_lists"></a>

### 嵌套列表间距

嵌套列表时，有序列表和项目符号列表都使用 4 空格缩进：

<div class='goodcode'></div>

```markdown
1.  Use 2 spaces after the item number, so the text itself is indented 4 spaces.
    Use a 4-space indent for wrapped text.
2.  Use 2 spaces again for the next item.

*   Use 3 spaces after a bullet, so the text itself is indented 4 spaces.
    Use a 4-space indent for wrapped text.
    1.  Use 2 spaces with numbered lists, as before.
        Wrapped text in a nested list needs an 8-space indent.
    2.  Looks nice, doesn't it?
*   Back to the bulleted list, indented 3 spaces.
```

下面的写法也能工作，但非常混乱：

<div class='badcode'></div>

```markdown
* One space,
with no indent for wrapped text.
     1. Irregular nesting...
```

即使没有嵌套，使用 4 空格缩进也能让换行文本
    布局保持一致：

<div class='goodcode'></div>

```markdown
*   Foo,
    wrapped with a 4-space indent.

1.  Two spaces for the list item
    and 4 spaces before wrapped text.
2.  Back to 2 spaces.
```

不过，当列表较小、无嵌套且为单行时，两种列表都可以
    仅用一空格：

<div class='goodcode'></div>

```markdown
* Foo
* Bar
* Baz.

1. Foo.
2. Bar.
```

<a id="code"></a>

## 代码

<a id="inline"></a>

### 内联

&#96;反引号&#96; 标识会被原样渲染的 `inline code`。将它们用于
    简短的代码引用、字段名等：

<div class='goodcode'></div>

```markdown
You'll want to run `really_cool_script.sh arg`.

Pay attention to the `foo_bar_whammy` field in that table.
```

在泛指文件类型、而非某个具体已有文件时，
    使用内联代码：

<div class='goodcode'></div>

```markdown
Be sure to update your `README.md`!
```

<a id="code_escape"></a>

### 使用代码区段进行转义

当你不希望文本被当作普通 Markdown 处理时（例如会导致
    错误自动链接的虚假路径或示例 URL），请用反引号将其括起来：

<div class='goodcode'></div>

```markdown
An example Markdown shortlink would be: `Markdown/foo/Markdown/bar.md`

An example query might be: `https://www.google.com/search?q=$TERM`
```

<a id="codeblocks"></a>

### 代码块

对于超过一行的代码引用，请使用围栏代码块：

<div class='goodcode'></div>

````markdown
```python
def Foo(self, bar):
  self.bar = bar
```
````

<a id="declare"></a>

#### 声明语言

显式声明语言是最佳实践，这样语法高亮器
    和下一位编辑者都无需猜测。

<a id="indented_codeblock"></a>

#### 使用围栏代码块而非缩进代码块

4 空格缩进同样会被解释为代码块。然而，我们强烈
    建议对所有代码块使用围栏。

缩进代码块在源代码中有时看起来更整洁，但它们
    有几个缺点：

*   你无法指定语言。某些 Markdown 特性与语言
    说明符相关联。
*   代码块的开始和结束位置不明确。
*   缩进代码块在 Code Search 中更难搜索。

```markdown
You'll need to run:

    bazel run :thing -- --foo

And then:

    bazel run :another_thing -- --bar

And again:

    bazel run :yet_again -- --baz
```

<a id="escape_newlines"></a>

#### 转义换行符

因为大多数命令行片段都是为了直接复制粘贴到终端中，
    最佳实践是对任何换行符进行转义。在
    行尾使用单个反斜杠：

<div class='goodcode'></div>

````markdown
```shell
$ bazel run :target -- --flag --foo=longlonglonglonglongvalue \
  --bar=anotherlonglonglonglonglonglonglonglonglonglongvalue
```
````

<a id="nest_codeblock"></a>

#### 在列表中嵌套代码块

如果你需要在列表中放置代码块，请确保对其进行缩进，
    以免破坏列表：

<div class='goodcode'></div>

````markdown
*   Bullet.

    ```c++
    int foo;
    ```

*   Next bullet.
````

你也可以用 4 空格创建一个嵌套代码块。只需在
    列表缩进的基础上再缩进 4 空格：

<div class='goodcode'></div>

```markdown
*   Bullet.

        int foo;

*   Next bullet.
```

<a id="links"></a>

## 链接

长链接会让源 Markdown 难以阅读，并破坏 80 字符
    换行。**请尽可能缩短你的链接**。

<a id="explicitpaths"></a>

### 为 Markdown 内部的链接使用显式路径

为 Markdown 链接使用显式路径。例如：

<div class='goodcode'></div>

```markdown
[...](/path/to/other/markdown/page.md)
```

你无需使用完整的限定 URL：

<div class='badcode'></div>

```markdown
[...](https://bad-full-url.example.com/path/to/other/markdown/page.md)
```

<a id="relativelinks"></a>

### 除非在同一目录内，否则避免相对路径

相对路径在同一目录内相当安全。例如：

<div class='goodcode'></div>

```markdown
[...](other-page-in-same-dir.md)
[...](/path/to/another/dir/other-page.md)
```

如果需要用 `../` 指定其他目录，请避免相对链接：

<div class='badcode'></div>

```markdown
[...](../../bad/path/to/another/dir/other-page.md)
```

<a id="link_title"></a>

### 使用有意义的 Markdown 链接标题

Markdown 链接语法允许你设置链接标题。请明智地使用它。用户往往
    不细读文档，而是快速浏览。

链接会吸引眼球。但将链接标题设为「这里」「链接」，或只是
    复制目标 URL，对匆忙的读者传达的恰恰是零信息，
    而且浪费空间：

<div class='badcode'></div>

```markdown
See the Markdown guide for more info: [link](markdown.md), or check out the
style guide [here](style.md).

Check out a typical test result:
[https://example.com/foo/bar](https://example.com/foo/bar).
```

相反，先自然地写出句子，然后再回过头用
    链接包裹最恰当的短语：

<div class='goodcode'></div>

```markdown
See the [Markdown guide](markdown.md) for more info, or check out the
[style guide](style.md).

Check out a
[typical test result](https://example.com/foo/bar).
```

<a id="reference_links"></a>

### 谨慎使用引用式链接

对于长链接或图片 URL，你可能需要将链接的使用
    与链接的定义分开，如下所示：

<!-- Known bug: We use a zero-width non-breaking space (U+FEFF) here to prevent -->
<!-- reference links from rendering within code blocks. -->

<div class='goodcode'></div>

```markdown
See the [Markdown style guide][style], which has suggestions for making docs more
readable.

[style]: http://Markdown/corp/Markdown/docs/reference/style.md
```

<a id="reference_links_long"></a>

#### 为长链接使用引用式链接

当链接的长度若在行内会损害周围文本的可读性时，使用
    引用式链接。引用式链接会让源文本中链接的
    目标更难看清，并增加额外的
    语法。

在这个例子中，使用引用式链接并不合适，因为该链接
    还不够长，不至于打断文本的流畅性：

<div class='badcode'></div>

```markdown
The [style guide][style_guide] says not to use reference links unless you have
to.

[style_guide]: https://google.com/Markdown-style
```

不如直接写在行内：

<div class='goodcode'></div>

```markdown
https://google.com/Markdown-style says not to use reference links unless you have to.
```

在这个例子中，链接目标足够长，使用
    引用式链接是合理的：

<div class='goodcode'></div>

```markdown
The [style guide] says not to use reference links unless you have to.

[style guide]: https://docs.google.com/document/d/13HQBxfhCwx8lVRuN2Wf6poqvAfVeEXmFVcawP5I6B3c/edit
```

在表格中更频繁地使用引用式链接。保持表格内容简短尤为重要，因为
    Markdown 不提供在单元格表格中跨多行断行的机制，
    而更小的表格更易读。

例如，下面这个表格的可读性因行内链接而变差：

<div class='badcode'></div>

```markdown
Site                                                             | Description
---------------------------------------------------------------- | -----------------------
[site 1](http://google.com/excessively/long/path/example_site_1) | This is example site 1.
[site 2](http://google.com/excessively/long/path/example_site_2) | This is example site 2.
```

相反，使用引用式链接来保持行宽可控：

<div class='goodcode'></div>

```markdown
Site     | Description
-------- | -----------------------
[site 1] | This is example site 1.
[site 2] | This is example site 2.

[site 1]: http://google.com/excessively/long/path/example_site_1
[site 2]: http://google.com/excessively/long/path/example_site_2
```

<a id="reference_links_dedupe"></a>

#### 使用引用式链接减少重复

当在文档中多次引用同一链接目标时，考虑
    使用引用式链接以减少重复。

<a id="reference_links_define"></a>

#### 在首次使用之后定义引用式链接

我们建议将引用式链接的定义放在下一个标题之前、即它们首次被使用的
    那一节末尾。如果你的编辑器对它们该放在何处有
    自己的主张，不要与之对抗；工具总是赢家。

我们将「节」定义为两个标题之间的所有文本。把引用式链接
    视作脚注，把当前节视作当前页面。

这种安排让在源视图中查找链接目标变得容易，同时保持
    文本流畅、不被杂乱信息干扰。在包含大量引用式链接的
    长文档中，它还能避免文件底部的「脚注过载」，否则会
    让人难以挑出相关链接目标。

这条规则有一个例外：在多个节中使用的引用式链接定义，应当
    放在文档末尾。这能避免
    在某一节被更新或移动时出现悬空链接。

在下面的例子中，引用定义离它首次使用之处很远，
    这让文档更难阅读：

<div class='badcode'></div>

```markdown
# Header

Some text with a [link][link_def].

Some more text with the same [link][link_def].

## Header 2

... lots of text ...

## Header 3

Some more text using a [different_link][different_link_def].

[link_def]: http://reallyreallyreallylonglink.com
[different_link_def]: http://differentreallyreallylonglink.com
```

相反，把它放在首次使用之后的那个标题之前：

<div class='goodcode'></div>

```markdown
# Header

Some text with a [link][link_def].

Some more text with the same [link][link_def].

[link_def]: http://reallyreallyreallylonglink.com

## Header 2

... lots of text ...

## Header 3

Some more text using a [different_link][different_link_def].

[different_link_def]: http://differentreallyreallylonglink.com
```

<a id="images"></a>

## 图片

参见
[image syntax](https://gerrit.googlesource.com/gitiles/+/HEAD/Documentation/markdown.md#Images).

谨慎使用图片，并优先选择简单的截图。本指南的设计理念是：纯文本
    能让用户更快进入沟通的正事，减少读者分心
    与作者拖延。不过，有时展示你的意思
    会非常有帮助。

*   当向读者*展示*某事物比*描述*它更容易时，请使用图片。例如，解释
    如何操作 UI 时，用图片往往比用
    文字更简单。
*   务必提供恰当的文字来描述你的图片。看不见图片的读者
    无法看到你的图片，却仍然需要
    理解内容！参见下文关于替代文本的最佳实践。

<a id="tables"></a>

## 明智地使用表格

在合适的时候使用表格：用于需要被快速浏览的
    表格化数据的呈现。

当你的数据可以轻松地用列表呈现时，避免使用表格。在
    Markdown 中，列表更易写、更易读。

例如：

<div class='badcode'></div>

```markdown
Fruit  | Metrics      | Grows on | Acute curvature    | Attributes                                                                                                  | Notes
------ | ------------ | -------- | ------------------ | ----------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------
Apple  | Very popular | Trees    |                    | [Juicy](http://cs/SomeReallyReallyReallyReallyReallyReallyReallyReallyLongQuery), Firm, Sweet               | Apples keep doctors away.
Banana | Very popular | Trees    | 16 degrees average | [Convenient](http://cs/SomeDifferentReallyReallyReallyReallyReallyReallyReallyReallyLongQuery), Soft, Sweet | Contrary to popular belief, most apes prefer mangoes. Don't you? See the [design doc][banana_v2] for the newest hotness in bananiels.
```

这个表格说明了几个典型问题：

*   **分布不佳**：若干列在各行之间没有差异，且
    有些单元格为空。这通常是你的数据或许
    并不适合表格化呈现的信号。

*   **维度失衡**：相对于列数，行数很少。当这个比值朝
    任一方向失衡时，表格几乎就只是
    一种不灵活的文本格式。

*   某些单元格中的**冗长散文**。表格应当让人一眼就能
    读懂一个简洁的故事。

[列表](#lists) 和子标题有时足以呈现相同的信息。我们
    来看看以列表形式呈现的这份数据：

<div class='goodcode'></div>

```markdown
## Fruits

Both types are highly popular, sweet, and grow on trees.

### Apple

*   [Juicy](http://SomeReallyReallyReallyReallyReallyReallyReallyReallyReallyReallyReallyReallyReallyReallyReallyReallyLongURL)
*   Firm

Apples keep doctors away.

### Banana

*   [Convenient](http://cs/SomeDifferentReallyReallyReallyReallyReallyReallyReallyReallyLongQuery)
*   Soft
*   16 degrees average acute curvature.

Contrary to popular belief, most apes prefer mangoes. Don't you?

See the [design doc][banana_v2] for the newest hotness in bananiels.
```

列表形式更宽松，因此可以说读者在这种情况下
    更容易找到她感兴趣的内容。

不过，有时表格是最佳选择。当你满足以下条件时：

*   两个维度上相对均匀的数据分布。
*   许多具有不同属性的并行条目。

在这些情况下，表格格式正合适。事实上，紧凑的
    表格能提升可读性：

<div class='goodcode'></div>

```markdown
Transport        | Favored by     | Advantages
---------------- | -------------- | -----------------------------------------------
Swallow          | Coconuts       | [Fast when unladen][airspeed]
Bicycle          | Miss Gulch     | [Weatherproof][tornado_proofing]
X-34 landspeeder | Whiny farmboys | [Cheap][tosche_station] since the XP-38 came out

[airspeed]: http://google3/airspeed.h
[tornado_proofing]: http://google3/kansas/
[tosche_station]: http://google3/power_converter.h
```

注意，这里使用了 [引用式链接](#reference-links) 来保持表格
    单元格可控。

<a id="html"></a>

## 强烈倾向于 Markdown 而非 HTML

请尽可能优先使用标准 Markdown 语法，并避免 HTML 技巧。如果你
    似乎无法完成想要的效果，请重新考虑
    是否真的需要它。除了 [大表格](#tables)，Markdown 几乎
    已经能满足所有需求。

任何一点 HTML 技巧都会降低我们 Markdown 语料库的可读性
    和可移植性。这反过来限制了与其他工具集成的
    实用性——这些工具可能将源代码以纯文本呈现，也可能
    将其渲染。参见 [Philosophy](philosophy.md)。

Gitiles 不渲染 HTML。
