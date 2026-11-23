<div class="numbered"></div>

# Google HTML/CSS 风格指南

<!-- mdformat off -->
* TOC
{:toc}
<!-- mdformat on -->

<div class="numbered"></div>

<a id="Background"></a>

## 背景

本文档定义了 HTML 与 CSS 的格式与风格规则，旨在
改善协作、提升代码质量，并支撑相关基础设施。它适用于
使用 HTML 与 CSS 的原始工作文件，包括 Sass 与 GSS
文件。只要保持整体代码质量，工具可自由进行混淆、压缩与
编译。

<div class="numbered"></div>

<a id="General"></a>

## 通用

<div class="numbered"></div>

<a id="General_Style_Rules"></a>

### 通用风格规则

<div class="numbered"></div>

<a id="Protocol"></a>

#### 协议

尽可能为嵌入资源使用 HTTPS。

对图片及其他媒体文件、样式表和脚本，始终使用 HTTPS
（`https:`），除非相应文件无法通过 HTTPS 获取。

<div class='badcode'></div>

```html
<!-- Not recommended: omits the protocol -->
<script src="//ajax.googleapis.com/ajax/libs/jquery/3.4.0/jquery.min.js"></script>

<!-- Not recommended: uses HTTP -->
<script src="http://ajax.googleapis.com/ajax/libs/jquery/3.4.0/jquery.min.js"></script>
```

<div class='goodcode'></div>

```html
<!-- Recommended -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.0/jquery.min.js"></script>
```

<div class='badcode'></div>

```css
/* Not recommended: omits the protocol */
@import '//fonts.googleapis.com/css?family=Open+Sans';

/* Not recommended: uses HTTP */
@import 'http://fonts.googleapis.com/css?family=Open+Sans';
```

<div class='goodcode'></div>

```css
/* Recommended */
@import 'https://fonts.googleapis.com/css?family=Open+Sans';
```

<div class="numbered"></div>

<a id="General_Formatting_Rules"></a>

### 通用格式规则

<div class="numbered"></div>

<a id="Indentation"></a>

#### 缩进

每次缩进 2 个空格。

不要使用制表符，也不要混用制表符与空格进行缩进。

<div class='goodcode'></div>

```html
<ul>
  <li>Fantastic
  <li>Great
</ul>
```

<div class='goodcode'></div>

```css
.example {
  color: blue;
}
```

<div class="numbered"></div>

<a id="Capitalization"></a>

#### 大小写

只使用小写。

所有代码都必须小写：这适用于 HTML 元素名、属性、
属性值（`text/CDATA` 除外）、CSS 选择器、属性以及属性
值（字符串除外）。

<div class='badcode'></div>

```html
<!-- Not recommended -->
<A HREF="/">Home</A>
```

<div class='goodcode'></div>

```html
<!-- Recommended -->
<img src="google.png" alt="Google">
```

<div class='badcode'></div>

```css
/* Not recommended */
color: #E5E5E5;
```

<div class='goodcode'></div>

```css
/* Recommended */
color: #e5e5e5;
```

<div class="numbered"></div>

<a id="Trailing_Whitespace"></a>

#### 行尾空格

删除行尾空格。

行尾空格并无必要，还会让差异比对变得复杂。

<div class='badcode'></div>

```html
<!-- Not recommended -->
<p>What?_
```

<div class='goodcode'></div>

```html
<!-- Recommended -->
<p>Yes please.
```

<div class="numbered"></div>

<a id="General_Meta_Rules"></a>

### 通用元规则

<div class="numbered"></div>

<a id="Encoding"></a>

#### 编码

使用 UTF-8（无 BOM）。

确保编辑器使用 UTF-8 作为字符编码，且不带字节序
标记。

在 HTML 模板与文档中通过
`<meta charset="utf-8">` 指定编码。不要指定样式表的编码，
因为它们默认采用 UTF-8。

