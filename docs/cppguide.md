# Google C++ 风格指南

<style>
h5 > a.anchorjs-link,
h6 > a.anchorjs-link {
  display: none;
}
</style>

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

<a id="Background"></a>

## 背景

C++ 是 Google 众多开源项目所使用的主要开发语言之一。正如每位
C++ 程序员所知，这门语言具备许多强大的特性，但这种强大也带来了
复杂性，而复杂性反过来又会让代码更容易出错，并且更难阅读与
维护。

本指南的目标是通过详细说明编写 C++ 代码时该做与不该做的事，来
驾驭这种复杂性。制定这些规则是为了让代码库保持可管理，同时仍
允许程序员富有成效地使用 C++ 语言的各项
特性。

*风格*（也就是可读性）是我们对那些约束 C++ 代码的约定所使用的
称呼。「风格」这个术语其实有点用词不当，因为这些约定所涵盖的
远不止源文件的排版格式。

Google 开发的大多数开源项目都遵循本指南中的
各项要求。

请注意，本指南并非 C++ 教程：我们假定读者已经熟悉这门
语言。

还要注意，本指南中许多代码片段本身并不算良好的风格！即使是那些
用来展示良好风格与排版的示例，往往也带有一些特性，使它们不适合
作为提交的代码。许多示例缺少真实代码中必不可少的注释或技术细节，
而现有的那些注释，又常常是些位置古怪、针对规则或示例本身的
评述。请勿把这些片段照搬为真实代码的
模板。

<a id="Goals"></a>

### 风格指南的目标

我们为什么要有这份文档？

我们认为本指南应当服务于几个核心目标。这些正是支撑每一条具体规则的
根本 **原因**。把这些理念摆到前台，我们希望让讨论有据可依，也让更
广泛的社区更清楚地理解：这些规则为何存在，以及为何做出某些特定的
决定。如果你明白每条规则服务于什么目标，大家就更容易看清一条规则
何时可以被豁免（有些确实可以），以及要改动本指南中的某条规则，
需要提出什么样的论证或替代
方案。

就我们目前所见，风格指南的目标如下：

**风格规则应当物有所值**
:   一条风格规则带来的收益，必须大到足以让我们有理由要求
    全体工程师都记住它。这里的收益，是相对于「假如没有这条
    规则，我们会得到的代码库」来衡量的；因此，一条针对危害
    极大做法的规则，如果人们本来就不太可能那样做，它的收益
    也可能很小。这条原则主要解释的是我们**没有**哪些规则，
    而不是有哪些规则：例如，`goto` 违背了后面的许多原则，
    但它如今已几乎绝迹，因此《风格指南》
    并不讨论它。

**为读者优化，而不是为编写者优化**
:   我们的代码库（以及提交到其中的绝大多数单个组件）
    预计会存续相当长的一段时间。因此，我们大部分代码
    被阅读的时间将多于被编写的时间。我们明确选择为
    一位普通软件工程师阅读、维护和调试代码库中代码
    的体验做优化，而不是图编写这些代码时省力。
    「为读者留下线索」是这条原则中尤其常见的一个要点：
    当某段代码中发生了令人意外或不寻常的事情时（例如
    指针所有权的转移），在使用处为读者留下文字提示
    是很有价值的（`std::unique_ptr` 在调用点毫不含糊
    地展示了所有权的转移）。

**与既有代码保持一致**
:   在整个代码库中统一使用同一种风格，能让我们把精力放在其他
    （更重要的）问题上。一致性也让自动化成为可能：那些格式化你的
    代码或调整你的 `#include` 的工具，只有在你的代码符合工具的
    预期时才能正常工作。在很多情况下，被归为「保持一致」的规则
    其实可以归结为「随便挑一种，然后别再纠结」；在这些地方允许
    灵活性所带来的潜在价值，抵不过人们为此争论不休的
    成本。不过，一致性也有其限度：当既没有明确的技术论据、
    也没有长期方向时，它是一个不错的平局决胜依据。它在局部
    适用得更重（按单个文件，或针对一组紧密相关的接口）。一般
    不应把一致性当作理由，用来在不考虑新风格的收益、
    也不考虑代码库随时间向更新风格收敛趋势的
    情况下，仍以旧风格
    行事。

**在适当的时候与更广泛的 C++ 社区保持一致**
:   与其他组织使用 C++ 的方式保持一致，其价值与在代码库内部
    保持一致出于同样的理由。如果 C++ 标准中的某项特性解决了一个
    问题，或者某种惯用法已广为人知并被接受，那就是采用它的
    一个理由。然而，有时标准特性和惯用法本身存在缺陷，或者
    设计时压根没有把我们代码库的需求考虑在内。在这些情况下
    （如下文所述），对标准特性加以限制或禁用是恰当的。在
    某些情况下，我们更偏爱自研或第三方库，而不是 C++ 标准中
    定义的库，或是出于对其优越性的判断，或是因为把代码库
    迁移到标准接口的价值不足。

**避免令人意外或危险的构造**
:   C++ 有些特性，比人们乍看之下以为的更令人意外、也更危险。
    风格指南中某些限制正是为防止落入这些陷阱而设。对于这类
    限制，给予风格指南豁免的门槛很高，因为豁免此类规则
    往往会直接危及程序的
    正确性。

**避免普通 C++ 程序员会觉得棘手或难以维护的构造**
:   C++ 有些特性，由于会给代码引入复杂性，可能并不普遍
    适用。在被广泛使用的代码中，使用更刁钻的语言构造
    或许更容易被接受，因为更复杂实现带来的任何收益，
    都会被大量使用成倍放大；而在接触代码库中新的部分时，
    理解这份复杂性的成本无需再次付出。拿不准时，
    可以向你的项目负责人申请对这类规则的豁免。
    这对我们的代码库尤为重要，因为代码所有权和团队
    成员会随时间变化：即便目前所有接触某段代码的人
    都理解它，也无法保证几年之后这种理解
    依然
    成立。

**留意我们的规模**
:   在一个拥有 1 亿行以上代码、数千名工程师的代码库中，某位
    工程师犯下的一些错误或做出的简化，可能会让许多人付出
    代价。例如，避免污染全局命名空间尤其重要：在数亿行代码的
    代码库中，名字冲突很难处理；如果所有人都把东西放进全局
    命名空间，这类冲突也
    很难避免。

**必要时向优化让步**
:   性能优化有时是必要且恰当的，即便它与本文档中的
    其他原则相冲突。

本文档的意图是在合理限制的前提下提供最大程度的指导。
一如既往，常识与良好的品味应当占上风。这里所说的，特指
整个 Google C++ 社区既有的约定，而不只是你个人或你团队
的偏好。对聪明或不同寻常的构造要保持怀疑、慎于使用：
没有明文禁止并不等于获准照做。请运用你的判断力，
如果拿不准，请尽管向你的项目负责人
征求更多
意见。

<a id="C++_Version"></a>

## C++ 版本

目前，代码应以 C++20 为目标，也就是说不应使用 C++23 的特性。
本指南所面向的 C++ 版本会（积极地）随时间推进。

