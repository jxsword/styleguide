# Google Java 风格指南

<!-- mdformat off -->
* TOC
{:toc}
<!-- mdformat on -->

<!-- GitHub pages run markdown through Liquid templating which uses two open
     braces which also shows up in our code examples. Disable parsing for the
     whole document as we don't use Liquid templating anywhere -- the HTML
     conversion is via Kramdown.

     NB: Must come after the [TOC].
     {% raw %} -->

<a id="s1-introduction"></a>

## 1 简介

本文档是 Google 针对 Java™ 编程语言源代码
所制定的编码标准的**完整**定义。
当且仅当一个 Java 源文件遵守本文中的规则时，
才称其*符合 Google 风格*。

与其他编程语言的风格指南一样，本文所涵盖的问题不仅涉及
格式上的美观问题，还涉及其他类型的约定或
编码标准。不过，本文档主要关注我们普遍遵循的
**硬性规则**，并避免给出无法明确强制执行的
*建议*（无论由人还是由工具执行）。

<a id="s1.1-terminology"></a>

### 1.1 术语说明

在本文档中，除非另有说明：

1.  术语 *class* 是广义用法，指普通类、记录类、
    枚举类、接口或注解类型（`@interface`）。
2.  术语 *member*（类的成员）是广义用法，指嵌套类、
    字段、方法*或构造函数*；即，类中除初始化器外的
    全部顶层内容。
3.  术语 *comment* 始终指*实现*注释。我们不使用
    “文档注释”这一说法，而是使用通行的术语
    “Javadoc”。

本文档中还会不时出现其他“术语说明”。

<a id="s1.2-guide-notes"></a>

### 1.2 指南说明

本文档中的示例代码是**非规范性的**。也就是说，虽然
这些示例符合 Google 风格，但它们未必展示了呈现该代码的
*唯一*恰当方式。示例中做出的可选格式选择不应作为
规则强制执行。

<a id="s2-source-file-basics"></a>

## 2 源文件基础

<a id="s2.1-file-name"></a>

### 2.1 文件名