（有关编码以及何时、如何指定编码的更多内容，请参阅
[HTML 与 CSS 中的字符编码处理](https://www.w3.org/International/tutorials/tutorial-char-enc/)。）

<div class="numbered"></div>

<a id="Comments"></a>

#### 注释

在可能且需要的地方解释代码。

用注释解释代码：它涵盖什么、用于什么目的、
为何采用或偏好相应的方案？

（此项为可选，因为始终要求代码具备完整文档并不被视为
切合实际的期望。HTML 与 CSS 代码的适用性差异极大，
取决于项目的复杂度。）

<div class="numbered"></div>

<a id="Action_Items"></a>

#### 待办事项

对临时代码、短期方案，或虽够用但并不完美的代码，
使用 `TODO` 注释。

`TODO` 注释以全大写的 `TODO` 一词开头，后跟括号括起的
链接，指向包含背景信息的资源，最好是缺陷引用。首选缺陷
引用，因为缺陷会被跟踪并带有后续评论。在这段上下文之后
加上冒号和一段解释性文字。

目的在于形成一致的 `TODO` 格式，便于通过搜索
找到更多细节。

<div class='goodcode'></div>

```django
{# TODO(b/12345): Revisit centering. #}
<center>Test</center>
```

<div class="numbered"></div>

<a id="HTML"></a>

## HTML

<div class="numbered"></div>

<a id="HTML_Style_Rules"></a>

### HTML 风格规则

<div class="numbered"></div>

<a id="Document_Type"></a>

#### 文档类型

使用 `<!doctype html>`。

始终让 HTML 处于
[无怪异模式](https://developer.mozilla.org/en-US/docs/Web/HTML/Quirks_Mode_and_Standards_Mode)
状态：在文档开头加入 `<!doctype html>`。

没有 doctype 的文档会以“怪异模式”渲染，而使用其他
doctype 的文档可能以“有限怪异模式”渲染。这些模式
不遵循各种核心 HTML 与 CSS 结构中广为理解、
有充分文档记载的行为，容易引发难以察觉的故障与
不兼容问题，尤其在复用假定为无怪异模式的代码时。

<div class="numbered"></div>

<a id="HTML_Validity"></a>

#### HTML 有效性

尽可能使用有效的 HTML。

使用有效的 HTML 代码，除非为了达成原本无法实现的
文件大小性能目标而无法做到。

使用 [W3C HTML 验证器](https://validator.w3.org/nu/) 之类的工具
进行测试。

使用有效的 HTML 是一项可度量的基线质量属性，有助于
了解技术需求与约束，并确保正确地
使用 HTML。

<div class='badcode'></div>

```html
<!-- Not recommended -->
<title>Test</title>
<article>This is only a test.
```

<div class='goodcode'></div>

```html
<!-- Recommended -->
<!doctype html>
<meta charset="utf-8">
<title>Test</title>
<article>This is only a test.</article>
```

<div class="numbered"></div>

<a id="Semantics"></a>

#### 语义

按 HTML 的用途来使用它。

按元素的创建意图使用元素（有时被误称为“标签”）。例如，
标题用标题元素，`p` 元素用于
段落，`a` 元素用于锚点，等等。

按用途使用 HTML 对可访问性、复用以及
代码效率都很重要。

<div class='badcode'></div>

```html
<!-- Not recommended -->
<div onclick="goToRecommendations();">All recommendations</div>
```

<div class='goodcode'></div>

```html
<!-- Recommended -->
<a href="recommendations/">All recommendations</a>
```

<div class="numbered"></div>

<a id="Multimedia_Fallback"></a>

#### 多媒体后备内容

为多媒体提供替代内容。

对于图片、视频以及通过 `canvas` 制作的动画对象等多媒体，
务必提供替代访问方式。对图片而言，这意味着使用有意义的
替代文本（`alt`）；对视频与音频，则尽可能提供文字稿与字幕。

提供替代内容对可访问性很重要：没有 `@alt` 时，
视障用户几乎无从得知图片的内容，其他用户也可能
无法理解视频或音频内容讲的是什么。

（对于 `alt` 属性会造成冗余的图片，以及纯装饰性、
又无法立即用 CSS 处理的图片，不要提供替代文本，
如 `alt=""`。）

<div class='badcode'></div>

```html
<!-- Not recommended -->
<img src="spreadsheet.png">
```

<div class='goodcode'></div>

```html
<!-- Recommended -->
<img src="spreadsheet.png" alt="Spreadsheet screenshot.">
```

<div class="numbered"></div>

<a id="Separation_of_Concerns"></a>

#### 关注点分离

将结构、表现与行为相互分离。

严格区分结构（标记）、表现（样式）与行为
（脚本），并尽量将三者之间的交互压到
绝对最低限度。

也就是说，确保文档与模板只包含 HTML，且这些 HTML
仅用于结构目的。把所有表现层的内容移入样式表，
把所有行为层的内容移入脚本。

此外，通过在文档与模板中尽可能少地链接样式表
与脚本，让接触面尽可能小。

将结构、表现与行为分离对维护很重要。修改 HTML
文档与模板的代价，总是高于更新样式表
与脚本。

<div class='badcode'></div>

```html
<!-- Not recommended -->
<!doctype html>
<title>HTML sucks</title>
<link rel="stylesheet" href="base.css" media="screen">
<link rel="stylesheet" href="grid.css" media="screen">
<link rel="stylesheet" href="print.css" media="print">
<h1 style="font-size: 1em;">HTML sucks</h1>
<p>I’ve read about this on a few sites but now I’m sure:
  <u>HTML is stupid!!1</u>
<center>I can’t believe there’s no way to control the styling of
  my website without doing everything all over again!</center>
```

<div class='goodcode'></div>

```html
<!-- Recommended -->
<!doctype html>
<title>My first CSS-only redesign</title>
<link rel="stylesheet" href="default.css">
<h1>My first CSS-only redesign</h1>
<p>I’ve read about this on a few sites but today I’m actually
  doing it: separating concerns and avoiding anything in the HTML of
  my website that is presentational.
<p>It’s awesome!
```

<div class="numbered"></div>

<a id="Entity_References"></a>

#### 实体引用

不要使用实体引用。

没有必要使用 `&mdash;`、`&rdquo;` 或
`&#x263a;` 之类的实体引用，前提是文件、编辑器
以及团队之间都使用相同的编码（UTF-8）。

唯一的例外是 HTML 中有特殊含义的字符（如 `<`
与 `&`），以及控制字符或“不可见”字符（如不换行空格）。

<div class='badcode'></div>

```html
<!-- Not recommended -->
The currency symbol for the Euro is &ldquo;&eur;&rdquo;.
```

<div class='goodcode'></div>

```html
<!-- Recommended -->
The currency symbol for the Euro is “€”.
```

<div class="numbered"></div>

<a id="Optional_Tags"></a>

#### 可选标签

省略可选标签（可选）。

为了优化文件大小并便于速览，可考虑省略可选
标签。
[HTML5 规范](https://html.spec.whatwg.org/multipage/syntax.html#syntax-tag-omission)
定义了哪些标签可以省略。

（由于这种做法与 Web 开发者通常所学的内容差异很大，
可能需要一段宽限期才能将其确立为通用准则。
出于一致性与简洁性考虑，最好省略所有可选
标签，而不是只省略其中一部分。）

<div class='badcode'></div>

```html
<!-- Not recommended -->
<!doctype html>
<html>
  <head>
    <title>Spending money, spending bytes</title>
  </head>
  <body>
    <p>Sic.</p>
  </body>
</html>
```

<div class='goodcode'></div>

```html
<!-- Recommended -->
<!doctype html>
<title>Saving money, saving bytes</title>
<p>Qed.
```

<div class="numbered"></div>

<a id="type_Attributes"></a>

#### `type` 属性

省略样式表与脚本的 `type` 属性。

不要为样式表（除非不使用 CSS）和脚本使用 `type` 属性
（除非不使用 JavaScript，或在加载 JavaScript 模块时
使用 `type="module"`）。

在这些上下文中指定 `type` 属性并无必要，因为 HTML5 默认隐含
[`text/css`](https://html.spec.whatwg.org/multipage/obsolete.html#attr-style-type)
和
[`text/javascript`](https://html.spec.whatwg.org/multipage/scripting.html#attr-script-type)
作为默认值。即便对较旧的浏览器，这样省略也是安全的。

<div class='badcode'></div>

```html
<!-- Not recommended -->
<link rel="stylesheet" href="https://www.google.com/css/maia.css"
    type="text/css">
```

<div class='goodcode'></div>

```html
<!-- Recommended -->
<link rel="stylesheet" href="https://www.google.com/css/maia.css">
```

<div class='badcode'></div>

```html
<!-- Not recommended -->
<script src="https://www.google.com/js/gweb/analytics/autotrack.js"
    type="text/javascript"></script>
```

<div class='goodcode'></div>

```html
<!-- Recommended -->
<script src="https://www.google.com/js/gweb/analytics/autotrack.js"></script>
```

[JavaScript 模块](https://html.spec.whatwg.org/multipage/scripting.html#attr-script-type)
在通过 `<script>` 加载时必须使用 `type="module"`。

<div class='goodcode'></div>

```html
<!-- Recommended -->
<script src="https://example.com/js/app.js" type="module"></script>
```

<div class="numbered"></div>

<a id="id_Attributes"></a>

#### `id` 属性

避免不必要的 `id` 属性。

样式优先使用 `class` 属性，脚本优先使用 `data` 属性。

在确实必须使用 `id` 属性时，务必在取值中包含连字符，
以确保它不符合 JavaScript 标识符语法，例如使用
`user-profile`，而不是 `profile` 或 `userProfile`。

当元素带有 `id` 属性时，浏览器会将其作为
[全局 `window` 原型上的命名属性](https://html.spec.whatwg.org/multipage/window-object.html#named-access-on-the-window-object)，
这可能导致意外行为。虽然含连字符的 `id` 属性值
仍可作为属性名使用，但无法作为全局 JavaScript
变量被引用。

<div class='badcode'></div>

```html
<!-- Not recommended: `window.userProfile` will resolve to reference the <div> node -->
<div id="userProfile"></div>
```

<div class='goodcode'></div>

```html
<!-- Recommended: `id` attribute is required and its value includes a hyphen -->
<div aria-describedby="user-profile">
  …
  <div id="user-profile"></div>
  …
</div>
```

<div class="numbered"></div>

<a id="HTML_Formatting_Rules"></a>

### HTML 格式规则

<div class="numbered"></div>

<a id="General_Formatting"></a>

#### 通用格式

每个块级、列表或表格元素都另起一行，并缩进其
每个子元素。

与元素的样式无关（CSS 允许元素按 `display` 属性
承担不同角色），每个块级、列表或表格元素都
另起一行。

此外，若它们是块级、列表或表格元素的子元素，也要缩进。

（如果遇到列表项之间空白的问题，可以把所有 `li`
元素放在同一行。建议检查工具抛出警告，
而不是报错。）

<div class='goodcode'></div>

```html
<blockquote>
  <p><em>Space</em>, the final frontier.</p>
</blockquote>
```

<div class='goodcode'></div>

```html
<ul>
  <li>Moe
  <li>Larry
  <li>Curly
</ul>
```

<div class='goodcode'></div>

```html
<table>
  <thead>
    <tr>
      <th scope="col">Income
      <th scope="col">Taxes
  <tbody>
    <tr>
      <td>$ 5.00
      <td>$ 4.50
</table>
```

<div class="numbered"></div>

<a id="HTML_Line-Wrapping"></a>

#### HTML 换行

断开长行（可选）。

虽然 HTML 没有列数限制的建议，但如果断行能显著提升
可读性，可以考虑将长行换行。

换行时，每个续行都应缩进，以便将折行的属性与
子元素区分开。项目内应保持一致的换行方式，
最好由自动化代码格式化工具强制实施。

<div class='goodcode'></div>

```html
<button
  mat-icon-button
  color="primary"
  class="menu-button"
  (click)="openMenu()"
>
  <mat-icon>menu</mat-icon>
</button>
```

<div class='goodcode'></div>

```html
<button mat-icon-button color="primary" class="menu-button"
    (click)="openMenu()">
  <mat-icon>menu</mat-icon>
</button>
```

<div class='goodcode'></div>

```html
<button
    mat-icon-button
    color="primary"
    class="menu-button"
    (click)="openMenu()">
  <mat-icon>menu</mat-icon>
</button>
```

<div class='goodcode'></div>

```html
<button mat-icon-button
        color="primary"
        class="menu-button"
        (click)="openMenu()">
  <mat-icon>menu</mat-icon>
</button>
```

<div class="numbered"></div>

<a id="HTML_Quotation_Marks"></a>

#### HTML 引号

为属性值加引号时，使用双引号。

属性值使用双引号（`""`）而非单引号（`''`）
包裹。

<div class='badcode'></div>

```html
<!-- Not recommended -->
<a class='maia-button maia-button-secondary'>Sign in</a>
```

<div class='goodcode'></div>

```html
<!-- Recommended -->
<a class="maia-button maia-button-secondary">Sign in</a>
```

<div class="numbered"></div>

<a id="CSS"></a>

## CSS

<div class="numbered"></div>

<a id="CSS_Style_Rules"></a>

### CSS 风格规则

<div class="numbered"></div>

<a id="CSS_Validity"></a>

#### CSS 有效性

尽可能使用有效的 CSS。

除非是在处理 CSS 验证器的缺陷，或需要专有语法，
否则都使用有效的 CSS 代码。

使用 [W3C CSS 验证器](https://jigsaw.w3.org/css-validator/) 之类的工具
进行测试。

使用有效的 CSS 是一项可度量的基线质量属性，有助于发现
可能不起作用、可以删除的 CSS 代码，并确保正确地
使用 CSS。

<div class="numbered"></div>

<a id="ID_and_Class_Naming"></a>

#### 类命名

使用有意义或通用的类名。

不要使用表现性或晦涩的名称，始终使用能反映
相应元素用途的类名，或者使用通用的类名。

应优先选用具体且能反映元素用途的名称，因为它们
最易理解，也最不容易变化。

通用名称只是为那些与同级元素相比没有特定含义
或没有区别的元素准备的退路，通常作为“辅助类”使用。

使用功能性或通用名称，可降低不必要的文档或
模板改动。

<div class='badcode'></div>

```css
/* Not recommended: meaningless */
.yee-1901 {}

/* Not recommended: presentational */
.button-green {}
.clear {}
```

<div class='goodcode'></div>

```css
/* Recommended: specific */
.gallery {}
.login {}
.video {}

/* Recommended: generic */
.aux {}
.alt {}
```

<div class="numbered"></div>

<a id="ID_and_Class_Name_Style"></a>

#### 类名风格

类名应尽可能短，同时又要足够长。

在尽可能简洁的同时，尽量表达出类的含义。

这样使用类名，有助于达到可接受的可理解性
与代码效率。

<div class='badcode'></div>

```css
/* Not recommended */
.navigation {}
.atr {}
```

<div class='goodcode'></div>

```css
/* Recommended */
.nav {}
.author {}
```

<div class="numbered"></div>

<a id="ID_and_Class_Name_Delimiters"></a>

#### 类名分隔符

类名中的单词用连字符分隔。

不要用连字符以外的任何字符（包括不用任何字符）
把选择器中的单词与缩写拼接在一起，以提升
可理解性与可速览性。

<div class='badcode'></div>

```css
/* Not recommended: does not separate the words “demo” and “image” */
.demoimage {}

/* Not recommended: uses underscore instead of hyphen */
.error_status {}
```

<div class='goodcode'></div>

```css
/* Recommended */
.video-id {}
.ads-sample {}
```

<div class="numbered"></div>

<a id="Prefixes"></a>

#### 前缀

为选择器加上应用专属前缀（可选）。

在大型项目中，以及代码会被嵌入其他项目或外部站点时，
为类名使用前缀（作为命名空间）。使用简短、唯一的
标识符，后跟一个连字符。

使用命名空间有助于避免命名冲突，并让维护
更轻松，例如在查找替换操作中。

<div class='goodcode'></div>

```css
.adw-help {} /* AdWords */
.maia-note {} /* Maia */
```

<div class="numbered"></div>

<a id="Type_Selectors"></a>

#### 类型选择器

避免用类型选择器限定类名。

除非确有必要（例如配合辅助类），否则不要将元素名
与类结合使用。

避免不必要的祖先选择器，是出于
[性能方面的考虑](https://www.stevesouders.com/blog/2009/06/18/simplifying-css-selectors/)。

<div class='badcode'></div>

```css
/* Not recommended */
ul.example {}
div.error {}
```

<div class='goodcode'></div>

```css
/* Recommended */
.example {}
.error {}
```

<div class="numbered"></div>

<a id="ID_Selectors"></a>

#### ID 选择器

避免使用 ID 选择器。

ID 属性应当在整个页面内唯一，但当页面包含
由许多不同工程师协作开发的大量组件时，这很难
保证。任何情况下都应优先使用类选择器。

<div class='badcode'></div>

```css
/* Not recommended */
#example {}
```

<div class='goodcode'></div>

```css
/* Recommended */
.example {}
```

<div class="numbered"></div>

<a id="Shorthand_Properties"></a>

#### 简写属性

尽可能使用简写属性。

CSS 提供了多种
[简写](https://www.w3.org/TR/CSS21/about.html#shorthand) 属性（如
`font`），应尽可能使用，即使只显式设置了
一个值。

使用简写属性有助于提升代码效率与可理解性。

<div class='badcode'></div>

```css
/* Not recommended */
border-top-style: none;
font-family: palatino, georgia, serif;
font-size: 100%;
line-height: 1.6;
padding-bottom: 2em;
padding-left: 1em;
padding-right: 1em;
padding-top: 0;
```

<div class='goodcode'></div>

```css
/* Recommended */
border-top: 0;
font: 100%/1.6 palatino, georgia, serif;
padding: 0 1em 2em;
```

<div class="numbered"></div>

<a id="0_and_Units"></a>

#### 0 与单位

除非必要，省略“0”值之后的单位。

除非必要，不要在 `0` 值之后使用单位。

<div class='goodcode'></div>

```css
flex: 0px; /* This flex-basis component requires a unit. */
flex: 1 1 0px; /* Not ambiguous without the unit, but needed in IE11. */
margin: 0;
padding: 0;
```

<div class="numbered"></div>

<a id="Leading_0s"></a>

#### 前导 0

值中始终包含前导“0”。

在 -1 与 1 之间的值或长度前加上 `0`。

<div class='goodcode'></div>

```css
font-size: 0.8em;
```

<div class="numbered"></div>

<a id="Hexadecimal_Notation"></a>

#### 十六进制记法

尽可能使用 3 字符的十六进制记法。

对于允许使用简写的颜色值，3 字符十六进制记法更短、
更简洁。

<div class='badcode'></div>

```css
/* Not recommended */
color: #eebbcc;
```

<div class='goodcode'></div>

```css
/* Recommended */
color: #ebc;
```

<div class="numbered"></div>

<a id="Important_Declarations"></a>

#### 重要声明

避免使用 `!important` 声明。

这类声明会破坏 CSS 天然的层叠，使样式难以
推理与组合。应改用 [selector specificity] 来覆盖
属性。

[selector specificity]: https://developer.mozilla.org/en-US/docs/Web/CSS/Specificity

<div class='badcode'></div>

```css
/* Not recommended */
.example {
  font-weight: bold !important;
}
```

<div class='goodcode'></div>

```css
/* Recommended */
.example {
  font-weight: bold;
}
```

<div class="numbered"></div>

<a id="Hacks"></a>

#### Hack 技巧

避免用户代理检测以及 CSS “hack”——先尝试
其他方法。

通过用户代理检测，或者借助特殊的 CSS 过滤器、
变通方案和 hack 来处理样式差异，是很诱人的做法。
但为了实现并维持高效、可管理的代码库，这两种做法
都应被视为最后手段。换句话说，对检测与 hack 大开方便之门，
从长远看会损害项目，因为项目往往倾向于走阻力最小的路。
也就是说，允许并让检测与 hack 易于使用，就意味着
会更频繁地使用检测与 hack——而更频繁，
就已经是过于频繁了。

<div class="numbered"></div>

<a id="CSS_Formatting_Rules"></a>

### CSS 格式规则

<div class="numbered"></div>

<a id="Declaration_Order"></a>

#### 声明顺序

按字母顺序排列声明（可选）。

在项目内一致地对声明排序。若没有工具来
自动执行并强制统一的排序，可考虑按字母顺序
排列声明，以一种易于学习、记忆和手工维护的
方式获得一致的代码。

排序时忽略厂商特定前缀。不过，同一 CSS 属性的
多个厂商特定前缀之间仍应保持有序（例如
-moz 前缀排在 -webkit 之前）。

<div class='goodcode'></div>

```css
background: fuchsia;
border: 1px solid;
-moz-border-radius: 4px;
-webkit-border-radius: 4px;
border-radius: 4px;
color: black;
text-align: center;
text-indent: 2em;
```

<div class="numbered"></div>

<a id="Block_Content_Indentation"></a>

#### 块内容缩进

缩进所有块内容。

缩进所有[块内容](https://www.w3.org/TR/CSS21/syndata.html#block)，
即规则中的规则以及声明，以体现层次结构并
提升可理解性。

<div class='goodcode'></div>

```css
@media screen, projection {

  html {
    background: #fff;
    color: #444;
  }

}
```

<div class="numbered"></div>

<a id="Declaration_Stops"></a>

#### 声明结尾

每条声明后都使用分号。

出于一致性与可扩展性考虑，每条声明都以分号
结尾。

<div class='badcode'></div>

```css
/* Not recommended */
.test {
  display: block;
  height: 100px
}
```

<div class='goodcode'></div>

```css
/* Recommended */
.test {
  display: block;
  height: 100px;
}
```

<div class="numbered"></div>

<a id="Property_Name_Stops"></a>

#### 属性名后的空格

在属性名的冒号后使用一个空格。

出于一致性考虑，属性与值之间始终使用单个空格
（但属性与冒号之间不加空格）。

<div class='badcode'></div>

```css
/* Not recommended */
h3 {
  font-weight:bold;
}
```

<div class='goodcode'></div>

```css
/* Recommended */
h3 {
  font-weight: bold;
}
```

<div class="numbered"></div>

<a id="Declaration_Block_Separation"></a>

#### 声明块分隔

在最后一个选择器与声明块之间使用一个空格。

在最后一个选择器与起始左花括号之间，始终使用单个
空格，该花括号用于开始
[声明块](https://www.w3.org/TR/CSS21/syndata.html#rule-sets)。

在给定规则中，左花括号应与最后一个选择器
位于同一行。

<div class='badcode'></div>

```css
/* Not recommended: missing space */
.video{
  margin-top: 1em;
}

/* Not recommended: unnecessary line break */
.video
{
  margin-top: 1em;
}
```

<div class='goodcode'></div>

```css
/* Recommended */
.video {
  margin-top: 1em;
}
```

<div class="numbered"></div>

<a id="Selector_and_Declaration_Separation"></a>

#### 选择器与声明分隔

用换行分隔选择器与声明。

每个选择器与声明都始终另起一行。

<div class='badcode'></div>

```css
/* Not recommended */
a:focus, a:active {
  position: relative; top: 1px;
}
```

<div class='goodcode'></div>

```css
/* Recommended */
h1,
h2,
h3 {
  font-weight: normal;
  line-height: 1.2;
}
```

<div class="numbered"></div>

<a id="Rule_Separation"></a>

#### 规则分隔

用换行分隔规则。

规则之间始终留一个空行（两个换行符）。

<div class='goodcode'></div>

```css
html {
  background: #fff;
}

body {
  margin: auto;
  width: 50%;
}
```

<div class="numbered"></div>

<a id="CSS_Quotation_Marks"></a>

#### CSS 引号

属性选择器与属性值使用单引号（`''`）而非
双引号（`""`）。

不要在 URI 值（`url()`）中使用引号。

例外：如果确实需要使用 `@charset` 规则，请使用双引号——
[不允许使用单引号](https://www.w3.org/TR/CSS21/syndata.html#charset)。

<div class='badcode'></div>

```css
/* Not recommended */
@import url("https://www.google.com/css/maia.css");

html {
  font-family: "open sans", arial, sans-serif;
}
```

<div class='goodcode'></div>

```css
/* Recommended */
@import url(https://www.google.com/css/maia.css);

html {
  font-family: 'open sans', arial, sans-serif;
}
```

<div class="numbered"></div>

<a id="CSS_Meta_Rules"></a>

### CSS 元规则

<div class="numbered"></div>

<a id="Section_Comments"></a>

#### 分节注释

用分节注释划分章节（可选）。

如有可能，用注释将样式表的各节组织在一起，
并用空行分隔各节。

<div class='goodcode'></div>

```css
/* Header */

.adw-header {}

/* Footer */

.adw-footer {}

/* Gallery */

.adw-gallery {}
```

<a id="Parting_Words"></a>

## 结语

*保持一致。*

如果你在编辑代码，花几分钟看看周围的代码，
弄清它的风格。如果他们在所有算术运算符两侧都加空格，
你也应该如此。如果他们的注释周围有用井号围成的小方框，
你的注释也照样加上井号围成的小方框。

制定风格准则的意义，在于形成一套通用的编码词汇，
让读者专注于你要表达什么，而不是你如何表达。
我们在此给出全局风格规则，好让大家了解这套词汇，但局部
风格同样重要。如果你往文件里添加的代码与周围既有代码
看起来截然不同，读者阅读时就会被打乱节奏。
请避免这种情况。