请勿使用[非标准扩展](#Nonstandard_Extensions)。

在项目中采用 C++17 与 C++20 的特性之前，请先考虑向其他环境的
可移植性。

<a id="Header_Files"></a>

## 头文件

通常，每个 `.cc` 文件都应有一个对应的 `.h` 文件。有一些常见的
例外，例如单元测试，以及那些小型 `.cc` 文件——其中仅含一个
`main()` 函数。

正确使用头文件，能对你代码的可读性、体积和性能产生
巨大的影响。

下面这些规则将带你避开使用头文件时的
各种陷阱。

<a id="Self_contained_Headers"></a>

### 自包含的头文件 []() {#The_-inl.h_Files}

头文件应当是自包含的（可独立编译），并以 `.h` 结尾。
那些供包含使用的非头文件应以 `.inc` 结尾，并且应当
少用。

所有头文件都应当是自包含的。使用者和重构工具在包含某个头文件时，
不应被迫遵守特殊条件。具体来说，头文件应当带有
[头文件保护](#The__define_Guard)，并包含它所需要的其他所有
头文件。

当一个头文件声明了内联函数或模板，而该头文件的客户会对其进行
实例化时，这些内联函数和模板也必须在头文件中有定义，要么
直接定义在头文件里，要么定义在它所包含的文件中。不要把这些
定义挪到单独包含的（`-inl.h`）头文件中；这种做法过去很常见，
但现已不再允许。当一个模板的所有实例化都发生在同一个 `.cc`
文件中时——或是因为它们是
[显式](https://en.cppreference.com/w/cpp/language/class_template#Explicit_instantiation)
实例化，或是因为其定义仅对该 `.cc` 文件可见——该模板的
定义可以留在那个文件中。

确有少数情形，专为被包含而设计的文件并非自包含的。它们通常
打算被包含在不寻常的位置，例如另一个文件的中间。它们可能
不使用[头文件保护](#The__define_Guard)，也可能不包含自己的
前置依赖。这类文件请以 `.inc` 为扩展名命名。请少用，
并尽可能优先选用自包含的头文件。

<a id="The__define_Guard"></a>

### #define 保护

所有头文件都应有 `#define` 保护，以防止被多次包含。符号名的
格式应为
<code><i>&lt;PROJECT&gt;</i>&#95;<i>&lt;PATH&gt;</i>&#95;<i>&lt;FILE&gt;</i>&#95;H&#95;</code>。

为保证唯一性，它们应基于项目源码树中的完整路径。例如，
文件 `foo/src/bar/baz.h` 在项目 `foo` 中应具有如下
保护：

<div class='goodcode'></div>

```cpp
#ifndef FOO_BAR_BAZ_H_
#define FOO_BAR_BAZ_H_

...

#endif  // FOO_BAR_BAZ_H_
```

<a id="Include_What_You_Use"></a>

### 包含你所需要的头文件

如果源文件或头文件引用了在别处定义的符号，该文件应直接包含
那个意图提供该符号声明或定义的头文件。不应出于任何其他
理由去包含
头文件。

不要依赖传递包含。这样人们就能从自己的头文件中移除不再需要的
`#include` 语句，而不会破坏使用者。这也适用于相关的头文件：
`foo.cc` 应当包含 `bar.h`，即便 `foo.h` 已经包含了
`bar.h`，只要它用到了其中的符号。

<a id="Forward_Declarations"></a>

### 前置声明

尽可能避免使用前置声明。请改为
[包含你所需要的头文件](#Include_What_You_Use)。

##### 定义

「前置声明」是指对一个实体做出声明，却不附带相应的
定义。

<div class='neutralcode'></div>

```cpp
// In a C++ source file:
class B;
void FuncInB();
extern int variable_in_b;
ABSL_DECLARE_FLAG(flag_in_b);
```

##### 优点

*   前置声明可以节省编译时间，因为 `#include` 会迫使编译器打开
    更多文件、处理更多输入。
*   前置声明可以避免不必要的重新编译。由于头文件中的无关改动，
    `#include` 可能迫使你的代码更频繁地被
    重新编译。

##### 缺点

*   前置声明可能隐藏依赖关系，使得头文件变动时用户代码跳过必要的
    重新编译。
*   与 `#include` 语句相比，前置声明会让自动化工具难以发现定义
    该符号的模块。
*   前置声明可能被库后续的改动所破坏。对函数和模板做前置声明，
    会妨碍头文件维护者对其 API 做出本可兼容的改动，
    例如放宽参数类型、为模板参数添加默认值，
    或迁移到一个新的
    命名空间。
*   对命名空间 `std::` 中的符号做前置声明会导致未定义行为。
*   有时很难判断到底需要前置声明还是完整的 `#include`。
    用前置声明替换 `#include` 可能悄无声息地改变代码的
    含义：

    <div class='neutralcode'></div>

    ```cpp
    // b.h:
    struct B {};
    struct D : B {};

    // good_user.cc:
    #include "b.h"
    void f(B*);
    void f(void*);
    void test(D* x) { f(x); }  // Calls f(B*)
    ```

    如果把 `#include` 替换为对 `B` 和 `D` 的前置声明，
    `test()` 就会调用 `f(void*)`。

*   对某个头文件中的多个符号做前置声明，可能比直接
    `#include` 该头文件更啰嗦。

*   为便于前置声明而组织代码（例如用指针成员代替对象成员），
    会让代码更慢、更复杂。

##### 结论

不要对你的项目并不拥有的实体使用前置声明。

对于你确实拥有的实体：

*   尽量让某个声明所在的头文件足够轻量，以便能够
    直接包含它。
*   如果完整头文件包含起来代价太高，试着加快该头文件的
    编译速度。
*   如果你凭最佳的工程判断认为，前置声明是解决变慢问题的
    更好办法，那就运用这一判断，使用前置声明。

<a id="Defining_Functions_in_Header_Files"></a>

### 在头文件中定义函数 []() {#Inline_Functions}

只有当定义很短时，才在头文件中把函数定义放在它的声明处。
如果定义出于其他原因必须留在头文件中，请把它放到文件的
内部部分。若有必要使该定义满足 ODR 安全，请用 `inline`
说明符标记它。

##### 定义

定义在头文件中的函数有时被称为「内联函数」，这是一个含义
有点过载的术语，指向若干彼此不同却又相互重叠的
情形：

1.  *文本内联*的符号，其定义会在声明处
    直接展现在读者面前。
2.  定义在头文件中的函数或变量是*可内联展开*的，因为它的
    定义可供编译器取得，并用于
    [内联展开](https://en.wikipedia.org/wiki/Inline_expansion)，
    从而可能生成更高效的目标代码。
3.  *ODR 安全*的实体不违反
    [「单一定义规则」](https://en.cppreference.com/w/cpp/language/definition)，
    对于定义在头文件中的东西，这往往要求加上
    [inline](https://en.cppreference.com/w/cpp/language/inline)
    关键字。

虽然函数往往是更容易引起困惑的来源，但这些定义同样适用于
变量，本文的规则也一并适用。

##### 优点

*   以文本内联的方式定义函数，能减少访问器、修改器这类简单
    函数的样板代码。
*   如上所述，对于小函数，头文件中的函数定义*可以*借助
    编译器的内联展开，带来更高效的
    目标代码。
*   函数模板和 `constexpr` 函数通常需要定义在声明它们的
    头文件中（但不一定在公开部分）。

##### 缺点

*   把函数定义嵌进公开 API，会让该 API 更难快速浏览，
    并给该 API 的读者带来认知负担——函数越
    复杂，代价越高。
*   公开的定义会暴露实现细节，这些细节往好了说是无害的，
    往坏了说往往纯属多余。

##### 结论

只有当函数很短时（比如说 10 行或更少），才在它的公开声明处
定义它。更长的函数体请放到 `.cc` 文件中，除非出于性能或
技术原因必须留在头文件里。

即便某个定义必须放在头文件中，这也不足以构成把它放进公开
部分的理由。相反，定义可以放在头文件的内部部分，例如类的
[私有](#Access_Control) 部分、名称中包含 `internal` 的
命名空间内，或者类似 `// Implementation details only below here`
这样的注释之下。

一旦定义进入头文件，就必须具备 ODR 安全性：要么带有
`inline` 说明符，要么因是函数模板、或是在首次声明时
定义于类体内而被隐式指定为内联。

<div class='goodcode'></div>

```cpp
template <typename T>
class Foo {
 public:
  int bar() { return bar_; }

  void MethodWithHugeBody();

 private:
  int bar_;
};

// Implementation details only below here

template <typename T>
void Foo<T>::MethodWithHugeBody() {
  ...
}
```

<a id="Names_and_Order_of_Includes"></a>

### 头文件的名称与顺序

按以下顺序包含头文件：相关头文件、C 系统头文件、C++ 标准库
头文件、其他库的头文件、你所在项目的头文件。

项目的所有头文件都应以项目源码目录下级路径的形式列出，不要
使用 UNIX 目录别名 `.`（当前目录）或 `..`（父目录）。
例如，`google-awesome-project/src/base/logging.h` 应当
被包含为：

<div class='goodcode'></div>

```cpp
#include "base/logging.h"
```

只有当某个库要求使用尖括号路径时，才用尖括号来包含头文件。
具体而言，以下头文件需要使用
尖括号：

*   C 和 C++ 标准库头文件（例如 `<stdlib.h>` 与 `<string>`）。
*   POSIX、Linux 和 Windows 系统头文件（例如 `<unistd.h>` 与
    `<windows.h>`）。
*   少数情况下的第三方库（例如 `<Python.h>`）。

在 <code><var>dir/foo</var>.cc</code> 或
<code><var>dir/foo_test</var>.cc</code> 中，若其主要目的是实现或
测试 <code><var>dir2/foo2</var>.h</code> 中的内容，请按如下顺序
排列你的包含：

1.  <code><var>dir2/foo2</var>.h</code>。
2.  一个空行
3.  C 系统头文件，以及尖括号中带 `.h` 扩展名的其他头文件，
    例如 `<unistd.h>`、`<stdlib.h>`、`<Python.h>`。
4.  一个空行
5.  C++ 标准库头文件（不带扩展名），例如 `<algorithm>`、
    `<cstddef>`。
6.  一个空行
7.  其他库的 `.h` 文件。
8.  一个空行。
9.  你所在项目的 `.h` 文件。

用空行把每个非空分组隔开。

按照推荐的顺序，如果相关头文件
<code><var>dir2/foo2</var>.h</code> 漏掉了任何必要的包含，那么
<code><var>dir/foo</var>.cc</code> 或 <code><var>dir/foo</var>_test.cc</code>
的构建就会失败。因此，这条规则能确保构建失败首先出现在这些
文件的维护者面前，而不是其他包里无干的人面前。

<code><var>dir/foo</var>.cc</code> 与 <code><var>dir2/foo2</var>.h</code>
通常位于同一目录（例如 `base/basictypes_test.cc` 与
`base/basictypes.h`），但有时也可能位于不同的
目录中。

请注意，像 `stddef.h` 这样的 C 头文件与它们对应的 C++ 版本
（`cstddef`）本质上可以互换。两种风格都可以接受，但请优先
与既有代码保持一致。

在每个分组内，包含语句应按字母顺序排列。请注意，较旧的代码
可能不符合这条规则，应在方便时予以修正。

例如，
`google-awesome-project/src/foo/internal/fooserver.cc` 中的包含可能如下所示：

<div class='goodcode'></div>

```cpp
#include "foo/server/fooserver.h"

#include <sys/types.h>
#include <unistd.h>

#include <string>
#include <vector>

#include "base/basictypes.h"
#include "foo/server/bar.h"
#include "third_party/absl/flags/flag.h"
```

**例外：**

有时，平台相关的代码需要条件包含。这类代码可以把条件包含放在
其他包含之后。当然，请让平台相关的代码保持短小且局部化。
示例：

<div class='goodcode'></div>

```cpp
#include "foo/public/fooserver.h"

#ifdef _WIN32
#include <windows.h>
#endif  // _WIN32
```

<a id="Scoping"></a>

## 作用域

<a id="Namespaces"></a>

### 命名空间

除少数例外，请把代码放进命名空间。命名空间应有基于项目名称、
可能还基于其路径的唯一名称。不要使用
*using 指令*（例如 `using namespace foo`）。不要使用内联命名空间。
关于匿名命名空间，请参见[内部链接](#Internal_Linkage)。

##### 定义

命名空间把全局作用域划分成一个个彼此不同、带有名字的作用域，
因此有助于防止全局作用域中的名字冲突。

##### 优点

命名空间提供了一种在大型程序中防止名字冲突的方法，同时
又让大多数代码可以使用相当简短的名字。

例如，如果两个不同的项目都在全局作用域中有一个类 `Foo`，
这些符号可能在编译期或运行期发生冲突。如果每个项目都把自己的
代码放进命名空间，`project1::Foo` 与 `project2::Foo` 就成了
互不冲突的不同符号，而每个项目命名空间内的代码仍可不带前缀地
引用 `Foo`。

内联命名空间会自动把其中的名字放入外围作用域。
例如，请看下面这段代码：

<div class='neutralcode'></div>

```cpp
namespace outer {
inline namespace inner {
  void foo();
}  // namespace inner
}  // namespace outer
```

表达式 `outer::inner::foo()` 与 `outer::foo()` 可以互换。
内联命名空间主要用于跨版本的 ABI 兼容性。

##### 缺点

命名空间可能让人困惑，因为它们让「弄清某个名字指向哪个定义」
这件事变得更复杂。

尤其是内联命名空间，会让人困惑，因为名字实际上并不局限于
声明它们的那个命名空间。它们只有作为某种更大的版本管理策略的
一部分时才有意义。

在某些场景下，不得不反复用全限定名来引用符号。对于嵌套很深的
命名空间，这会带来大量
视觉噪声。

##### 结论

命名空间应按如下方式使用：

*   遵循[命名空间名称](#Namespace_Names)一节中的规则。
*   多行命名空间应以注释收尾，形式如给出的
    示例所示。
*   命名空间应包裹整个源文件中位于包含、
    [gflags](https://gflags.github.io/gflags/) 定义/声明，以及来自其他
    命名空间的类前置声明之后的部分。

    <div class='goodcode'></div>

    ```cpp
    // In the .h file
    namespace mynamespace {

    // All declarations are within the namespace scope.
    // Notice the lack of indentation.
    class MyClass {
     public:
      ...
      void Foo();
    };

    }  // namespace mynamespace
    ```

    <div class='goodcode'></div>

    ```cpp
    // In the .cc file
    namespace mynamespace {

    // Definition of functions is within scope of the namespace.
    void MyClass::Foo() {
      ...
    }

    }  // namespace mynamespace
    ```

    更复杂的 `.cc` 文件可能还有额外内容，例如标志或
    using 声明。

    <div class='goodcode'></div>

    ```cpp
    #include "a.h"

    ABSL_FLAG(bool, someflag, false, "a flag");

    namespace mynamespace {

    using ::foo::Bar;

    ...code for mynamespace...    // Code goes against the left margin.

    }  // namespace mynamespace
    ```

*   要把生成的协议消息代码放进某个命名空间，请使用 `package`
    说明符，写在 `.proto` 文件中。详情参见
    [Protocol Buffer 包](https://protobuf.dev/reference/cpp/cpp-generated/#package)
    一节。

*   不要在命名空间 `std` 中声明任何东西，包括对标准库类的
    前置声明。在命名空间 `std` 中声明实体属于未定义行为，
    也就是说不可移植。要声明来自标准库的实体，请包含
    相应的头文件。

*   不得使用 *using 指令* 来让某个命名空间中的所有名字
    都可用。

    <div class='badcode'></div>

    ```cpp
    // Forbidden -- This pollutes the namespace.
    using namespace foo;
    ```

*   不要在头文件的命名空间作用域使用 *命名空间别名*，除非是在
    明确标注为仅供内部使用的命名空间中，因为导入到头文件某个
    命名空间中的任何东西，都会成为该文件导出的公开 API 的
    一部分。在不适用这些条件时可以使用命名空间别名，但它们
    必须具有[恰当的名称](#Naming_Aliases)。

    <div class='goodcode'></div>

    ```cpp
    // In a .h file, an alias must not be a separate API, or must be hidden in
    // an implementation detail.
    namespace librarian {

    namespace internal {  // Internal, not part of the API.
    namespace sidetable = ::pipeline_diagnostics::sidetable;
    }

    inline void my_inline_function() {
      // Local to a function.
      namespace baz = ::foo::bar::baz;
      ...
    }

    }  // namespace librarian
    ```

    <div class='goodcode'></div>

    ```cpp
    // Remove uninteresting parts of some commonly used names in .cc files.
    namespace sidetable = ::pipeline_diagnostics::sidetable;
    ```

*   不要使用内联命名空间。

*   使用名称中带 "internal" 的命名空间，用来标明 API 中那些
    不应被 API 使用者提及的部分。

    <div class='badcode'></div>

    ```cpp
    // We shouldn't use this internal name in non-absl code.
    using ::absl::container_internal::ImplementationDetail;
    ```

    请注意，嵌套的 `internal` 命名空间中，各库之间仍有
    冲突风险，因此请给命名空间中的每个库加上库文件名，
    以获得唯一的内部命名空间。例如，`gshoe/widget.h` 应使用
    `gshoe::internal_widget`，而不是仅仅
    `gshoe::internal`。

*   新代码中首选单行的嵌套命名空间声明，但并不
    强制要求。

    <div class='goodcode'></div>

    ```cpp
    namespace my_project::my_component {

      ...

    }  // namespace my_project::my_component
    ```

<a id="Internal_Linkage"></a>

### 内部链接 []() {#Unnamed_Namespaces_and_Static_Variables}

当 `.cc` 文件中的定义无需在该文件之外被引用时，请通过把它们放进
匿名命名空间、或把它们声明为 `static` 来赋予其内部链接。不要在
`.h` 文件中使用这两种构造中的任何一种。

##### 定义

所有声明都可以通过放进匿名命名空间而获得内部链接。函数和变量
也可以通过声明为 `static` 获得内部链接。这意味着你所声明的
任何东西都无法从另一个文件访问。如果另一个文件声明了同名的
东西，那么这两个实体完全是彼此
独立的。

##### 结论

对于 `.cc` 文件中所有无需在别处被引用的代码，鼓励使用内部链接。
不要在 `.h` 文件中使用内部链接。

匿名命名空间的格式与具名命名空间相同。在收尾注释中，
让命名空间名留空：

<div class='goodcode'></div>

```cpp
namespace {
...
}  // namespace
```

<a id="Nonmember,_Static_Member,_and_Global_Functions"></a>

### 非成员、静态成员与全局函数

优先把非成员函数放进命名空间；尽量少用完全全局的
函数。

不要创建由静态成员组成的类，除非有充分理由。命名空间中的自由函数
是定义非实例操作的惯用方式。把它们包进一个类，往往是不必要的
Java 式做法。充分理由的例子包括策略类或 trait，
为某种独立表示赋予类型语义，或是封闭接口
以防止被扩展。

##### 优点

非成员函数和静态成员函数在某些情况下很有用。把非成员函数放进
命名空间，可以避免污染全局命名空间。

##### 缺点

非成员函数和静态成员函数，也许更适合作为某个新类的成员，
尤其当它们访问外部资源或具有显著的
依赖关系时。

##### 结论

有时，定义一个不绑定到类实例的函数是有用的。这样的函数既可以
是静态成员，也可以是非成员函数。非成员函数不应依赖外部变量，
并且几乎总应存在于某个命名空间中。不要仅仅为了把静态成员
归拢到一起而创建类；这与给这些名字加个公共前缀并无区别，
而且这种归拢通常也
并无必要。

如果你定义了一个只在自己的 `.cc` 文件中才需要的非成员函数，请使用
[内部链接](#Internal_Linkage) 来限制它的作用域。

<a id="Local_Variables"></a>

### 局部变量

把函数的变量放在尽可能窄的作用域中，并在声明处
初始化变量。

C++ 允许你在函数中的任意位置声明变量。我们鼓励你把变量声明在
尽可能局部的作用域中，并尽可能靠近第一次使用的地方。这能让
读者更容易找到声明，看清变量的类型以及它被初始化成了什么。
特别地，应当使用初始化，而不是先声明再赋值，
例如：

<div class='badcode'></div>

```cpp
int i;
i = f();      // Bad -- initialization separate from declaration.
```

<div class='goodcode'></div>

```cpp
int i = f();  // Good -- declaration has initialization.
```

<div class='badcode'></div>

```cpp
int jobs = NumJobs();
// More code...
f(jobs);      // Bad -- declaration separate from use.
```

<div class='goodcode'></div>

```cpp
int jobs = NumJobs();
f(jobs);      // Good -- declaration immediately (or closely) followed by use.
```

<div class='badcode'></div>

```cpp
std::vector<int> v;
v.push_back(1);  // Prefer initializing using brace initialization.
v.push_back(2);
```

<div class='goodcode'></div>

```cpp
std::vector<int> v = {1, 2};  // Good -- v starts initialized.
```

`if`、`while` 和 `for` 语句所需的变量，通常应当声明在
这些语句内部，以便把这些变量限制在相应的
作用域中。例如：

<div class='goodcode'></div>

```cpp
while (const char* p = strchr(str, '/')) str = p + 1;
```

有一点需要注意：如果变量是对象，那么每次进入作用域并创建它时
都会调用其构造函数，每次离开作用域时都会调用其
析构函数。

<div class='badcode'></div>

```cpp
// Inefficient implementation:
for (int i = 0; i < 1000000; ++i) {
  Foo f;  // My ctor and dtor get called 1000000 times each.
  f.DoSomething(i);
}
```

把这类在循环中使用的变量声明在循环之外，
可能更高效：

<div class='goodcode'></div>

```cpp
Foo f;  // My ctor and dtor get called once each.
for (int i = 0; i < 1000000; ++i) {
  f.DoSomething(i);
}
```

<a id="Static_and_Global_Variables"></a>

### 静态变量与全局变量

具有
[静态存储期](http://en.cppreference.com/w/cpp/language/storage_duration#Storage_duration)
的对象一律禁止使用，除非它们是
[可平凡析构的](http://en.cppreference.com/w/cpp/types/is_destructible)。
通俗地说，这意味着析构函数什么都不做，即便把成员和基类的
析构函数也考虑进来。更正式地说，这意味着该类型既没有
用户定义的析构函数、也没有虚析构函数，并且所有基类和非静态
成员都可平凡析构。静态的函数局部变量可以使用
动态初始化。对静态类成员变量或命名空间作用域的变量使用
动态初始化是不被鼓励的，但在有限情形下允许；详见
下文。

一条经验法则：如果某个全局变量的声明单独来看可以是 `constexpr`，
那它就满足这些要求。

##### 定义

每个对象都有一个*存储期*，它与其生命周期
相关联。具有静态存储期的对象，从被初始化的那一刻起，
一直存活到程序结束。这类对象表现为命名空间作用域的
变量（「全局变量」）、类的静态数据成员，或是带有
`static` 说明符的函数局部变量。函数局部静态变量在
控制流第一次经过其声明处时初始化；其他所有具有静态
存储期的对象，都在程序启动过程中被初始化。所有具有
静态存储期的对象都在程序退出时被销毁（这发生在
未汇合的线程被终止
之前）。

初始化可以是*动态*的，意思是初始化期间会发生某些不平凡的事。
（例如，设想一个会分配内存的构造函数，或者一个用当前进程
ID 初始化的变量。）另一种初始化是*静态*初始化。不过，
这两者并不完全对立：对于具有静态存储期的对象，
*总是*会发生静态初始化（把对象初始化为某个给定的常量，
或初始化为所有字节都置零的表示），而动态初始化
则在其后
发生。

##### 优点

全局和静态变量在大量应用场景中都非常有用：具名常量、某个
翻译单元内部使用的辅助数据结构、命令行标志、日志、注册
机制、后台基础设施，
等等。

##### 缺点

使用动态初始化、或带有非平凡析构函数的全局和静态变量，会
带来复杂性，很容易导致难以定位的缺陷。跨翻译单元时，
动态初始化的顺序不确定，销毁顺序也不确定（只保证销毁
按初始化的逆序发生）。当某个初始化引用了另一个具有
静态存储期的变量时，就可能在某个对象的生命周期开始之前
（或结束之后）访问它。此外，当程序启动了在退出时
未汇合的线程，而这些对象的析构函数已经运行时，
这些线程就可能在这些对象的生命周期结束之后
仍去访问
它们。

##### 结论

###### 关于销毁的结论

当析构函数是平凡的时，其执行完全不受顺序约束（实际上它们
并不算「被运行」）；否则我们就会面临在对象生命周期结束之后
仍去访问它的风险。因此，我们只允许具有静态存储期且
可平凡析构的对象。基本类型（如指针和 `int`）可平凡析构，
由可平凡析构类型组成的数组也是如此。请注意，标有
`constexpr` 的变量
是可平凡析构的。

<div class='goodcode'></div>

```cpp
const int kNum = 10;  // Allowed

struct X { int n; };
const X kX[] = {{1}, {2}, {3}};  // Allowed

void foo() {
  static const char* const kMessages[] = {"hello", "world"};  // Allowed
}

// Allowed: constexpr guarantees trivial destructor.
constexpr std::array<int, 3> kArray = {1, 2, 3};
```

<div class='badcode'></div>

```cpp
// bad: non-trivial destructor
const std::string kFoo = "foo";

// Bad for the same reason, even though kBar is a reference (the
// rule also applies to lifetime-extended temporary objects).
const std::string& kBar = StrCat("a", "b", "c");

void bar() {
  // Bad: non-trivial destructor.
  static std::map<int, int> kData = {{1, 0}, {2, 0}, {3, 0}};
}
```

请注意，引用不是对象，因此不受可析构性方面的约束。
不过，对动态初始化的约束仍然适用。特别地，形如
`static T& t = *new T;` 的函数局部静态引用
是允许的。

###### 关于初始化的结论

初始化是一个更复杂的话题。这是因为我们不仅要考虑类的
构造函数是否执行，还必须考虑初始化器的
求值：

<div class='neutralcode'></div>

```cpp
int n = 5;    // Fine
int m = f();  // ? (Depends on f)
Foo x;        // ? (Depends on Foo::Foo)
Bar y = g();  // ? (Depends on g and on Bar::Bar)
```

除第一条语句外，其余都会让我们面临不确定的初始化顺序。

我们要找的概念，在 C++ 标准的正式术语里叫做*常量初始化*。
它指的是：初始化表达式是一个常量表达式，而且如果对象是
通过构造函数调用来初始化的，那么该构造函数也必须
被指定为 `constexpr`：

<div class='goodcode'></div>

```cpp
struct Foo { constexpr Foo(int) {} };

int n = 5;  // Fine, 5 is a constant expression.
Foo x(2);   // Fine, 2 is a constant expression and the chosen constructor is constexpr.
Foo a[] = { Foo(1), Foo(2), Foo(3) };  // Fine
```

常量初始化始终是允许的。具有静态存储期的变量若采用常量
初始化，应标以 `constexpr` 或 `constinit`。任何未作此类标记
的非局部静态存储期变量，都应被推定为采用动态初始化，
并需非常仔细地加以审查。

相比之下，下面这些初始化是有问题的：

<div class='badcode'></div>

```cpp
// Some declarations used below.
time_t time(time_t*);      // Not constexpr!
int f();                   // Not constexpr!
struct Bar { Bar() {} };

// Problematic initializations.
time_t m = time(nullptr);  // Initializing expression not a constant expression.
Foo y(f());                // Ditto
Bar b;                     // Chosen constructor Bar::Bar() not constexpr.
```

非局部变量的动态初始化是不被鼓励的，而且一般是被禁止的。
不过，如果程序的任何方面都不依赖于该初始化相对于所有其他
初始化的先后顺序，我们确实允许它。在这些限制下，
初始化的顺序不会带来可观察到的差异。
例如：

<div class='goodcode'></div>

```cpp
int p = getpid();  // Allowed, as long as no other static variable
                   // uses p in its own initialization.
```

静态局部变量的动态初始化是允许的（而且很常见）。

###### 常见模式

*   全局字符串：如果你需要一个具名的全局或静态字符串常量，
    请考虑使用 `constexpr` 的 `string_view`、字符数组或
    字符指针变量，令其指向某个字符串字面量。字符串字面量本身
    已具有静态存储期，通常就足够了。参见
    [TotW #140](https://abseil.io/tips/140)。
*   映射、集合及其他动态容器：如果你需要一个静态、固定的
    集合，例如供检索的集合或查找表，那么不能把标准库中的
    动态容器用作静态变量，因为它们带有非平凡的析构函数。
    请改用由平凡类型构成的简单数组，例如「int 到 int 的映射」
    可用由 int 数组组成的数组，或者用由配对构成的数组
    （例如 `int` 与 `const char*` 的配对）。对于小规模集合，
    线性查找完全够用（且因内存局部性而高效）；可考虑使用
    [absl/algorithm/container.h](https://github.com/abseil/abseil-cpp/blob/master/absl/algorithm/container.h)
    提供的工具来完成标准操作。如有必要，可让集合保持有序，
    并采用二分查找算法。如果你确实更偏爱标准库中的动态
    容器，请考虑使用函数局部的静态指针，做法
    如下文
    所述。
*   智能指针（`std::unique_ptr`、`std::shared_ptr`）：智能指针
    会在销毁时执行清理，因此被禁止使用。请考虑你的用例
    是否适合本节所述的其他某种模式。一个简单的办法是
    使用指向动态分配对象的普通指针，并且永不释放它
    （见最后一项）。
*   自定义类型的静态变量：如果你需要某种自行定义的类型的
    静态常量数据，请给该类型一个平凡析构函数和一个
    `constexpr` 构造函数。
*   如果上述办法都不行，你可以动态创建一个对象并永不释放，
    做法是使用函数局部的静态指针或引用（例如
    `static const auto& impl = *new T(args...);`）。

<a id="thread_local"></a>

### thread_local 变量

未在函数内部声明的 `thread_local` 变量，必须用真正的编译期
常量来初始化，而且这一点必须通过使用
[`constinit`](https://en.cppreference.com/w/cpp/language/constinit)
属性来强制保证。定义线程局部数据时，请优先选用 `thread_local` 而非其他方式。

##### 定义

变量可以用 `thread_local` 说明符声明：

<div class='neutralcode'></div>

```cpp
thread_local Foo foo = ...;
```

这样的变量实际上是一组对象，因此当不同线程访问它时，
它们访问的其实是不同的对象。`thread_local` 变量在许多方面
都很像
[静态存储期变量](#Static_and_Global_Variables)：例如，它们可以声明在
命名空间作用域、函数内部，或作为静态类成员，但不能作为
普通类成员。

`thread_local` 变量实例的初始化与静态变量很相似，
区别在于必须为每个线程分别初始化，而不是在程序启动时
只初始化一次。这意味着在函数内部声明的 `thread_local` 变量是
安全的，但其他 `thread_local` 变量会面临与静态变量相同的
初始化顺序问题（甚至更多）。

`thread_local` 变量有一个微妙的销毁顺序问题：在线程关闭期间，
`thread_local` 变量会按初始化的相反顺序被销毁（C++ 通常
就是如此）。如果某个 `thread_local` 变量的析构函数所触发的代码
引用了该线程上任何已被销毁的 `thread_local`，我们就会
遇到一个特别难以诊断的释放后使用
问题。

##### 优点

*   线程局部数据天然不存在竞态（因为通常只有一个线程可以
    访问它），这使得 `thread_local` 在并发
    编程中很有用。
*   `thread_local` 是创建线程局部数据时唯一受标准支持的
    方式。

##### 缺点

*   访问某个 `thread_local` 变量，可能在线程启动、或在该线程上
    首次使用它时，触发数量不可预测且无法控制的其他
    代码执行。
*   `thread_local` 变量实际上是全局变量，除不缺线程安全
    之外，具备全局变量的一切缺点。
*   `thread_local` 变量所占用的内存（最坏情况下）随运行中的
    线程数增长，在程序中可能相当可观。
*   数据成员不能是 `thread_local`，除非同时也是 `static`。
*   如果 `thread_local` 变量带有复杂的析构函数，我们可能
    遭遇释放后使用的缺陷。特别地，此类变量的析构函数
    不得（直接或间接地）调用任何引用了可能已被销毁的
    `thread_local` 的代码。这一性质很难强制保证。
*   在全局/静态场景下用来避免释放后使用的办法，对
    `thread_local` 并不奏效。具体来说，跳过全局和静态
    变量的析构函数是允许的，因为它们的生命周期在程序
    关闭时结束。因此，任何「泄漏」都会由操作系统清理我们的
    内存和其他资源而立即得到处理。相比之下，跳过
    `thread_local` 变量的析构函数，会造成资源泄漏，其规模与程序
    生命周期内终止的线程总数成正比。

##### 结论

类作用域或命名空间作用域的 `thread_local` 变量，必须用真正的
编译期常量初始化（即不得有动态初始化）。为强制这一点，
类作用域或命名空间作用域的 `thread_local` 变量必须
标注为
[`constinit`](https://en.cppreference.com/w/cpp/language/constinit)（或
`constexpr`，但那应当很少见）：

<div class='goodcode'></div>

```cpp
constinit thread_local Foo foo = ...;
```

函数内部的 `thread_local` 变量没有初始化方面的顾虑，但在线程
退出时仍有释放后使用的风险。请注意，你可以用一个函数作用域的
`thread_local` 来模拟类作用域或命名空间作用域的 `thread_local`，
做法是定义一个把它暴露出来的函数或静态方法：

<div class='goodcode'></div>

```cpp
Foo& MyThreadLocalFoo() {
  thread_local Foo result = ComplicatedInitialization();
  return result;
}
```

请注意，只要线程退出，`thread_local` 变量就会被销毁。
如果此类变量的析构函数引用了任何其他（可能已被销毁的）
`thread_local`，我们就会遭遇难以诊断的释放后使用缺陷。
请优先选用平凡类型，或可证明在销毁时不运行任何用户代码的
类型，以尽量减少访问其他 `thread_local` 的可能。

定义线程局部数据时，应优先选用 `thread_local`，
而非其他机制。

<a id="Classes"></a>

## 类

类是 C++ 中代码的基本单元。我们自然会大量使用它们。本节
列出编写类时应当遵循的主要
该做与不该做之事。

<a id="Doing_Work_in_Constructors"></a>

### 在构造函数中工作

避免在构造函数中调用虚方法，并且在无法发出错误信号时，
避免可能失败的初始化。

##### 定义

在构造函数的函数体中，可以执行任意的
初始化。

##### 优点

*   无需担心类是否已被初始化。
*   通过调用构造函数而完全初始化的对象可以是 `const`，
    也可能更易于配合标准容器或算法使用。

##### 缺点

*   如果这些工作调用了虚函数，这些调用不会被分派到子类的
    实现。即便你的类目前没有被子类化，日后对类的修改也可能
    悄悄引入这个问题，造成很大的
    困惑。
*   构造函数没有简便的办法发出错误信号，除非让程序崩溃
    （并不总是合适）或使用异常（而异常是
    [被禁止的](#Exceptions)）。
*   如果这些工作失败，我们得到的就是一个初始化代码失败了的
    对象，因此它可能处于异常状态，需要一套 `bool IsValid()`
    状态检查机制（或类似手段），而这类机制很容易忘记调用。
*   无法取构造函数的地址，因此构造函数中所做的任何工作
    都难以转交给别的线程之类的地方。

##### 结论

构造函数绝不应调用虚函数。如果对你的代码而言合适，
终止程序可能是一种恰当的错误处理方式。否则，
请考虑工厂函数或 `Init()` 方法，相关描述见
[TotW #42](https://abseil.io/tips/42)。对于没有其他状态来决定
可调用哪些公开方法的对象，请避免使用 `Init()` 方法
（这种半构造的对象尤其难以正确使用）。

<a id="Implicit_Conversions"></a>

### 隐式转换 []() {#Explicit_Constructors}

不要定义隐式转换。对转换运算符和单参数构造函数请使用
`explicit` 关键字。

##### 定义

隐式转换允许把一种类型的对象（称为 <dfn>源
类型</dfn>）用在需要另一种类型（称为 <dfn>目标
类型</dfn>）的场合，例如把 `int` 实参传给接受
`double` 形参的函数。

除了语言本身定义的隐式转换，使用者还可以自行定义：在源类型
或目标类型的类定义中添加适当的成员即可。源类型中的隐式
转换，由一个以目标类型命名的类型转换运算符定义（例如
`operator bool()`）。目标类型中的隐式转换，则由
一个可以把源类型作为唯一实参（或唯一无默认值的实参）的
构造函数
来定义。

`explicit` 关键字可以加在构造函数或转换运算符上，以确保
它只能在使用处目标类型显式出现时才被使用，例如通过
强制转换。这不仅适用于隐式转换，也适用于列表
初始化语法：

<div class='neutralcode'></div>

```cpp
class Foo {
  explicit Foo(int x, double y);
  ...
};

void Func(Foo f);
```

<div class='badcode'></div>

```cpp
Func({42, 3.14});  // Error
```

这类代码严格来说并不是隐式转换，但就 `explicit` 而言，
语言把它当作隐式转换来对待。

##### 优点

*   隐式转换能让类型更易用、更有表现力，因为在类型显而易见
    时无需显式写出类型名。
*   隐式转换可以比重载更简单，例如用一个带 `string_view`
    形参的函数，替代分别针对 `std::string` 和 `const char*`
    的多个重载。
*   列表初始化语法是一种简洁而有表现力的对象
    初始化方式。

##### 缺点

*   隐式转换可能掩盖类型不匹配的缺陷：目标类型与使用者
    的预期不符，或者使用者根本没意识到会发生
    转换。
*   隐式转换会让代码更难读，尤其是在存在重载时，
    因为它让「实际调用的到底是哪段代码」变得
    不那么明显。
*   只接受单个实参的构造函数，可能会在无意中被用作
    隐式类型转换，即便本意并非如此。
*   当单参数构造函数没有标注 `explicit` 时，没有可靠的
    办法判断它是有意定义隐式转换，还是作者
    只是忘了标注。
*   隐式转换可能导致调用点出现歧义，尤其当存在双向的
    隐式转换时。这既可能是两个类型都提供了隐式转换，
    也可能是同一个类型同时带有隐式构造函数和隐式
    类型转换
    运算符。
*   如果目标类型是隐式的，列表初始化也会遭遇同样的
    问题，尤其当列表中只有一个元素时。

##### 结论

类型转换运算符，以及可以用单个实参调用的构造函数，
在类定义中都必须标注 `explicit`。作为例外，拷贝和移动
构造函数不应标注 `explicit`，因为它们并不执行
类型转换。

对于设计成可互换的类型，隐式转换有时是必要且恰当的，
例如当两种类型的对象只是同一个底层值的不同表示时。
在这种情况下，请联系你的项目负责人，申请对这条规则的
豁免。

无法用单个实参调用的构造函数可以省略 `explicit`。
只接受单个 `std::initializer_list` 形参的构造函数也应
省略 `explicit`，以便支持拷贝初始化（例如
`MyType m = {1, 2};`）。

<a id="Copyable_Movable_Types"></a>

### 可拷贝与可移动类型 []() {#Copy_Constructors}

类的公开 API 必须清楚地表明该类是可拷贝的、仅可移动的，
还是既不可拷贝也不可移动。如果这些操作对你的类型而言
清晰而有意义，就请支持拷贝和/或移动。

##### 定义

可移动类型是指可以从临时对象初始化或赋值的类型。

可拷贝类型是指可以从同类型的任何其他对象初始化或赋值
的类型（因此按定义它也是可移动的），附带条件是源对象的
值不发生改变。`std::unique_ptr<int>` 就是可移动但不可拷贝
类型的例子（因为在向目标赋值时，源
`std::unique_ptr<int>` 的值必须被修改）。
`int` 和 `std::string` 是既可移动也可拷贝的类型的例子。
（对 `int` 而言，移动和拷贝操作相同；对 `std::string` 而言，
存在一种比拷贝开销更小的移动操作。）

对于用户定义的类型，拷贝行为由拷贝构造函数和
拷贝赋值运算符定义。移动行为由移动构造函数和移动
赋值运算符定义（如果存在），否则由拷贝构造函数和
拷贝赋值运算符定义。

在某些情况下，编译器会隐式调用拷贝/移动构造函数，
例如按值传递对象时。

##### 优点

可拷贝、可移动类型的对象可以按值传递和返回，这让
API 更简单、更安全、也更通用。与按指针或引用传递对象
不同，这里不存在所有权、生命周期、可变性之类
问题上的混淆，也不必在契约中把它们写清楚。它还
避免了客户代码与实现之间的非局部交互，让它们
更易于理解、维护，也更便于编译器优化。此外，这类
对象可以用于要求按值传递的泛型 API（例如大多数
容器），并在类型组合等方面带来额外的
灵活性。

拷贝/移动构造函数和赋值运算符，通常比 `Clone()`、
`CopyFrom()` 或 `Swap()` 之类的替代方案更容易正确定义，
因为它们可以由编译器生成——要么隐式生成，要么用
`= default`。它们很简洁，并能确保所有数据成员都被拷贝。
拷贝和移动构造函数通常也更高效，因为它们不需要堆分配，
也不需要分开的初始化与赋值步骤，并且有资格享受
[拷贝消除](http://en.cppreference.com/w/cpp/language/copy_elision)
之类的优化。

移动操作让资源可以隐式而高效地从右值对象中转移出来。
在某些情况下，这能让编码风格更平实。

##### 缺点

有些类型并不需要可拷贝，为这类类型提供拷贝操作可能
令人困惑、毫无意义，甚至完全错误。表示单例对象的类型
（`Registerer`）、与特定作用域绑定的对象（`Cleanup`），
或与对象身份紧密耦合的类型（`Mutex`），都无法有意义地
拷贝。打算以多态方式使用的基类类型，其拷贝操作是
危险的，因为使用它们可能导致
[对象切片](https://en.wikipedia.org/wiki/Object_slicing)。默认生成的、
或实现得草率的拷贝操作可能不正确，由此产生的缺陷
既令人困惑又难以诊断。

拷贝构造函数会被隐式调用，因此很容易被忽略。对于习惯
了那些按引用传递是惯例或强制要求的语言的程序员，这
可能造成困惑。它还可能助长过度的拷贝，从而引发
性能问题。

##### 结论

每个类的公开接口都必须清楚地表明该类支持哪些拷贝和
移动操作。这通常应表现为在声明的 `public` 部分显式
声明和/或删除相应的
操作。

具体来说，可拷贝的类应显式声明拷贝操作，仅可移动的类
应显式声明移动操作，而不可拷贝/移动的类应显式删除
拷贝操作。可拷贝的类也可以声明移动操作，以支持高效的
移动。显式声明或删除全部四种拷贝/移动操作是允许的，
但并非必须。如果你提供了拷贝或移动赋值运算符，
就必须同时提供相应的
构造函数。

<div class='goodcode'></div>

```cpp
class Copyable {
 public:
  Copyable(const Copyable& other) = default;
  Copyable& operator=(const Copyable& other) = default;

  // The implicit move operations are suppressed by the declarations above.
  // You may explicitly declare move operations to support efficient moves.
};

class MoveOnly {
 public:
  MoveOnly(MoveOnly&& other) = default;
  MoveOnly& operator=(MoveOnly&& other) = default;

  // The copy operations are implicitly deleted, but you can
  // spell that out explicitly if you want:
  MoveOnly(const MoveOnly&) = delete;
  MoveOnly& operator=(const MoveOnly&) = delete;
};

class NotCopyableOrMovable {
 public:
  // Not copyable or movable
  NotCopyableOrMovable(const NotCopyableOrMovable&) = delete;
  NotCopyableOrMovable& operator=(const NotCopyableOrMovable&)
      = delete;

  // The move operations are implicitly disabled, but you can
  // spell that out explicitly if you want:
  NotCopyableOrMovable(NotCopyableOrMovable&&) = delete;
  NotCopyableOrMovable& operator=(NotCopyableOrMovable&&)
      = delete;
};
```

只有在这些声明/删除显而易见时，才可以省略它们：

*   如果类没有 `private` 部分，例如一个
    [struct](#Structs_vs._Classes)，或纯接口的基类，那么其
    可拷贝性/可移动性可由任意公开数据成员的相应性质确定。
*   如果基类明显不可拷贝或不可移动，派生类自然也不会
    具备这些能力。让这些操作保持隐式的纯接口基类，
    不足以让具体子类变得清晰。
*   请注意，如果你显式声明或删除了拷贝的构造函数或
    赋值操作，另一个拷贝操作就不再显而易见，必须
    加以声明或删除。移动操作同理。

如果随意的使用者难以理解拷贝/移动的含义，或者它会带来
意料之外的开销，那么该类型就不应可拷贝/可移动。对可
拷贝类型而言，移动操作纯粹是一种性能优化，也是缺陷和
复杂性的潜在来源，因此除非它比相应的拷贝操作显著
更高效，否则请避免定义它们。如果你的类型提供了拷贝
操作，建议你把类设计成这些操作的默认实现就是
正确的。请记得像审查其他任何代码一样，审查所有默认
生成操作的正确性。

为消除切片风险，请优先把基类做成抽象类：把它们的构造
函数设为 protected、把析构函数声明为 protected，
或给它们一个或多个纯虚成员函数。请尽量避免从
具体类派生。

<a id="Structs_vs._Classes"></a>

### 结构体与类

`struct` 仅用于承载数据的被动对象；其余一切都用
`class`。

在 C++ 中，`struct` 与 `class` 关键字的行为几乎完全相同。我们为
每个关键字附加了各自的语义含义，因此你应当为所定义的数据类型
选用恰当的关键字。

`structs` 应当用于承载数据的被动对象，可以带有
相关联的常量。所有字段都必须是 public。struct 类型本身不得
带有隐含不同字段之间关系的不变式，因为用户对这些字段的
直接访问可能破坏这些不变式，但 struct 的使用者可以对
它的特定用法提出要求与保证。构造函数、
析构函数和辅助方法可以存在；但这些方法不得
要求或强制任何不变式。

若需要更多功能或不变式，或 struct 具有较广的可见性
且预期会不断演化，则 `class` 更为合适。若有疑问，就使用
`class`。

为与 STL 保持一致，无状态类型可用 `struct` 代替 `class`，
例如 traits、[模板元函数](#Template_metaprogramming)
以及某些仿函数。

注意，结构体与类中的成员变量遵循
[不同的命名规则](#Variable_Names)。

<a id="Structs_vs._Tuples"></a>

### 结构体与 pair、tuple

当各元素可以有有意义的名称时，优先使用 `struct` 而不是 pair
或 tuple。

虽然使用 pair 与 tuple 可以免去定义自定义类型，
在*编写*代码时可能省些工夫，但有意义的字段名几乎
总在*阅读*代码时比 `.first`、`.second` 或
`std::get<X>` 清晰得多。C++14 引入 `std::get<Type>` 可按类型访问 tuple
元素（当类型唯一时）而非按索引，这有时能部分缓解该问题，但字段名
通常仍远比类型清晰，
也更有信息量。

在泛型代码中，若 pair 或 tuple 的元素没有特定含义，使用它们
可能是合适的。为了与现有代码或 API 互操作，也可能
必须使用它们。

<a id="Inheritance"></a>

### 继承 []() {#Multiple_Inheritance}

组合通常比继承更合适。使用继承时，
应将其声明为 `public`。

##### 定义

当子类继承基类时，它会包含基类所定义的
全部数据与操作的定义。“接口继承”是指
从纯抽象基类（不含状态、也没有已定义方法的基类）
继承；其余所有继承都是“实现继承”。

##### 优点

实现继承通过在特化既有类型时复用基类代码，
缩小了代码规模。由于继承是编译期
声明，你和编译器都能理解其操作并发现
错误。接口继承可用于以程序化方式强制某个
类暴露特定的 API。同样，编译器能发现错误，
此处是指类未定义该 API 必需的方法时。

##### 缺点

对于实现继承，由于实现子类的代码分散在
基类与子类之间，因此更难
理解其实现。子类无法覆写非虚
函数，因而子类不能改变实现。

多重继承尤其成问题，因为它往往带来
更高的性能开销（事实上，从单继承变为
多继承的性能下降，往往大于从普通调用
变为虚分派的性能下降），而且它可能导致
“菱形”继承结构，容易产生歧义、混乱，
乃至直接的缺陷。

##### 结论

所有继承都应是 `public`。若想使用私有继承，
则应改为把基类的实例作为成员包含进来。若不打算
让某个类用作基类，可对它使用 `final` 加以标记，
表明它不可被继承。

不要过度使用实现继承。组合往往
更合适。尽量把继承的使用限制在“是一个（is-a）”场景：`Bar`
继承 `Foo`，仅当能合理地说 `Bar` “是 `Foo` 的一种”。

把 `protected` 的使用限制在那些可能需要
被子类访问的成员函数上。注意，
[数据成员应为 `private`](#Access_Control)。

覆写虚函数或虚析构函数时，应显式
且仅用一个 `override` 或（较少情况下）`final` 说明符来注解；
声明覆写时不要使用 `virtual`。理由：若某个
标为 `override` 或 `final` 的函数或析构函数并未覆写基类虚函数，
将无法编译，这有助于发现常见错误。这些说明符还起到
文档作用；若没有说明符，读者就必须检查该类的所有祖先，
才能确定该函数或析构函数
是否为虚函数。

允许多重继承，但多重*实现*继承
则强烈不建议。

<a id="Operator_Overloading"></a>

### 运算符重载

审慎地重载运算符。不要使用用户自定义字面量。

##### 定义

C++ 允许用户代码
[声明内置运算符的重载版本](http://en.cppreference.com/w/cpp/language/operators)
使用 `operator` 关键字，只要其中一个参数是用户自定义
类型即可。`operator` 关键字还允许用户代码定义新种类的
字面量（借助 `operator""`），以及定义类型转换函数，例如
`operator bool()`。

##### 优点

运算符重载让用户自定义类型的行为与内置类型一致，
从而使代码更简洁、更直观。重载的运算符
是某些操作的惯用名称（例如 `==`、`<`、`=` 和 `<<`），
遵循这些约定能让用户自定义类型更具可读性，
并使其能与依赖这些名称的库互操作。

用户自定义字面量是创建用户自定义类型对象的一种
非常简洁的表示法。

##### 缺点

*   提供一组正确、一致且不出人意料的运算符重载
    需要相当谨慎，否则可能导致困惑与缺陷。

*   过度使用运算符会使代码晦涩，尤其当
    重载运算符的语义不遵循惯例时。

*   函数重载的种种隐患同样适用于运算符
    重载，甚至有过之而无不及。

*   运算符重载会误导直觉，让人以为开销高昂的
    操作是廉价的内置操作。

*   查找重载运算符的调用点可能需要能理解
    C++ 语法的搜索工具，而非 grep 之类。

*   若把重载运算符的参数类型弄错，得到的可能
    是另一个重载，而非编译错误。例如 `foo < bar`
    可能做一件事，而 `&foo < &bar` 做的事完全不同。

*   某些运算符重载本身就有危险。重载一元 `&`
    会使同一段代码因重载声明是否可见而
    具有不同含义。`&&`、`||` 和 `,`（逗号）的重载
    无法匹配内置运算符的求值顺序语义。

*   运算符常在类外定义，因此存在
    不同文件为同一运算符引入不同定义的风险。若
    两个定义被链接进同一个二进制文件，就会产生未定义
    行为，表现为难以察觉的运行期缺陷。

*   用户自定义字面量（UDL）允许创造新的语法形式，
    即便经验丰富的 C++ 程序员也不熟悉，例如
    用 `"Hello World"sv` 作为 `std::string_view("Hello World")` 的简写。
    现有的表示法虽不够简洁，却更清晰。

*   由于 UDL 不能带命名空间限定，使用 UDL 还需要
    借助 using 指令（[我们禁止使用](#Namespaces)）或 using 声明
    （[我们在头文件中禁止](#Aliases)，除非引入的名称
    属于该头文件所暴露接口的一部分）。鉴于
    头文件必须避免使用 UDL 后缀，我们更希望避免
    字面量约定在头文件与源文件之间出现差异。

##### 结论

仅当运算符含义显而易见、不出人意料，且
与对应的内置运算符一致时，才定义重载。例如把 `|` 用作
按位或 / 逻辑或，而不要当作 shell 风格的管道。

只在自己的类型上定义运算符。更确切地说，要在
与所操作类型相同的头文件、`.cc` 文件和命名空间中定义。这样，
只要类型可用，运算符就可用，从而把多重定义的
风险降到最低。如有可能，避免把运算符定义成模板，因为它们
必须对任意模板实参都满足这条规则。若定义了某个
运算符，还应定义其他有意义的相关运算符，并确保
它们的定义保持一致。

优先把不修改操作数的二元运算符定义为非成员函数。若
把二元运算符定义为类成员，隐式转换将作用于
右侧实参，而不作用于左侧实参。这会令使用者困惑：
若 `a + b` 能编译，而 `b + a` 却不能。

对于值可比较相等性的类型 `T`，应定义非成员
`operator==`，并记录 `T` 的两个值在何时被视为相等。若
若对于值 `t1`（类型 `T`）何时小于
另一个值 `t2` 存在唯一而明确的界定，也可定义 `operator<=>`，它应
与 `operator==` 保持一致。尽量不要重载其余的比较与
排序运算符。

不要刻意回避定义运算符重载。例如，
优先定义 `==`、`=` 和 `<<`，而不是 `Equals()`、`CopyFrom()` 和
`PrintTo()`。反过来，也不要仅仅因为其他
库期望它们就定义运算符重载。例如，若你的类型没有天然的
顺序，却想把它存入 `std::set`，应使用自定义比较器，
而不要重载 `<`。

不要重载 `&&`、`||`、`,`（逗号）或一元 `&`。不要重载
`operator""`，即不要引入用户自定义字面量。不要使用他人
（包括标准库）提供的任何此类字面量。

类型转换运算符在关于
[隐式转换](#Implicit_Conversions) 一节中讨论。`=` 运算符在关于
[拷贝构造函数](#Copy_Constructors) 一节中讨论。为配合流而重载 `<<` 在关于
[流](#Streams) 的一节中讨论。另见关于
[函数重载](#Function_Overloading) 的规则，它们同样适用于
运算符重载。

<a id="Access_Control"></a>

### 访问控制

把类的数据成员设为 `private`，除非它们是
[常量](#Constant_Names)。这能简化对不变式的推理，
代价是引入一些简单的样板代码，形式为访问器（通常带 `const`），
仅在必要时才需要。

出于技术原因，我们允许定义在
`.cc` 文件中的测试夹具类，使用下述库时其数据成员可为 `protected`：
[Google Test](https://github.com/google/googletest)。若测试夹具类
定义在使用它的 `.cc` 文件之外（例如在 `.h` 文件中），
则应把数据成员设为 `private`。

<a id="Declaration_Order"></a>

### 声明顺序

把相似的声明归在一起，把 `public` 部分放在前面。

类定义通常应以 `public:` 部分开头，随后是
`protected:`，再是 `private:`。空的部分应省略。

在每个部分内，优先把同类声明归在一起，
并优先采用以下顺序：

1.  类型与类型别名（`typedef`、`using`、`enum`、嵌套的结构体与
    类，以及 `friend` 类型）
2.  （可选，仅用于结构体）非 `static` 数据成员
3.  静态常量
4.  工厂函数
5.  构造函数与赋值运算符
6.  析构函数
7.  其他所有函数（`static` 与非 `static` 成员函数，以及
    `friend` 函数）
8.  其他所有数据成员（静态与非静态）

不要在类定义中内联放置庞大的方法定义。通常，
只有很简单、对性能至关重要且非常短的方法才可以
内联定义。详见
[在头文件中定义函数](#Defining_Functions_in_Header_Files)
一节。

<a id="Functions"></a>

## 函数

<a id="Inputs_and_Outputs"></a>

### 输入与输出 [](){#Function_Parameter_Ordering} []() {#Output_Parameters}

C++ 函数的输出自然地通过返回值提供，
有时也通过输出参数（或输入 / 输出参数）提供。

优先使用返回值而非输出参数：它们能提升可读性，
而且往往带来相同或更好的性能。参见
[TotW #176](https://abseil.io/tips/176)。

优先按值返回，退而求其次按引用返回。避免返回
裸指针，除非它可能为 null。

参数要么是函数的输入，要么是函数的输出，
要么两者兼是。非可选的输入参数通常应为值或 `const`
引用，而非可选的输出参数与输入 / 输出参数通常
应为引用（不能为 null）。一般用 `std::optional` 表示
可选的按值输入；当非可选形式本应使用引用时，用 `const` 指针。
用非 `const` 指针表示
可选的输出参数与可选的输入 / 输出参数。

避免定义要求引用参数的生命周期长于调用本身的函数。
某些情况下引用参数会绑定到临时对象，引发生命周期
缺陷。应设法消除生命周期要求（例如通过
复制参数），或把需要保留的参数按指针传递，并记录
生命周期与非 null 要求。参见 [TotW 116](https://abseil.io/tips/116)
了解更多。

排列函数参数时，把所有仅用于输入的参数放在任何
输出参数之前。尤其不要仅仅因为参数是新增的，
就把它加到函数参数末尾；新增的仅输入参数应放在
输出参数之前。这不是铁律。既是输入又是输出的
参数会让情况变得复杂；同往常一样，与相关函数
保持一致可能需要你变通这条规则。可变参数函数也可能
需要不同寻常的参数顺序。

<a id="Write_Short_Functions"></a>

### 编写简短的函数

优先编写短小而专注的函数。

我们承认长函数有时是合适的，因此不对函数
长度设硬性上限。若函数超过约 40 行，应考虑
能否在不破坏程序结构的前提下将其拆分。

即便你的长函数现在工作得完美无缺，几个月后
修改它的人可能会加入新行为，从而产生难以发现的缺陷。
让函数保持短小简单，能使他人更易阅读
和修改你的代码。小函数也更易测试。

在处理某些代码时，你可能会遇到又长又复杂的函数。
不要畏惧修改既有代码：若使用这样的函数
确实困难、发现错误难以调试，或想在多个不同场景中
复用其中一部分，就应考虑把这个函数
拆成更小、更易管理的片段。

<a id="Function_Overloading"></a>

### 函数重载

仅当读者查看调用点时，无需先弄清楚
具体调用的是哪个重载，就能大致明白发生了什么，
才使用重载函数（包括构造函数）。

##### 定义

你可以编写一个接受 `const std::string&` 的函数，并
用另一个接受 `const char*` 的函数来重载它。不过此时应考虑
<code>std::string_view </code> 取而代之。

<div class='neutralcode'></div>

```cpp
class MyClass {
 public:
  void Analyze(const std::string& text);
  void Analyze(const char* text, size_t textlen);
};
```

##### 优点

重载允许同名函数接受不同的实参，
从而使代码更直观。对模板化代码而言它可能是必需的，
对 Visitor 模式也很方便。

基于 `const` 或引用限定符的重载可以让工具代码
更易用、更高效，或二者兼得。参见 [TotW #148](https://abseil.io/tips/148)
了解更多。

##### 缺点

若函数仅按实参类型重载，读者可能不得不
理解 C++ 复杂的匹配规则才能明白发生了什么。而且，
若派生类只覆写了某个函数的部分重载版本，
许多人会被其中的继承语义搞糊涂。

##### 结论

当各重载版本之间没有语义差异时，可以重载函数。
这些重载可以在类型、限定符或实参数量上有所不同。
但阅读这类调用的读者不必知道选中了重载集中的
哪一个成员，只需知道调用的是该集合中的**某个**即可。

为体现这种统一的设计，优先使用一条全面覆盖的“总括式”
注释来记录整个重载集，并把它放在第一条
声明之前。

若读者可能难以把这条总括注释对应到某个
具体重载，为特定重载单独加注释也是可以的。

<a id="Default_Arguments"></a>

### 默认参数

当默认值保证始终取同一值时，允许在非虚函数上
使用默认参数。遵循与
[函数重载](#Function_Overloading) 相同的限制；若默认参数带来的可读性
提升不足以抵消下述缺点，
则优先使用重载函数。

##### 优点

常常有函数使用默认值，但偶尔你又想
覆盖这些默认值。默认参数提供了一种简便做法，
无需为少见的例外定义许多函数。与重载
函数相比，默认参数的语法更干净，样板代码更少，
“必需”实参与“可选”实参的区分也更清晰。

##### 缺点

带默认值的参数是实现重载函数语义的另一种方式，
因此[不应重载函数的所有理由](#Function_Overloading)
同样适用。

虚函数调用中实参的默认值由目标对象的
静态类型决定，而且无法保证同一函数的所有覆写
都声明了相同的默认值。

默认参数在每个调用点都会重新求值，这可能使
生成的代码膨胀。读者还可能以为默认值固定在
声明处，而非在每次调用时变化。

存在默认参数时，函数指针会令人困惑，因为
函数签名往往与调用签名不一致。增加函数
重载即可避免这些问题。

##### 结论

虚函数上禁止使用默认参数，因为它们在那里
无法正常工作；当所指定的默认值因求值时机不同
而可能得到不同值时，也禁止使用。（例如不要写
`void f(int n = counter++);`。）

在其他一些情况下，默认参数对函数声明可读性的
提升足以抵消上述缺点，因此允许使用。
若有疑问，就使用重载。

<a id="trailing_return"></a>

### 尾置返回类型语法

仅在普通语法（前置返回类型）不可行，或可读性
差得多时，才使用尾置返回类型。

##### 定义

C++ 允许两种不同形式的函数声明。在较旧的形式中，
返回类型出现在函数名之前。例如：

<div class='neutralcode'></div>

```cpp
int Foo(int x);
```

较新的形式在函数名前使用 `auto` 关键字，并在
实参列表之后写尾置返回类型。例如，上面的声明
可以等价地写成：

<div class='neutralcode'></div>

```cpp
auto Foo(int x) -> int;
```

尾置返回类型处于函数的作用域内。这对简单情形没有影响，
像 `int` 这样的类型便是如此；但对更复杂的情形
就很重要，例如在类作用域中声明的类型，或依据
函数参数写出的类型。

##### 优点

尾置返回类型是显式指定
[lambda 表达式](#Lambda_expressions)返回类型的唯一方式。某些情况下编译器
能推导出 lambda 的返回类型，但并非总是如此。即便编译器
可以自动推导，有时显式写出来对读者
也更清晰。

有时在函数形参列表已经出现之后再指定返回类型，
会更轻松、更易读。当返回类型依赖于
模板参数时尤其如此。例如：

<div class='neutralcode'></div>

```cpp
template <typename T, typename U>
auto Add(T t, U u) -> decltype(t + u);
```

对比

<div class='neutralcode'></div>

```cpp
template <typename T, typename U>
decltype(declval<T&>() + declval<U&>()) Add(T t, U u);
```

##### 缺点

尾置返回类型语法在 C、Java 等类 C++ 语言中
没有对应形式，因此有些读者会觉得陌生。

既有代码库中有数量庞大的函数声明，
它们不会改成新语法，因此现实的选择是
只用旧语法，或混用两种。只采用一种形式
更利于风格统一。

##### 结论

多数情况下，继续使用较旧的函数声明风格，即
把返回类型放在函数名之前。仅在必需时（如 lambda）
才使用新的尾置返回类型形式；或者当把类型放在
函数形参列表之后，能让你以可读得多的方式
写出该类型时也可使用。后一类情形应当很少；
它主要出现在相当复杂的模板代码中，而这类代码
[在多数情况下是不被鼓励的](#Template_metaprogramming)。

<a id="Google-Specific_Magic"></a>

## Google 特有的魔法

我们使用各种技巧与工具让 C++ 代码更健壮，
也有一些使用 C++ 的方式可能与你在别处见到的不同。

<a id="cpplint"></a>

### cpplint

使用 <code>cpplint.py</code> 检测风格错误。

<code>cpplint.py</code> 是一个读取源文件并识别许多
风格错误的工具。它并不完美，既有误报也有
漏报，但仍是一件有价值的工具。

有些项目提供了如何从其项目工具中运行 `cpplint.py` 的
说明。若你所贡献的项目没有，则可以单独下载
[`cpplint.py`](https://raw.githubusercontent.com/cpplint/cpplint/HEAD/cpplint.py)
来使用。

<a id="Other_C++_Features"></a>

## 其他 C++ 特性

<a id="Ownership_and_Smart_Pointers"></a>

### 所有权与智能指针

动态分配的对象最好有单一、固定的所有者。
转移所有权时优先使用智能指针。

##### 定义

“所有权”是一种用于管理动态分配内存
（及其他资源）的记账技术。动态分配对象的所有者，
是负责确保该对象在不再需要时被删除的
对象或函数。所有权有时可以共享，此时通常由
最后一个所有者负责删除。即便所有权不共享，
也可以从一段代码转移到另一段代码。

“智能”指针是行为类似指针的类，例如通过重载
`*` 与 `->` 运算符。某些智能指针类型可用于自动完成
所有权记账，以确保这些职责得到履行。
[`std::unique_ptr`](http://en.cppreference.com/w/cpp/memory/unique_ptr) 是一种
智能指针类型，表达对某个动态分配对象的独占所有权；
当 `std::unique_ptr` 离开作用域时，该对象即被删除。
它不能被复制，但可以被*移动*以表示所有权转移。
[`std::shared_ptr`](http://en.cppreference.com/w/cpp/memory/shared_ptr) 是一种
智能指针类型，表达对某个动态分配对象的共享所有权。
`std::shared_ptr` 可以被复制；对象的所有权由所有副本
共享，当最后一个 `std::shared_ptr` 被
销毁时，对象即被删除。

##### 优点

*   若没有某种所有权逻辑，管理动态分配的内存
    几乎是不可能的。
*   转移对象的所有权可能比复制它更省开销（如果
    复制本身可行的话）。
*   转移所有权可能比“借用”指针或
    引用更简单，因为它减少了在两方使用者之间协调对象
    生命周期的需要。
*   智能指针能提升可读性，因为它让所有权逻辑显式、
    自文档化且不含糊。
*   智能指针可以免去手工的所有权记账，简化代码，
    并排除一大类错误。
*   对 `const` 对象而言，共享所有权是深度拷贝之外
    一种简单而高效的替代方案。

##### 缺点

*   所有权必须通过指针（无论智能指针还是
    普通指针）来表示和转移。指针语义比值语义更复杂，
    在 API 中尤其如此：你不只需操心所有权，
    还得操心别名、生命周期与可变性等问题。
*   值语义的性能开销常被高估，因此所有权转移
    带来的性能收益未必抵得上其在可读性与
    复杂度上的代价。
*   转移所有权的 API 会把调用方限定在单一的
    内存管理模型里。
*   使用智能指针的代码不太能明确体现资源释放
    发生在何处。
*   `std::unique_ptr` 用移动语义表达所有权转移，这可能
    较为复杂，也会让一些程序员困惑。
*   共享所有权可能是诱人的捷径，使人不去精心设计
    所有权，从而模糊系统的设计。
*   共享所有权需要在运行期显式记账，
    开销可能很高。
*   在某些情况下（例如循环引用），共享所有权的对象可能
    永远不会被删除。
*   智能指针并非普通指针的完美替代品。

##### 结论

若确实需要动态分配，优先把所有权留给执行分配的
代码。若其他代码需要访问该对象，可考虑传给它一份
副本，或传递指针 / 引用而不转移所有权。优先
使用 `std::unique_ptr` 让所有权转移显式化。例如：

<div class='goodcode'></div>

```cpp
std::unique_ptr<Foo> FooFactory();
void FooConsumer(std::unique_ptr<Foo> ptr);
```

没有充分理由时，不要把代码设计成使用共享所有权。
一个理由是避免昂贵的拷贝操作，但只有当性能收益
显著、且底层对象不可变时，才应这样做
（即 `std::shared_ptr<const Foo>`）。若确实使用共享所有权，
优先使用 `std::shared_ptr`。

绝不要使用 `std::auto_ptr`。请改用 `std::unique_ptr`。

<a id="Rvalue_references"></a>

### 右值引用

仅在下面列出的某些特殊情形中使用右值引用。

##### 定义

右值引用是一种只能绑定到临时
对象的引用。其语法与传统引用语法相似。例如，
`void f(std::string&& s);` 声明的函数，其参数是对
`std::string` 的右值引用。

<a id="Forwarding_references"></a>当 `&&` 记号作用于
函数形参中未限定的模板实参时，会适用特殊的模板实参
推导规则。这样的引用称为转发引用。

##### 优点

*   定义移动构造函数（接受指向本类类型的右值引用的
    构造函数）使得移动值而非复制值成为可能。若 `v1`
    是 `std::vector<std::string>`，那么 `auto v2(std::move(v1))`
    很可能只产生一些简单的指针操作，而不是
    复制大量数据。很多情况下这能带来显著的
    性能提升。
*   右值引用使实现可移动但不可复制的类型成为可能，
    这对那些没有合理的复制定义、却仍希望
    作为函数实参传递、放入容器等的
    类型很有用。
*   `std::move` 是有效使用某些标准库类型
    （如 `std::unique_ptr`）所必需的。
*   使用右值引用记号的[转发引用](#Forwarding_references)
    使编写通用函数包装器成为可能，它能把实参
    转发给另一个函数，且无论实参是否为临时对象、
    以及是否为 const 都能工作。这称为“完美
    转发”。

##### 缺点

*   右值引用并未被广泛理解。诸如引用折叠、
    以及转发引用的特殊推导规则之类的规则，
    都有些晦涩。
*   右值引用常被误用。在期望实参在调用后
    仍处于有效指定状态的签名中，或在
    不执行移动操作的签名中，使用右值引用
    有违直觉。

##### 结论

不要使用右值引用（也不要把 `&&` 限定符用于方法），
以下情形除外：

*   可以用它们定义移动构造函数与移动赋值运算符
    （如[可复制与可移动类型](#Copyable_Movable_Types)中所述）。
*   可以用它们定义 `&&` 限定的方法，这些方法在逻辑上“消耗”
    `*this`，使其处于不可用或空状态。注意这仅适用于
    方法限定符（位于函数签名右括号之后）；
    若想“消耗”普通函数
    形参，优先按值传递。
*   可以把转发引用与
    [`std::forward`](http://en.cppreference.com/w/cpp/utility/forward) 结合使用，
    以支持完美转发。
*   可以用它们定义成对的重载，例如一个接受 `Foo&&`、
    另一个接受 `const Foo&`。通常首选的做法就是
    按值传递，但成对重载的函数有时能带来更好的
    性能，例如当函数有时并不消耗输入时。
    一如既往：若为了性能而编写更复杂的代码，
    务必有证据表明它确实有效。

<a id="Friends"></a>

### 友元

在合理范围内，我们允许使用 `friend` 类与函数。

友元通常应定义在同一个文件中，这样读者就不必
到别的文件里去查找类私有成员的使用处。
`friend` 的一种常见用法，是让 `FooBuilder` 类成为 `Foo` 的友元，
以便它能正确构造 `Foo` 的内部状态，又不必把该状态
暴露给外界。某些情况下，让单元测试类成为
被测类的友元也很有用。

友元扩展了类的封装边界，但并未打破它。在
只想让另一个类访问某成员时，这比把该成员设为 `public`
更好。不过，多数类应当只通过
公开成员与其他类交互。

<a id="Exceptions"></a>

### 异常

我们不使用 C++ 异常。

##### 优点

*   异常让应用的较高层能够决定如何处理
    深层嵌套函数中的“不可能发生”的失败，
    而无需错误码那种晦涩且易出错的记账。
*   多数其他现代语言都使用异常。在 C++ 中使用异常
    会使其与 Python、Java 以及他人所熟悉的
    C++ 更加一致。
*   某些第三方 C++ 库使用异常，在内部关闭异常
    会增大与这些库集成的难度。
*   异常是构造函数失败的唯一方式。我们可以用
    工厂函数或 `Init()` 方法来模拟，但二者分别需要
    堆分配，或引入新的“无效”状态。
*   异常在测试框架中确实很好用。

##### 缺点

*   向既有函数添加 `throw` 语句时，必须检查
    它的所有传递调用方。它们要么至少提供基本的
    异常安全保证，要么绝不捕获该异常，并接受
    程序因此终止。例如，若 `f()` 调用
    `g()` 而后者调用 `h()`，若 `h` 抛出的异常被 `f` 捕获，`g` 就得
    小心处理，否则可能无法正确清理。
*   更一般地说，异常使程序的控制流难以
    仅凭阅读代码来评估：函数可能在你意想不到的
    地方返回。这带来可维护性与调试上的困难。
    可以通过限制异常的使用方式与位置来
    降低这一代价，但代价是开发者需要了解
*   异常安全既需要 RAII，也需要不同的编码实践。需要大量
    配套机制，才能轻松写出正确的异常安全代码。
    此外，为避免要求读者理解整个调用图，
    异常安全代码必须把写入持久状态的逻辑
    隔离到“提交”阶段。这既带来好处也带来代价
    （也许你不得不为了隔离提交而把代码写得晦涩）。
    允许使用异常会迫使我们即便在并不值得时，
    也始终付出这些代价。
*   启用异常会给生成的每个二进制文件增加数据，
    使编译时间变长（可能只是略微），并可能加大地址空间压力。
*   异常的存在可能促使开发者在不合时宜时抛出异常，
    或在不安全时进行恢复。例如，无效的用户输入
    不应导致抛出异常。我们还得把风格指南
    写得更长，才能把这些限制
    记录下来！

##### 结论

表面上看，使用异常的好处大于代价，在新项目中
尤其如此。然而对既有代码而言，引入异常
会牵连所有依赖它的代码。若异常能传播到新项目
之外，把新项目集成到既有的无异常代码中也会
变得棘手。由于 Google 现有的多数 C++ 代码并未为
处理异常做好准备，采纳会产生异常的新代码
相对困难。

鉴于 Google 的既有代码并不容忍异常，使用异常的
代价略高于新项目中的代价。转换过程会
缓慢且易出错。我们认为异常的现有替代方案，
例如错误码与断言，并不会带来
显著的负担。

我们反对使用异常并非基于哲学或道德
立场，而是出于实际考虑。因为我们希望在 Google
使用自己的开源项目，而这些项目若使用异常就很难
做到，所以也需要在 Google 的开源项目中劝阻
使用异常。若一切从头再来，情况大概会有所不同。

这项禁令同样适用于与异常处理相关的特性，例如
`std::exception_ptr` 和 `std::nested_exception`。

这条规则对 Windows 代码有一处[例外](#Windows_Code)
（这里并非双关）。

<a id="noexcept"></a>

### `noexcept`

在有用且正确时才指定 `noexcept`。

##### 定义

`noexcept` 说明符用于指明函数是否会抛出
异常。若异常从标为 `noexcept` 的函数中逸出，
程序会通过 `std::terminate` 崩溃。

`noexcept` 运算符执行编译期检查，若某个
表达式被声明为不抛出任何异常，则返回 true。

##### 优点

*   把移动构造函数指定为 `noexcept` 在某些情形下能提升性能，
    例如 `std::vector<T>::resize()` 在 T 的移动构造函数为
    `noexcept` 时，会移动对象而非复制对象。
*   为函数指定 `noexcept` 可在启用异常的环境中触发编译器优化，
    例如若已知不会抛出异常，编译器就不必
    为栈展开生成额外代码：这正是
    `noexcept` 说明符带来的效果。

##### 缺点

*   在遵循本指南且禁用异常的项目中，很难确保
    `noexcept` 说明符是正确的，甚至很难界定
    “正确”究竟意味着什么。
*   撤销 `noexcept` 即便不是不可能，也很困难，因为它
    取消了调用方可能依赖的某项保证，且难以察觉。

##### 结论

若 `noexcept` 对性能有益，且准确反映了
函数的预期语义——即倘若函数体内某处抛出
了异常，就表示发生了致命错误——则可以使用它。
可以认为移动构造函数上的 `noexcept` 有实在的
性能收益。若你认为在某个其他函数上指定
`noexcept` 有显著性能收益，请与项目负责人讨论。

若异常被完全禁用（即多数 Google C++ 环境），优先使用无条件的 `noexcept`。
否则使用带简单条件的条件 `noexcept` 说明符，使其仅在函数
确实可能抛出的少数情形下求值为 false。条件中可以包含
对相关操作是否可能抛出的类型特征检查，例如
用于移动构造对象的
`std::is_nothrow_move_constructible`；也可以检查分配是否
可能抛出，例如 `absl::default_allocator_is_nothrow` 之于标准
默认分配。注意很多情况下异常的唯一可能诱因是
分配失败（我们认为移动构造函数除分配失败外
不应抛出异常），而且许多应用适合
把内存耗尽当作致命错误，而不是程序
应尝试恢复的异常情况。即便对于
其他潜在失败，也应把接口简洁性置于
支持所有可能的抛异常场景之上：例如，与其写出
依赖哈希函数是否可能抛出的复杂 `noexcept` 子句，
不如简单地注明你的组件不支持
会抛出的哈希函数，并无条件地设为 `noexcept`。

<a id="Run-Time_Type_Information__RTTI_"></a>

### 运行期类型信息（RTTI）

避免使用运行期类型信息（RTTI）。

##### 定义

RTTI 允许程序员在运行期查询对象的 C++ 类。
这通过 `typeid` 或 `dynamic_cast` 实现。

##### 优点

RTTI 的标准替代方案（见下文）要求修改或
重新设计相关的类层次结构。有时这类修改
并不可行或并不合意，在广泛使用的成熟代码中尤其如此。

RTTI 在某些单元测试中很有用。例如，在测试
工厂类时，测试需要验证新建对象是否具有
预期的动态类型，此时 RTTI 很有用。它也便于管理
对象与其 mock 之间的关系。

在需要处理多个抽象对象时 RTTI 很有用。请看

<div class='neutralcode'></div>

```cpp
bool Base::Equal(Base* other) = 0;
bool Derived::Equal(Base* other) {
  Derived* that = dynamic_cast<Derived*>(other);
  if (that == nullptr)
    return false;
  ...
}
```

##### 缺点

在运行期查询对象的类型，往往意味着设计有问题。
需要知道对象在运行期的类型，通常表明
你的类层次结构设计有缺陷。

不加节制地使用 RTTI 会让代码难以维护。它可能
导致基于类型的判定树或 switch 语句散落在代码各处，
日后修改时必须逐一检查。

##### 结论

RTTI 有正当用途，但容易被滥用，使用时必须谨慎。
在单元测试中可以随意使用，但在其他代码中
应尽量避免。尤其在新代码中使用 RTTI 前要三思。若
你发现自己需要根据对象的类写出行为不同的代码，
可考虑以下某种不查询类型的替代方案：

*   若要根据具体的子类类型走不同代码路径，
    首选虚函数。这样把工作放在对象
    自身内部。
*   若工作不属于对象内部，而属于某段处理代码，
    可考虑双分派方案，例如 Visitor 设计模式。
    这让对象之外的机制也能借助内置类型系统
    判定类的类型。

当程序逻辑能保证某个基类实例实际上
就是特定派生类的实例时，可以对该对象随意使用 `dynamic_cast`。
通常来说，
[`absl::down_cast`](https://github.com/abseil/abseil-cpp/blob/master/absl/base/casts.h)
是更好的替代方案。

基于类型的判定树强烈表明你的代码
走错了方向。

<div class='badcode'></div>

```cpp
if (typeid(*data) == typeid(D1)) {
  ...
} else if (typeid(*data) == typeid(D2)) {
  ...
} else if (typeid(*data) == typeid(D3)) {
...
```

这样的代码在类层次结构中加入新的子类时
通常会失效。而且，当子类的属性变化时，
很难找出并修改所有受影响的代码段。

不要手工实现类似 RTTI 的变通方案。反对 RTTI 的理由
同样适用于带类型标签的类层次结构之类。而且，
变通方案会掩盖你的真实意图。

<a id="Casting"></a>

### 类型转换

使用 C++ 风格的类型转换，如 `static_cast<float>(double_value)`，或用花括号
初始化来转换算术类型，例如
`int64_t y = int64_t{1} << 42`。不要使用 `(int)x` 这类转换形式，
除非转换目标是 `void`。`T(x)` 这类形式仅当 `T` 是类
类型时才可使用。

##### 定义

C++ 引入了一套不同于 C 的转换体系，
用以区分不同种类的转换操作。

##### 优点

C 风格转换的问题在于操作的歧义：有时你
做的是*转换*（例如 `(int)3.5`），有时做的是*强制转换*
（例如 `(int)"hello"`）。花括号初始化与 C++ 转换常能避免
这种歧义。此外，C++ 转换在搜索时
也更显眼。

##### 缺点

C++ 风格的转换语法冗长而笨重。

##### 结论

通常不要使用 C 风格转换。需要显式类型转换时，
改用下列 C++ 风格转换。其中一些属于标准 C++
语言的一部分，另一些定义在
[`absl/base/casts.h`](https://github.com/abseil/abseil-cpp/blob/master/absl/base/casts.h)。
选用第一条**确实适用**的：

*   用花括号初始化转换算术类型（例如 `int64_t{x}`）。
    这是最安全的做法，因为若转换可能造成
    信息丢失，代码将无法编译。语法也更简洁。
*   显式转换为类类型时，使用函数风格转换；例如
    优先用 `std::string(some_cord)` 而非 `static_cast<std::string>(some_cord)`。
*   用 `absl::implicit_cast` 安全地沿类型层次向上转换，例如把
    `Foo*` 转为 `SuperclassOfFoo*`，或把 `Foo*` 转为 `const Foo*`。C++
    通常会自动完成，但某些情形需要显式的
    向上转换，例如使用 `?:` 运算符时。
*   把 `static_cast` 当作会做值转换的 C 风格转换的等价物；
    当你需要把指针从某个类显式向上转换为
    它的超类，或需要把指针从超类
    显式向下转换为子类时使用。后一种情形下，必须确认对象
    确实是该子类的实例。
*   用 `absl::down_cast` 把指针从超类转换为子类。
    必须确认对象确实是该子类的实例。
*   用 `const_cast` 去除 `const` 限定符（见
    [const](#Use_of_const)）。
*   用 `reinterpret_cast` 在指针类型与整数及其他指针类型
    （包括 `void*`）之间做不安全的相互转换。仅在
    你清楚自己在做什么、并理解别名问题时才使用。
    也可以考虑先解引用指针（不做转换），再用
    `std::bit_cast` 转换得到的值。
*   用 `std::bit_cast` 以另一种等大小的类型解释某个值的
    原始位（类型双关），例如把某个
    `double` 的位解释为 `int64_t`。

参见 [RTTI 一节](#Run-Time_Type_Information__RTTI_) 了解
`dynamic_cast` 的使用指导。

<a id="Streams"></a>

### 流

在适当场合使用流，并坚持“简单”的用法。仅为表示值的类型重载 `<<`，
用于流式输出，且只写出用户可见的
值，不写出任何实现细节。

##### 定义

流是 C++ 中标准的 I/O 抽象，标准
头文件 `<iostream>` 便是代表。它们在 Google 代码中被广泛使用，
主要用于调试日志与测试诊断。

##### 优点

`<<` 与 `>>` 流运算符为格式化 I/O 提供了一套
易学、可移植、可复用且可扩展的 API。相比之下 `printf`
甚至不支持 `std::string`，更不用说用户自定义类型，
而且很难可移植地使用。`printf` 还迫使你在
众多略有差异的版本中做选择，并在几十种
转换说明符之间周旋。

流通过 `std::cin`、`std::cout`、
`std::cerr` 和 `std::clog` 为控制台 I/O 提供了一流支持。C API 也能做到，
却受制于必须手工缓冲输入。

##### 缺点

*   流的格式可通过修改流的状态来配置。
    这类修改是持久的，因此代码行为可能受
    流的全部先前历史影响，除非你不嫌麻烦，
    在其他代码可能动过它时每次都将其恢复到已知状态。
    用户代码不仅能修改内置状态，还能通过
    注册机制添加新的状态变量与行为。

*   由于上述问题、流式代码中代码与数据混杂，
    以及运算符重载的使用（它可能选中与你预期
    不同的重载），很难精确控制流的输出。

*   用一串 `<<` 运算符拼出输出的做法
    会妨碍国际化，因为它把语序固化在代码里，
    而且流对本地化的支持
    [有缺陷](http://www.boost.org/doc/libs/1_48_0/libs/locale/doc/html/rationale.html#rationale_why)。

*   流的 API 精妙而复杂，程序员必须积累
    使用经验才能用得好。

*   解析 `<<` 的众多重载对编译器代价极高。
    在大型代码库中普遍使用时，可能占用多达 20% 的
    语法与语义分析时间。

##### 结论

仅当流是最适合该任务的工具时才使用它。
典型情形是：I/O 是临时的、局部的、人类可读的，
且面向其他开发者而非最终用户。要与周围代码
以及整个代码库保持一致；若已有成熟工具
能解决你的问题，就改用该工具。尤其是日志库
通常比 `std::cerr` 或 `std::clog` 更适合诊断输出，
而 `absl/strings` 中的库（或等价物）通常比
`std::stringstream` 更合适。

面向外部用户或处理不可信数据的 I/O 应避免使用流。
应改用合适的模板库来处理国际化、
本地化与安全加固等问题。

若确实使用流，应避开流 API 中带状态的部分
（错误状态除外），如 `imbue()`、`xalloc()` 和 `register_callback()`。
使用显式的格式化函数（如 `absl::StreamFormat()`），而不是
流操纵器或格式标志，来控制数字进制、精度、
填充等格式细节。

仅当你的类型表示某个值、且 `<<` 输出该值的
人类可读字符串表示时，才为它重载 `<<` 作为
流式运算符。避免在 `<<` 的输出中暴露实现细节；
若为调试需要打印对象内部信息，改用有名称的函数
（最常见的约定是名为 `DebugString()` 的方法）。

<a id="Preincrement_and_Predecrement"></a>

### 前置自增与前置自减

除非需要后置语义，否则自增与自减运算符一律使用前缀形式（`++i`）。
不必使用后缀形式。

##### 定义

当变量被自增（`++i` 或 `i++`）或自减（`--i` 或 `i--`），
而表达式的值不被使用时，必须决定采用
前置自增（自减）还是后置自增（自减）。

##### 优点

后置自增 / 自减表达式求值得到的是*修改之前
的值*。这可能让代码更紧凑，却更难读。
前缀形式通常更易读，效率绝不更差，
而且可能更高效，因为它无需复制操作
之前的值。

##### 缺点

在 C 语言中形成了使用后置自增的传统，即便
表达式的值不被使用，在 `for` 循环中尤其如此。

##### 结论

使用前置自增 / 自减，除非代码明确需要
后置自增 / 自减表达式的结果。

<a id="Use_of_const"></a>

### const 的用法

在 API 中，只要有意义就使用 `const`。对某些用途，`constexpr` 是
比 `const` 更好的选择。

##### 定义

声明的变量与参数前可加上关键字 `const`，
表示这些变量不会被改变（例如 `const int foo`）。
类函数可以带 `const` 限定符，表示该函数不改变
类成员变量的状态（例如
`class Foo { int Bar(char c) const; };`）。

##### 优点

让人更容易理解变量是如何被使用的。让
编译器能做更好的类型检查，甚至生成更好的代码。
有助于人们确信程序的正确性，因为他们知道
所调用的函数在修改变量方面是受限的。有助于
人们知道在多线程程序中哪些函数无需加锁
即可安全使用。

##### 缺点

`const` 具有传染性：若把 `const` 变量传给函数，
该函数的原型中也必须带 `const`（否则变量就需要 `const_cast`）。
调用库函数时，这可能成为特别棘手的问题。

##### 结论

我们强烈建议在 API 中使用 `const`（即用于函数参数、
方法和非局部变量），只要有意义且准确。这
为「某操作可以改动哪些对象」提供了一致、且多数
由编译器验证的说明。拥有一种一致可靠的方式来区分
读与写，对编写线程安全代码至关重要，在许多其他
场合也很有用。尤其是：

*   若函数保证不修改按引用或按指针传入的实参，
    则对应的函数参数应当是
    指向 const 的引用（`const T&`）或指向 const 的指针（`const T*`），
    二者分别对应上述两种传参方式。
*   对按值传递的函数参数，`const` 对调用方没有影响，
    因此不建议在函数声明中使用。参见
    [TotW #109](https://abseil.io/tips/109)。
*   应将方法声明为 `const`，除非它会改变对象的逻辑状态，
    或让用户能改动该状态（例如返回非
    `const` 引用，但这很少见），或无法被安全地并发调用，
    则另当别论。

在局部变量上使用 `const` 既不鼓励也不反对。

一个类的所有 `const` 操作都应能彼此安全地并发调用。
若做不到，就必须明确把该类注明为
“线程不安全”。

#### const 应放在哪里

有些人更喜欢 `int const* foo` 而非 `const int* foo` 的形式。
他们认为这样更易读，因为更一致：它保持了
`const` 始终跟在它所修饰对象之后的规则。然而，
在几乎没有深层嵌套指针表达式的代码库中，
这种一致性论证并不成立，因为多数 `const` 表达式只有一个 `const`，
且作用于底层值。此时并无一致性可维护。把
`const` 放在前面可以说更易读，因为它沿袭英语把
“形容词”（`const`）放在“名词”（`int`）之前的习惯。

话虽如此，我们虽鼓励把 `const` 放在前面，但并不强制。
但务必与周围代码保持一致！

<a id="Use_of_constexpr"></a>

### constexpr、constinit 与 consteval 的用法

用 `constexpr` 定义真正的常量，或确保常量初始化。
用 `constinit` 确保非常量变量的常量初始化。

##### 定义

某些变量可声明为 `constexpr`，表示它们是
真正的常量，即在编译 / 链接期就固定下来。某些函数与构造函数
可以声明为 `constexpr`，从而能用于定义
`constexpr` 变量。函数可声明为 `consteval`，以把其用途
限制在编译期。

##### 优点

使用 `constexpr` 可以定义含浮点表达式的常量，
而不限于字面量；可以定义用户自定义类型的常量；
也可以定义带函数调用的常量。

##### 缺点

过早把某个东西标为 `constexpr`，若日后必须降级，
可能带来迁移问题。当前对这些函数与构造函数中
`constexpr` 所允许内容的限制，可能诱使这些定义里出现
晦涩的变通写法。

##### 结论

`constexpr` 定义能更可靠地刻画出接口中的常量部分。
用 `constexpr` 指定真正的常量，以及
支撑其定义的函数。`consteval` 可用于不得
在运行期调用的代码。不要把函数定义复杂化，只为了
能在 `constexpr` 中使用；也不要用 `constexpr` 或 `consteval` 来强制内联。

<a id="Integer_Types"></a>

### 整数类型

在 C++ 内置的整数类型中，唯一使用的是 `int`。
若程序需要不同大小的整数类型，应取自
`<stdint.h>` 的精确宽度整数类型，例如 `int16_t`。若某个值可能大于或等于
2<sup>31</sup>，就使用 `int64_t` 之类的 64 位类型。请记住，
即便你的值对 `int` 来说绝不会太大，它也可能
被用于需要更大类型的中间计算。若有疑问，
就选更大的类型。

##### 定义

C++ 并未为 `int` 之类的整数类型规定确切大小。
当代架构上的常见大小是：`short` 为 16 位、`int` 为 32 位、
`long` 为 32 或 64 位、`long long` 为 64 位，但不同平台
会做出不同选择，对 `long` 尤其如此。

##### 优点

声明方式统一。

##### 缺点

C++ 中整型的大小会因编译器与架构而异。

##### 结论

标准库头文件 `<stdint.h>` 定义了 `int16_t`、
`uint32_t`、`int64_t` 等类型。当需要对整数大小作出保证时，
应始终优先使用它们，而不是 `short`、`unsigned long long` 之类。
在内置整数类型中，只应使用 `int`。
在适当场合，欢迎使用 `size_t`、
`ptrdiff_t` 等标准类型别名。

我们经常使用 `int`，用于那些明知不会太大的整数，
例如循环计数器。这类场合就用朴素的 `int`。应假定
`int` 至少为 32 位，但不要假定它超过 32 位。
若需要 64 位整数类型，使用 `int64_t` 或 `uint64_t`。

对于已知可能“很大”的整数，使用 `int64_t`。

不应使用 `uint32_t` 之类的无符号整数类型，
除非有正当理由，例如表示位模式而非数值，
或需要按 2<sup>N</sup> 取模的有定义溢出。尤其不要用
无符号类型来表示某个数绝不会为负。应改用断言
来表达这一点。

在标准库整数类型上优先省略 `std::` 前缀，
多出的 5 个字符不值得带来额外的杂乱。

若你的代码是会返回大小的容器，务必使用能容纳
该容器任何可能用法的类型。若有疑问，
宁用较大的类型，也不用较小的类型。

转换整数类型时要小心。整数转换与提升可能
导致未定义行为，引发安全缺陷及其他问题。

#### 关于无符号整数

无符号整数适合表示位域与模运算。
由于历史偶然，C++ 标准也用无符号整数
表示容器的大小——标准委员会的许多成员认为
这是个错误，但如今实际上已无法修正。
无符号运算并不刻画简单整数的行为，
而是由标准定义为刻画模运算（在溢出 / 下溢时
回绕），这意味着很大一类缺陷无法
被编译器诊断出来。在另一些情况下，这种有定义的行为
还会妨碍优化。

话虽如此，混用整数类型的有无符号同样
造成大量问题。我们能给出的最佳建议是：尽量使用
迭代器与容器，而不是指针与大小；尽量不混用有无符号；
尽量避免无符号类型（表示位域或模运算时
除外）。不要仅仅为了断言某个变量非负
就使用无符号类型。

<a id="Floating-Point_Types"></a>

### 浮点类型

在 C++ 内置的浮点类型中，只使用 `float` 与
`double`。可以假定它们分别表示 IEEE-754 binary32 与
binary64。

不要使用 `long double`，因为它给出的结果不可移植。

<a id="Architecture_Portability"></a>

### 架构可移植性 []() {#64-bit_Portability}

编写具备架构可移植性的代码。不要依赖某个
特定处理器独有的 CPU 特性。

*   输出值时，使用类型安全的数值格式化库，例如
    [`absl::StrCat`](https://github.com/abseil/abseil-cpp/blob/master/absl/strings/str_cat.h)，
    [`absl::Substitute`](https://github.com/abseil/abseil-cpp/blob/master/absl/strings/substitute.h)，
    [`absl::StrFormat`](https://github.com/abseil/abseil-cpp/blob/master/absl/strings/str_format.h)，
    或 [`std::ostream`](#Streams)，而不是 `printf` 系列函数。
*   在把结构化数据移入或移出进程时，使用
    序列化库（如 [Protocol Buffers](https://protobuf.dev/)）来编码，
    而不要直接复制内存中的表示。
*   若需要把内存地址当作整数处理，
    用 `uintptr_t` 保存，而不是 `uint32_t` 或 `uint64_t`。
*   按需使用[花括号初始化](#Casting)来创建 64 位常量。
    例如：

    <div class='goodcode'></div>

    ```cpp
    int64_t my_value{0x123456789};
    uint64_t my_mask{uint64_t{3} << 48};
    ```

*   使用可移植的[浮点类型](#Floating-Point_Types)；避免
    `long double`。

*   使用可移植的[整数类型](#Integer_Types)；避免 `short`、`long` 与
    `long long`。

<a id="Preprocessor_Macros"></a>

### 预处理器宏

避免定义宏，尤其是在头文件中；优先使用内联函数、枚举
和 `const` 变量。给宏命名时以项目的命名空间作为前缀。
不要用宏来声明 C++ API 的组成部分。

宏意味着你看到的代码与编译器看到的代码并不相同。
这可能引入意料之外的行为，尤其因为宏具有全局
作用域。

用宏来声明 C++ API 的组成部分时，
宏带来的问题尤其严重，公开 API 更是如此。开发者
错误使用该接口时，编译器给出的每一条错误信息
现在都必须解释宏是如何构成该接口的。重构与
分析工具在更新接口时会困难得多。因此，
我们明确禁止以这种方式使用宏。例如，应避免
下面这样的模式：

<div class='badcode'></div>

```cpp
class WOMBAT_TYPE(Foo) {
  // ...

 public:
  EXPAND_PUBLIC_WOMBAT_API(Foo)

  EXPAND_WOMBAT_COMPARISONS(Foo, ==, <)
};
```

所幸在 C++ 中，宏远不像在 C 中那样不可或缺。
与其用宏内联对性能至关重要的代码，不如用内联函数。
与其用宏保存常量，不如用 `const` 变量。与其
用宏来“简写”长变量名，不如用引用。与其
用宏来条件编译代码……嗯，干脆完全不要这样做
（当然，为防止头文件被重复包含而使用的 `#define` 保护
除外）。它会让测试困难得多。

宏能做到这些其他技术做不到的事，你也确实会在
代码库中见到它们，尤其在底层库中。它们的某些
特殊能力（如字符串化、拼接等）无法通过
语言本身获得。但在使用宏之前，请仔细考虑
是否存在不用宏就能达到同样效果的办法。若需要添加
用于声明 API 的宏，请联系项目负责人，申请
对本规则的豁免。

下面这种用法模式可以避开宏的许多问题；
若使用宏，请尽可能遵循：

*   不要在 `.h` 文件中定义宏。
*   紧挨着使用之前 `#define` 宏，用完立即 `#undef`。
*   不要只是先 `#undef` 现有宏再换成自己的；
    而应另选一个很可能独一无二的名字。
*   尽量不要使用会展开成不平衡 C++ 结构的宏，
    至少要把这种行为写清楚。
*   最好别用 `##` 来生成函数 / 类 / 变量名。

从头文件导出宏（即在头文件中定义宏，且未在
头文件结束前 `#undef`）是极其不推荐的。
若确实从头文件导出宏，它必须具有全局
唯一的名字。为此，必须以由项目
命名空间名（但用大写）构成的前缀来命名。

<a id="0_and_nullptr/NULL"></a>

### 0 与 nullptr/NULL

指针用 `nullptr`，字符用 `'\0'`（不要用字面量 `0`）。

对指针（地址值）使用 `nullptr`，因为它提供类型安全。

空字符使用 `'\0'`。使用正确的类型能让代码
更易读。

<a id="sizeof"></a>

### sizeof

优先使用 `sizeof(varname)` 而非 `sizeof(type)`。

取某个特定变量的大小时使用 `sizeof(varname)`。
若有人改动了该变量的类型，`sizeof(varname)` 会
相应地自动更新，无论改动发生在现在还是以后。与特定变量无关的代码可用 `sizeof(type)`，
例如管理外部或内部数据格式、且不便使用
合适 C++ 类型变量的代码。

<div class='goodcode'></div>

```cpp
MyStruct data;
memset(&data, 0, sizeof(data));
```

<div class='badcode'></div>

```cpp
memset(&data, 0, sizeof(MyStruct));
```

<div class='goodcode'></div>

```cpp
if (raw_size < sizeof(int)) {
  LOG(ERROR) << "compressed record not big enough for count: " << raw_size;
  return false;
}
```

<a id="Type_deduction"></a>

### 类型推导（包括 auto） []() {#auto}

仅在类型推导能让不熟悉该项目的读者更容易理解代码，或能让代码
更安全时使用。不要仅仅为了避免书写显式类型所带来的不便
而使用它。

##### 定义

在若干场景中，C++ 允许（甚至要求）由编译器推导类型，而不是在代码中
显式地写出类型：

[函数模板实参推导](https://en.cppreference.com/w/cpp/language/template_argument_deduction)
:   调用函数模板时可以不显式给出模板实参。编译器会根据函数
    实参的类型推导出这些模板实参：

    <div class='neutralcode'></div>

    ```cpp
    template <typename T>
    void f(T t);

    f(0);  // Invokes f<int>(0)
    ```

    lambda 表达式同样可以带有模板参数，其推导方式
    完全相同：

    <div class='neutralcode'></div>

    ```cpp
    // Sort `vec` in decreasing order
    std::sort(vec.begin(), vec.end(), []<typename T>(T lhs, T rhs) { return lhs > rhs; });
    ```

[`auto` 变量声明](https://en.cppreference.com/w/cpp/language/auto)
:   变量声明可以用 `auto` 关键字代替类型。编译器会根据变量的
    初始化器推导其类型，所遵循的规则与以同一初始化器进行函数
    模板实参推导的规则相同
    （前提是你没有用花括号代替圆括号）。

    <div class='neutralcode'></div>

    ```cpp
    auto a = 42;  // a is an int
    auto& b = a;  // b is an int&
    auto c = b;   // c is an int
    auto d{42};   // d is an int, not a std::initializer_list<int>
    ```

    `auto` 可以用 `const` 限定，也可以作为指针
    或引用类型的一部分使用，并且（自 C++17 起）可作为非类型模板实参。
    这种语法有一种罕见的变体，用 `decltype(auto)` 代替 `auto`，在这种情况下
    推导出的类型是对初始化器应用
    [`decltype`](https://en.cppreference.com/w/cpp/language/decltype) 的
    结果。

[函数返回类型推导](https://en.cppreference.com/w/cpp/language/function#Return_type_deduction)
:   `auto`（以及 `decltype(auto)`）也可以用来代替函数返回
    类型。编译器会根据函数体中的 `return` 语句推导返回类型，
    所遵循的规则与变量声明相同：

    <div class='neutralcode'></div>

    ```cpp
    auto f() { return 0; }  // The return type of f is int
    ```

    [Lambda 表达式](#Lambda_expressions) 的返回类型也可以用同样的
    方式推导，但触发它的是省略返回类型，而不是显式写出
    `auto`。容易混淆的是，函数的[尾置返回类型](#trailing_return)
    语法同样在返回类型的位置使用 `auto`，但那并不依赖
    类型推导；它只是显式返回类型的一种
    替代语法。

[`auto` 参数](https://en.cppreference.com/w/cpp/language/auto.html)
:   函数或 lambda 表达式可以用 `auto` 关键字代替一个
    或多个参数类型。这会使它成为函数模板而不是
    普通函数，并且每个 `auto` 函数参数对应一个
    独立的模板参数：

    <div class='neutralcode'></div>

    ```cpp
    // Sort `vec` in decreasing order
    std::sort(vec.begin(), vec.end(), [](auto lhs, auto rhs) { return lhs > rhs; });
    ```

[Lambda 初始化捕获](https://isocpp.org/wiki/faq/cpp14-language#lambda-captures)
:   lambda 捕获可以带有显式的初始化器，借此可以声明
    全新的变量，而不只是捕获已有的变量：

    <div class='neutralcode'></div>

    ```cpp
    [x = 42, y = "foo"] { ... }  // x is an int, and y is a const char*
    ```

    这种语法不允许指定类型；类型改为按照 `auto` 变量的规则
    推导。

[类模板实参推导](https://en.cppreference.com/w/cpp/language/class_template_argument_deduction)
:   参见[下文](#CTAD)。

[结构化绑定](https://en.cppreference.com/w/cpp/language/structured_binding)
:   用 `auto` 声明 tuple、结构体或数组时，你可以为各个元素
    指定名称，而不必为整个对象命名；这些名称称为
    「结构化绑定」，整个声明称为
    「结构化绑定声明」。这种语法无法指定
    外围对象或各个名称的类型：

    <div class='neutralcode'></div>

    ```cpp
    auto [iter, success] = my_map.insert({key, value});
    if (!success) {
      iter->second = value;
    }
    ```

    `auto` 也可以用 `const`、`&` 和 `&&` 限定，但请注意，
    这些限定符在技术上作用于那个匿名的 tuple、结构体或数组，
    而不是作用于各个绑定。决定各绑定类型的规则相当复杂；
    其结果通常并不出人意料，只是
    即便声明的是引用，绑定类型一般也不会是引用（不过它们的行为
    通常仍与引用类似）。

（以上概述省略了许多细节与注意事项；欲了解更多信息，
请参阅相关链接。）

##### 优点

*   C++ 类型名可能又长又笨重，尤其当它们涉及
    模板或命名空间时。
*   当同一个 C++ 类型名在单个声明或一小片代码区域中反复
    出现时，这种重复可能无助于可读性。
*   有时让类型被推导出来更安全，因为这可以避免
    意外发生拷贝或类型转换。

##### 缺点

当类型显式写出时，C++ 代码通常更清晰，尤其是当类型
推导需要依赖代码中相距较远处的信息时。在如下
表达式中：

<div class='badcode'></div>

```cpp
auto foo = x.add_foo();
auto i = y.Find(key);
```

如果 `y` 的类型不是非常明确，或者 `y` 是在许多行之前声明的，
那么结果类型可能并不显而易见。

程序员必须理解类型推导何时会、何时不会产生
引用类型，否则就会在本无意之时得到拷贝。

如果推导出的类型被用作接口的一部分，那么程序员可能
只是想改动它的值，却改动了它的类型，从而引发比预期
更为剧烈的 API 变动。

##### 结论

基本规则是：仅在类型推导能让代码更清晰或更安全时才使用它，
不要仅仅为了避免书写显式类型所带来的不便而使用它。
在判断代码是否更清晰时，请记住你的
读者未必与你在同一团队，也未必熟悉你的项目，因此
那些你和评审者觉得多余的累赘类型，往往
会为其他人提供有用的信息。例如，你可以假定
`make_unique<Foo>()` 的返回类型是显而易见的，但
`MyWidgetFactory()` 的返回类型大概并非如此。

这些原则适用于所有形式的类型推导，但具体细节各有不同，
如下文各节所述。

###### 函数模板实参推导

函数模板实参推导几乎总是可以的。类型推导是
与函数模板交互时合乎预期的默认方式，因为它让
函数模板能够表现得像是无数个普通函数重载的集合。
因此，函数模板几乎总是被设计成让模板
实参推导清晰且安全，否则就干脆无法编译。

###### 局部变量类型推导

对于局部变量，你可以使用类型推导来消除显而易见或无关紧要的
类型信息，从而让代码更清晰，使读者
能够把注意力放在代码中有意义的部分：

<div class='neutralcode'></div>

```cpp
std::unique_ptr<WidgetWithBellsAndWhistles> widget =
    std::make_unique<WidgetWithBellsAndWhistles>(arg1, arg2);
absl::flat_hash_map<std::string,
                    std::unique_ptr<WidgetWithBellsAndWhistles>>::const_iterator
    it = my_map_.find(key);
std::array<int, 6> numbers = {4, 8, 15, 16, 23, 42};
```

<div class='goodcode'></div>

```cpp
auto widget = std::make_unique<WidgetWithBellsAndWhistles>(arg1, arg2);
auto it = my_map_.find(key);
std::array numbers = {4, 8, 15, 16, 23, 42};
```

类型中有时既有有用的信息，也有样板代码，例如上面例子中的
`it`：显然它的类型是迭代器，而且在
许多上下文中，容器类型甚至键类型都无关紧要，但
值的类型大概是有用的。在这种情况下，往往可以
用显式类型来定义局部变量，以传达相关
信息：

<div class='goodcode'></div>

```cpp
if (auto it = my_map_.find(key); it != my_map_.end()) {
  WidgetWithBellsAndWhistles& widget = *it->second;
  // Do stuff with `widget`
}
```

如果类型是某个模板的实例，且模板参数是样板代码而模板
本身含有信息，那么可以使用类模板实参推导来
消除样板代码。不过，真正能带来明显好处的情形
相当罕见。请注意，类模板实参推导
还要遵守一条[单独的风格规则](#CTAD)。

对于类似 `map` 的容器，为其元素写出显式类型很容易出错。
在这种情况下，针对键和值使用[结构化绑定](#Structured_Bindings)
几乎总是比用单个变量表示那个 pair 更清晰。

如果有更简单的方案可用，就不要使用 `decltype(auto)`；因为它是
一个相当冷僻的特性，会严重损害代码的清晰度。

关于何时在变量声明中使用 `auto` 的更多细节，
请参阅 [TotW #232](https://abseil.io/tips/232)。

###### 返回类型推导

仅当函数体中的 `return` 语句数量很少、且几乎没有其他代码时，
才使用返回类型推导（对函数和 lambda 一视同仁），
否则读者可能无法一眼看出返回
类型是什么。此外，仅当函数或 lambda 的作用域非常
狭窄时才使用它，因为带有推导返回类型的函数并不定义抽象
边界：实现*就是*接口。特别是，头文件中的公开
函数几乎绝不应使用推导返回类型。

###### 函数参数类型推导

如果可以为参数指定具体的类型，就应避免使用参数类型推导
（无论是使用 `auto` 还是模板
参数）。如果它只会被一种类型调用，那么几乎总是把该类型
显式写出更清晰，除非调用点就在其定义处附近（以便
读者能轻易同时看到两者），或者它是被传给一个
广为人知的接口的 lambda，以至于它最终会以何种类型被调用
一目了然（例如上面的 `std::sort` 示例）

不要在非 lambda 函数中使用 `auto` 参数。请改用具名的模板
参数，因为它们更明确地表明该函数
是一个模板：

<div class='badcode'></div>

```cpp
void F(auto arg) { ... }
```

<div class='goodcode'></div>

```cpp
template <typename T>
void F(T arg) { ... }
```

在 lambda 表达式中，如果需要引用某个参数的类型，请优先
把该类型作为模板参数：

<div class='badcode'></div>

```cpp
[](auto x) { decltype(x) y; ... }
```

<div class='goodcode'></div>

```cpp
[]<typename T>(T x) { T y; ... }
```

###### Lambda 初始化捕获

初始化捕获由一条[更具体的风格规则](#Lambda_expressions)规定，
该规则在很大程度上取代了类型推导的通用规则。

<a id="Structured_Bindings"></a>

###### 结构化绑定

与其他形式的类型推导不同，结构化绑定通过为较大对象的各元素
赋予有意义的名称，实际上能向读者提供
额外的信息。这意味着，结构化绑定声明可能带来
相对于显式类型的净可读性提升，即便在 `auto` 无法奏效的
情形下也是如此。当对象是 pair 或 tuple 时（如上面的 `insert` 示例），
结构化绑定尤其有益，因为它们本来就没有
有意义的字段名，但请注意，除非 `insert` 之类的既有 API
[迫使你使用 pair 或 tuple](#Structs_vs._Tuples)，否则通常
不应使用它们。

类似 `std::map<K, V>` 这类容器的元素尤其能从
结构化绑定中受益；不仅 pair 的两个部分可以取更
贴切的名称，而且使用类型推导还避开了常见的错误：忘记给元素的
键类型加上 `const` 限定，而它往往出人意料地
仍能通过编译，只是引入了非预期的拷贝。

如果被绑定的对象是结构体，有时为各元素取更贴合
你的用途的名称会有帮助，但请记住，这也可能
意味着这些名称对读者而言不如字段名那么容易辨认。
如果绑定的名称与底层字段名不一致，我们建议
用注释注明底层字段名，所用语法与函数
参数注释相同：

<div class='goodcode'></div>

```cpp
auto [/*field_name1=*/bound_name1, /*field_name2=*/bound_name2] = ...
```

与函数参数注释一样，这能让工具检测出你是否
把字段的顺序弄错了。

<a id="CTAD"></a>

### 类模板实参推导

只对明确选择支持类模板实参推导的模板
使用类模板实参推导。

##### 定义

[类模板实参推导](https://en.cppreference.com/w/cpp/language/class_template_argument_deduction)
（通常缩写为 "CTAD"）发生在：声明变量时所用的类型
指名了某个模板，却没有提供模板实参列表（连空的
尖括号都没有）：

<div class='neutralcode'></div>

```cpp
std::array a = {1, 2, 3};  // `a` is a std::array<int, 3>
```

编译器使用模板的「推导指引」从初始化器推导出实参，
这些推导指引可以是显式的，也可以是隐式的。

显式推导指引看起来像带有尾置返回类型的函数声明，
只是没有开头的 `auto`，而且函数名就是
模板名。例如，上面的例子依赖 `std::array` 的
下面这条推导指引：

<div class='neutralcode'></div>

```cpp
namespace std {
template <class T, class... U>
array(T, U...) -> std::array<T, 1 + sizeof...(U)>;
}
```

主模板（相对于模板特化）中的构造函数
也会隐式地定义推导指引。

当你声明一个依赖 CTAD 的变量时，编译器会按照构造函数
重载决议的规则选出一条推导指引，而该
指引的返回类型就成为该变量的类型。

##### 优点

CTAD 有时能让你省去代码中的样板代码。

##### 缺点

由构造函数隐式生成的推导指引可能具有
不合预期的行为，甚至完全错误。对于那些在 C++17 引入 CTAD
之前编写的构造函数，这个问题尤其突出，因为
这些构造函数的作者根本无从知晓（更谈不上修正）
其构造函数会给 CTAD 带来哪些问题。此外，添加
显式推导指引来修复这些问题，又可能破坏任何
依赖隐式推导指引的既有代码。

CTAD 还带有许多与 `auto` 相同的缺点，因为二者
都是从初始化器推导变量类型的全部或部分的机制。
CTAD 确实比 `auto` 给读者提供了更多信息，但它
也没有给出「信息被省略了」这一明显提示。

##### 结论

除非某个模板的维护者通过提供至少一条显式推导指引
明确选择支持 CTAD，否则不要对该模板使用 CTAD
（`std` 命名空间中的所有模板也被视为已选择支持）。
如果编译器提供了相应的警告，应当用该警告来强制这一点。

CTAD 的使用还必须遵循关于
[类型推导](#Type_deduction) 的通用规则。

<a id="Designated_initializers"></a>

### 指定初始化器

只使用符合 C++20 标准形式的指定初始化器。

##### 定义

[指定初始化器](https://en.cppreference.com/w/cpp/language/aggregate_initialization#Designated_initializers)
是一种通过显式命名字段来初始化
聚合体（「朴素的结构体」）的语法：

<div class='neutralcode'></div>

```cpp
struct Point {
  float x = 0.0;
  float y = 0.0;
  float z = 0.0;
};

Point p = {
  .x = 1.0,
  .y = 2.0,
  // z will be 0.0
};
```

显式列出的字段将按指定方式初始化，其余字段
则以传统聚合初始化表达式（如 `Point{1.0, 2.0}`）中
相同的方式初始化。

##### 优点

指定初始化器可以带来方便且高度可读的聚合
表达式，尤其适用于字段顺序不如上面 `Point` 示例
那样直观的结构体。

##### 缺点

虽然指定初始化器长期以来一直是 C 标准的一部分，
并作为扩展被 C++ 编译器所支持，但在 C++20 之前，
C++ 并不支持它们。

C++ 标准中的规则比 C 及编译器扩展更严格，要求指定初始化器
的出现顺序与字段在结构体定义中出现的顺序一致。
因此在上面的例子中，按 C++20 先初始化 `x` 再初始化 `z`
是合法的，但先 `y` 后 `x` 则不合法。

##### 结论

只使用与 C++20 标准兼容形式的指定初始化器：
初始化器的顺序与相应字段在结构体定义中
出现的顺序一致。

<a id="Lambda_expressions"></a>

### Lambda 表达式

在适当的地方使用 lambda 表达式。当 lambda 会逃出当前作用域时，
请优先使用显式捕获。

##### 定义

lambda 表达式是一种创建匿名函数对象的简洁方式。
在把函数作为参数传递时，它们往往很有用。例如：

<div class='neutralcode'></div>

```cpp
std::sort(v.begin(), v.end(), [](int x, int y) {
  return Weight(x) < Weight(y);
});
```

它们还允许从外围作用域捕获变量，既可以
按名称显式捕获，也可以使用默认捕获隐式捕获。显式捕获
要求把每个变量都列出来，并指定为按值捕获或按引用捕获：

<div class='neutralcode'></div>

```cpp
int weight = 3;
int sum = 0;
// Captures `weight` by value and `sum` by reference.
std::for_each(v.begin(), v.end(), [weight, &sum](int x) {
  sum += weight * x;
});
```

默认捕获会隐式捕获 lambda 体中引用的任何变量，
若使用了任何成员，还会连 `this` 一起捕获：

<div class='neutralcode'></div>

```cpp
const std::vector<int> lookup_table = ...;
std::vector<int> indices = ...;
// Captures `lookup_table` by reference, sorts `indices` by the value
// of the associated element in `lookup_table`.
std::sort(indices.begin(), indices.end(), [&](int a, int b) {
  return lookup_table[a] < lookup_table[b];
});
```

变量捕获也可以带有显式的初始化器，可用于
按值捕获只能移动的变量，或用于普通的
引用捕获或值捕获无法处理的其他情形：

<div class='neutralcode'></div>

```cpp
std::unique_ptr<Foo> foo = ...;
[foo = std::move(foo)] () {
  ...
}
```

这类捕获（常称为「初始化捕获」或「广义 lambda 捕获」）
并不一定真的「捕获」外围作用域中的任何东西，甚至
不必拥有来自外围作用域的名称；这种语法是定义
lambda 对象成员的一种完全通用的方式：

<div class='neutralcode'></div>

```cpp
[foo = std::vector<int>({1, 2, 3})] () {
  ...
}
```

带有初始化器的捕获，其类型按照与
`auto` 相同的规则推导。

##### 优点

*   lambda 比定义函数对象以传给 STL 算法的其他方式
    简洁得多，这可能提升可读性。
*   恰当地使用默认捕获可以消除冗余，并突出
    与默认情况不同的重要例外。
*   lambda、`std::function` 和 `std::bind` 可以组合起来作为
    通用的回调机制；它们让编写以绑定函数为
    参数的函数变得容易。

##### 缺点

*   lambda 中的变量捕获可能成为悬垂指针错误的来源，
    尤其当 lambda 逃出当前作用域时。
*   按值默认捕获可能具有误导性，因为它并不能防止
    悬垂指针错误。按值捕获指针并不会产生深
    拷贝，因此它常常与按引用捕获有着相同的生命周期问题。
    在按值捕获 `this` 时尤其令人困惑，因为
    `this` 的使用往往是隐式的。
*   捕获实际上声明了新的变量（无论捕获是否带有
    初始化器），但它们看起来完全不像 C++ 中任何其他变量声明
    语法。特别是，没有位置写明变量的类型，甚至
    连 `auto` 占位符都没有（尽管初始化捕获可以通过
    类型转换等方式间接表明）。这甚至会让人难以认出
    它们是声明。
*   初始化捕获本质上依赖[类型推导](#Type_deduction)，并且
    带有许多与 `auto` 相同的缺点，此外还有
    一个问题：其语法甚至不会提示读者
    正在发生推导。
*   对 lambda 的使用可能失控；非常长的嵌套
    匿名函数会让代码更难理解。

##### 结论

*   在适当的地方使用 lambda 表达式，并采用
    [下文](#Formatting_Lambda_Expressions)所述的格式。
*   如果 lambda 可能逃出当前作用域，请优先使用显式捕获。
    例如，不要这样写：

    <div class='badcode'></div>

    ```cpp
    {
      Foo foo;
      ...
      executor->Schedule([&] { Frobnicate(foo); })
      ...
    }
    // BAD! The fact that the lambda makes use of a reference to `foo` and
    // possibly `this` (if `Frobnicate` is a member function) may not be
    // apparent on a cursory inspection. If the lambda is invoked after
    // the function returns, that would be bad, because both `foo`
    // and the enclosing object could have been destroyed.
    ```

    而应写成：

    <div class='goodcode'></div>

    ```cpp
    {
      Foo foo;
      ...
      executor->Schedule([&foo] { Frobnicate(foo); })
      ...
    }
    // BETTER - The compile will fail if `Frobnicate` is a member
    // function, and it's clearer that `foo` is dangerously captured by
    // reference.
    ```

*   仅当 lambda 的生命周期明显短于任何潜在捕获对象时，
    才使用按引用默认捕获（`[&]`）。

*   仅把按值默认捕获（`[=]`）用作给短小 lambda 绑定少数
    变量的手段，且要求所捕获变量的集合一眼
    就能看出，并且不会导致隐式捕获 `this`。（这
    意味着，出现在非静态类成员函数中、且在其函数体内
    引用了非静态类成员的 lambda，必须显式捕获 `this`
    或通过 `[&]` 捕获。）不要编写带有
    按值默认捕获的长 lambda 或复杂 lambda。

*   捕获只用于真正从外围作用域捕获变量。
    不要使用带有初始化器的捕获来引入新名称，或
    大幅改变既有名称的含义。请改用常规方式
    声明一个新变量，然后再捕获它，或者不用 lambda
    简写，显式定义一个函数对象。

*   关于指定参数类型和返回类型的指导，
    请参阅[类型推导](#Type_deduction)一节。

<a id="Template_metaprogramming"></a>

### 模板元编程

避免复杂的模板编程。

##### 定义

模板元编程指的是一族技术，它们利用 C++ 模板
实例化机制是图灵完备的这一事实，可在类型域中
执行任意的编译时计算。

##### 优点

模板元编程能够实现极其灵活、类型安全且
高性能的接口。诸如
[GoogleTest](https://github.com/google/googletest)、`std::tuple`、
`std::function` 和 Boost.Spirit 之类的设施，若没有它便不可能实现。

##### 缺点

模板元编程所使用的技术，除语言专家之外往往
无人能懂。以复杂方式使用模板的代码常常
难以阅读，也难以调试或维护。

模板元编程常常导致极其糟糕的编译时错误
消息：即便接口很简单，一旦用户用错，复杂的实现细节
就会暴露出来。

模板元编程会妨碍大规模重构，因为它让
重构工具的工作变得更难。首先，模板代码会在
多个上下文中展开，很难验证转换在
所有这些上下文中都合理。其次，某些重构工具使用的 AST
只表示模板展开之后的代码结构。因此可能
难以自动回溯到需要改写的
原始源码构造。

##### 结论

模板元编程有时能带来比不用它时更干净、更易用的
接口，但它也常常诱使人过于卖弄技巧。最适合
用于少数底层组件，让额外的
维护负担分摊到大量的使用之上。

在使用模板元编程或其他复杂的模板
技术之前请三思；想一想团队中的普通成员在你转到
另一个项目之后，是否还能充分理解你的代码并加以
维护，或者一个非 C++ 程序员、或随意浏览
代码库的人，是否能看懂错误信息、或追踪
他们想调用的函数的执行流程。如果你正在使用递归模板实例化、
类型列表、元函数或表达式模板，或者依赖 SFINAE、或依赖
`sizeof` 技巧来检测函数重载决议，那么
很可能你已经走得太远了。

如果使用模板元编程，你应当预期要付出相当大的
努力来尽量降低并隔离复杂性。应当尽可能把
元编程隐藏为实现细节，使
面向用户的头文件保持可读，并应确保棘手的代码
得到特别充分的注释。应当仔细记录代码的用法，
并说明「生成的」代码大致是什么样子。请格外
留意用户出错时编译器给出的
错误信息。错误信息是用户界面的一部分，你的代码
应作必要的调整，使错误信息从用户角度
易于理解且可据此采取行动。

<a id="Concepts"></a>

### 概念与约束

谨慎使用概念。一般而言，概念与约束只应
用在 C++20 之前本会使用模板的场合。避免在头文件中引入
新的概念，除非这些头文件被标记为库内部使用。
不要定义编译器无法强制实施的概念。优先
使用约束而非模板元编程，并避免使用 `template<Concept T>`
语法；请改用 `requires(Concept<T>)` 语法。

##### 定义

`concept` 关键字是一种新机制，用于为模板参数定义
需求（例如类型特征或接口规格）。
`requires` 关键字提供了在模板上放置匿名约束、
并在编译时验证约束是否得到满足的机制。概念与
约束常常一起使用，但也可以各自独立使用。

##### 优点

*   涉及模板时，概念能让编译器生成好得多的
    错误信息，从而减少困惑并显著改善
    开发体验。
*   概念可以减少定义和使用编译时约束所需的
    样板代码，往往能提升最终
    代码的清晰度。
*   约束提供了一些用模板和 SFINAE 技术
    难以实现的能力。

##### 缺点

*   与模板一样，概念会让代码显著更复杂、
    更难理解。
*   概念的语法可能令读者困惑，因为在使用处
    概念看起来与类类型相似。
*   概念，尤其是在 API 边界处，会增加代码
    耦合、僵化与固化。
*   概念与约束可能复制函数体中的逻辑，造成
    代码重复并增加维护成本。
*   概念会模糊其底层契约的事实来源，因为它们
    是可被用于多个位置的独立命名实体，
    而这些位置彼此独立地演化。这会导致
    明示的需求与隐含的需求随时间产生分歧。
*   概念与约束以新颖且不明显的方式
    影响重载决议。
*   与 SFINAE 一样，约束使大规模重构代码变得更难。

##### 结论

当存在等价的标准库预定义概念时，应优先使用它们，
而不是类型特征。（例如，若在 C++20 之前会使用
`std::is_integral_v`，那么在 C++20 代码中就应使用
`std::integral`。）同样，应优先使用现代约束语法
（通过 `requires(Condition)`），并避免使用遗留的
模板元编程构造（如 `std::enable_if<Condition>`）与 `template<Concept T>` 语法。

不要手动重新实现任何已有的概念或特征。例如，请使用
`requires(std::default_initializable<T>)` 而不是
`requires(requires { T v; })` 或类似写法。

新的 `concept` 声明应当很少，且只在库内部定义，
使其不暴露在 API 边界上。更一般地说，在 C++17 中
不会使用其遗留模板等价物的场合，不要
使用概念或约束。

不要定义那些重复函数体，或施加从代码正文
或所产生的错误信息中即可看出无关紧要或显而易见的
要求的概念。例如，请避免以下写法：

<div class='badcode'></div>

```cpp
template <typename T>     // Bad - redundant with negligible benefit
concept Addable = std::copyable<T> && requires(T a, T b) { a + b; };
template <Addable T>
T Add(T x, T y, T z) { return x + y + z; }
```

相反，除非你能证明概念或约束在该特定情形下
带来了显著改善，例如在深层嵌套或
不明显的需求所产生的错误信息中，否则请优先
把代码留作普通模板。

概念应当能由编译器静态验证。不要使用任何
主要收益来自语义（或其他无法强制实施的）
约束的概念。在编译时无法强制实施的要求，
应改用注释、断言或测试等其他机制来施加。

<a id="modules"></a>

### C++20 模块

不要使用 C++20 模块。

C++20 引入了「模块」这一新的语言特性，旨在替代
对头文件的文本式包含。它引入了三个新的关键字来
提供支持：`module`、`export` 和 `import`。

模块是 C++ 编写与编译方式的一次重大转变，我们
仍在评估它们未来如何融入 Google 的 C++ 生态。
此外，我们的构建系统、编译器及其他工具目前
对它们的支持尚不充分，在编写和使用模块的
最佳实践方面还需要进一步探索。

<a id="coroutines"></a>

### 协程

只通过经项目负责人批准的库来使用 C++20
协程。

##### 定义

C++20 引入了
[协程](https://en.cppreference.com/w/cpp/language/coroutines.html)：
即可以暂停并在之后恢复执行的函数。它们在
异步编程中尤其方便，相比传统的基于回调的框架
能带来显著改进。

与大多数其他编程语言（Kotlin、Rust、TypeScript 等）不同，
C++ 并不提供协程的具体实现。相反，它要求
用户实现自己的可等待类型（借助一个
[promise 类型](https://en.cppreference.com/w/cpp/language/coroutines#Promise)），
由该类型决定协程的参数类型、协程的执行方式，并
允许在协程执行的各个阶段运行用户自定义代码。

##### 优点

*   协程可用于实现安全而高效、适合
    特定任务的库，例如异步编程。
*   协程在语法上几乎与非协程函数完全相同，
    这使它们比替代方案可读性好得多。
*   高度的可定制性使得与替代方案相比，
    可以向协程中插入更详细的调试信息。

##### 缺点

*   并不存在标准的协程 promise 类型，而且每个
    用户自定义的实现很可能在某些方面各不相同。
*   由于返回类型、promise 类型中各种
    可定制的钩子，以及编译器生成的代码之间存在
    起承托作用的交互，协程语义极难从
    阅读用户代码中推导出来。
*   协程众多可定制的方面带来了大量
    陷阱，尤其围绕悬垂引用和竞态条件。

总之，设计一个高质量且可互操作的协程库
需要大量艰巨的工作、缜密的思考和
详尽的文档。

##### 结论

只使用经项目负责人批准可在项目范围内
使用的协程库。不要自行实现 promise 或可等待类型。

<a id="Disallowed_Stdlib"></a>

### 禁用的标准库特性

某些现代 C++ 库功能会助长妨碍可读性的
编码做法——例如移除可能对读者有帮助的
受检冗余信息（如类型名称），或助长模板元编程。
另一些扩展重复了既有机制已提供的功能，
这可能导致困惑与转换成本。

##### 结论

不得使用以下 C++ 标准库特性：

*   编译期有理数（`<ratio>`），因为担心它与
    更偏重模板的接口风格绑定在一起。
*   `<cfenv>` 和 `<fenv.h>` 头文件，因为许多编译器
    并不能可靠地支持这些特性。
*   `<filesystem>` 头文件，它对测试的支持不足，
    并且存在固有的安全漏洞。

<a id="Third_party_Libraries"></a>

### 第三方库

选择使用第三方库时，请与你周围的代码
保持一致。

##### 定义

第三方库是指主要并非在与你的代码
相同的仓库中开发的库。

##### 优点

*   复用高质量的第三方库可以避免大量
    重复实现其功能的劳动。
*   有些第三方库在其问题领域中根基极深，
    避开它们反而会让代码更难读。

##### 缺点

*   第三方库可能采用与我们不同的编程实践。
    在某些情况下这可能具有「病毒式」传播性，使
    使用该库的代码更难遵循我们的风格与编程实践。
*   第三方库可能带来许多隐性的支持负担，例如
    许可证合规、漏洞监控与修补，以及应对
    上游的破坏性变更。

##### 结论

为解决某个特定问题而选择库时，请先检查
你的代码库是否已有通常用于该类问题的库。
若有，就使用它。若没有，请按大致
递减的优先级顺序，优先选用以下来源的库：

*   [Abseil](https://abseil.io/) .
*   C++ 标准库（[此处](#Disallowed_Stdlib)所讨论的情形除外）
*   代码库中已有的第一方库。
*   第三方库

如果你选择使用第三方库，请务必遵循你的代码库
关于第三方代码的政策。

<a id="Nonstandard_Extensions"></a>

### 非标准扩展

除非另有规定，不得使用 C++ 的非标准扩展。

##### 定义

编译器支持各种不属于标准 C++ 的扩展。这类
扩展包括 GCC 的 `__attribute__`、内建函数（如
`__builtin_prefetch` 或 SIMD）、`#pragma`、内联汇编、`__COUNTER__`、
`__PRETTY_FUNCTION__`、复合语句表达式（例如，
`foo = ({ int x; Bar(&x); x })`、变长数组与 `alloca()`，以及
「[Elvis 运算符](https://en.wikipedia.org/wiki/Elvis_operator)」`a?:b`。

##### 优点

*   非标准扩展可能提供标准 C++ 中不存在
    的有用特性。
*   给编译器的重要性能指导只能
    通过扩展来指定。

##### 缺点

*   非标准扩展并非在所有编译器中都能工作。使用
    非标准扩展会降低代码的可移植性。
*   即便所有目标编译器都支持它们，这些扩展
    往往也缺乏良好规约，不同编译器之间
    可能存在细微的行为差异。
*   非标准扩展给语言增加了读者必须了解
    才能读懂代码的特性。
*   非标准扩展需要额外的工作才能跨架构移植。

##### 结论

不要使用非标准扩展。你可以使用借助非标准扩展
实现的可移植性包装器，前提是这些包装器
由指定的项目级可移植性头文件提供。

<a id="Aliases"></a>

### 别名

公开别名是为了 API 使用者的利益而设，应当
有清晰的文档。

##### 定义

有多种方式可以创建作为其他实体别名的名称：

<div class='neutralcode'></div>

```cpp
using Bar = Foo;
typedef Foo Bar;  // But prefer `using` in C++ code.
using ::other_namespace::Foo;
using enum MyEnumType;  // Creates aliases for all enumerators in MyEnumType.
```

在新代码中，`using` 比 `typedef` 更可取，因为它
与 C++ 其余部分提供了更一致的语法，并且能与模板配合。

与其他声明一样，在头文件中声明的别名属于该
头文件的公开 API，除非它们位于函数定义中、类的
私有部分，或显式标记的内部命名空间中。位于
这些区域或 `.cc` 文件中的别名属于实现细节（因为客户代码
无法引用它们），不受本规则限制。

##### 优点

*   别名可以通过简化冗长或复杂的名称来提升可读性。
*   别名可以通过在一处为 API 中反复使用的类型命名
    来减少重复，这*或许*能让日后更改该类型更容易。

##### 缺点

*   当别名放在客户代码可引用的头文件中时，它们
    会增加该头文件 API 中的实体数量，从而提高其
    复杂度。
*   客户很容易依赖公开别名中非预期的细节，
    使改动变得困难。
*   人们可能忍不住创建一个只打算用于实现的
    公开别名，却没有考虑它对 API 或
    可维护性的影响。
*   别名可能带来名称冲突的风险。
*   别名可能因为给熟悉的结构起了陌生的
    名字而降低可读性。
*   类型别名可能造成不清晰的 API 契约：无法
    确定该别名是保证与其所别名类型完全相同、
    具有相同的 API，还是仅能在指定的狭窄情形下使用。

##### 结论

不要仅仅为了在实现中少打字就把别名放进公开 API；
只有当你打算让客户使用它时才这样做。

定义公开别名时，请记录新名称的意图，包括
它是否保证始终与当前所别名的类型相同，
还是只打算提供较为有限的兼容性。这让
使用者知道能否把这些类型视为可互换，或者是否
必须遵循更具体的规则，并有助于实现保留
一定的自由度来更改该别名。

不要把命名空间别名放进公开 API。（另见
[命名空间](#Namespaces)。）

例如，以下别名记录了它们打算在客户
代码中如何被使用：

<div class='goodcode'></div>

```cpp
namespace mynamespace {
// Used to store field measurements. DataPoint may change from Bar* to some internal type.
// Client code should treat it as an opaque pointer.
using DataPoint = ::foo::Bar*;

// A set of measurements. Just an alias for user convenience.
using TimeSeries = std::unordered_set<DataPoint, std::hash<DataPoint>, DataPointComparator>;
}  // namespace mynamespace
```

以下别名没有记录预期用途，而且其中一半
并不打算供客户使用：

<div class='badcode'></div>

```cpp
namespace mynamespace {
// Bad: none of these say how they should be used.
using DataPoint = ::foo::Bar*;
using ::std::unordered_set;  // Bad: just for local convenience
using ::std::hash;           // Bad: just for local convenience
typedef unordered_set<DataPoint, hash<DataPoint>, DataPointComparator> TimeSeries;
}  // namespace mynamespace
```

不过，在函数定义、类的 `private` 部分、显式标记的内部
命名空间以及 `.cc` 文件中，为局部方便而设的别名是可以的：

<div class='goodcode'></div>

```cpp
// In a .cc file
using ::foo::Bar;
```

<a id="Switch_Statements"></a>

### switch 语句

如果不是以枚举值为条件，switch 语句应始终
带有 `default` 分支（对于枚举值，若有任何
取值未处理，编译器会给出警告）。如果 default 分支
绝不应执行，请将其视为错误。例如：

<div class='goodcode'></div>

```cpp
switch (var) {
  case 0: {
    ...
    break;
  }
  case 1: {
    ...
    break;
  }
  default: {
    LOG(FATAL) << "Invalid value in switch statement: " << var;
  }
}
```

从一个 case 标签贯穿到另一个必须使用
`[[fallthrough]];` 属性加以注解。`[[fallthrough]];` 应放在
执行流程中确实会贯穿到下一个 case 标签的位置。
一个常见的例外是连续的 case 标签之间没有代码，
此时无需注解。

<div class='goodcode'></div>

```cpp
switch (x) {
  case 41:  // No annotation needed here.
  case 43:
    if (dont_be_picky) {
      // Use this instead of or along with annotations in comments.
      [[fallthrough]];
    } else {
      CloseButNoCigar();
      break;
    }
  case 42:
    DoSomethingSpecial();
    [[fallthrough]];
  default:
    DoSomethingGeneric();
    break;
}
```

<a id="Inclusive_Language"></a>

## 包容性语言

在所有代码中，包括命名和注释，请使用包容性语言，
避免使用其他程序员可能觉得不尊重或冒犯的词语
（例如 "master" 与 "slave"、"blacklist" 与 "whitelist"，
或 "redline"），即便这些词也有表面中性的含义。
同样，请使用性别中立的语言，除非你指的是
某个特定的人（并使用其代词）。例如，对性别
未指明的人使用 "they"/"them"/"their"
（[即便用作单数](https://apastyle.apa.org/style-grammar-guidelines/grammar/singular-they)），
对软件、计算机及其他非人的事物则使用 "it"/"its"。

<a id="Naming"></a>

## 命名

最重要的一致性规则是那些约束命名的规则。
一个名称的风格能立刻告诉我们被命名的实体
是何种东西：类型、变量、函数、常量、宏等，
而不必去搜索该实体的声明。我们大脑中的
模式匹配机制在很大程度上依赖这些命名规则。

关于命名的风格规则相当武断，但我们认为在这一
领域一致性比个人偏好更重要，因此无论
你是否觉得它们合理，规则就是规则。

就下述命名规则而言，「单词」指的是你用英文
书写时内部不含空格的任何字符串。要么所有
单词全部小写，单词之间用下划线分隔
（「[snake_case](https://en.wikipedia.org/wiki/Snake_case)」），
要么采用混合大小写，每个单词的首字母大写
（「[camelCase](https://en.wikipedia.org/wiki/Camel_case)」或
「[PascalCase](https://en.wiktionary.org/wiki/Pascal_case)」）。

<a id="General_Naming_Rules"></a>

### 选择名称

给事物起的名称应让新读者能理解其用途或
意图，即便这位读者与所有者不在同一团队。
不必担心节省横向空间，因为让新读者
立刻看懂你的代码要重要得多。

请考虑名称将被使用的上下文。即便
名称在远离使其可用的代码之处被使用，也应
具有描述性。不过，名称不应通过重复
紧邻上下文中已有的信息来分散读者的注意力。
一般而言，这意味着描述性应与名称的可见作用域
相称。头文件中声明的自由函数或许应提及该头文件
所属的库，而局部变量则不必说明它位于哪个函数中。

尽量少用项目之外的人可能不认识的缩写
（尤其是首字母缩略词与首字母缩写）。不要通过
删除单词内部的字母来缩写。使用缩写时，请优先把
它当作单个「单词」来大写，例如用 `StartRpc()`
而非 `StartRPC()`。经验法则是：若某缩写被
Wikipedia 收录，大概就没问题。请注意，某些
众所周知的缩写是可以的，例如循环索引用 `i`、模板参数用 `T`。

你最常看到的名称与大多数名称不同；少数
「词汇表」名称复用得极广，始终处于上下文中。
这些名称往往很短甚至经过缩写，其完整含义
来自明确的长篇文档，而不只是定义处的
注释与名称中的单词。例如，`absl::Status` 在
[开发者指南中有专门页面](https://abseil.io/docs/cpp/guides/status)，
记录其正确用法。你大概不会经常定义新的
词汇表名称，但若真要定义，请获取额外的设计
评审，以确保所选名称在被广泛使用时表现良好。

<div class='goodcode'></div>

```cpp
class MyClass {
 public:
  int CountFooErrors(const std::vector<Foo>& foos) {
    int n = 0;  // Clear meaning given limited scope and context
    for (const auto& foo : foos) {
      ...
      ++n;
    }
    return n;
  }
  // Function comment doesn't need to explain that this returns non-OK on
  // failure as that is implied by the `absl::Status` return type, but it
  // might document behavior for some specific codes.
  absl::Status DoSomethingImportant() {
    std::string fqdn = ...;  // Well-known abbreviation for Fully Qualified Domain Name
    return absl::OkStatus();
  }
 private:
  const int kMaxAllowedConnections = ...;  // Clear meaning within context
};
```

<div class='badcode'></div>

```cpp
class MyClass {
 public:
  int CountFooErrors(const std::vector<Foo>& foos) {
    int total_number_of_foo_errors = 0;  // Overly verbose given limited scope and context
    for (int foo_index = 0; foo_index < foos.size(); ++foo_index) {  // Use idiomatic `i`
      ...
      ++total_number_of_foo_errors;
    }
    return total_number_of_foo_errors;
  }
  // A return type with a generic name is unclear without widespread education.
  Result DoSomethingImportant() {
    int cstmr_id = ...;  // Deletes internal letters
  }
 private:
  const int kNum = ...;  // Unclear meaning within broad scope
};
```

<a id="File_Names"></a>

### 文件名

文件名应全部小写，可以包含下划线（`_`）或连字符
（`-`）。请遵循你的项目所使用的惯例。如果没有
可遵循的一致本地惯例，请优先使用「`_`」。

可接受的文件名示例：

*   `my_useful_class.cc`
*   `my-useful-class.cc`
*   `myusefulclass.cc`
*   `myusefulclass_test.cc // _unittest and _regtest are deprecated.`

C++ 文件应使用 `.cc` 扩展名，头文件应使用
`.h` 扩展名。依赖于在特定位置被文本式包含的文件
应以 `.inc` 结尾（另见关于
[自包含的头文件](#Self_contained_Headers)一节）。

不要使用 `/usr/include` 中已存在的文件名，例如 `db.h`。

一般来说，让文件名非常具体。例如，使用
`http_server_logs.h` 而非 `logs.h`。一种很常见的情况是
有一对文件，例如 `foo_bar.h` 和 `foo_bar.cc`，
共同定义一个名为 `FooBar` 的类。

<a id="Type_Names"></a>

### 类型名称

类型名称以大写字母开头，每个新单词首字母大写，
不使用下划线：`MyExcitingClass`、`MyExcitingEnum`。

所有类型的名称——类、结构体、类型别名、枚举，以及类型
模板参数——都遵循相同的命名约定。类型名称应
以大写字母开头，每个新单词的首字母大写。
不要使用下划线。例如：

<div class='goodcode'></div>

```cpp
// classes and structs
class UrlTable { ...
class UrlTableTester { ...
struct UrlTableProperties { ...

// typedefs
typedef hash_map<UrlTableProperties*, std::string> PropertiesMap;

// using aliases
using PropertiesMap = hash_map<UrlTableProperties*, std::string>;

// enums
enum class UrlTableError { ...
```

<a id="Concept_Names"></a>

### 概念名称

概念名称遵循与[类型名称](#Type_Names)相同的规则。

<a id="Variable_Names"></a>

### 变量名称

变量（包括函数参数）和数据成员的名称采用
`snake_case`（全部小写，单词之间用下划线分隔）。
类（而非结构体）的数据成员还额外带有尾随
下划线。例如：`a_local_variable`、`a_struct_data_member`、`a_class_data_member_`。

#### 常见变量名称

例如：

<div class='goodcode'></div>

```cpp
std::string table_name;  // OK - snake_case.
```

<div class='badcode'></div>

```cpp
std::string tableName;   // Bad - mixed case.
```

#### 类的数据成员

类的数据成员，无论静态还是非静态，都像
普通的非成员变量那样命名，但要带尾随下划线。
例外是静态常量类成员，它们应遵循
[常量命名](#Constant_Names)的规则。

<div class='goodcode'></div>

```cpp
class TableInfo {
 public:
  ...
  static const int kTableVersion = 3;  // OK - constant naming.
  ...

 private:
  std::string table_name_;             // OK - underscore at end.
  static Pool<TableInfo>* absl_nullable pool_;       // OK.
};
```

#### 结构体的数据成员

结构体的数据成员，无论静态还是非静态，都像
普通的非成员变量那样命名。它们不带类中
数据成员所具有的尾随下划线。

<div class='goodcode'></div>

```cpp
struct UrlTableProperties {
  std::string name;
  int num_entries;
  static Pool<UrlTableProperties>* absl_nullable pool;
};
```

关于何时使用结构体、何时使用类的讨论，
请参见[结构体与类](#Structs_vs._Classes)。

<a id="Constant_Names"></a>

### 常量名称

声明为 `constexpr` 或 `const`、且其值在程序
运行期间固定不变的变量，以带前导 "k" 的
混合大小写形式命名。在极少数无法用大小写
分隔单词的情况下，可用下划线作分隔符。例如：

<div class='goodcode'></div>

```cpp
const int kDaysInAWeek = 7;
const int kAndroid8_0_0 = 24;  // Android 8.0.0
```

所有具备
[静态存储期](http://en.cppreference.com/w/cpp/language/storage_duration#Storage_duration)
的此类变量都应以这种方式命名，包括静态常量类
数据成员，以及模板中不同实例可能具有
不同值的变量。例如：

<div class='goodcode'></div>

```cpp
template <int kMaxAttempts>
class ExponentialBackoff final {
  static constexpr absl::string_view kLogTag = "exponential backoff";
  ...
};
```

对于其他存储类别的变量，例如自动变量，
此约定是可选的；否则适用通常的变量命名规则。

例如：

<div class='goodcode'></div>

```cpp
void ComputeFoo(absl::string_view suffix) {
  // Either of these is acceptable.
  const absl::string_view kPrefix = "prefix";
  const absl::string_view prefix = "prefix";
  ...
}
```

<div class='badcode'></div>

```cpp
void ComputeFoo(absl::string_view suffix) {
  // Bad - different invocations of ComputeFoo give kCombined different values.
  const std::string kCombined = absl::StrCat(kPrefix, suffix);
  ...
}
```

<a id="Function_Names"></a>

### 函数名称

通常，函数遵循
[PascalCase](https://en.wiktionary.org/wiki/Pascal_case)：
以大写字母开头，每个新单词的首字母大写。

<div class='goodcode'></div>

```cpp
AddTableEntry()
DeleteUrl()
OpenFileOrDie()
```

同样的命名规则也适用于作为 API 一部分
暴露、且意图看起来像函数的类和命名空间作用域
常量，因为它们是对象而非函数这一事实
属于无关紧要的实现细节。

访问器和修改器（get 与 set 函数）可以像变量
那样以 `snake_case` 命名。它们往往对应实际的
成员变量，但并非必须。例如 `int count()` 和 `void set_count(int count)`。

<a id="Namespace_Names"></a>

### 命名空间名称

命名空间名称采用 `snake_case`（全部小写，
单词之间用下划线分隔）。

为命名空间[选择名称](#General_Naming_Rules)时，请注意，
在命名空间之外的头文件中使用名称时必须
使用完全限定名，因为[无限定别名通常被禁止](#Aliases)。

顶层命名空间必须全局唯一且易于辨认，因此每个
命名空间都应由单个项目或团队所有，其名称
基于该项目或团队的名称。通常，命名空间中的
所有代码都应位于一个或多个与该命名空间同名的目录下。

嵌套命名空间应避开众所周知的顶层命名空间
名称，尤其是 `std` 和 `absl`，因为在 C++ 中，
嵌套命名空间并不能防止与其他命名空间
中的名称发生冲突（参见 [TotW #130](https://abseil.io/tips/130)）。

<a id="Enumerator_Names"></a>

### 枚举值命名

枚举值（限定作用域和非限定作用域枚举皆然）的命名应类似于
[常量](#Constant_Names)，而非[宏](#Macro_Names)。也就是说，应使用
`kEnumName` 而非 `ENUM_NAME`。

<div class='goodcode'></div>

```cpp
enum class UrlTableError {
  kOk = 0,
  kOutOfMemory,
  kMalformedInput,
};
```

<div class='badcode'></div>

```cpp
enum class AlternateUrlTableError {
  OK = 0,
  OUT_OF_MEMORY = 1,
  MALFORMED_INPUT = 2,
};
```

在 2009 年 1 月之前，风格是把枚举值命名得像
[宏](#Macro_Names)一样。这导致了枚举值与宏之间的名称冲突问题，
于是作出了改用优先采用常量式命名的变更。新代码应使用
常量式命名。

<a id="Template_Parameter_Names"></a>

### 模板参数命名

模板参数应遵循其所属类别的命名风格：类型
模板参数应遵循[类型](#Type_Names)的命名规则，而
非类型模板参数应遵循[变量](#Variable_Names)或
[常量](#Constant_Names)的命名规则。

<a id="Macro_Names"></a>

### 宏命名

你不会真的要[定义宏](#Preprocessor_Macros)吧？如果
确实要定义，它们形如：
`MY_MACRO_THAT_SCARES_SMALL_CHILDREN_AND_ADULTS_ALIKE`。

请参阅[宏的说明](#Preprocessor_Macros)；一般而言宏
*不应* 使用。不过，若确实必须要用，则应以
全大写字母加下划线命名，并带有项目专属前缀。

<div class='neutralcode'></div>

```cpp
#define MYPROJECT_ROUND(x) ...
```

<a id="Naming_Aliases"></a>

### 别名

[别名](#Aliases)的名称遵循与任何其他新名称相同的原则，
只是应用在该别名被定义的上下文中，而非原始名称
出现的上下文。

<a id="Exceptions_to_Naming_Rules"></a>

### 命名规则的例外

如果你要命名的对象类似于现有的 C 或 C++ 实体（或通过
互操作引入的 Rust 实体），则可以沿用现有的命名约定
方案。

`bigopen()`
:   函数名，遵循 `open()` 的形式

`uint`
:   `typedef`

`bigpos`
:   `struct` 或 `class`，遵循 `pos` 的形式

`sparse_hash_map`
:   类似 STL 的实体；遵循 STL 的命名约定

`LONGLONG_MAX`
:   常量，如 `INT_MAX`

<a id="Comments"></a>

## 注释

注释对于保持代码的可读性绝对至关重要。以下规则
描述了应当在何处注释、注释什么。但请记住：注释固然
非常重要，最好的代码却是自文档化的。给类型和变量起
含义清晰的名字，远胜于使用晦涩的名字然后再用注释
去解释。

编写注释时，要面向你的读者：下一位需要理解你代码的
贡献者。不妨慷慨些——下一位可能就是你自己！

<a id="Comment_Style"></a>

### 注释风格

使用 `//` 或 `/* */` 语法均可，只要保持一致。

虽然两种语法都可接受，但 `//` *要常见得多*。注释方式
以及在何处使用何种风格，都应保持一致。

<a id="File_Comments"></a>

### 文件注释

每个文件都以许可证样板代码开头。

如果某个源文件（例如 `.h` 文件）声明了多个面向用户的
抽象（通用函数、相关的类，等等），请加一段注释，
描述这些抽象的集合。要包含足够的细节，让后来的
作者知道哪些内容不适合放在这里。不过，关于各个抽象
的详细文档应归属于这些抽象本身，而不是放在
文件层级。

例如，若你为 `frobber.h` 写了文件注释，就无需
在 `frobber.cc` 或 `frobber_test.cc` 中再写文件注释。另一方面，
若你在 `registered_objects.cc` 中写一组类，而它没有
对应的头文件，则必须在其中加上文件注释：
`registered_objects.cc`。

#### 法律声明与作者行

每个文件都应包含许可证样板代码。请为项目采用的
许可证选择合适的样板代码（例如 Apache 2.0、BSD、
LGPL、GPL）。

若你对带有作者行的文件作出重大修改，请考虑删除
该作者行。新文件通常不应包含版权声明或
作者行。

<a id="Class_Comments"></a>

### 结构体与类的注释

每个含义不明显的类或结构体声明都应附带一段
注释，说明其用途以及应当如何使用。

<div class='goodcode'></div>

```cpp
// Iterates over the contents of a GargantuanTable.
// Example:
//    std::unique_ptr<GargantuanTableIterator> iter = table->NewIterator();
//    for (iter->Seek("foo"); !iter->done(); iter->Next()) {
//      process(iter->key(), iter->value());
//    }
class GargantuanTableIterator {
  ...
};
```

<a id="Class_Comments_Details"></a>

#### 类注释

类注释应为读者提供足够的信息，使其了解如何以及
何时使用该类，以及正确使用该类所需的任何
额外注意事项。请记录该类所作的同步假设
（若有）。若该类的实例可被多个线程访问，
请格外注意记录围绕多线程使用的规则与
不变式。

类注释通常很适合放一小段示例代码，用来演示该类
一个简单而集中的用法。

当声明与实现充分分离时（例如 `.h` 与 `.cc` 文件），
描述该类用法的注释应与其接口定义放在一起；
关于类的操作与实现的注释应伴随该类方法的
实现。

<a id="Function_Comments"></a>

### 函数注释

声明处的注释描述函数的用法（当用法不明显时）；
函数定义处的注释描述其操作。

#### 函数声明

几乎每个函数声明都应在紧邻其前的位置附上注释，
说明该函数做什么以及如何使用。只有当函数简单而
一目了然时（例如类的显而易见属性的简单访问器），
才可省略这些注释。私有方法和在
`.cc` 文件中声明的函数也不例外。函数注释应以
*此函数* 为隐含主语，并以动词短语开头；例如
「Opens the file」，而非「Open the file」。一般而言，
这类注释并不描述函数如何完成任务。相反，这部分
应留给函数定义中的注释。

函数声明处的注释中应提及的内容类型：

*   输入和输出是什么。若函数实参名以
    \`backticks\` 形式给出，代码索引工具也许能更好地
    呈现文档。
*   对于类的成员函数：对象是否会在方法调用结束后仍
    保留引用或指针实参。这在构造函数的指针/引用
    实参中相当常见。
*   对于每个指针实参，该指针是否可能为 null。
*   对于每个可为 null 的指针实参，如何处理 null 输入。
*   对于每个输出或输入/输出实参，该实参所处的任何
    状态会发生什么（例如，状态是被追加还是被覆盖？）。
*   函数的使用方式是否存在任何性能影响。

示例如下：

<div class='goodcode'></div>

```cpp
// Returns an iterator for this table, positioned at the first entry
// lexically greater than or equal to `start_word`. If there is no
// such entry, returns a null pointer. The client must not use the
// iterator after the underlying GargantuanTable has been destroyed.
//
// This method is equivalent to:
//    std::unique_ptr<Iterator> iter = table->NewIterator();
//    iter->Seek(start_word);
//    return iter;
std::unique_ptr<Iterator> GetIterator(absl::string_view start_word) const;
```

不过，不要无谓地冗长，也不要陈述完全显而易见的内容。

为函数重写编写文档时，应聚焦于该重写本身的
细节，而不是重复被重写函数的注释。在许多这类
情况下，重写不需要额外的文档，因而也不需要
注释。

为构造函数和析构函数写注释时，请记住，读你代码的
人知道构造函数和析构函数是做什么的，因此只说
「销毁此对象」之类的注释并无用处。请记录构造函数
如何处理其参数（例如，是否取得指针的所有权），以及
析构函数会做哪些清理。若这些都很简单，就跳过
注释。析构函数没有头文件注释是相当常见的。

#### 函数定义

若函数完成其工作的方式有任何巧妙之处，函数
定义处应有解释性注释。例如，在定义处的注释中，
你可以描述所用的编码技巧、概述所经历的步骤，
或解释为何选择以此方式实现该函数，而不是采用
某个可行的替代方案。例如，你可以说明为何函数
前半部分必须获取锁，而后半部分却
不需要。

注意，你 *不应* 只是重复函数声明（在
`.h` 文件或其他任何地方）所附的注释。简要复述
函数做什么是可以的，但注释的重点应放在它如何
做到。

<a id="Variable_Comments"></a>

### 变量注释

一般而言，变量的实际名称应足够具有描述性，让人
清楚了解该变量的用途。在某些情况下，还需要
更多注释。

#### 类数据成员

每个类数据成员（也称实例变量或成员变量）的用途
都必须清楚。若存在任何未由类型和名称清楚表达的
不变式（特殊值、成员之间的关系、生命周期要求），
就必须加以注释。不过，若类型和名称已经足够
（`int num_events_;`），则无需注释。

尤其要加注释描述哨兵值（如 nullptr 或 -1）的存在
及含义（当它们并不明显时）。例如：

<div class='goodcode'></div>

```cpp
private:
 // Used to bounds-check table accesses. -1 means
 // that we don't yet know how many entries the table has.
 int num_total_entries_;
```

#### 全局变量

所有全局变量都应有一段注释，说明它们是什么、
用途是什么，以及（若不清楚）为何需要是全局的。例如：

<div class='goodcode'></div>

```cpp
// The total number of test cases that we run through in this regression test.
const int kNumTestCases = 6;
```

<a id="Implementation_Comments"></a>

### 实现注释

在实现中，应在代码里巧妙、不明显、有趣或
重要的部分加上注释。

#### 解释性注释

棘手或复杂的代码块之前应有注释。

<a id="Function_Argument_Comments"></a>

#### 函数实参注释

当某个函数实参的含义不明显时，请考虑以下
补救办法之一：

*   若该实参是字面常量，且同一常量以默认它们
    相同的方式被用于多次函数调用，则应使用
    具名常量来显式表达该约束，并
    保证其成立。
*   考虑修改函数签名，把 `bool` 实参替换为
    `enum` 实参。这会让实参值具有自描述性。
*   对于有若干配置选项的函数，考虑定义单个类或
    结构体来容纳所有选项，并传入它的一个实例。
    这种做法有若干优点。选项在调用处按名称引用，
    从而明确其含义。它还减少了函数实参的数量，
    使函数调用更易读写。另一个额外好处是，
    新增选项时，你不必改动调用处。
*   用具名变量替换庞大或复杂的嵌套
    表达式。
*   作为最后手段，在调用处用注释阐明实参
    含义。

请看下面的例子：

<div class='badcode'></div>

```cpp
// What are these arguments?
const DecimalNumber product = CalculateProduct(values, 7, false, nullptr);
```

与之相比：

<div class='goodcode'></div>

```cpp
ProductOptions options;
options.set_precision_decimals(7);
options.set_use_cache(ProductOptions::kDontUseCache);
const DecimalNumber product =
    CalculateProduct(values, options, /*completion_callback=*/nullptr);
```

<a id="Implementation_Comment_Donts"></a>

#### 禁忌

不要陈述显而易见的内容。尤其不要逐字描述代码
做了什么，除非该行为对精通 C++ 的读者而言也不明显。
相反，应提供更宏观的注释，描述代码 *为何* 做它所
做的事，或让代码具有自描述性。

比较下面这段：

<div class='badcode'></div>

```cpp
// Find the element in the vector.  <-- Bad: obvious!
if (std::find(v.begin(), v.end(), element) != v.end()) {
  Process(element);
}
```

与这一段对比：

<div class='goodcode'></div>

```cpp
// Process "element" unless it was already processed.
if (std::find(v.begin(), v.end(), element) != v.end()) {
  Process(element);
}
```

具有自描述性的代码不需要注释。上例中的注释
会显得显而易见：

<div class='goodcode'></div>

```cpp
if (!IsAlreadyProcessed(element)) {
  Process(element);
}
```

<a id="Punctuation_Spelling_and_Grammar"></a>

### 标点、拼写与语法 []() {#Punctuation,_Spelling_and_Grammar}

留意标点、拼写和语法；写得好的注释比写得糟的
注释更易阅读。

注释应像叙述性文字一样易读，大小写和标点
都要正确。很多情况下，完整句子比句子片段
更易读。较短的注释（如代码行末的注释）有时
可以不必那么正式，但应保持风格一致。

尽管被代码评审者指出「该用分号的地方用了逗号」
可能令人懊恼，但源代码保持高度的清晰与可读性
非常重要。正确的标点、拼写和语法有助于
实现这一目标。

<a id="TODO_Comments"></a>

### TODO 注释

使用 `TODO` 注释标注临时的、短期方案的，或
够用但不完美的代码。

`TODO` 应包含全大写的字符串 `TODO`，后跟 bug ID、
姓名、电子邮件地址，或对该问题掌握最充分背景的
人员或议题的其他标识符，该问题由 `TODO` 引用。
主要目的是形成一致的、可被搜索到的 `TODO`，以便
按要求查到更多细节。`TODO` 并不表示被提及的人
承诺会修复该问题。因此，创建带姓名的 `TODO` 时，
给出的几乎总是你自己的名字。

<div class='goodcode'></div>

```cpp
// TODO(bug 12345): remove the "Last visitors" feature.
// TODO(example.com/my-design-doc): Manually fix up this code the next time it's touched.
// TODO(user@example.com): Use a "*" here for concatenation operator.
// TODO(username): change this to use relations.
```

若你的 `TODO` 形如「将来某日做某事」，请确保
要么包含一个非常具体的日期（「2005 年 11 月前修复」），
要么包含一个非常具体的事件（「当所有客户端都能处理 XML 响应时移除这段代码。」）。

<a id="Formatting"></a>

## 格式

编码风格和格式在很大程度上是随意定的，但若
所有人都使用同一种风格，项目就容易理解得多。
个人可能并不认同格式规则的每一处，有些规则
也可能需要一段时间适应，但重要的是所有项目
贡献者都遵循风格规则，以便大家都能轻松阅读并理解彼此的代码。

为帮助你正确地格式化代码，我们提供了
[emacs 的设置文件](https://raw.githubusercontent.com/google/styleguide/gh-pages/google-c-style.el)。

<a id="Line_Length"></a>

### 行长度

代码中的每一行文本最多不超过 80 个字符。

我们承认这条规则有争议，但已有如此多的既有代码
遵循它，而且我们认为一致性很重要。

##### 优点

支持这条规则的人认为，强迫他们调整窗口大小
很不礼貌，而且没有必要用更长的行。有些人习惯
把几个代码窗口并排摆放，因此无论如何都没有
空间把窗口加宽。人们搭建工作环境时会假定一个
特定的最大窗口宽度，而 80 列一直是传统标准。
为何要改变它呢？

##### 缺点

主张改变的人认为，更宽的行能让代码更易读。
80 列的限制是墨守成规地退回到 1960 年代的大型机；
现代设备屏幕很宽，可以轻松显示更长的行。

##### 结论

80 个字符是上限。

若满足以下条件，一行可以超过 80 个字符：

*   一行注释，若无法在不损害可读性、剪贴或自动
    链接便利性的情况下拆分 —— 例如，某行包含示例
    命令或长度超过 80 个字符的字面 URL。
*   无法在 80 列处轻松折行的字符串字面量。这
    可能是因为它包含 URI 或其他语义上关键的片段，
    或因为该字面量包含某种嵌入语言，或因为它是
    换行具有意义的多行字面量，如帮助信息。在这些
    情况下，拆开字面量会降低可读性、可搜索性、
    点击链接的能力，等等。除测试代码外，此类
    字面量应出现在文件顶部附近的命名空间作用域中。
    若 Clang-Format 之类的工具无法识别不可拆分的
    内容，请[禁用该工具](https://clang.llvm.org/docs/ClangFormatStyleOptions.html#disabling-formatting-on-a-piece-of-code)
    按需围绕该内容处理即可。

    （我们必须在此类字面量的易用性/可搜索性与
    其周围代码的可读性之间取得平衡。）

*   一条 include 语句。

*   [头文件保护。](#The__define_Guard)

*   一条 using 声明。

<a id="Non-ASCII_Characters"></a>

### 非 ASCII 字符

非 ASCII 字符应当很少见，且必须使用 UTF-8 编码。

你不该在源代码中硬编码面向用户的文本，即便是英文，
因此非 ASCII 字符的使用应很少见。不过，在某些
情况下，在代码里包含这类词是合适的。例如，若你的
代码解析来自外部来源的数据文件，把这些数据文件中
用作分隔符的非 ASCII 字符串硬编码进来可能是合适的。
更常见的是，单元测试代码（无需本地化）可能包含
非 ASCII 字符串。在这种情况下，应使用 UTF-8，
因为大多数能处理不止 ASCII 的工具都理解这种编码。

十六进制编码也可以，且在能提升可读性时值得推荐——
例如，`"\xEF\xBB\xBF"` 或更简单的 `"\uFEFF"` 是
Unicode 零宽不换行空格字符，若直接以 UTF-8 写入
源代码，它将不可见。

尽可能避免使用 `u8` 前缀。从 C++20 起，它的语义与
C++17 中有显著不同：产生的是 `char8_t` 数组而非
`char` 数组，并且在 C++23 中还会再次变化。

不应使用 `char16_t` 和 `char32_t` 字符类型，因为它们
面向非 UTF-8 文本。出于类似原因，也不应使用 `wchar_t`
（除非你编写的代码与大量使用 `wchar_t` 的
Windows API 交互）。

<a id="Spaces_vs._Tabs"></a>

### 空格与制表符

只使用空格，每次缩进 2 个空格。

我们用空格做缩进。不要在代码中使用制表符。应把
编辑器设置为按下 Tab 键时输出空格。

<a id="Function_Declarations_and_Definitions"></a>

### 函数声明与定义

返回类型与函数名放在同一行，参数放得下时也放在
同一行。参数列表一行放不下时，像在
[函数调用](#Function_Calls)中折行实参那样折行。

函数形如：

<div class='goodcode'></div>

```cpp
ReturnType ClassName::FunctionName(Type par_name1, Type par_name2) {
  DoSomething();
  ...
}
```

如果文本太多、一行放不下：

<div class='goodcode'></div>

```cpp
ReturnType ClassName::ReallyLongFunctionName(Type par_name1, Type par_name2,
                                             Type par_name3) {
  DoSomething();
  ...
}
```

或者连第一个参数都放不下时：

<div class='goodcode'></div>

```cpp
ReturnType LongClassName::ReallyReallyReallyLongFunctionName(
    Type par_name1,  // 4 space indent
    Type par_name2,
    Type par_name3) {
  DoSomething();  // 2 space indent
  ...
}
```

需要注意的几点：

*   选择好的参数名。
*   只有当参数在函数定义中未使用时，才可省略
    参数名。
*   若返回类型与函数名无法放在同一行，
    就在两者之间断行。
*   若在函数声明或定义的返回类型之后断行，
    不要缩进。
*   左圆括号始终与函数名在同一行。
*   函数名与左圆括号之间绝不留空格。
*   圆括号与参数之间绝不留空格。
*   左花括号始终位于函数声明最后一行的行尾，
    而不是下一行的行首。
*   右花括号要么单独占最后一行，要么与左花括号
    在同一行。
*   右圆括号与左花括号之间
    应有一个空格。
*   若可能，所有参数应对齐。
*   默认缩进为 2 个空格。
*   折行后的参数缩进 4 个空格。

从上下文即可看出未使用的参数可以省略名称：

<div class='goodcode'></div>

```cpp
class Foo {
 public:
  Foo(const Foo&) = delete;
  Foo& operator=(const Foo&) = delete;
};
```

可能不那么一目了然的未使用参数，应在函数定义中
把变量名注释掉：

<div class='goodcode'></div>

```cpp
class Shape {
 public:
  virtual void Rotate(double radians) = 0;
};

class Circle : public Shape {
 public:
  void Rotate(double radians) override;
};

void Circle::Rotate(double /*radians*/) {}
```

<div class='badcode'></div>

```cpp
// Bad - if someone wants to implement later, it's not clear what the
// variable means.
void Circle::Rotate(double) {}
```

属性，以及会展开为属性的宏，应出现在函数声明或
定义的开头、返回类型之前：

<div class='goodcode'></div>

```cpp
  ABSL_ATTRIBUTE_NOINLINE void ExpensiveFunction();
  [[nodiscard]] bool IsOk();
```

<a id="Formatting_Lambda_Expressions"></a>

### Lambda 表达式

参数与函数体的格式和其他函数一样，捕获列表的
格式和其他以逗号分隔的列表一样。

对于按引用捕获，不要在和号（`&`）与
变量名之间留空格。

<div class='goodcode'></div>

```cpp
int x = 0;
auto x_plus_n = [&x](int n) -> int { return x + n; };
```

短 lambda 可以内联写成函数实参。

<div class='goodcode'></div>

```cpp
absl::flat_hash_set<int> to_remove = {7, 8, 9};
std::vector<int> digits = {3, 9, 1, 8, 4, 7, 1};
digits.erase(std::remove_if(digits.begin(), digits.end(), [&to_remove](int i) {
               return to_remove.contains(i);
             }),
             digits.end());
```

<a id="Floating_Literals"></a>

### 浮点字面量

浮点字面量应始终带有小数点，且两侧都有数字，
即使使用指数记法也是如此。若所有浮点字面量都
采用这种常见形式，可读性会更好，因为这有助于
确保它们不被误认为整型字面量，也确保指数记法中的 `E`/`e`
不被误认为十六进制数字。用整型字面量初始化浮点
变量是可以的（假定变量类型能精确表示
该整数），但要注意，指数记法中的数字
绝不是整型字面量。

<div class='badcode'></div>

```cpp
float f = 1.f;
long double ld = -.5L;
double d = 1248e6;
```

<div class='goodcode'></div>

```cpp
float f = 1.0f;
float f2 = 1.0;  // Also OK
float f3 = 1;    // Also OK
long double ld = -0.5L;
double d = 1248.0e6;
```

<a id="Function_Calls"></a>

### 函数调用

要么把调用全部写在一行，要么在圆括号处折行，
要么让实参从新的一行开始、缩进四个空格，并
继续沿用该 4 空格缩进。若无其他考虑，应使用
最少的行数，包括在适当之处把多个实参放在
同一行。

函数调用采用以下格式：

<div class='goodcode'></div>

```cpp
bool result = DoSomething(argument1, argument2, argument3);
```

若实参无法全部放在一行，应拆成多行，后续每一行
都与第一个实参对齐。不要在左圆括号之后或右圆
括号之前加空格：

<div class='goodcode'></div>

```cpp
bool result = DoSomething(averyveryveryverylongargument1,
                          argument2, argument3);
```

实参也可以全部放在后续行上，并使用四空格
缩进：

<div class='goodcode'></div>

```cpp
if (...) {
  ...
  ...
  if (...) {
    bool result = DoSomething(
        argument1, argument2,  // 4 space indent
        argument3, argument4);
    ...
  }
```

把多个实参放在一行，以减少调用函数所需的行数，
除非存在特定的可读性问题。有些人认为严格每行
只放一个实参的格式更易读，也更便于编辑实参。
不过，我们优先考虑读者，而非编辑实参的便利，
而且大多数可读性问题用以下技巧来解决
效果更好。

若把多个实参放在一行会因构成某些实参的表达式
复杂或令人费解而降低可读性，请尝试创建变量，
用具有描述性的名称承载这些实参：

<div class='goodcode'></div>

```cpp
int my_heuristic = scores[x] * y + bases[x];
bool result = DoSomething(my_heuristic, x, y, z);
```

或者把令人费解的实参单独放一行，并附上解释性注释：

<div class='goodcode'></div>

```cpp
bool result = DoSomething(scores[x] * y + bases[x],  // Score heuristic.
                          x, y, z);
```

若仍存在某个实参单独占一行明显更易读的情况，
就让它单独占一行。该决定应针对那个变得更易读
的实参，而不是一条通用规则。

有时实参会构成一种对可读性很重要的结构。在这种
情况下，尽管按该结构来编排实参的格式：

<div class='goodcode'></div>

```cpp
// Transform the widget by a 3x3 matrix.
my_widget.Transform(x1, x2, x3,
                    y1, y2, y3,
                    z1, z2, z3);
```

<a id="Braced_Initializer_List_Format"></a>

### 花括号初始化列表格式

花括号初始化列表的格式，应与在相同位置格式化
函数调用完全一致。

若花括号列表跟在某个名称（如类型名或变量名）之后，
格式化时就当 `{}` 是以该名称调用的函数调用的圆括号。
若没有名称，则假定名称长度为零。

<div class='goodcode'></div>

```cpp
// Examples of braced init list on a single line.
return {foo, bar};
functioncall({foo, bar});
std::pair<int, int> p{foo, bar};

// When you have to wrap.
SomeFunction(
    {"assume a zero-length name before {"},
    some_other_function_parameter);
SomeType variable{
    some, other, values,
    {"assume a zero-length name before {"},
    SomeOtherType{
        "Very long string requiring the surrounding breaks.",
        some, other, values},
    SomeOtherType{"Slightly shorter string",
                  some, other, values}};
SomeType variable{
    "This is too long to fit all in one line"};
MyType m = {  // Here, you could also break before {.
    superlongvariablename1,
    superlongvariablename2,
    {short, interior, list},
    {interiorwrappinglist,
     interiorwrappinglist2}};
```

<a id="Formatting_Looping_Branching"></a>

### 循环与分支语句 []() {#Conditionals}

从较高层面看，循环或分支语句由以下
**组成部分**构成：

*   一个或多个**语句关键字**（例如 `if`、`else`、`switch`、`while`、
    `do` 或 `for`）。
*   一个**条件或迭代说明符**，位于圆括号内。
*   一个或多个**受控语句**，或受控语句组成的块。

对于这些语句：

*   语句的各组成部分之间应以单个空格分隔（而不是
    换行）。
*   在条件或迭代说明符内部，每个分号与下一个
    记号之间放一个空格（或一个换行），除非该记号
    是右圆括号或另一个分号。
*   在条件或迭代说明符内部，左圆括号之后
    或右圆括号之前不要放空格。
*   把所有受控语句都放进块中（即使用花括号）。
*   在受控块内部，紧跟左花括号之后放一个换行，
    紧跟右花括号之前也放一个换行。

<div class='goodcode'></div>

```cpp
if (condition) {                   // Good - no spaces inside parentheses, space before brace.
  DoOneThing();                    // Good - two-space indent.
  DoAnotherThing();
} else if (int a = f(); a != 3) {  // Good - closing brace on new line, else on same line.
  DoAThirdThing(a);
} else {
  DoNothing();
}

// Good - the same rules apply to loops.
while (condition) {
  RepeatAThing();
}

// Good - the same rules apply to loops.
do {
  RepeatAThing();
} while (condition);

// Good - the same rules apply to loops.
for (int i = 0; i < 10; ++i) {
  RepeatAThing();
}
```

<div class='badcode'></div>

```cpp
if(condition) {}                   // Bad - space missing after `if`.
else if ( condition ) {}           // Bad - space between the parentheses and the condition.
else if (condition){}              // Bad - space missing before `{`.
else if(condition){}               // Bad - multiple spaces missing.

for (int a = f();a == 10) {}       // Bad - space missing after the semicolon.

// Bad - `if ... else` statement does not have braces everywhere.
if (condition)
  foo;
else {
  bar;
}

// Bad - `if` statement too long to omit braces.
if (condition)
  // Comment
  DoSomething();

// Bad - `if` statement too long to omit braces.
if (condition1 &&
    condition2)
  DoSomething();
```

出于历史原因，我们允许（但不鼓励）上述规则有
一个例外：受控语句的花括号，或花括号内部的
换行，可以省略，条件是省略后整条语句出现在
单独一行（此时右圆括号与受控语句之间有一个
空格）或两行（此时右圆括号之后有一个换行且
没有花括号）。

<div class='neutralcode'></div>

```cpp
// OK - each case fits on one line.
if (x == kFoo) { return new Foo(); }
while (TrySomething()) {}

// OK - braces are optional in this case.
if (x == kFoo) return new Foo();

// OK - condition fits on one line, body fits on another.
if (x == kBar)
  Bar(arg1, arg2, arg3);
```

此例外不适用于多关键字语句，如 `if ... else` 或
`do ... while`。

<div class='badcode'></div>

```cpp
// Bad - `if ... else` statement is missing braces.
if (x) DoThis();
else DoThat();

// Bad - `do ... while` statement is missing braces.
do DoThis();
while (x);
```

仅在语句简短时使用这种风格，并要考虑到，条件
或受控语句复杂的循环与分支语句加上花括号
可能更易读。有些项目要求始终使用花括号。

`case` 块在 `switch` 语句中可以带花括号，也可以不带，
取决于你的偏好。若确实加上花括号，应按下面
所示放置。

<div class='goodcode'></div>

```cpp
switch (var) {
  case 0: {  // 2 space indent
    Foo();   // 4 space indent
    break;
  }
  default: {
    Bar();
  }
}
```

空的循环体应使用一对空花括号，或使用不带花括号的 `continue`，
而不是单个分号。空花括号仍受通用折行规则
约束，也受上述历史例外约束。

<div class='goodcode'></div>

```cpp
while (condition) {  // Good - `{}` indicates no logic.
}                    // A linebreak is usually required.

while (condition) {}  // But OK if it fits on one line.

while (condition) {
  // Comments are okay, too
}

while (condition) continue;  // Good - `continue` indicates no logic.
```

<div class='badcode'></div>

```cpp
while (condition);  // Bad - looks like part of `do-while` loop.
```

<a id="Pointer_and_Reference_Expressions"></a>

### 指针与引用表达式和类型

点号或箭头周围不留空格。指针运算符不带尾随空格。

以下是格式正确的指针与引用
表达式示例：

<div class='goodcode'></div>

```cpp
x = *p;
p = &x;
x = r.y;
x = r->y;
```

注意：

*   访问成员时，点号或箭头周围不留空格。
*   指针运算符在 `*` 或 `&` 之后不留空格。

涉及指针或引用时（变量声明或定义、实参、返回
类型、模板参数，等等），不得在星号/和号之前
放空格。用一个空格把类型与所声明的名称
（若有）分隔开。

<div class='goodcode'></div>

```cpp
// These are fine.
char* c;
const std::string& str;
int* GetPointer();
std::vector<char*>  // Note no space between '*' and '>'
```

在同一条声明中声明多个变量是允许的（虽不常见），
但若其中任何一个带有指针或引用修饰，则不允许。
这类声明很容易被误读。

<div class='neutralcode'></div>

```cpp
// Fine if helpful for readability.
int x, y;
```

<div class='badcode'></div>

```cpp
int x, *y;  // Disallowed - no & or * in multiple declaration
int *x, *y;  // Disallowed - no & or * in multiple declaration
int *x;  // Disallowed - & or * must be left of the space
char * c;  // Bad - spaces on both sides of *
const std::string & str;  // Bad - spaces on both sides of &
```

<a id="Boolean_Expressions"></a>

### 布尔表达式

当布尔表达式超过
[标准行长度](#Line_Length)时，断行方式要
保持一致。

在此例中，逻辑与运算符始终位于行尾：

<div class='goodcode'></div>

```cpp
if (this_one_thing > this_other_thing &&
    a_third_thing == a_fourth_thing &&
    yet_another && last_one) {
  ...
}
```

注意，在此例中代码折行时，两个 `&&` 逻辑与
运算符都位于行尾。这在 Google 代码中更常见，
不过也允许把所有运算符都放在行首。可以酌情
插入额外的圆括号，因为用得恰当时它们对提升
可读性很有帮助，但要小心不要过度使用。
还要注意，应始终使用标点运算符，例如 `&&` 以及
`~`，而不是词语运算符，例如 `and` 和 `compl`。

<a id="Return_Values"></a>

### 返回值

不要无谓地用圆括号把 `return` 表达式括起来。

在 `return expr;` 中使用圆括号，仅限 `x = expr;` 中也会用圆括号之处。

<div class='goodcode'></div>

```cpp
return result;                  // No parentheses in the simple case.
// Parentheses OK to make a complex expression more readable.
return (some_long_condition &&
        another_condition);
```

<div class='badcode'></div>

```cpp
return (value);                // You wouldn't write var = (value);
return(result);                // return is not a function!
```

<a id="Variable_and_Array_Initialization"></a>

### 变量与数组初始化

可以在 `=`、`()` 和 `{}` 之间选择；以下都正确：

<div class='goodcode'></div>

```cpp
int x = 3;
int x(3);
int x{3};
std::string name = "Some Name";
std::string name("Some Name");
std::string name{"Some Name"};
```

在类型上使用花括号初始化列表 `{...}` 时要小心，
若该类型有 `std::initializer_list` 构造函数：非空的
*braced-init-list* 会尽可能优先选择 `std::initializer_list`
构造函数。注意，空的 `{}` 很特殊，若存在默认
构造函数就会调用它。要强制调用非 `std::initializer_list` 构造函数，请改用圆括号。

<div class='goodcode'></div>

```cpp
std::vector<int> v(100, 1);  // A vector containing 100 items: All 1s.
std::vector<int> v{100, 1};  // A vector containing 2 items: 100 and 1.
```

此外，花括号形式能防止整型窄化。这可以
避免某些类型的编程错误。

<div class='goodcode'></div>

```cpp
int pi(3.14);  // OK -- pi == 3.
int pi{3.14};  // Compile error: narrowing conversion.
```

<a id="Preprocessor_Directives"></a>

### 预处理指令

预处理指令开头的井号应始终位于
行首。

即使预处理指令位于已缩进的代码体内部，
指令也应从行首开始。

<div class='goodcode'></div>

```cpp
// Good - directives at beginning of line
  if (lopsided_score) {
#if DISASTER_PENDING      // Correct -- Starts at beginning of line
    DropEverything();
# if NOTIFY               // OK but not required -- Spaces after #
    NotifyClient();
# endif
#endif
    BackToNormal();
  }
```

<div class='badcode'></div>

```cpp
// Bad - indented directives
  if (lopsided_score) {
    #if DISASTER_PENDING  // Wrong!  The "#if" should be at beginning of line
    DropEverything();
    #endif                // Wrong!  Do not indent "#endif"
    BackToNormal();
  }
```

<a id="Class_Format"></a>

### 类格式

各节按 `public`、`protected`、`private` 顺序排列，每节缩进一个空格。

类定义的基本格式（略去注释，关于需要哪些注释，
参见[类注释](#Class_Comments)）
如下：

<div class='goodcode'></div>

```cpp
class MyClass : public OtherClass {
 public:      // Note the 1 space indent!
  MyClass();  // Regular 2 space indent.
  explicit MyClass(int var);
  MyClass(const MyClass& other);
  MyClass& operator=(const MyClass& other);
  ~MyClass() {}

  void SomeFunction();
  void SomeFunctionThatDoesNothing() {}

  void set_some_var(int var) { some_var_ = var; }
  int some_var() const { return some_var_; }

 private:
  bool SomeInternalFunction();

  int some_var_;
  int some_other_var_;
};
```

需要注意的几点：

*   任何基类名称都应与子类名称在同一行，但受
    80 列限制约束。
*   `public:`、`protected:` 和 `private:` 关键字应
    缩进一个空格。
*   除第一次出现外，这些关键字之前应有一个空行。
    在小型类中，此规则可选。
*   不要在这些关键字之后留空行。
*   `public` 节应放在最前，其次是 `protected`，
    最后是 `private` 节。
*   关于各节内声明的排序规则，参见
    [声明顺序](#Declaration_Order)。

<a id="Constructor_Initializer_Lists"></a>

### 构造函数初始化列表

构造函数初始化列表可以全部放在一行，或让后续行
缩进四个空格。

初始化列表可接受的格式如下：

<div class='goodcode'></div>

```cpp
// When everything fits on one line:
MyClass::MyClass(int var) : some_var_(var) {
  DoSomething();
}

// If the signature and initializer list are not all on one line,
// you must wrap before the colon and indent 4 spaces:
MyClass::MyClass(int var)
    : some_var_(var), some_other_var_(var + 1) {
  DoSomething();
}

// When the list spans multiple lines, put each member on its own line
// and align them:
MyClass::MyClass(int var)
    : some_var_(var),             // 4 space indent
      some_other_var_(var + 1) {  // lined up
  DoSomething();
}

// As with any other code block, the close curly can be on the same
// line as the open curly, if it fits.
MyClass::MyClass(int var)
    : some_var_(var) {}
```

<a id="Namespace_Formatting"></a>

### 命名空间格式

命名空间的内容不缩进。

[命名空间](#Namespaces)不会增加额外一级缩进。例如，
使用：

<div class='goodcode'></div>

```cpp
namespace {

void foo() {  // Correct.  No extra indentation within namespace.
  ...
}

}  // namespace
```

不要在命名空间内部缩进：

<div class='badcode'></div>

```cpp
namespace {

  // Wrong!  Indented when it should not be.
  void foo() {
    ...
  }

}  // namespace
```

<a id="Horizontal_Whitespace"></a>

### 水平空白

水平空白的使用取决于位置。绝不要在行尾
留下尾随空白。

#### 通用

<div class='goodcode'></div>

```cpp
int i = 0;  // Two spaces before end-of-line comments.

void f(bool b) {  // Open braces should always have a space before them.
  ...
int i = 0;  // Semicolons usually have no space before them.
// Spaces inside braces for braced-init-list are optional.  If you use them,
// put them on both sides!
int x[] = { 0 };
int x[] = {0};

// Spaces around the colon in inheritance and initializer lists.
class Foo : public Bar {
 public:
  // For inline function implementations, put spaces between the braces
  // and the implementation itself.
  Foo(int b) : Bar(), baz_(b) {}  // No spaces inside empty braces.
  void Reset() { baz_ = 0; }  // Spaces separating braces from implementation.
  ...
```

添加尾随空白会给其他编辑同一文件的人在合并时
带来额外工作，删除已有的尾随空白同样如此。因此，
不要引入尾随空白。若你本就要改动那一行，就顺手
删掉它，或在一次单独的清理操作中处理（最好在
没有其他人改动该文件时）。

#### 循环与条件语句

<div class='goodcode'></div>

```cpp
if (b) {          // Space after the keyword in conditions and loops.
} else {          // Spaces around else.
}
while (test) {}   // There is usually no space inside parentheses.
switch (i) {
for (int i = 0; i < 5; ++i) {
// Loops and conditions may have spaces inside parentheses, but this
// is rare.  Be consistent.
switch ( i ) {
if ( test ) {
for ( int i = 0; i < 5; ++i ) {
// For loops always have a space after the semicolon.  They may have a space
// before the semicolon, but this is rare.
for ( ; i < 5 ; ++i) {
  ...

// Range-based for loops always have a space before and after the colon.
for (auto x : counts) {
  ...
}
switch (i) {
  case 1:         // No space before colon in a switch case.
    ...
  case 2: break;  // Use a space after a colon if there's code after it.
```

#### 运算符

<div class='goodcode'></div>

```cpp
// Assignment operators always have spaces around them.
x = 0;

// Other binary operators usually have spaces around them, but it's
// OK to remove spaces around factors.  Parentheses should have no
// internal padding.
v = w * x + y / z;
v = w*x + y/z;
v = w * (x + z);

// No spaces separating unary operators and their arguments.
x = -5;
++x;
if (x && !y)
  ...
```

#### 模板与强制转换

<div class='goodcode'></div>

```cpp
// No spaces inside the angle brackets (< and >), before
// <, or between >( in a cast
std::vector<std::string> x;
y = static_cast<char*>(x);

// No spaces between type and pointer.
std::vector<char*> x;
```

<a id="Vertical_Whitespace"></a>

### 垂直空白

节制地使用垂直空白；不必要的空行会让整体
代码结构更难看清。只在有助于读者理解
结构的地方使用空行。

不要在缩进已提供清晰分界的地方添加空行，
例如代码块的开头或结尾。确实要用空行把代码
分成紧密相关的块，类似于散文中的分段。在
一条语句或声明内部，通常只为了不超过
[行长度限制](#Line_Length)而插入换行，或为了
给内容的一部分附上注释而插入换行。

<a id="Exceptions_to_the_Rules"></a>

## 规则的例外

上文所述的编码约定是强制性的。不过，与所有好的
规则一样，这些规则有时也有例外，我们在此讨论。

<a id="Existing_Non-conformant_Code"></a>

### 既有的不符合风格指南的代码

处理不符合本风格指南的代码时，可以偏离
这些规则。

若你发现自己正在修改按本指南之外的规范编写的
代码，为了与该代码中的局部约定保持一致，可能
不得不偏离这些规则。若不确定该怎么做，请询问
原作者或目前负责该代码的人。请记住，
*一致性* 也包括局部
一致性。

<a id="Windows_Code"></a>

### Windows 代码

Windows 程序员发展出了一套自己的编码约定，主要
源自 Windows 头文件及其他 Microsoft 代码中的约定。我们
希望让任何人都能轻松读懂你的代码，因此为在所有平台上
编写 C++ 的人准备了同一套准则。

如果你习惯了流行的 Windows 风格，有几条准则值得
重申，因为你可能会忽略它们：

*   不要使用匈牙利命名法（例如将整数命名为 `iNum`）。
    请使用 Google 的命名约定，包括源文件使用 `.cc`
    扩展名。
*   Windows 为基本类型定义了许多自己的同义类型，例如
    `DWORD`、`HANDLE` 等。在调用 Windows API 函数时
    使用这些类型是完全可以接受的，而且值得鼓励。即便
    如此，仍应尽可能贴近底层的 C++ 类型。例如，使用 `const TCHAR*`
    而非 `LPCTSTR`。
*   使用 Microsoft Visual C++ 编译时，请将编译器警告
    级别设为 3 级或更高，并把所有警告当作错误。
*   不要使用 `#pragma once`；请改用标准的 Google 头文件
    保护。头文件保护中的路径应相对于项目目录树的
    顶层。
*   事实上，除非绝对必要，不要使用任何非标准扩展，如 `#pragma`
    和 `__declspec`。允许使用 `__declspec(dllimport)` 和
    `__declspec(dllexport)`；但必须通过
    `DLLIMPORT`、`DLLEXPORT` 之类的宏来使用它们，
    以便别人在共享代码时能轻松禁用这些扩展。

不过，在 Windows 上，有少数几条规则我们偶尔需要
打破：

*   通常我们
    [强烈不建议使用多重实现继承](#Multiple_Inheritance)；
    但在使用 COM 和某些 ATL/WTL 类时却必须如此。你可以
    使用多重实现继承来实现 COM 或 ATL/WTL 类与
    接口。
*   虽然你不应该在自己的代码中使用异常，但 ATL
    和某些 STL 中大量使用了异常，包括 Visual C++
    附带的那个 STL。使用 ATL 时，应定义 `_ATL_NO_EXCEPTIONS`
    来禁用异常。你应当研究是否也能在 STL 中
    禁用异常，但如果不行，在编译器中开启异常
    也是可以的。（注意，这只是为了让 STL 能够
    编译。你仍然不应自己编写异常处理代码。）
*   使用预编译头的通常做法是在每个源文件的开头包含
    一个头文件，其名称通常类似 `StdAfx.h` 或
    `precompile.h`。为了让代码更容易与其他项目共享，
    请避免显式包含该文件（`precompile.cc` 除外），
    并改用编译器选项 `/FI` 自动包含该文件。
*   资源头文件通常名为 `resource.h`，且只包含宏，
    因此不需要遵循这些风格规则。

<!-- NB: Keep this at the end of the file. See comment at top for details.
     {% endraw %} -->
