# Rust 风格指南

<!-- mdformat off -->
* TOC
{:toc}
<!-- mdformat on -->

<style>
.google3 {
  background-color: #34A853;
  color: white;
  border-radius: 5px;
  padding: 2px 6px;
}

.android {
  background-color: #a4c639;
  color: white;
  border-radius: 5px;
  padding: 2px 6px;
}

.chrome {
  background-color: #4285F4;
  color: white;
  border-radius: 5px;
  padding: 2px 6px;
}

.fuchsia {
  background-color: #c154c1;
  color: white;
  border-radius: 5px;
  padding: 2px 6px;
}

:is(h1, h2, h3, h4, h5, h6) :is(.google3, .android, .chrome, .fuchsia) {
  font-size: large;
  border-radius: 5px;
  padding: 4px 8px;
  vertical-align: 10%;
}
</style>

本文档是一份关于 Rust 编程语言在 Google 中使用的*风格指南*。
在此语境下，“风格”不仅仅指格式；它
还包含关于 API 与实现设计的指导。

Rust 被用在很多地方，包括
[google3](https://opensource.google/documentation/reference/glossary#google3)、
Android、ChromeOS、Fuchsia 和 Chrome，我们希望 Google 内部的 Rust 用法
在代码库内部和跨代码库都保持一致。除了为 Rust 代码带来一致性之外，
风格指导还有助于确立质量
标准。

## 背景

### 适用范围

本指南所列规则当前具有约束力的范围：

*   **在 Android、Chromium 及其他代码库中**：本风格指南是
    与其他代码库协商制定的，它们也打算开始
    采用本指南。这些代码库可能各自有关于应严格到何种程度
    应用本指南的规则。随着这些
    代码库采用本指南，此处会补充更多信息。

### 风格指南的目标

总体而言，我们编写本文档的理由与
[制定 C++ 风格指南的理由](https://google.github.io/styleguide/cppguide.html#Goals)相同。

大多数风格规则都源自下面列出的一个或多个目标。

<dl>

<dt>风格规则应把可读性与可维护性置于易写性之上</dt>
<dd>我们期望代码能长期存在，并且我们认为，
如果某条风格规则能提升可读性，那么在编写代码时
多付出一点额外努力，从长远看是值得的。
</dd>

<dt>风格规则应有利于更好的自动化</dt>
<dd>
大规模变更（LSCs）
在 Google 很常见，而一致性有助于
让 LSCs 更容易实施。
</dd>


<dt>在可能的情况下，风格规则应与更广泛的 Rust 生态保持一致</dt>
<dd>更广泛的 Rust 生态在风格上已经有相当高的一致性，
我们应尽可能依托这一点，以减少意外，并降低
学习 Google Rust 风格所需的工作量。
</dd>

<dt>风格规则应物有所值</dt>
<dd>Google 的每位 Rust 开发者和评审者都必须牢记这些风格规则：
因此，我们应谨慎，只纳入具有
实际收益的规则。
</dd>


<dt>风格规则可帮助避免细小的风格分歧</dt>
<dd>在很多情况下，理性的人对某种风格可能产生分歧，而且
我们预计这类分歧会经常出现在 CL 上。有了一条风格规则，就能
避免每次都重新争论。此类中没有其他
收益的规则应尽量少。
</dd>

</dl>

<a id="public-rules"></a>

## 遵循公开的 Rust 风格规则

遵循官方公开的 Rust 风格规则，但以它们不与
本风格指南冲突为前提。

*   [Rust 风格指南](https://doc.rust-lang.org/nightly/style-guide/)

    *   大多数代码格式约定由 rustfmt 自动强制执行。

*   [Rust API 指南](https://rust-lang.github.io/api-guidelines/)

所谓“冲突”，是指本风格指南建议的模式在 Rust 风格
指南中不被鼓励，或与其主要推荐的模式
相悖。

为什么本风格指南中的指导会偏离常规的 Rust 风格规则？

大多数风格指南有三个目标：一致性、可读性，以及鼓励
良好的 API 设计。无论具体做出何种选择，预先把这些选择
定下来都有助于大家减少无谓争论（bikeshedding）。

本风格指南同样有这些目标，但它还有一个不常见的额外目标：
为大规模变更（LSCs）铺平道路。像 Google 的许多大型代码库那样，
偶尔需要借助工具执行覆盖整个代码库的
重构：要让这件事顺利，代码
应当是工具易于处理的形式。一致性对此有帮助，
而有意识地采用便于重构的模式同样如此。

<a id="api-design-context"></a>

## 结合具体场景应用 API 设计规则

在应用与 API 设计相关的规则时，应区分两类
代码：

*   库代码

    *   供其他项目（应用或其他库）使用。
    *   解决相对通用的问题。

*   应用代码

    *   供单个应用内部使用。
    *   解决更具体的问题。

对于*库代码*，涉及 API 设计的风格指南规则具有约束力。

对于*应用代码*，API 设计方面的规则是强烈建议。在
应用这些规则时请记住：由于应用代码是为解决某个
具体问题而编写的，它通常应更看重简洁与直接，而非广泛的
可复用性。避免过早的泛化与抽象；专注于满足
当前需求所必需的东西。

<a id="code-organization"></a>

## 代码组织

*术语：*

*   *crate* 是一个编译单元。每个 crate 都包含一个匿名的 Rust
    模块，即“根模块”。

*   Rust *模块*是 crate 内部的代码组织单元。Rust 模块
    用于控制名称的可见性。模块可以嵌套，也
    可用于把代码拆分到多个文件和目录中。

以下各节说明：在 Chromium 中，最好**不要**用尽
把模块拆分到多个文件的所有可能性。

<a id="small-crates"></a>

### 优先使用小 crate <span class="chrome">[chrome]</span>

在 Chromium 中优先使用小 crate；理想情况下（但并非必须）是单个文件
（专注于一个抽象）。如果你的代码可以拆成小 crate，
就这么做。

一个 crate 对应一条 `rust_static_library`（chrome）规则，其中可
包含一个或多个 `.rs` 文件。

其他注意事项：

*   根模块可以 `re-export` 来自
    `leaf submodules` 的公共 API，从而使子模块成为 crate 的实现细节
    （因为用户无需了解这些子模块）。

*   这条关于小 crate 的规则对有子模块和无子模块的 crate 同样适用。
    先评估这些 API 是否需要放在同一个 crate 中，
    然后再考虑子模块是否有助于组织这些 API。

*   如果决定使用子模块，请遵循
    [预期的文件结构](#structure)。

在以下情况下允许使用更大的 crate：当
[trait impl 一致性规则](https://smallcultfollowing.com/babysteps/blog/2015/01/14/little-orphan-impls/)
迫使多个类型和 trait 必须放在同一个库中，或者当你正在
构建一个大型基础库时。

理由

在 Chromium 中推荐细粒度的库目标，这是因为我们的代码库规模庞大、
在构建图中添加依赖会产生非局部影响，
同时也是为了提升并行编译与构建缓存的性能。

<a id="structure"></a>

### 对 `rust_library` 源文件使用扁平的文件布局 <span class="chrome">[chrome]</span>

在 Chromium 中，属于同一个 `rust_library`（一个 Rust crate）的 `.rs` 源文件
必须位于同一个目录中。

不要用子目录来组织属于单个 crate 的文件。如果
觉得有必要把某个 crate 的文件放进子目录，这强烈表明
该 crate 已经[过于庞大](#small-crates)，应当
拆分。

这种 crate 布局有意区别于开源仓库中通常使用的
传统 Cargo 目录结构。

例外：`//third_party` 中同样用
[Cargo](https://doc.rust-lang.org/cargo/) 构建的 Rust 代码，应遵循传统的 Cargo
目录结构。

理由

Chromium 中的做法由以下因素决定：

*   基于对[小 crate](#small-crates) 的偏好，大多数
    `rust_library` 目标只会包含一个源文件。
*   由于上述原因，为每个 `rust_library`
    目标创建一个目录，会导致大多数目录只包含一个源文件。
*   多文件的 `rust_library` 目标也不应为子模块创建专门目录；
    这样可确保做法一致。

<a id="userdefined-item"></a>

### 以主要的用户定义项命名源文件和叶模块

当某个 `leaf module` 有一个主要的用户定义项（例如 `Foo`）时，该模块
应以该项命名（例如 `mod foo` 和 `foo.rs`）。

不以某个特定抽象为主要内容的叶模块，可以
按需命名。

理由

这让人一眼就能识别源文件或叶模块的
内容与用途。

<a id="non-leaf-modules"></a>

### 不要在非叶模块中实现 API

非叶模块中只应包含模块声明（而非
定义）和 `re-exports`。

注意，`leaf modules` 的定义允许以下子模块：
`mod test` 以及像 `#[cxx::bridge]` 这样的跨语言绑定模块。

例外：

*   在非叶模块中放少量起“串联作用”的核心实现代码
    也许是可以的。目标是不要在这些模块中放大量
    代码。

理由

这使查找更方便，并避免把结构与内容混在一起。

<a id="glob-imports"></a>

### 不要使用 glob 导入

不要使用 glob 导入，但在以下情形中可以
自行斟酌选择使用：

*   对内联模块使用 `use super::*`
*   在枚举的方法体以及主要
    处理该枚举的函数中使用 `use enum::*`
*   对非叶模块使用 `pub use submodule::*`
*   C++ 互操作：由于同一个命名空间（在 C++ 中）在不同
    Rust crate（在 Rust 中）里是各自的子模块，可以使用 glob 导入把
    这些命名空间合并成一份私有副本。例如：

    ```rust
    mod absl {
        pub use status::absl::*;
        pub use strings::absl::*;
    }
    ```

    在这个假想示例中，你可以像在 C++ 中一样从 Rust 使用 `absl::Status` 和 `absl::StrCat`，
    而不必把它们写成
    `status::absl::Status` 和 `strings::absl::StrCat`。

    这只能用于合并 C++ 命名空间，且合并后得到的
    模块不得公开。

若使用的第三方 crate 鼓励使用 prelude，是否允许由评审者
自行斟酌。

这也意味着应避免定义 prelude。

理由

glob 导入会增加执行 LSCs 的代码维护人员的负担，并且在没有交叉引用的环境中
更难判断某个类型的来源。

<a id="use-statement"></a>

### 一条 `use` 语句应只从一个模块导入条目

本规则对应 rustfmt 设置 `imports_granularity = Module`。

基本上，`use` 语句的 `{..}` 块内部不应出现任何 `::`。
例如：

<div class='goodcode'></div>

```rust
use foo::Foo;
use foo::bar::Bar;
use foo::bar::Baz;
```

<div class='goodcode'></div>

```rust
use foo::Foo;
use foo::bar::{Bar, Baz};
```

<div class='badcode'></div>

```rust
use foo::{Foo, bar::Bar};
```

<a id="prefer-local-trait-imports"></a>

### 优先使用局部作用域内的 trait 导入

在函数体内导入 trait，除非该 trait 的方法在整个文件中
被大量使用。

<div class='goodcode'></div>

```rust
fn foo(s: &str) -> Result<u8, std::num::ParseIntError> {
    // Import the trait within a function, not at the module scope.
    use std::str::FromStr;

    u8::from_str(s)
}
```

<a id="toplevel-functions"></a>

### 用模块名限定对顶层函数的调用

要使用定义在其他模块或 crate 中的顶层函数，应导入其
模块，并以 `modulename::functionname()` 的形式调用。例如：

<div class='goodcode'></div>

```rust
use std::mem;

let x = mem::transmute(y);
```

<div class='badcode'></div>

```rust
use std::mem::transmute;

let x = transmute(y);
```

例外：

*   导入名称已充分消除歧义的函数时，例如
    来自 C++ 的函数（在 C++ 中通常直接调用顶层（自由）
    函数）。
*   在 Chromium 中，导入来自
    [小而用途单一的第一方 crate](#small-crates) 的函数时。

*   当模块名本身容易冲突时。例如，当
    模块名是 C++ 命名空间名，且多个 crate 定义了相同的
    子模块时。

理由

许多 Rust 代码库一贯保持这样的风格：未限定的小写
名称被视为局部的，因此 `foo()` 可以认为来自同一模块。
这条规则主要是为了消除评审者之间的分歧，其收益主要是
一致性，以及在无交叉引用时阅读代码略为便利。

<a id="type-names"></a>

### 类型名应导入后不加限定地使用

默认情况下，代码中引用类型和 trait 时不应带
模块路径，例如应使用 `Regex` 而非 `regex::Regex`，并在
文件顶部或相关函数中写上
`use regex::Regex`。

例外：

*   存在歧义时，可以直接引用
    具有常见名称的类型，如 `io::Error`。也可以重命名
    （`use std::io::Error as IoError`）。
*   当你有大量成“组”的类型时，例如
    [`hir module in rustc`](https://doc.rust-lang.org/nightly/nightly-rustc/rustc_hir/hir/index.html)
    其中包含大量 HIR 类型。
*   在宏和生成代码中；此时要求 `use` 反而适得其反。
*   在依赖很多的代码中；此时把所有东西都导入会导致
    导入块非常庞大，却收益甚微。

理由

这条规则主要是为了消除评审者之间的分歧。

<a id="import-macro"></a>

### 使用恰当的导入机制 <span class="chrome">[chrome]</span>

*   <span class="chrome">Chrome</span> 使用 `chromium::import!()`。

<a id="code-formatting"></a>

## 代码格式与美观

<a id="formatting-other"></a>

### 使用恰当的格式化工具

使用恰当的格式化工具（例如 Chromium 中的 `git cl format`）。

配置（供风格指南作者参考）

如果代码库在意基于 stable 构建，且以下 `rustfmt` 选项在其 stable Rust 上
不可用，则可以选择不启用它们：

*   每行最多 100 列：
    [`max_width = 100`](https://rust-lang.github.io/rustfmt/?version=v1.6.0&search=#max_width)

*   在十六进制字面量中使用小写字母（`0xab123cdef` 而非
    `0xAB123CDEF`）：
    [`hex_literal_case = Lower`](https://rust-lang.github.io/rustfmt/?version=v1.6.0&search=#hex_literal_case)

*   宏匹配器的格式化：
    [`format_macro_matchers = true`](https://rust-lang.github.io/rustfmt/?version=v1.6.0&search=#format_macro_matchers)

*   对字面量中的不可见字符使用转义。例如，若希望
    文本包含零宽连接符，请使用 `\u{200D}`。

<a id="formatting-optout"></a>

### 选择退出自动格式化

可以使用 `#[rustfmt::skip]` 选择退出自动格式化，但仅限于
以下情形：

*   **手动对齐** – 如果因具体场景而有理由让一段
    代码按特定方式对齐（例如，为了可读性希望多行相似代码
    保持对齐，或某个
    构造矩阵的函数）。
*   **生成的代码**（理想情况下应改用 genrule）。

重要：不应因个人风格偏好而跳过格式化。

<a id="ownership-borrowing"></a>

## 所有权与借用

<a id="avoid-rc-arc"></a>

### 避免 `Rc` 和 `Arc`

管理内存时，优先使用唯一所有权和借用，而非 `Rc` 和 `Arc`。

例外：

*   当替代的所有权与借用结构在编写、理解或维护上
    会不合理地复杂时，使用 `Rc` 和 `Arc`。这属于需要
    在代码评审中讨论的判断。

理由

通常，Rust 可以不使用共享所有权
智能指针来表示对象图。这类指针会增加运行时开销，并带来其自身特有的
复杂性。来自其他语言的工程师可能倾向于过快地使用 `Rc` 和
`Arc`。

<a id="prefer-borrows"></a>

### 优先使用借用而非深拷贝

确实需要对象的深拷贝时才使用 `.clone()`。

避免把 `.clone()` 当作借用的替代。应让代码设计自然地
契合 Rust 的所有权与借用规则。不过，如果借用
关系变得过于复杂，`.clone()` 可以是务实的选择。

在克隆与借用之间做选择时，应考虑代码的
性能需求。

注意：本建议不适用于克隆 `Rc` 或 `Arc` 指针。克隆
引用计数指针并不会产生深拷贝，这是使用它们的
预期方式。

理由

由于内存分配和数据复制，深拷贝的代价可能很高。

<a id="inputs-and-outputs"></a>

## 函数输入与输出

<a id="flexible-references"></a>

### 对不可变数据接受灵活的引用

当函数接受借用的不可变数据时，应使用灵活性最高的
引用类型。传递指向数据本身的引用，而不是指向
智能指针、容器或包装器的引用。

<!-- mdformat off(keep table rows on single lines for Kramdown compatibility in the public style guide) -->

| 使用           | 而不是          | 原因？                                                          |
| ------------ | ------------ | ------------------------------------------------------------ |
| `&T`         | `&Box<T>`    | 借用 Box 内部的数据                                                 |
| `&[T]`       | `&Vec<T>`    | 接受任意切片，而非特定容器                                                |
| `&str`       | `&String`    | 接受字符串切片，而非指向拥有所有权字符串的引用                                      |
| `Option<&T>` | `&Option<T>` | 借用 Option 内部的数据                                              |

<!-- mdformat on -->

例外：

*   当期待非线性字符数据时，例如 Rope/Cord。

相关背景，请参见 Clippy 静态检查
[`borrowed_box`](https://rust-lang.github.io/rust-clippy/master/index.html#borrowed_box)
和
[ptr_arg](https://rust-lang.github.io/rust-clippy/master/index.html#ptr_arg)。

理由

接受不涉及具体智能指针、
容器或包装器的引用类型，会让函数更通用、性能更好：调用方
可以传入以各种方式持有的数据，而无需先复制。

<a id="return-iterators"></a>

### 返回类型中的迭代器与拥有所有权的集合

在可能的情况下，优先返回迭代器（具体类型或 `impl Iterator`），
而不是返回 `Vec<T>`。

注意：在应用代码中，如果返回 `Vec<T>` 能简化
代码，且并不明显需要迭代器在灵活性和性能上的
优势，那么这样做是可以的。

例外：

*   大多数调用方需要构造一个拥有所有权的 vector。
*   函数的实现本身就会自然地构造一个 vector。
*   返回值很可能需要被随机索引。
*   算法用 `for` 循环实现更合适，且强制分配带来的影响
    不大。
*   函数的设计目的就是创建一个新的拥有所有权的集合。
*   函数返回的是一个已存在的 vector。

理由

高度可复用的库代码通常应努力提供更灵活、
性能更好的 API。返回迭代器让调用方可以选择如何
消费数据：收集到 vector 中、在循环中处理，或链接
更多迭代器适配器。其中某些选择能让用户避免
不必要的分配。

在应用代码中，函数的使用模式往往更容易
预测。如果明确知道性能不是问题，或者数据反正会被
收集到 vector 中，那么返回 vector 会让 API 更简单。

<a id="accept-iterators"></a>

### 函数参数中的迭代器与切片

高度可复用的库代码若只需遍历输入，就应接受迭代器或
`impl IntoIterator`。

注意：在应用代码中，如果接受切片 `&[T]` 能简化
代码，且并不明显需要迭代器在灵活性和性能上的
优势，那么这样做是可以的。

理由

高度可复用的库代码通常应努力提供更灵活、
性能更好的 API。接受迭代器的函数为调用方带来：

*   更高的灵活性（数据可以来自任意集合）
*   更高的效率（数据无需被复制到一段连续的
    内存中）
*   更好的可组合性（函数能更好地配合迭代器链）

在应用代码中，函数的使用模式往往更容易
预测。如果明确知道性能不是问题，或者调用方反正总是持有
vector，那么接受切片会让 API 更简单。

<a id="accepting-into"></a>

### 接受 `Into`

在设计接受 `T`、但用户可能持有
多种类型的库 API 时，如果**调用点的
易用性至关重要**，可考虑接受 `impl Into<T>` 而非 `T`。

提示：这应与代码膨胀方面的顾虑相权衡；并不
要求在代码中大量使用 `Into<T>`。

注意：应用代码几乎不应使用 `impl Into<T>` 参数。

理由

使用 `impl Into<T>` 能让函数直接接受多种
兼容类型的不同实参。例如，接受 `impl Into<String>` 的函数
可以直接用 `String` 或 `&str` 字面量来调用。

这里的权衡在于：一边是调用点省去 `.into()` 的便利，
另一边是泛型的代价（API 签名更复杂、代码体积增大，
有时甚至带来类型推断困难）。

<a id="enum-vs-bool"></a>

### 在 API 中优先使用 `enum` 而非 `bool`

当参数用途不明显时，使用 `enum` 函数参数，
而不要用 `bool`。

如果确实使用 `bool`，可考虑用行内注释在实参列表中
说明该 `bool` 的用途。

<a id="reporting-errors"></a>

### 错误报告

选择契合你 API 契约的错误报告机制：`Option`、
`Result` 或 `panic!`。

**对于简单失败使用 `Option`**：原因显而易见，且调用方
不会从更多细节中获益。这最适合标准的、可预期的
结果，例如缺失值或解析不匹配。

<div class='goodcode'></div>

```rust
// Good: The cause of the failure is obvious (integer overflow). No further
// details could be reasonably provided.
fn checked_add(a: u32, b: u32) -> Option<u32> { ... }
```

**对于调用方需要上下文的可恢复失败使用 `Result`**，以便
处理错误。这类错误往往是由外部
因素（如 I/O 或网络）造成的“无法避免”的错误，即便实现正确的代码也无法
通过事先检查来预防。尽管如此，调用方仍能合理地
预见错误的种类（与文件相关的函数可能因 I/O
错误而失败）。错误细节让调用方能够区分失败模式并
恰当地恢复。

<div class='goodcode'></div>

```rust
// Good: The caller needs to know *why* it failed (NotFound vs PermissionDenied).
fn open_file(path: &Path) -> Result<File, io::Error> { ... }
```

**使用 `panic!` 来报告缺陷和被破坏的不变量。** 这类错误是
可以避免的：程序缺少某项检查，或是在未满足前置条件的情况下
调用了某个操作。这些缺陷必须在代码中修复，而不是
在运行时处理，不过借助
`catch_unwind` 或许可以实现粗粒度的恢复。

<div class='goodcode'></div>

```rust
// Good: Panics if the invariant (index must be in bounds) is violated.
// This indicates a bug in the caller's logic.
impl<T> MyVec<T> {
    pub fn remove(&mut self, index: usize) -> T {
        if index >= self.len() {
            panic!("index out of bounds");
        }
        // ...
    }
}
```

注意：某些代码库可能选择完全避免 panic，甚至要求
被破坏的不变量也通过 `Result` 报告。

例外：

*   面向开发者的二进制程序可以对非致命错误使用 panic。
*   测试可以使用 panic 来进行断言。

<a id="types"></a>

## 类型

<a id="newtypes-vs-type-aliases"></a>

### 新类型与类型别名

在以下情况下，使用
[新类型](https://doc.rust-lang.org/rust-by-example/generics/new_types.html)
而非类型别名：

*   如果你定义的类型有显著的语义差异。
*   对于值得拥有自己 API 的类型。
*   如果希望保留日后更改底层类型的灵活性，尤其是
    当你无法控制该类型的所有用法时。
*   为了类型安全，当这些类型容易被混淆时。例如，`Date`
    类型可以在内部计算中使用新类型来区分 `Day`、`Month` 和 `Year`
    这些数值。

<a id="prefer-named-fields"></a>

### 优先使用具名字段，而非元组和非新类型的元组结构体

优先使用带具名字段的类型而非元组，因为元组索引（`.0`、`.1`、……）
很快就会令人困惑。

例外：

*   新类型的元组结构体（只有一个字段的元组结构体）。
*   在极局部、不太可能产生混淆的场景中。

<a id="traits"></a>

## Trait

<a id="traits-yagni"></a>

### 在确有需要时才添加 trait 实现

一般原则是：底层库代码应主动预判用户的需求，
而应用代码则应按需添加 trait impl。

<a id="known-traits"></a>

### 实现已知的标准库 trait，而非自定义方法

如果某个方法的用途和行为与某个标准库 trait 相符，
就实现该 trait。例如，不要在 `Foo` 上编写
`fn from_str(&str) -> Self`，而应 `impl FromStr for Foo`。

出于可发现性的考虑，同时保留该方法和
trait 实现是可以接受的。

相关背景，请参见 Clippy 静态检查
[`should_implement_trait`](https://rust-lang.github.io/rust-clippy/master/index.html#should_implement_trait)
（[trait 列表](https://github.com/rust-lang/rust-clippy/blob/928349795f9f28f54e69bd0f0ffeed33de5e272a/clippy_lints/src/methods/mod.rs#L3940-L3971)）。

<a id="derive"></a>

### 尽可能使用 `#[derive()]`

如果手动实现可以用
`#[derive()]` 表达，就应避免手动实现。

<a id="generics-vs-dyn-trait"></a>

### 泛型与 `dyn Trait`

在库中，函数参数应优先接受泛型（`T: Trait` 或 `impl Trait`），
而不是 `dyn Trait`。

例外：

*   代码体积很重要的情形。

理由

-   效率

    -   额外的间接层：创建 `dyn Trait` 需要设置一个胖
        指针，并且对该 trait 上函数的每次调用都需要一次
        vtable 查找。
    -   如果函数接受 `dyn Trait`，编译器就无法执行某些
        在函数泛型时本可执行的优化，例如
        内联对该 trait 上函数的调用。

-   有些 trait 并不
    [`dyn` 兼容](https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility)。
    例如，若某个 trait 含有泛型函数、
    不带 `self` 参数的关联函数，或返回
    `Self` 的函数，则它不是 `dyn` 兼容的。

<a id="trait-vs-inherent-impl"></a>

### 何时定义 trait，何时使用固有实现

仅在以下目的下定义 trait：

*   为了支持泛型编程（在泛型
    函数和类型的约束中使用 `T: Trait`）。

*   为了接受或返回 `impl Trait` 或 `dyn Trait`。

*   为了定义[扩展 trait](#extension-traits)（但也请参见扩展 trait 一节中的
    注意事项）。

在所有其他想为某个类型实现功能的场合，请使用
[固有实现](https://doc.rust-lang.org/std/keyword.impl.html#inherent-implementations)。

不要仅仅为了组织代码而使用 trait。

<a id="extension-traits"></a>

### 扩展 trait

一种
[扩展 trait](https://rust-lang.github.io/rfcs/0445-extension-trait-conventions.html)
是为来自其他 crate 的类型添加方法的 trait。

扩展 trait 与其他 trait 的区别在于，它的唯一
目的就是为该类型添加方法；它并不打算用于泛型
（`T: Trait`、`impl Trait`）或动态分发（`dyn Trait`）。为表明这一点，
扩展 trait 的名称应带有 `~Ext` 后缀（例如
`ForeignTypeExt`）。

一般而言，拥有原始类型的团队也应拥有该扩展
trait。

例外：

*   预期会广为人知并带来
    显著价值的扩展方法，例如在基础库／框架中。

注意：本规则专门针对扩展 trait。把某个 trait 定义为输入 trait
（例如 `DateLike`）并在一批外部类型上
实现它，是相对常见的做法。

示例

```rust
extern crate foreign_crate;
use foreign_crate::ForeignType;

trait ForeignTypeExt {
  fn additional_method(&self);
}

impl ForeignTypeExt for ForeignType {
  fn additional_method(&self) { ... }
}
```

也可以为实现某个外部 trait 的
每一个类型定义扩展 trait。实际上，这等同于向
该外部 trait 添加默认方法：

```rust
extern crate foreign_crate;
use foreign_crate::ForeignTrait;

trait ForeignTraitExt {
  fn additional_method(&self);
}

impl<T: ForeignTrait> ForeignTraitExt for T {
  fn additional_method(&self) { ... }
}
```

理由

当同一个团队同时拥有扩展 trait 与被扩展的类型时，这
有助于避免基础类型与扩展 trait 之间，或两个扩展 trait 之间的
方法名冲突。

<a id="important-traits"></a>

### 重要 trait 的具体指导

*   **具有公共字段的类型**：考虑实现其所有子字段都
    已实现的 trait。

*   **错误类型**：尽可能实现 `Copy` trait。`Copy` 类型
    更易于管理和传播，因为它们可以按值传递
    而无需转移所有权。无法这样做的一个例子是
    错误必须包含非 `Copy` 字段（如 `String`）时。

*   **`Copy`**：当有理由确信该类型将来
    仍会是 `Copy` 时就实现它。

*   **`Clone`**：大多数类型都应实现 `Clone`，除非它们表示某种
    外部资源。

*   **`Default`**：若类型实现了 `new()` 或另有
    默认状态，就实现它。相关背景，请参见 Clippy 静态检查
    [`new_without_default`](https://rust-lang.github.io/rust-clippy/master/index.html#new_without_default).

*   **`PartialEq`** / **`Eq`**：若希望用户使用 `==` 运算符，
    优先实现 `PartialEq` 而非 `Eq`。确实要实现 `Eq` 时，应注意
    它额外要求的自反性（详情：
    https://doc.rust-lang.org/std/cmp/trait.Eq.html).

*   **`PartialOrd`** / **`Ord`**：若希望用户使用 `<` 或 `>`
    运算符，优先实现 `PartialOrd` 而非 `Ord`。确实
    实现 `Ord` 时，应注意它要求全序（详情：
    https://doc.rust-lang.org/std/cmp/trait.Ord.html).

*   **映射键**

    *   如果你认为某个类型很可能被用作映射键或
        以其他方式被缓存，就实现 `Hash` 和 `Eq`。
    *   此外，如果该类型有明确的全序，则实现 `Ord`
        （以及它所需的任何 trait）。

<a id="from-impls"></a>

### 为重要的 `From` impl 配对显式构造方法

如果某个类型有一个重要的 `From` impl，且预期它会成为构造该类型的
主要方式之一，就添加固有的 `::new()`、`::new_from_foo()` 或
`::from_foo()` 方法。

<a id="options-should-implement-default"></a>

### 选项结构体应实现 Default

字段全部公开、主要用作某个函数“选项袋”的
结构体应实现 `Default`。

理由

这便于使用结构体更新语法
(`Struct { a: 0, ..Default::default()}` ).

<a id="concurrency"></a>

## 并发

<a id="poison"></a>

### 处理中毒

无论使用场景看起来多么诱人，都绝不探入已中毒的 mutex 内部去
获取其中的数据。

<a id="async-await-chrome"></a>

### 不要使用 `async` / `.await` <span class="chrome">[chrome]</span>

不要在 Chromium 中使用 `async` / `.await`。

<a id="std-thread"></a>

### 不要通过 Rust 标准库启动新线程 <span class="chrome">[chrome]</span>

在 Chromium 中，优先使用 sequences 而非线程。

<a id="fuchsia-mutex"></a>

### 使用 `fuchsia_sync::Mutex` <span class="fuchsia">[Fuchsia]</span>

使用 Fuchsia 的 mutex 类型，而不要使用 `std::sync` 或 `parking_lot` 中的类型。

<a id="macros"></a>

## 宏

在考虑如何表达某个 API 时，按以下顺序优先选择：

-   常规的 Rust 函数、类型、trait、对象和模块。（尽可能避免宏、
    代码生成和元编程）。

-   `macro_rules!` 风格的宏。

-   其他代码生成策略（例如 `genrule`）。

-   `proc_macro` 宏。

当决定使用宏或代码生成时，请权衡其收益
与代价：

-   IDE、Code Search 及其他开发者工具在使用宏的代码上
    效果会变差。
-   宏可能制造出语言的方言，使工程师更难
    跨代码库协作。
-   大规模变更更难实施，成本也更高。

理由

**优先使用非宏机制：** 宏可能制造出语言的方言，
使工程师更难跨代码库协作。当读者看到某处
使用了宏时，相比不使用宏的代码，他们能对该代码做出的假设更少。
宏比常规 Rust 代码更难写对。

**简单的代码生成使用 `macro_rules!`：** 由于 Rust 宏作用于
AST，因此可能比基于文本的代码生成更稳健。

<a id="naming"></a>

## 命名

<a id="naming-methods"></a>

### 方法命名

方法命名遵循 Rust 标准库的风格。另请参见
Comprehensive Rust 课程中关于
[命名约定](https://google.github.io/comprehensive-rust/idiomatic/foundations-api-design/predictable-api/naming-conventions.html)
的指导。

具体注意事项：

*   结合恰当的 `self` 约定，使用 `as_...()`、`to_...()` 或 `into_...()`
    这类前缀。另请参见 Rust API 指南中的
    [这一节](https://rust-lang.github.io/api-guidelines/naming.html#ad-hoc-conversions-follow-as_-to_-into_-conventions-c-conv)
    以及 Clippy 静态检查
    [`wrong_self_convention`](https://rust-lang.github.io/rust-clippy/master/index.html#wrong_self_convention).

<a id="lifetimes"></a>

### 生命周期命名

生命周期应使用描述性名称，尤其是类型生命周期。

例外：

*   像 `Cow` 那样极其泛化的抽象的类型生命周期。
*   在适用时使用匿名生命周期（`'_`）是可以的。
*   当单字符生命周期只是表达方法输入与输出之间的关系，
    或是局部高阶生命周期约束（`for<'a>`）所需时，是可以使用的。
    最多两个这样的局部生命周期是可以的；如果需要更多，
    我们强烈建议使用描述性
    名称。

<a id="generic-parameters"></a>

### 泛型参数命名

为泛型参数使用简短名称（单字符或多字符），
并与其所代表的事物相关。单字母泛型是可以的，
但所选字母应在某种程度上能提示对象类型，理想情况下
取自最重要的 trait 约束。

当泛型处于相对无约束的语境时，`T` 或 `U` 都可以；也就是说，
这是一个面向大多数类型使用的 API，例如 `Vec<T>`。

<a id="naming-extension-traits"></a>

### 扩展 trait 的命名

为[扩展 trait](#extension-traits) 命名时，给名称加上 `~Ext`
后缀（例如 `ForeignTypeExt`）。

<a id="naming-initialization-functions"></a>

### 初始化函数的命名

为初始化函数命名时请遵循以下指导：

*   构造函数：使用 `new()`；若不止一个，则用 `new_with_foo()`。如果
    构造函数返回 `Result`，则使用 `try_new()`。

*   值到值的转换：使用 `from_foo()`，并配套一个 `From` impl。
    请参见
    [此处](https://doc.rust-lang.org/std/convert/trait.From.html#when-to-implement-from)
    了解关于何时可把某个操作视为值到值
    转换的细节。

<a id="avoid-abbreviations"></a>

### 避免缩写

不要使用项目之外的人不太可能知道的缩写（尤其是首字母缩略词和
首字母缩写）。不要通过删除单词内部的字母来
缩写。

另请参见
[Google C++ 风格指南](https://google.github.io/styleguide/cppguide.html#General_Naming_Rules)。

例外：

*   Wikipedia 上收录的常见缩写。
*   不太可能让项目之外的人困惑的缩写，例如 `IpAddr`。
    这应由你和评审者共同判断。总体而言，
    仍应倾向于不缩写。

<a id="writing-doc"></a>

## 何时以及如何撰写文档

为公共 API 添加文档注释，可借助 `missing_docs`
静态检查来辅助完成。

文档注释的最佳实践：

*   考虑加入示例：不必每个函数都有示例，但应在*某处*的示例中
    覆盖足够多的功能，让人了解该 crate 的
    工作方式。

*   对于可能因格式错误的输入而 panic 的函数，始终记录其
    panic 情形。

*   清楚地记录 unsafe 函数和 trait 的不变量。

*   使用大写和标点。

*   不要解释编程语言的基础知识。例如，不要
    这样做：

    ```rust
    struct MockFileSystem { ... }

    /// A mock implementation of the FileSystem trait, intended to be used in unit tests.
    impl FileSystem for MockFileSystem
    ```

例外：

*   注释应说出代码尚未表达的东西。如果
    没有什么有见地的话可说，与其琐碎地重复
    函数名，不如省略注释。例如，不要这样做
    （这种情况下 `allow` 该检查也是可以的）：

    ```rust
    /// Removes an element.
    pub fn remove_element() -> Element {}
    ```

*   通常可以省略对单个枚举变体的文档，
    尤其当它们的名称已不言自明时。

**如何格式化文档注释**

编写文档注释时请遵循以下指导：

*   使用 `///` 注释来记录紧随其后的条目，例如
    函数、结构体、枚举、trait 和类型别名。
*   使用 `//!` 注释来记录模块或库本身。这些
    注释应放在文件顶部。
*   遵循
    [Rust 官方风格指南中关于文档注释的部分](https://doc.rust-lang.org/nightly/style-guide/#doc-comments)所列规则。
*   使用 Markdown 语法。
*   对非文档注释使用普通注释语法（`//`），例如
    实现注释、用户不关心的 TODO、被注释掉的
    源代码等。
*   倾向于用直截了当的方式，使用 `///` 和 `//!`
    注释来记录，而不是从宏生成文档。这让
    文档在查看或修改源代码时可直接阅读。

混用文档注释（`///` 和 `//!`）与
普通注释（`//`）是可以接受的，甚至值得鼓励。如果有一样东西希望公开记录，
另一样东西想作为实现注释记下，那就两者都用！
例如：

<div class='goodcode'></div>

```rust
/// Finds the first `FooItem` with the given `name`, or `None` if not present.
// TODO: example.com/12345 - `name` should be &str, not String.
pub fn get_named(items: &[FooItem], name: String) -> Option<&FooItem> {...}
```

理由

许多（但并非全部）语言对文档注释与实现注释采用不同的
注释约定（例如额外的 `*` 字符）。
Rust 和 Python 的特别之处在于，不仅注释约定
不同，而且语法本身也完全不同。这给
Rust 生态带来实实在在的好处：

*   文档注释可被工具消费，包括 `rustdoc` 之类的文档生成器、
    IDE 功能以及 Kythe。
*   文档注释有标准的结构和格式规则（Markdown），
    从而可在这些场景中使用富文本。
*   文档注释语法使用上的错误（例如把它用在表达式
    而非可记录条目上）会触发静态检查，从而及早发现文档
    错误。如果没有静态检查错误，文档注释就保证
    对文档工具可见，为文档流程消除一定程度的不稳定与
    不可预测性。
*   文档注释是 AST 的一部分，因此可以由宏产生和消费，
    包括 `macro_rules!` 宏和过程宏。

<a id="other-features"></a>

## 其他 Rust 特性

<a id="unsafe"></a>

### Unsafe 代码

不要用 unsafe 代码，除非无法用安全代码实现
同样的功能。

如果确实必须编写 unsafe 代码：

*   把 unsafe 代码封装在安全的抽象中，并尽可能与业务
    逻辑隔离。理想情况下，unsafe 代码应位于单独的
    crate 中，除标准库外几乎没有依赖。
*   添加以 `SAFETY:` 开头的安全注释，说明代码为何
    正确。
*   为 unsafe 代码补充技术论证。视语境而定，这
    可以是针对单个 unsafe 块的论证，也可以是覆盖
    整个文件或构建目标的更通用的论证。该论证
    应回答以下问题：
    *   为什么这段代码没有用等价的安全写法？
    *   如果理由是性能，是否有基准测试？

<a id="unstable-features"></a>

### 不使用不稳定的特性

不要使用不稳定的特性。

例外：

*   <span class="android">Android</span> 嵌入式编程可能需要
    使用某些不稳定的特性。启用它们需要经过评审
    （以便寻找替代方案），但正确构建某个产物所绝对必需的
    特性通常会获得批准。
*   <span class="chrome">Chrome</span> 风格仲裁者可以对整个代码库
    一揽子批准少量特性。通常，只有具备明确稳定化路径的
    特性才会获得批准。
*   <span class="fuchsia">Fuchsia</span> 请参见
    [此处](https://fuchsia.dev/fuchsia-src/development/languages/rust/unstable) 的指导。

<a id="getters-and-setters"></a>

### getter 与 setter

编写和命名 getter 与 setter 应遵循以下指导：

*   对返回 `&T` 的 getter 使用 `foo()`；若 `T: Copy`，则按值返回 `T`。
*   对返回 `&mut T` 的 getter 使用 `foo_mut()`。
*   对会“清空”该值（把它设为 `None`
    或其他默认状态）并返回旧值的 getter 使用 `take_foo()`。
*   对按值接受 `T` 的 setter 使用 `set_foo()`。
*   对通过闭包操作的访问器使用 `with_foo()` / `with_mut_foo()`
    （详见[下文](#closure-accessors)）。这类访问器的调用形如
    `object.with_foo(|foo| frob(foo))`。
*   对返回旧值的 setter 使用 `replace_foo()`。

示例

```rs
impl Stuff {
   fn foo(&self) -> &Foo { ...  }
   fn foo_mut(&mut self) -> &mut Foo { ... }

   /// Sets "baz" property to `None` and returns the old value.
   fn take_baz(&mut self) -> Option<Baz> { ... }

   fn set_foo(&mut self, foo: Foo) { ... }

   /// Calls `f` with a borrow of the "bar" property.
   /// Returns the return value of `f`.
   fn with_bar<R>(&self, f: impl FnOnce(&Bar) -> R) -> R { ... }

   /// Calls `f` with a mutable borrow of the "bar" property.
   /// Returns the return value of `f`.
   fn with_mut_bar<R>(&self, f: impl FnOnce(&mut Bar) -> R) -> R { ... }

   /// Sets "foo" property to `foo` and returns the old value.
   fn replace_foo(&mut self, foo: Foo) -> Foo  { ... }
}
```

<a id="closure-accessors"></a>

#### 关于接受闭包的访问器的更多说明

接受闭包的访问器（`.with_foo()`）通常按
`object.with_foo(|foo| do_something_with(foo))` 的形式调用。在以下情形中，
它们可能是不错的选择：

*   当属性位于内部可变性包装器（例如
    `Mutex` 或 `RefCell`）中时。这些机制需要把对属性的访问
    限制在某个作用域内，而闭包正好提供了这个作用域。这通常
    比直接返回实现该作用域的 RAII 对象
    （例如 `MutexGuard<T>`）更可取，因为后者会泄露实现
    细节。

*   当属性被修改后还需要后续工作或校验，且
    无法使用 `set_foo()` 访问器时（例如因为该属性的
    类型克隆代价很高，或根本无法克隆）。

`with_foo()` 访问器通常会允许闭包返回一个值，并
通过 `with_foo()` 把它返回出去。

如果需要提供两个接受闭包的访问器，一个用于只读访问、
一个用于可变访问，通常把它们命名为 `with_foo()` 和
`with_mut_foo()`。否则，可变访问的
访问器也常使用 `with_foo()`。

<a id="expected-api-sets"></a>

### 成套实现预期的 API

如果实现了 `len()`，也要实现 `is_empty()`。相关背景，请参见 Clippy
静态检查
[`len_without_is_empty`](https://rust-lang.github.io/rust-clippy/master/index.html#len_without_is_empty)。

<a id="doc-hidden"></a>

### 不要访问你不拥有的、标记为 `#[doc(hidden)]` 的条目

把标记为 `#[doc(hidden)]` 的条目视为私有。除非你拥有
该代码，否则不要访问它们。

<a id="const-functions"></a>

### 负责任地使用 `const` 函数

只有当预期某个公共函数将来仍是 `const`（或能承诺在变化时
协助调用方迁移）时，才把它标记为 `const`。

理由

把 `const` 函数改成普通函数属于破坏性变更。

<a id="operator-overloads"></a>

### 避免出于非数学目的的重载

让运算符重载回归其原本的数学／逻辑用途，而不仅仅
是为了让代码更简洁（作为“语法糖”）。

<a id="non-exhaustive-enums"></a>

### 对公开暴露的枚举应用 `#[non_exhaustive]`

如果某个枚举是供其他团队使用的公共 API 的一部分，就把它标记为
`#[non_exhaustive]`。

例外：

*   枚举永远不会改变。例如：
    *   描述既有本体的枚举（例如，
        `enum Color { Red, Green, Blue }`）。
    *   只有两种状态、本可用布尔值表示的枚举（例如，
        `enum Visibility { Visible, Hidden }`）
*   枚举将来*可能*改变，但你承诺通过 LSC
    修复由此产生的破坏。

相关背景，请参见 Clippy 静态检查
[`exhaustive_enums`](https://rust-lang.github.io/rust-clippy/master/index.html#exhaustive_enums).

理由

把枚举标记为 `#[non_exhaustive]` 会迫使用户在 `match` 语句中
加入通配分支（`_ => ...`）。这确保日后向枚举
新增变体时代码仍能编译。

这条规则主要对跨团队边界使用的枚举很重要，因为
破坏范围可能很大。只被使用少量次数的枚举不会造成大范围
破坏，因此可以忽略本规则。

<a id="non-exhaustive-structs"></a>

### 对含公共字段的公共结构体应用 `#[non_exhaustive]`

含公共字段、且属于供其他团队使用的公共 API 的
结构体应标记为 `#[non_exhaustive]`。

例外：

*   结构体字段不太可能改变，例如因为它们描述某个
    既有本体（例如 Rectangle 类型），或评审者能有把握地
    确认它们不会改变。
*   结构体字段将来*可能*改变，但你承诺通过
    LSC 修复由此产生的破坏。
*   你希望让用户能够使用函数式记录更新（FRU）结构体
    初始化语法（`Person { name: "foo", ..Default::default() }`）。

理由

向所有字段都公开的结构体新增字段（即便是私有字段）属于
破坏性变更，因为调用方无法再在结构体
字面量中列出所有字段。

`#[non_exhaustive]` 结构体不能用结构体字面量
语法构造，同一 crate 内的代码除外。这样可以新增私有字段
而不破坏用户。

这条规则主要对跨团队边界使用的结构体很重要，
因为破坏范围可能很大。只被使用少量次数的
结构体不会造成大范围破坏，因此可以忽略本
规则。

<a id="must-use-on-functions"></a>

### 函数上的 `#[must_use]`

在以下情形中对函数使用 `#[must_use]`：

*   如果调用方忽略返回值就无法正确使用该函数。这包括
    纯函数（无副作用的函数），例如
    `HashMap::get()`。

*   任何返回值代表错误或关于函数行为的其他关键
    信息的函数。如果返回类型本身已经标注了
    `#[must_use]`（`Result` 便是如此），则该
    函数无需再标注 `#[must_use]`。

<a id="must-use-on-types"></a>

### 类型上的 `#[must_use]`

对那些由本应标注 `#[must_use]` 的函数
返回的类型使用 `#[must_use]`，依据的
是[上述规则](#must-use-on-functions)。

示例：

*   该类型是错误类型（类似于 `Result` 或 `StatusOr`）。

*   该类型表示一个惰性求值的计算。换句话说，
    函数调用本身什么也不做，需要访问返回值才能
    产生某种预期的副作用。

<a id="global-initialization"></a>

### 不要在 `main()` 之前运行代码

不要在 `main()` 之前让代码运行，例如不要使用
诸如 [ctor crate](https://docs.rs/ctor/latest/ctor/) 之类的技术。

## 实现方面的考虑

<a id="type-inference"></a>

### 不要过度使用类型推断

添加足够的显式类型，让熟悉该代码库的人能够
推断出被省略的类型是什么。

优先把类型加在变量声明上，而不是使用
[turbofish](https://doc.rust-lang.org/reference/glossary.html#turbofish)。如果
编译器迫使你添加 turbofish，一般可以加上 `_`
推断标记。

以下具体情形中大概应该添加类型：

*   调用具有泛型返回类型的方法时，例如 `.into()` 或
    `.parse()`。
*   复杂迭代器链的结果。

<a id="dont-check-then-unwrap"></a>

### 优先使用模式匹配，而非先检查再 unwrap

当输入数据保证某个操作不会 panic 时，避免使用可能 panic 的
操作。例如，不要对已知有效的值使用 `Option::unwrap`，
而应使用模式匹配向编译器证明正确性。

<div class='goodcode'></div>

```rust
// Good: The match arm proves to the compiler that `x` is `Some`.
// A panic is obviously not possible.
if let Some(value) = option {
    use_value(value);
}
```

<div class='badcode'></div>

```rust
// Bad: Correctness of `unwrap` relies on a runtime check that `option` is `Some`.
if option.is_some() {
    use_value(option.unwrap());
}
```

<a id="expect-over-unwrap"></a>

### 优先使用 `expect` 而非 `unwrap`

如果因为某个不变量无法在类型系统中表达而必须触发 panic，
请优先使用 `expect` 而非 `unwrap`，以说明原因。

<a id="non-exhaustive-enum-matching"></a>

### 匹配 `non_exhaustive` 枚举时不要省略模式

在针对 `non_exhaustive` 枚举的 `match` 语句中，
应尽量列出所有枚举变体。

如果你不关心具体的变体，就把它放进通配符分支。如果
你*只*关心特定变体，就使用 `if let` 或 `let … else {}`。

示例：

```rust
#[non_exhaustive]
pub enum Shape {
    Circle,
    Square,
    Triangle,
}
```

<div class='goodcode'></div>

```rust
fn process_shape(shape: Shape) {
  match shape {
    Shape::Circle => println!("It's a circle"),
    Shape::Square => println!("It's a square"),
    // Triangle and any future variants don't require any actions.
    Shape::Triangle | _ => {}
  }
}
```

<div class='goodcode'></div>

```rust
fn process_shape(shape: Shape) {
  if let Shape::Circle = shape {
    println!("It's a circle");
  }
}
```

<div class='badcode'></div>

```rust
fn process_shape(shape: Shape) {
  match shape {
    Shape::Circle => println!("It's a circle"),
    _ => {}
  }
}
```

例外：

*   你只关心特定变体，*而且* `match` 比
    `if let` 更清晰。

<a id="assertion-context"></a>

### 使用上下文字符串澄清断言

虽然有些断言不言自明，但许多断言能从额外的上下文中
受益：它说明断言为何预期成立，或是什么导致它被
违反。请使用 `assert!` 的可选格式字符串参数来传达
这一上下文。

你应始终考虑添加上下文，尤其是在以下
情形中：

*   如果你正打算给断言加一条注释。请改用格式字符串：
    它有一个好处，即会出现在日志中。
*   如果你预期失败的断言会被用户看到。在这种情况下，
    人类可读的解释比一个 Rust 表达式更有帮助。
*   如果记录某个值有助于理解断言为何失败。
*   用于澄清失败的断言究竟意味着
    *   客户端误用了某个 API（即他们应当改变对该
        API 的使用方式），还是
    *   实现中存在缺陷（即客户端应当提交一份缺陷
        报告）。

示例

**解释断言为何应当成立**

<div class='goodcode'></div>

```rust
    assert!(
        values.is_sorted(),
        "`values` is populated from a `PriorityQueue`, so we expect it to be sorted"
    );
```

**记录一个值以澄清断言为何失败**

<div class='goodcode'></div>

```rust
assert!(refund > 0, "Refund must be positive, got {refund:?}");
```

**标记 API 的误用**

<div class='goodcode'></div>

```rust
impl Database {
    ...

    fn execute_query(&self, query: &str) {
        assert!(self.stream.is_some(), "Call connect() before executing queries");
    }

    ...
}
```

**不要只用上下文字符串重复条件**

<div class='badcode'></div>

```rust
assert!(values.is_sorted(), "values should always be sorted");
```

<a id="combinator-chains"></a>

### 直接迭代更清晰时不要使用迭代器组合子链

避免以损害可读性的方式使用组合子链。具体而言：

*   避免又长又复杂的组合子链。
*   不要在 `for` 循环的头部构造组合子链。应当
    把组合子链赋给一个变量，再在 `for` 循环中
    消费该变量。
*   避免使用 `Iterator::for_each`，除非你确信有充分理由。
    `for` 循环通常更易读。

对于较短的链，以及组合子本身提供了大量
逻辑、否则就得在相应的 `for` 循环中逐一
写出的情形，组合子*确实*更可取。

示例

**复杂的组合子链**

下面是一条难以阅读的组合子链示例，因为它涉及
条件判断，并且会修改外部状态：

<div class='badcode'></div>

```rust
let mut error_count = 0;
let _processed_items: Vec<_> = items
    .into_iter()
    .map(transformation_that_may_fail)
    .map(|result| {
        if result.is_err() {
            error_count += 1;
        }
        result
    })
    .filter_map(Result::ok)
    .collect();
```

对应的 `for` 循环更易读：

<div class='goodcode'></div>

```rust
let mut error_count = 0;
let mut processed_items = Vec::with_capacity(items.len());

for item in items {
    match transformation_that_may_fail(item) {
        Ok(val) => processed_items.push(val),
        Err(_) => error_count += 1,
    }
}
```

**for 循环中的组合子链**

避免在 `for` 循环的头部构造组合子链：

<div class='badcode'></div>

```rust
for bug in bug_descriptions
    .iter()
    .filter_map(|description| parse_bug_description(description).ok())
    .filter(|bug| bug.priority <= Priority::P1)
{
    assign_bug(bug);
}
```

应当把组合子链赋给一个变量。这样可以减少杂乱，
而且变量名还能说明这条组合子链的作用：

<div class='goodcode'></div>

```rust
let urgent_bugs = bug_descriptions
    .iter()
    .filter_map(|description| parse_bug_description(description).ok())
    .filter(|bug| bug.priority <= Priority::P1);

for bug in urgent_bugs {
    assign_bug(bug);
}
```

**何时应优先使用组合子链**

下面是一个更适合使用组合子链的例子：

<div class='goodcode'></div>

```rust
let threshold_exceeded = values.iter().any(|&v| v > threshold);
```

对应的 for 循环更难读，而且重新发明了
`any()` 中已有的逻辑：

<div class='badcode'></div>

```rust
let mut threshold_exceeded = false;
for v in values {
  if v > threshold {
    threshold_exceeded = true;
    break;
  }
}
```

<a id="catch-unwind"></a>

### 不要调用 `panic::catch_unwind`

在第一方 Rust 代码中禁止使用 `panic::catch_unwind`。

例外：

*   只要绝不*依赖*它来保证任何性质，把它用作
    纵深防御机制是可以接受的。已经在努力
    避免 panic 的代码库，可以选择用 `catch_unwind`
    恢复机制包裹关键入口点，以防有 panic 漏过。
    代码作者必须让评审者相信，该代码库已经尽
    其所能来避免 panic。此例外仅适用于有可能
    以 `panic=unwind` 运行的代码 (因此不适用于
    <span class=chrome>Chrome</span>, <span class=android>Android</span>,
    <span class=fuchsia>Fuchsia</span>).

理由

Rust 代码可能运行在许多环境中，而 `panic::catch_unwind` 只有
在 `panic=unwind` 的环境中才能正常工作。虽然生产
二进制文件的最终 panic 处置方式尚未确定，但 Chrome、
Android 和 Fuchsia 都要求 `panic=abort`。

<a id="prefer-format-or-write"></a>

### 拼接与替换时优先使用 `format!` / `write!`

在以下情形中，优先使用 `format!()` 和 `write!()`，
而非其他方案：

*   拼接两个以上的字符串。例如，使用
    `format!("{a}{b}{c}")` 而非 `a + b + c`。
*   对字面量字符串执行替换（而不是使用
    `str::replace`）。

理由

*   `format!` / `write!` 比用 `+` 拼接字符串
    所需的内存分配更少。
*   优先使用标准格式字符串，不要自创模板语法。

<a id="test-framework"></a>

## 使用适合各代码库的测试框架

多数代码库使用自己专属的测试框架，而非 `#[test]`。

*   <span class="chrome">Chrome</span> 使用
    [rust_gtest_interop](https://source.chromium.org/chromium/chromium/src/+/main:testing/rust_gtest_interop/)。
    这使得把 Rust 测试集成到 C++ 测试二进制文件中成为可能。

*   <span class="fuchsia">Fuchsia</span> 使用 `#[fuchsia::test]`。参见
    [此处](https://fuchsia.dev/fuchsia-src/development/languages/rust/testing.md)
    了解更多详情。