对于包含类的源文件，其文件名由顶层类
（[有且仅有一个](#s3.4.1-one-top-level-class)）区分大小写的名称，
再加上 `.java` 扩展名组成。

<a id="s2.2-file-encoding"></a>

### 2.2 文件编码：UTF-8

源文件以 **UTF-8** 编码。

<a id="s2.3-special-characters"></a>

### 2.3 特殊字符

<a id="s2.3.1-whitespace-characters"></a>

#### 2.3.1 空白字符

除行终止符序列外，**ASCII 水平空格
字符**（**0x20**）是源文件中任何位置唯一允许出现的
空白字符。这意味着：

1.  所有其他空白字符在 `char` 和字符串字面量中
    以及文本块中都要转义。
2.  制表符**不**用于缩进。

<a id="s2.3.2-special-escape-sequences"></a>

#### 2.3.2 特殊转义序列

对于任何具有
[特殊转义序列](http://docs.oracle.com/javase/tutorial/java/data/characters.html)
的字符（`\b`、`\t`、`\n`、`\f`、`\r`、`\s`、`\"`、`\'` 和 `\\ `），使用该序列
而不是对应的八进制（例如 `\012`）或 Unicode（例如
`\u000a`）转义。

<a id="s2.3.3-non-ascii-characters"></a>

#### 2.3.3 非 ASCII 字符

对于其余的非 ASCII 字符，既可使用实际的 Unicode 字符
（例如 `∞`），也可使用等价的 Unicode 转义（例如 `\u221e`）。
选择仅取决于哪种方式使代码**更易于阅读和理解**，不过
强烈不建议在字符串字面量和注释之外使用 Unicode 转义。

**提示：** 在使用 Unicode 转义的情况下，偶尔甚至在实际使用
Unicode 字符时，附一条解释性注释也会很有帮助。

示例：

<!-- mdformat off -->

| 示例                                                  | 讨论                                                                |
| :------------------------------------------------------- | :------------------------------------------------------------------------ |
| `String unitAbbrev = "μs";`                              | 最佳：即使不加注释也一目了然。                             |
| `String unitAbbrev = "\u03bcs"; // "μs"`                 | 允许，但没有理由这样做。                                |
| `String unitAbbrev = "\u03bcs"; // Greek letter mu, "s"` | 允许，但别扭且容易出错。                               |
| `String unitAbbrev = "\u03bcs";`                         | 不佳：读者完全看不出这是什么。                                |
| `return '\ufeff' + content; // byte order mark`          | 良好：对不可打印字符使用转义，必要时加注释。 |

<!-- mdformat on -->

**提示：** 不要仅仅因为担心某些程序
可能无法正确处理非 ASCII 字符，就降低代码的可读性。若果真如此，
那些程序是**有问题的**，必须予以**修复**。

<a id="filestructure"></a>

<a id="s3-source-file-structure"></a>

## 3 源文件结构

普通源文件由以下各部分**按顺序**组成：

1.  许可或版权信息（如有）
2.  包声明
3.  导入语句
4.  有且仅有一个顶层类声明

**恰好一个空行**用于分隔实际存在的各部分。

`package-info.java` 文件与之相同，但不包含类声明。

`module-info.java` 文件不包含包声明，
并以模块声明取代类声明，但除此之外
遵循相同的结构。

<a id="s3.1-copyright-statement"></a>

### 3.1 许可或版权信息（如有）

若文件中应包含许可或版权信息，则放在此处。

<a id="s3.2-package-statement"></a> <!-- historical link -->

<a id="s3.2-package-declaration"></a>

### 3.2 包声明

每个源文件都必须有包声明。
不使用[紧凑源文件](https://openjdk.org/jeps/512)。（显然，
此规则不适用于 `module-info.java` 文件，它采用不包含包声明的
不同语法。）

包声明**不换行**。列宽限制（第 4.4 节，
[列宽限制：100](#s4.4-column-limit)）不适用于包声明。

<a id="imports"></a>

<a id="s3.3-import-statements"></a>

### 3.3 导入语句

<a id="s3.3.1-wildcard-imports"></a>

#### 3.3.1 不使用通配符导入

**通配符（“按需”）导入**，无论静态与否，**都不使用**。

<a id="s3.3.1.1-module-imports"></a>

#### 3.3.1.1 不使用模块导入

[模块导入](https://docs.oracle.com/en/java/javase/25/language/module-import-declarations.html)
**一律不使用**。

示例：

```java
import module java.base;
```

<a id="s3.3.2-import-line-wrapping"></a>

#### 3.3.2 不换行

导入语句**不换行**。列宽限制（第 4.4 节，
[列宽限制：100](#s4.4-column-limit)）不适用于导入语句。

<a id="s3.3.3-import-ordering-and-spacing"></a>

#### 3.3.3 顺序与间距

导入语句按以下顺序排列：

1.  所有静态导入放在同一组中。
2.  所有非静态导入放在同一组中。

若同时存在静态导入和非静态导入，则用一个空行分隔
两组。导入语句之间不得有其他空行。

每组内，导入的名称按 ASCII 排序顺序排列。（**注意：**
这与导入*行*按 ASCII 排序顺序排列并不相同，因为 '.'
排在 ';' 之前。）

<a id="s3.3.4-import-class-not-static"></a>

#### 3.3.4 类不使用静态导入

静态嵌套类不使用静态导入，
而是使用普通导入语句导入。

<a id="s3.4-class-declaration"></a>

### 3.4 类声明

<a id="oneclassperfile"></a>

<a id="s3.4.1-one-top-level-class"></a>

#### 3.4.1 有且仅有一个顶层类声明

每个顶层类都独占一个源文件。

<a id="s3.4.2-class-member-ordering"></a> <!-- historical link -->

<a id="s3.4.2-ordering-class-contents"></a>

#### 3.4.2 类内容的顺序

为类的成员和初始化器选择的顺序，会对可学习性
产生很大影响。然而，并不存在唯一正确的做法；
不同的类可以以不同方式排列其内容。

重要的是每个类都采用***某种*逻辑顺序**，
其维护者在被问及时能够解释该顺序。例如，
不要习惯性地把新方法一律追加到类的末尾，因为那样会产生
“按添加日期先后排列”的顺序，而这并不是逻辑顺序。

<a id="overloads"></a>

<a id="s3.4.2.1-overloads-never-split"></a>

##### 3.4.2.1 重载：永不拆分

类中同名的方法应出现在单个连续的分组中，
其间不得夹杂其他成员。多个构造函数同样如此。
即使各方法或构造函数的 `static`、`private` 等修饰符
有所不同，此规则依然适用。

<a id="s3.5-module-declaration"></a>

### 3.5 模块声明

<a id="s3.5.1-ordering-module-directives"></a>

#### 3.5.1 模块指令的顺序与间距

模块指令按以下顺序排列：

1.  所有 `requires` 指令放在同一块中。
2.  所有 `exports` 指令放在同一块中。
3.  所有 `opens` 指令放在同一块中。
4.  所有 `uses` 指令放在同一块中。
5.  所有 `provides` 指令放在同一块中。

实际存在的各块之间用一个空行分隔。

<a id="s4-formatting"></a>

## 4 格式

**术语说明：** *块状结构*指类、方法、构造函数或
switch 的主体。注意，根据第 4.8.3.1 节关于
[数组初始化器](#s4.8.3.1-array-initializers)的说明，任何数组初始化器都*可以*
选择性地视为块状结构。

<a id="braces"></a>

<a id="s4.1-braces"></a>

### 4.1 花括号

<a id="s4.1.1-braces-always-used"></a>

#### 4.1.1 可选花括号的使用

`if`、`else`、`for`、`do` 和 `while` 语句都要使用花括号，
即使语句体为空或仅包含一条语句。

其他可选花括号（如 lambda 表达式中的）仍保持可选。

<a id="s4.1.2-blocks-k-r-style"></a>

#### 4.1.2 非空块：K & R 风格

对于*非空*块和块状结构，花括号遵循
Kernighan 和 Ritchie 风格：

*   左花括号前不换行，下文另有详述者除外。
*   左花括号后换行。
*   右花括号前换行。
*   右花括号后换行，*仅当*该花括号结束一条
    语句，或结束方法、构造函数或*具名*类的主体时。
    例如，若该花括号后紧跟的内容是
    `else` 或逗号，则其后*不*换行。

例外：在这些规则允许单条语句（以
分号 `;` 结尾）出现的位置，也可出现一个语句块，且该块的
左花括号前要换行。引入这类块通常是为了
限制局部变量的作用域。

示例：

```java
return () -> {
  while (condition()) {
    method();
  }
};

return new MyClass() {
  @Override public void method() {
    if (condition()) {
      try {
        something();
      } catch (ProblemException e) {
        recover();
      }
    } else if (otherCondition()) {
      somethingElse();
    } else {
      lastThing();
    }
    {
      int x = foo();
      frob(x);
    }
  }
};
```

关于枚举类的几处例外，见第 4.8.1 节
[枚举类](#s4.8.1-enum-classes)。

<a id="emptyblocks"></a>

<a id="s4.1.3-braces-empty-blocks"></a>

#### 4.1.3 空块：可简写

空块或空的块状结构可以采用 K & R 风格
（如[第 4.1.2 节](#s4.1.2-blocks-k-r-style)所述）。
也可以在开启后立即闭合，中间不含任何字符或换行
（`{}`），**除非**它属于*多块语句*（即直接
包含多个块的语句：`if/else` 或 `try/catch/finally`）。

示例：

<div class='goodcode'></div>

```java
  // This is acceptable
  void doNothing() {}

  // This is equally acceptable
  void doNothingElse() {
  }
```

<div class='badcode'></div>

```java
  // This is not acceptable: No concise empty blocks in a multi-block statement
  try {
    doSomething();
  } catch (Exception e) {}
```

<a id="s4.2-block-indentation"></a>

### 4.2 块缩进：+2 个空格

每开启一个新的块或块状结构，缩进增加两个
空格。块结束时，缩进回到先前的缩进级别。
缩进级别适用于整个块中的代码和注释。
（参见第 4.1.2 节中的示例，
[非空块：K & R 风格](#s4.1.2-blocks-k-r-style)。）

<a id="s4.3-one-statement-per-line"></a>

### 4.3 每行一条语句

每条语句后都要换行。

<a id="columnlimit"></a>

<a id="s4.4-column-limit"></a>

### 4.4 列宽限制：100

Java 代码的列宽限制为 100 个字符。“字符”指任意
Unicode 码点。除下文所述例外，任何超过此限制的行都必须
换行，详见第 4.5 节[换行](#s4.5-line-wrapping)。

**提示：** 每个 Unicode 码点都算作一个字符，
即使其显示宽度更大或更小。例如，若使用
[全角字符](https://en.wikipedia.org/wiki/Halfwidth_and_fullwidth_forms)，
可以选择在比本规则严格要求更早的位置换行。

**例外：**

1.  无法遵守列宽限制的行（例如 Javadoc 中的长
    URL，或长的 JSNI 方法引用）。
2.  `package` 声明和导入语句（见第 3.2 节
    [包声明](#s3.2-package-statement)与第 3.3 节
    [导入语句](#s3.3-import-statements)）。
3.  [文本块](#s4.8.9-text-blocks)的内容。
4.  注释中可能被复制粘贴到 shell 的命令行。
5.  在极少数确有需要时，非常长的标识符
    允许超出列宽限制。此时，外围代码的
    有效换行以
    [google-java-format](https://github.com/google/google-java-format) 生成的结果为准。

<a id="s4.5-line-wrapping"></a>

### 4.5 换行

**术语说明：** 当本可占据单行的代码被
拆分为多行时，这一操作称为*换行*。

不存在全面而确定的公式，能*精确地*说明
在每种情况下如何换行。同一段代码
往往有多种有效的换行方式。

**注意：** 虽然换行的典型原因是避免超出列宽限制，
但即使代码实际上能容纳在列宽限制内，作者也*可以*
自行决定是否换行。

**提示：** 提取方法或局部变量或许能解决问题，
而无需换行。

<a id="s4.5.1-line-wrapping-where-to-break"></a>

#### 4.5.1 在何处断行

换行的首要原则是：优先在**较高的语法
级别**处断行。此外：

1.  在*非赋值*运算符处断行时，断行位置在
    符号*之前*。（注意，这与 Google 针对其他语言
    （如 C++ 和 JavaScript）的风格做法不同。）

    *   这也适用于以下“类运算符”符号：

        *   点号分隔符（`.`）
        *   方法引用的两个冒号（`::`）
        *   类型边界中的与号（`<T extends Foo & Bar>`）
        *   catch 块中的竖线（`catch (FooException | BarException e)`）。

2.  在*赋值*运算符处断行时，断行位置通常
    在符号*之后*，但两种方式均可接受。

    *   这也适用于增强 `for`（“foreach”）
        语句中的冒号。

3.  方法、构造函数或记录类的名称与其后的
    左圆括号（`(`）保持相连。

4.  逗号（`,`）与其前面的标记保持相连。

5.  lambda 或 switch 规则中的箭头两侧绝不
    断行，但若箭头后的文本是单个不带花括号的
    表达式，则可在箭头后紧接处断行。示例：

    ```java
    MyLambda<String, Long, Object> lambda =
        (String label, Long value, Object obj) -> {
          ...
        };

    Predicate<String> predicate = str ->
        longExpressionInvolving(str);

    switch (x) {
      case ColorPoint(Color color, Point(int x, int y)) ->
          handleColorPoint(color, x, y);
      ...
    }
    ```

**注意：** 换行的首要目标是代码清晰，*并不
一定*要让代码占用尽可能少的行数。

<a id="indentation"></a>

<a id="s4.5.2-line-wrapping-indent"></a>

#### 4.5.2 续行至少缩进 +4 个空格

换行时，第一行之后的每一行（即每个*续行*）
相对原行至少缩进 +4。

存在多个续行时，可按需要在 +4 之外调整
缩进。一般而言，当且仅当两个续行以语法上
平行的元素开头时，才使用相同的缩进级别。

第 4.6.3 节[水平对齐](#s4.6.3-horizontal-alignment)
讨论了一种不推荐的做法：用数量不定的空格
将某些标记与前几行对齐。

<a id="s4.6-whitespace"></a>

### 4.6 空白

<a id="s4.6.1-vertical-whitespace"></a>

#### 4.6.1 纵向空白（空行）

以下位置总是出现单个空行：

1.  类的连续成员或初始化器*之间*：字段、
    构造函数、方法、嵌套类、静态初始化器和
    实例初始化器。

    *   **例外：** 两个连续字段之间（其间无其他
        代码）的空行是可选的。此类空行按需用于
        形成字段的*逻辑分组*。
    *   **例外：** 枚举常量之间的空行见
        [第 4.8.1 节](#s4.8.1-enum-classes)。

2.  按本文档其他章节的要求（如第 3 节
    [源文件结构](#s3-source-file-structure)，以及第 3.3 节
    [导入语句](#s3.3-import-statements)）。

在有助于提升可读性的任何位置也可出现单个空行，
例如用在语句之间，把代码组织成逻辑上的小节。
类的第一个成员或初始化器之前、最后一个成员或
初始化器之后的空行，既不鼓励也不反对。

允许出现*多个*连续空行，但绝不要求
（也不鼓励）。

<a id="s4.6.2-horizontal-whitespace"></a>

#### 4.6.2 横向空白

除语言或其他风格规则所要求之处，以及
字面量、注释和 Javadoc 内部之外，单个 ASCII 空格还
出现在以下位置，且**仅限**于此。

1.  将 `if`、`for` 或 `catch` 等任意关键字与同行的
    左圆括号（`(`）分隔开

2.  将 `else` 或 `catch` 等任意关键字与同行其前的
    右花括号（`}`）分隔开

3.  任意左花括号（`{`）之前，但有两处例外：

    *   `@SomeAnnotation({a, b})`（不加空格）
    *   `String[][] x = {{"foo"}};`（`{{` 之间按
        下文第 10 条不要求加空格）

4.  任意二元或三元运算符的两侧。这也适用于
    以下“类运算符”符号：

    *   分隔多个类型边界的与号：
        `<T extends Foo & Bar>`
    *   处理多个异常的 catch 块的竖线：
        `catch (FooException | BarException e)`
    *   冒号（`:`）用于增强 `for`（“foreach”）语句
    *   lambda 表达式中的箭头：`(String str) -> str.length()` \
        或 switch 规则：`case "FOO" -> bar();`

    但不适用于

    *   方法引用的两个冒号（`::`），写作
        `Object::toString`
    *   点号分隔符（`.`），写作 `object.toString()`

5.  `,:;` 之后，或类型转换的右圆括号（`)`）之后

6.  任意内容与起始注释的双斜杠（`//`）之间。
    允许多个空格。

7.  起始注释的双斜杠（`//`）与注释文字之间。
    允许多个空格。

8.  声明的类型与标识符之间：`List<String> list`

9.  数组初始化器两个花括号的紧内侧*可选*

    *   `new int[] {5, 6}` 与 `new int[] { 5, 6 }` 均有效

10. 类型注解与 `[]` 或 `...` 之间。

此规则绝不解释为要求或禁止在行首、行尾
添加空格；它只涉及*内部*空格。

<a id="s4.6.3-horizontal-alignment"></a>

#### 4.6.3 水平对齐：绝不要求

**术语说明：** *水平对齐*指在代码中
添加数量不定的额外空格，目的是让
某些标记恰好位于前几行另一些标记的正下方。

Google 风格允许这种做法，但**绝不要求**。
即使在已经使用水平对齐的地方，也
不要求*保持*对齐。

下面先给出未对齐的示例，再给出使用对齐的示例：

```java
private int x; // this is fine
private Color color; // this too

private int   x;      // permitted, but future edits
private Color color;  // may leave it unaligned
```

**提示：** 对齐有助于可读性，但单纯为了保持
对齐而强求，会给将来带来问题。例如，考虑一处
只改动一行的变更。若该变更破坏了原有的对齐，
重要的是**不要**仅仅为了重新对齐，就在附近
几行引入额外改动。在本不受影响的行上引入
格式改动会污染版本历史、拖慢评审者，并加剧合并冲突。
这些实际考量优先于对齐。

<a id="parentheses"></a>

<a id="s4.7-grouping-parentheses"></a>

### 4.7 分组圆括号：推荐

仅当作者与评审者一致认为，省略可选的分组
圆括号不会使代码遭误解，且加上它们也不会
让代码更易读时，才可省略。假定
每位读者都牢记整张 Java 运算符优先级表，
是*不*合理的。

<a id="s4.8-specific-constructs"></a>

### 4.8 具体结构

<a id="s4.8.1-enum-classes"></a>

#### 4.8.1 枚举类

枚举常量后的逗号之后，是否换行可选。
也允许额外的空行（通常只有一个）。
下面是一种可能的写法：

```java
private enum Answer {
  YES {
    @Override public String toString() {
      return "yes";
    }
  },

  NO,
  MAYBE
}
```

没有方法、常量上也没有文档的枚举类，
可以选择按数组初始化器排版（见第 4.8.3.1 节
关于[数组初始化器](#s4.8.3.1-array-initializers)的说明）。

```java
private enum Suit { CLUBS, HEARTS, SPADES, DIAMONDS }
```

由于枚举类*就是类*，类的其他所有格式规则同样适用。

<a id="localvariables"></a>

<a id="s4.8.2-variable-declarations"></a>

#### 4.8.2 变量声明

<a id="s4.8.2.1-variables-per-declaration"></a>

##### 4.8.2.1 每条声明一个变量

每条变量声明（字段或局部变量）只声明一个变量：
不使用 `int a, b;` 这样的声明。

**例外：** 允许在
`for` 循环的头部声明多个变量。

<a id="s4.8.2.2-variables-limited-scope"></a>

##### 4.8.2.2 在需要时声明

局部变量**不**习惯性地声明在其所在块或
块状结构的开头。相反，局部变量应声明在
接近首次使用之处（在合理范围内），以尽量缩小
其作用域。局部变量声明通常带有初始化器，或
在声明后立即初始化。

<a id="s4.8.3-arrays"></a>

#### 4.8.3 数组

<a id="s4.8.3.1-array-initializers"></a>

##### 4.8.3.1 数组初始化器：可呈“块状”

任何数组初始化器都*可以*选择按“块状
结构”排版。例如，以下写法全部有效（**并非**
详尽列表）：

```java
new int[] {           new int[] {
  0, 1, 2, 3            0,
}                       1,
                        2,
new int[] {             3,
  0, 1,               }
  2, 3
}                     new int[]
                          {0, 1, 2, 3}
```

<a id="s4.8.3.2-array-declarations"></a>

##### 4.8.3.2 不使用 C 风格数组声明

方括号是*类型*的一部分，而非变量：
应写 `String[] args`，不写 `String args[]`。

<a id="s4.8.4-switch"></a>

#### 4.8.4 switch 语句与表达式

由于历史原因，Java 语言有两种不同的语法用于
`switch`，可称为*旧式*与*新式*。新式 switch 用
箭头（`->`）接在 switch 标签后，旧式 switch 用
冒号（`:`）。

**术语说明：** *switch 块*的花括号内是一个或多个
*switch 规则*（新式），或一个或多个*语句组*（旧式）。
*switch 规则*由一个 *switch 标签*（`case ...` 或 `default`）、
后接 `->` 以及表达式、块或 `throw` 组成。语句组
由一个或多个 switch 标签组成，每个后跟冒号，再接
一条或多条语句；对*最后一个*语句组，则是*零*条或
更多语句。（这些定义与 Java 语言规范
[§14.11](https://docs.oracle.com/javase/specs/jls/se21/html/jls-14.html#jls-14.11) 一致。）

<a id="s4.8.4.1-switch-indentation"></a>

##### 4.8.4.1 缩进

与任何其他块一样，switch 块的内容缩进 +2。
每个 switch 标签都以此 +2 缩进开始。

在新式 switch 中，若 switch 规则在其他方面
符合 Google 风格，则可写在一行内。（不得超出
列宽限制；若包含非空块，则 `{` 后必须换行。）
[第 4.5 节](#s4.5-line-wrapping)的换行规则同样适用，
包括续行的 +4 缩进。对于箭头后带非空块的
switch 规则，适用与其他位置块相同的规则：`{`
与 `}` 之间的各行相对 switch 标签所在行再缩进 +2。

```java
switch (number) {
  case 0, 1 -> handleZeroOrOne();
  case 2 ->
      handleTwoWithAnExtremelyLongMethodCallThatWouldNotFitOnTheSameLine();
  default -> {
    logger.atInfo().log("Surprising number %s", number);
    handleSurprisingNumber(number);
  }
}
```

在旧式 switch 中，每个 switch 标签的冒号后
都要换行。语句组内的语句再缩进 +2。

<a id="fallthrough"></a>

<a id="s4.8.4.2-switch-fall-through"></a>

##### 4.8.4.2 贯穿：须加注释

在旧式 switch 块中，每个语句组要么突然终止
（通过 `break`、`continue`、`return` 或抛出的异常），
要么以注释标明执行将会或*可能*继续进入
下一个语句组。任何能表达贯穿之意的注释
都足够（通常为 `// fall through`）。switch 块的
最后一个语句组不需要此特殊注释。示例：

```java
switch (input) {
  case 1:
  case 2:
    prepareOneOrTwo();
  // fall through
  case 3:
    handleOneTwoOrThree();
    break;
  default:
    handleLargeNumber(input);
}
```

注意，`case 1:` 之后不需要注释，
只在语句组末尾需要。

新式 switch 中不存在贯穿。

<a id="s4.8.4.3-switch-default"></a>

##### 4.8.4.3 穷尽性与 `default` 标签的存在

Java 语言要求 switch 表达式和多种 switch
语句是*穷尽的*。这实际上意味着，被 switch 的
每个可能取值都会被某个 switch 标签匹配。
若 switch 带有 `default` 标签，则它是穷尽的；
但例如当被 switch 的值是枚举、且枚举的每个值
都由某个 switch 标签匹配时也是如此。Google 风格要求
*每个* switch 都是穷尽的，即使语言本身并不要求，可能需要添加 `default`
标签，即便其中不含代码。

<a id="s4.8.4.4-switch-expressions"></a>

##### 4.8.4.4 switch 表达式

switch 表达式必须写成新式 switch：

```java
  return switch (list.size()) {
    case 0 -> "";
    case 1 -> list.getFirst();
    default -> String.join(", ", list);
  };
```

<a id="annotations"></a>

<a id="s4.8.5-annotations"></a>

#### 4.8.5 注解

<a id="s4.8.5.1-type-use-annotation-style"></a>

##### 4.8.5.1 类型使用注解

类型使用注解紧挨在被注解的类型之前。若某注解
带有下列元注解，则它是类型使用注解：
`@Target(ElementType.TYPE_USE)`。示例：

```java
final @Nullable String name;

public @Nullable Person getPersonByName(String name);
```

<a id="s4.8.5.2-class-annotation-style"></a>

##### 4.8.5.2 类、包和模块的注解

应用于类、包或模块声明的注解紧跟在
文档块之后，且每个注解独占一行（即每行
一个注解）。这些换行不构成折行（第 4.5 节，
[换行](#s4.5-line-wrapping)），因此缩进级别
不增加。示例：

```java
/// This is a class.
@Deprecated
@CheckReturnValue
public final class Frozzler { ... }
```

```java
/// This is a package.
@Deprecated
@CheckReturnValue
package com.example.frozzler;
```

```java
/// This is a module.
@Deprecated
@SuppressWarnings("CheckReturnValue") // TODO(b/12345): Fix existing CRV violations.
module com.example.frozzler { ... }
```

<a id="s4.8.5.3-method-annotation-style"></a>

##### 4.8.5.3 方法与构造函数的注解

方法和构造函数声明上的注解规则与
[上一节](#s4.8.5.2-class-annotation-style)相同。示例：

```java
@Deprecated
@Override
public String getNameIfPresent() { ... }
```

**例外：** 若方法或构造函数只有*一个*、
*无参数*的注解，则它*可以*与签名的第一行
写在一起，例如：

```java
@Override public int hashCode() { ... }
```

<a id="s4.8.5.4-field-annotation-style"></a>

##### 4.8.5.4 字段注解

应用于字段的注解同样紧跟在文档块之后，
但在这种情况下，*多个*注解（可能带参数）
可以列在同一行；例如：

```java
@Partial @Mock DataLoader loader;
```

<a id="s4.8.5.5-local-parameter-annotation-style"></a>

##### 4.8.5.5 参数与局部变量的注解

对于参数或局部变量上的注解，没有专门的
排版规则（当然，注解为类型使用注解时除外）。

<a id="comments"></a>

<a id="s4.8.6-comments"></a>

#### 4.8.6 注释

本节讨论*实现注释*。Javadoc 另在
第 7 节[Javadoc](#s7-javadoc)中讨论。

任何换行之前都可以有任意空白，后跟
实现注释。这样的注释使该行不再是空行。

<a id="s4.8.6.1-block-comment-style"></a>

##### 4.8.6.1 块注释风格

块注释的缩进级别与周围代码相同。可以采用
`/* ... */` 风格或 `// ...` 风格。对于多行 `/* ... */` 注释，
后续各行必须以 `*` 开头，并与上一行的 `*` 对齐。

```java
/*
 * This is          // And so           /* Or you can
 * okay.            // is this.          * even do this. */
 */
```

注释不用星号或其他字符围成方框。

**提示：** 编写多行注释时请用 `/* ... */` 风格，
这样自动格式化工具便可在需要时重新折行（段落式）。
多数格式化工具不会重新折行 `// ...` 风格的注释块。

<a id="todo"></a>

<a id="s4.8.6.2-todo-comments"></a>

##### 4.8.6.2 TODO 注释

使用 `TODO` 注释标注临时代码、短期解决方案，
或够用但不完美的代码。

`TODO` 注释以全大写的 `TODO` 开头，
后跟冒号，再接指向包含背景信息的资源的链接，
最好是缺陷引用。缺陷引用更可取，因为缺陷
会被跟踪且有后续评论。在这段背景信息之后，
跟一个以连字符 `-` 引出的说明字符串。

目的是形成一致的 `TODO` 格式，便于通过检索
找到更多细节。

<div class='goodcode'></div>

```java
// TODO: example.com/12345678 - Remove this after the 2047q4 compatibility window expires.
```

避免添加以个人或团队作为背景信息的 TODO：

<div class='badcode'></div>

```java
// TODO: username - File an issue and use a '*' for repetition.
```

若 `TODO` 属于“将来某日做某事”这种形式，
请确保要么给出非常具体的日期（“在 2005 年 11 月前修复”），
要么给出非常具体的事件（“当所有客户端都能处理 XML 响应时删除此代码。”）。

<a id="modifiers"></a>

<a id="s4.8.7-modifiers"></a>

#### 4.8.7 修饰符

类和成员的修饰符（若存在）按
Java 语言规范推荐的顺序出现：

```java
public protected private abstract default static final sealed non-sealed
  transient volatile synchronized native strictfp
```

`requires` 模块指令上的修饰符（若存在）按
以下顺序出现：

```java
transitive static
```

<a id="s4.8.8-numeric-literals"></a>

#### 4.8.8 数值字面量

`long` 型整数字面量使用大写 `L` 后缀，
绝不用小写（以免与数字 `1` 混淆）。例如用 `3000000000L`
而非 `3000000000l`。

<a id="s4.8.9-text-blocks"></a>

#### 4.8.9 文本块

文本块的起始 `"""` 总是位于新的一行。该行
要么遵循与其他结构相同的缩进规则，要么
完全不缩进（即从左边界开始）。结束 `"""` 位于
新的一行，与起始 `"""` 缩进相同，且其后可在
同一行接续其他代码。文本块中每一行文本的
缩进至少与起始、结束 `"""` 相同。（若某行
缩进更多，则文本块定义的字符串字面量在该行
开头会有空格。）

文本块的内容可以超出[列宽限制](#columnlimit)。

<a id="naming"></a>

<a id="s5-naming"></a>

## 5 命名

<a id="s5.1-identifier-names"></a>

### 5.1 所有标识符通用的规则

标识符只使用 ASCII 字母和数字，在下文注明的
少数情况下还使用下划线。因此，每个有效的标识符名称
都匹配正则表达式 `\w+`。

在 Google 风格中，**不**使用特殊的前缀或后缀。
例如，以下名称不符合 Google 风格：`name_`、`mName`、`s_name` 和 `kName`。

<a id="s5.2-specific-identifier-names"></a>

### 5.2 按标识符类型划分的规则

<a id="s5.2.1-package-names"></a>

#### 5.2.1 包与模块名

包名和模块名只使用小写字母和数字
（不用下划线）。连续的单词直接拼接。
例如用 `com.example.deepspace`，而非 `com.example.deepSpace` 或
`com.example.deep_space`。

<a id="s5.2.2-class-names"></a>

#### 5.2.2 类名

类名以 [UpperCamelCase](#s5.3-camel-case) 书写。

类名通常是名词或名词短语，例如 `Character` 或
`ImmutableList`。接口名也可以是名词或名词短语
（例如 `List`），但有时也可以是形容词或形容词短语
（例如 `Readable`）。

对于注解类型的命名，没有专门的规则，
甚至没有公认的惯例。

*测试*类的名称以 `Test` 结尾，例如
`HashIntegrationTest`。若它只针对一个类，其名称就是
该类名加上 `Test`，例如 `HashImplTest`。

<a id="s5.2.3-method-names"></a>

#### 5.2.3 方法名

方法名以 [lowerCamelCase](#s5.3-camel-case) 书写。

方法名通常是动词或动词短语，例如 `sendMessage`
或 `stop`。

JUnit *测试*方法名中可以使用下划线来分隔
名称的各个逻辑组成部分，其中*每个*部分都以
[lowerCamelCase](#s5.3-camel-case) 书写，例如
`transferMoney_deductsFromSource`。测试方法命名
并不存在唯一正确的方式。

<a id="constants"></a>

<a id="s5.2.4-constant-names"></a>

#### 5.2.4 常量名

常量名使用 `UPPER_SNAKE_CASE`：全部大写字母，
单词之间以单个下划线分隔。但究竟什么
*是*常量呢？

常量是内容深度不可变、且方法无可察觉
副作用的 static final 字段。例如基本类型、字符串、
不可变值类，以及任何被设为 `null` 的值。若实例的
任何可观察状态可能改变，它就不是常量。仅仅
*打算*永不修改该对象还不够。示例：

```java
// Constants
static final int NUMBER = 5;
static final ImmutableList<String> NAMES = ImmutableList.of("Ed", "Ann");
static final Map<String, Integer> AGES = ImmutableMap.of("Ed", 35, "Ann", 32);
static final Joiner COMMA_JOINER = Joiner.on(','); // because Joiner is immutable
static final SomeMutableType[] EMPTY_ARRAY = {};

// Not constants
static String nonFinal = "non-final";
final String nonStatic = "non-static";
static final Set<String> mutableCollection = new HashSet<String>();
static final ImmutableSet<SomeMutableType> mutableElements = ImmutableSet.of(mutable);
static final ImmutableMap<String, SomeMutableType> mutableValues =
    ImmutableMap.of("Ed", mutableInstance, "Ann", mutableInstance2);
static final Logger logger = Logger.getLogger(MyClass.getName());
static final String[] nonEmptyArray = {"these", "can", "change"};
```

这些名称通常是名词或名词短语。

<a id="s5.2.5-non-constant-field-names"></a>

#### 5.2.5 非常量字段名

非常量字段名（无论是否 static）以
[lowerCamelCase](#s5.3-camel-case) 书写。

这些名称通常是名词或名词短语，例如 `computedValues`
或 `index`。

<a id="s5.2.6-parameter-names"></a>

#### 5.2.6 参数名

参数名以 [lowerCamelCase](#s5.3-camel-case) 书写。

应避免 public 方法中使用单字符参数名。

<a id="s5.2.7-local-variable-names"></a>

#### 5.2.7 局部变量名

局部变量名以 [lowerCamelCase](#s5.3-camel-case) 书写。

即使局部变量是 final 且不可变的，也不视为
常量，不应按常量的风格命名。

<a id="s5.2.8-type-variable-names"></a>

#### 5.2.8 类型变量名

每个类型变量采用以下两种命名风格之一：

*   单个大写字母，后可可选地跟一个数字（如
    `E`、`T`、`X`、`T2`）
*   采用类名的形式（见第 5.2.2 节
    [类名](#s5.2.2-class-names)），后跟大写字母 `T`
    （例如 `RequestT`、`FooBarT`）。

<a id="s5.2.9-unnamed-variables"></a>

#### 5.2.9 未命名变量

凡适用之处都允许使用 `_` 语法来声明未命名
变量和参数。例如：

```java
Predicate<String> alwaysTrue = _ -> true;
```

<a id="acronyms"></a>

<a id="camelcase"></a>

<a id="s5.3-camel-case"></a>

### 5.3 驼峰命名法：定义

有时，把英文短语转换为驼峰形式存在不止
一种合理方式，例如出现首字母缩略词或
“IPv6”、“iOS”这类不寻常构造时。为提高可预测性，
Google 风格规定了以下（近乎）确定性的方案。

从名称的散文形式开始：

1.  把短语转换为纯 ASCII，并去掉所有撇号。
    例如，“Müller's algorithm” 可能变成 “Muellers algorithm”。

2.  把所得结果切分为单词，按空格和其余
    标点（通常是连字符）分割。

    *   *推荐：* 若某个词在日常用法中已有
        约定俗成的驼峰外观，就拆成其组成部分
        （例如 “AdWords” 变成 “ad words”）。注意，
        像 “iOS” 这样的词*本身*并不真正属于驼峰形式；
        它不符合*任何*惯例，因此此建议不适用。

3.  现在把*一切*转为小写（包括首字母缩略词），
    然后只把以下各项的首字符大写：

    *   ……每个单词，得到*大驼峰形式*，或
    *   ……除首词外的每个单词，得到*小驼峰形式*

4.  最后，把所有单词拼接成一个标识符。注意，
    原词的大小写几乎完全不予考虑。

在极少数情况下（例如由多段组成的版本号），可能
需要用下划线分隔相邻的数字，因为数字没有
大小写变体。

示例：

<!-- mdformat off -->

| 散文形式              | 正确                                  | 错误           |
| :---------------------- | :--------------------------------------- | :------------------ |
| "XML HTTP request"      | `XmlHttpRequest`                         | `XMLHTTPRequest`    |
| "new customer ID"       | `newCustomerId`                          | `newCustomerID`     |
| "inner stopwatch"       | `innerStopwatch`                         | `innerStopWatch`    |
| "supports IPv6 on iOS?" | `supportsIpv6OnIos`                      | `supportsIPv6OnIOS` |
| "YouTube importer"      | `YouTubeImporter`<br>`YoutubeImporter`\* |                     |
| "Turn on 2SV"           | `turnOn2sv`                              | `turnOn2Sv`         |
| "Guava 33.4.6"          | `guava33_4_6`                            | `guava3346`         |

<!-- mdformat on -->

\*可接受，但不推荐。

**注意：** 英语中有些词的连字符用法
存在歧义：例如 “nonempty” 和 “non-empty” 都正确，
因此方法名 `checkNonempty` 和 `checkNonEmpty` 也同样都正确。

<a id="s6-programming-practices"></a>

## 6 编程实践

<a id="s6.1-override-annotation"></a>

### 6.1 `@Override`：始终使用

只要合法，方法就应标注 `@Override` 注解。
这包括类方法重写超类方法、类方法
实现接口方法、接口方法重新声明
超接口方法，以及为记录组件显式声明的
访问器方法。

**例外：** 可省略 `@Override`，条件是父方法
标注了 `@Deprecated`。

<a id="caughtexceptions"></a>

<a id="s6.2-caught-exceptions"></a>

### 6.2 捕获的异常：不可忽略

捕获异常后什么都不做，极少是正确的。
（典型做法是记录日志，或者若认为该异常
“不可能”发生，则将其作为 `AssertionError` 重新抛出。）

若 catch 块中确实应当完全不采取任何行动，
则应在注释中说明其正当理由。

```java
try {
  int i = Integer.parseInt(response);
  return handleNumericResponse(i);
} catch (NumberFormatException _) {
  // it's not numeric; that's fine, just continue
}
return handleTextResponse(response);
```

<a id="s6.3-static-members"></a>

### 6.3 静态成员：用类名限定

当对静态类成员的引用必须加以限定时，
用该类的名称限定，而非该类类型的引用或表达式。

```java
Foo aFoo = ...;
Foo.aStaticMethod(); // good
aFoo.aStaticMethod(); // bad
somethingThatYieldsAFoo().aStaticMethod(); // very bad
```

<a id="finalizers"></a>

<a id="s6.4-finalizers"></a>

### 6.4 终结方法：不使用

不要重写 `Object.finalize`。
终结支持已[*列入移除计划*](https://openjdk.org/jeps/421)。

<a id="javadoc"></a>

<a id="s7-javadoc"></a>

## 7 Javadoc

<a id="s7.1-javadoc-formatting"></a>

### 7.1 格式

<a id="s7.1.1-javadoc-multi-line"></a>

#### 7.1.1 一般形式

Markdown Javadoc 与传统 Javadoc 均可接受。
Markdown Javadoc 形如下例：

```java
/// Javadoc text is written here,
/// wrapped normally...
public int method(String p1) { ... }
```

传统 Javadoc 块的*基本*格式如下例所示：

```java
/**
 * Multiple lines of Javadoc text are written here,
 * wrapped normally...
 */
public int method(String p1) { ... }
```

……或采用下面这个单行示例：

```java
/** An especially short bit of Javadoc. */
```

基本形式始终可接受。当整个 Javadoc 块
（含注释标记）能容纳在一行时，可改用
单行形式。注意，这仅适用于不存在块标签（如
`@param`）的情况。

<a id="s7.1.2-javadoc-paragraphs"></a>

#### 7.1.2 段落

对于传统 Javadoc，段落之间用一个空行分隔——
即只含对齐的前导星号（`*`）的一行——若存在
块标签组，其前也留一个空行。除第一段外，每段都有 `<p>`
紧接在首词之前，其后不加空格。其他块级元素的
HTML 标签，如 `<ul>` 或 `<table>`，前面*不*加 `<p>`。

对于 Markdown Javadoc，段落按 Markdown 的
通常方式分隔：用除前导 `///` 外为空白的一行。不需要 `<p>`。

<a id="s7.1.3-javadoc-at-clauses"></a> <!-- historical link -->

<a id="s7.1.3-javadoc-block-tags"></a>

#### 7.1.3 块标签

所使用的标准“块标签”按 `@param`、
`@return`、`@throws`、`@deprecated` 的顺序出现，
且这四类绝不附带空描述。当块标签无法
容纳在一行时，续行相对 `@` 的位置缩进四个
（或更多）空格（传统 Javadoc），Markdown Javadoc
则恰好缩进两个空格。（在某些上下文中，四空格
缩进在 Markdown 中会被解释为缩进代码块。）

<a id="s7.2-summary-fragment"></a>

### 7.2 摘要片段

每个 Javadoc 块都以简短的**摘要片段**开头。
这一片段非常重要：在类索引、方法索引等
某些上下文中，它是文本中唯一出现的部分。

它是片段——名词短语或动词短语，而非完整句子。
它**不**以 ``A `Foo` is a...`` 或 `This method returns...` 开头，
也不构成 `Save the record.` 那样的完整祈使句。不过，
该片段要像完整句子一样大写并加标点。

**提示：** 常见错误是把简单的 Javadoc 写成
`/// @return the customer ID`。这是不对的，应改为
`/// Returns the customer ID.` 或 `/// {@return the customer ID}`。

<a id="s7.3.3-javadoc-optional"></a> <!-- historical link -->

<a id="s7.3-javadoc-where-required"></a>

### 7.3 何处使用 Javadoc

*至少*，每个*可见*的类、成员或记录组件
都要有 Javadoc，下文注明少数例外。
顶层类若为 `public` 则可见；成员若为 `public` 或 `protected`
且所属类可见，则可见；记录组件
若所属记录可见，则可见。

也可以有额外的 Javadoc 内容，见第 7.3.4 节
[非必需的 Javadoc](#s7.3.4-javadoc-non-required)。

<a id="s7.3.1-javadoc-exception-self-explanatory"></a>

#### 7.3.1 例外：自解释的成员

对于“简单、显而易见”的成员和记录组件
（例如 `getFoo()` 方法），*若*除“这个 foo”之外*确实*没有
别的值得一说，则 Javadoc 可选。

**重要：** 不应援引此例外来为省略
相关信息辩护，一般读者可能需要了解这些信息。
例如，对于名为 `canonicalName` 的记录组件，
即使其文档只会写 `@param canonicalName the canonical name`，也不要省略，
因为一般读者可能不清楚“规范名称”一词的含义！

<a id="s7.3.2-javadoc-exception-overrides"></a>

#### 7.3.2 例外：重写方法

重写超类型方法的方法上并不总是有 Javadoc。

<a id="s7.3.4-javadoc-non-required"></a>

#### 7.3.4 非必需的 Javadoc

其他类、成员和记录组件*按需
或按意愿*添加 Javadoc。

凡是要用实现注释来阐明类或成员的
整体用途或行为时，应改用 Javadoc 来写
该注释（使用 `///` 或 `/**`）。

非必需的 Javadoc 并不严格要求遵循
第 7.1.1、7.1.2、7.1.3 和 7.2 节的格式规则，当然仍建议如此。

<!-- NB: Keep this at the end of the file. See comment at top for details.
     {% endraw %} -->
