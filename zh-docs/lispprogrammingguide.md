# Google Common Lisp 高效编程

## 简介

本文档旨在作为以下内容的补充：
[Lisp 风格指南](lispguide.md)。它旨在涵盖与以下内容无关的内容：
风格，但对新手 Lisp 程序员非常重要。三大主题
涵盖常见的优化技巧，以及
新手 Lisp 程序员常犯的错误。

<!-- mdformat off -->
* TOC
{:toc}
<!-- mdformat on -->

## 优化

### 使用库

-   优先使用已有的库，而不是重新实现。
-   在以下情况下，你可以重新实现某个库：

    -   有充分记录的的性能需求，或
    -   你需要现有库不提供的
        专门功能。

-   除非你已确认没有任何现成库可被修复或完善成所需的样子，否则
    不得新建库。这是一条反对 NIH 综合征（「非我发明」）的规则，
    该综合征在 Lisp 黑客中尤其
    普遍。

-   无论你选择旧库还是新库，都必须获得许可，以便
    将第三方代码纳入代码库。你必须在合适的邮件列表中讨论该库的使用，
    并请在你所在领域和/或 Lisp 库生态（若
    有）方面有经验的人评审你的代码。请准备好论证，为何这一特定方案
    与其他可用库相比
    是合理的。

-   某些库所采用的许可证与你所编写软件的许可证不兼容，
    不得视为可供使用。请
    留意这些问题，或咨询对此了解的人。

### 避免分配

-   确保对象在不再需要后无法再被访问到。
-   不要不必要地 `CONS`。

在具有自动存储管理（如 Lisp 或 Java）的语言中，
俗语「内存泄漏」指的是这样一种情况：虽然存储实际上已不再需要，
却因其仍可访问而
未被释放。

你应当小心：创建对象时，不要在它们不再需要后仍让它们
可被访问到！

以下是 Common Lisp 中一个典型的「粗心者陷阱」。如果你创建一个带填充指针的数组，
向其中放入对象，然后将填充指针重置
为零，这些对象不会被垃圾回收：Common Lisp 规范规定，
在填充指针末端之外引用数组元素仍然是允许的。同时这也意味着，
 `VECTOR-POP` 并不会从底层数组的存储中移除所返回的
元素。

不要不必要地 cons（即分配）。垃圾回收并非魔法。
过度分配通常会导致性能问题。

### 不安全的操作

-   不要定义或使用不安全的操作，除非：
    -   代码已经过性能剖析，且确有需要。
    -   有文档说明使用它们是安全的。

Common Lisp 实现通常提供后门，以不安全的方式更快地计算某些操作。例如，某些库提供
仅设计用于 fixnum 的算术
操作，在传入正确参数时能更快地得出正确
结果。其缺点是，此类操作在溢出时结果
不正确，并且在传入 fixnum 以外的值时可能产生未定义的
行为。

例如，QPX 和 QRes（位于 QUUX 中）定义了以
 `I` 为前缀的 fixnum 优化运算符，例如 `I+`、`I-`、`I*`、`I=`、`I<`、`I>` 等。

更一般地说，如果参数满足某些不变式（例如类型正确且足够小），不安全的操作将比
等效的安全操作更快地得出正确结果；然而，如果参数未能
满足所需的不变式，则该操作可能产生未定义的行为，
例如使软件崩溃，或者——有时更糟——悄无声静地给出
错误的答案。取决于软件是用于驾驶飞机或
其他关键生命设备，还是用于核算大量资金，
此类未定义行为可能致人死亡或破产。然而，适当的速度有时能
决定软件是慢得无法使用还是能完成任务，
或者决定软件是净亏损还是能
带来利润。


未经性能剖析结果表明需要此优化，且未经仔细文档说明
其使用安全性，你不得定义或使用不安全的操作。不安全的操作应仅限于内部
函数；你应仔细记录使用这些
函数并传入错误参数时的危险程度。你只能在
包内部的函数中使用不安全的操作，并且应当记录
这些声明的使用，因为以错误类型的参数调用这些函数会
导致未定义行为。在从包中导出的函数里使用 `check-type` 来净化
输入参数，从而使内部函数永远不会被传入
非法值。


在某些编译器上，通常可以通过将类型声明与具有足够高
 `SPEED` 与足够低 `SAFETY` 的 `OPTIMIZE` 声明结合，来定义新的不安全操作。除了为生产
 `SPEED` 与足够低 `SAFETY` 的 `OPTIMIZE` 声明结合，来定义新的不安全操作。除了为生产
在编译期发现错误可能比 `check-type` 断言更有帮助。这些
编译器在你切换到更安全但更慢的优化设置时，可能会将这些声明解释为断言；
这有助于在开发过程中定位代码中的动态错误，
但不应被用于生产代码，因为这种做法违背了将声明作为
性能技巧的
初衷。

### DYNAMIC-EXTENT

-   将 `DYNAMIC-EXTENT` 视为不安全的操作，对使用它的任何代码进行性能剖析，并
    记录其为何安全。
-   确信底层代码不会更改，从而导致你的
    假设/文档失效。

`DYNAMIC-EXTENT` 声明是
[unsafe operations](#unsafe-operations) 的一种特例。

 `DYNAMIC-EXTENT` 声明的目的是通过减少垃圾回收来提升性能，适用于那些
显然可知对象生命周期处于函数「动态范围」之内的情况。也就是说，
对象在函数被调用后的某个时刻被创建，并且
在函数通过任何方式退出后始终不可访问。


通过声明变量或局部函数 `DYNAMIC-EXTENT`，程序员向 Lisp
*断言*：任何曾作为该变量的值、或作为该函数定义的
闭包的对象，其生命周期都在该（最内层）函数所声明变量的动态
范围内。

Lisp 实现随后便可自由利用该信息来让程序
运行得更快。通常，Lisp 实现可以利用这一知识来
进行栈分配：

-   为存储 `&REST` 参数而创建的列表。
-   在函数内部分配的列表、向量与结构体。
-   闭包。

如果断言是错误的，即程序员的声明不成立，那么
结果可能是*灾难性的*：Lisp 可能在函数返回后的任何时刻终止，
或者永远挂起，又或者——最糟糕的是——产生不正确的
结果，且不报任何运行时错误！

即使断言是正确的，对函数的未来修改也可能引入
对断言的违反。这增加了危险性。

在大多数情况下，此类对象是短暂的。现代 Lisp 实现使用
分代垃圾回收器，在这种情况下相当高效。


因此，`DYNAMIC-EXTENT` 声明应当谨慎使用。你只有在以下情况才能
使用它们：

1.  有充分理由认为其对性能的整体影响是
    显著的，并且
2.  能够完全确定该断言为真。
3.  代码不太可能被以导致该
    声明失效的方式修改。

第（1）点是避免过早优化原则的一个特例。
只有当此类对象以极高的频率分配时，
此类优化才有意义，例如「在内部循环中」。

注意，通过分析函数被调用的位置以及它被传递给哪些其他函数，相对容易确定该函数不会
逃出当前调用帧的动态范围；因此，你在声明函数
 `DYNAMIC-EXTENT` 时应有所
谨慎，但这并非一个高风险的
声明。另一方面，要确定没有任何曾绑定或赋值给该变量的对象、以及它们的子对象
会逃出当前调用帧的动态范围，并且在函数的任何未来修改中
依然如此，则要困难得多。因此，你在声明变量
 `DYNAMIC-EXTENT` 时应
极为谨慎。

通常很难预测此类优化对性能的影响。
在编写作为可复用代码库一部分的函数或宏时，
无法先验地知道代码会运行多少次。理想情况下，
应当有工具能通过运行模拟和测试用例，来判断使用此类
优化的可行性与适用性，但在实践中这
并不像理应那般容易。这是一种权衡。如果你非常、非常有把握
断言为真（即任何绑定到该变量的对象及其所有
子对象都仅在指定作用域的动态范围内被使用），而
且节省多少时间并不明显、也难以衡量，那么
加入该声明可能比省略它更好。（理想情况下，
进行此类测量的难度本应比实际更低。）

### REDUCE vs APPLY

-   在 `CONS` 起来的列表上，优先使用 `REDUCE` 而非 `APPLY`。
-   出于可读性与性能的考虑，优先使用 apply。

在语义上首个操作符参数本就保证相同语义的情况下，你应当使用 `REDUCE` 而非 `APPLY`，
并配合一个临时构造的列表，其中
二者的语义一致。当然，如果 `APPLY` 能完成你想要的而 `REDUCE`
不能，你就必须使用 `APPLY`。例如：

<div class='badcode'></div>

```lisp
;; This copies the list
(apply #'+ (mapcar #'acc frobs))
```

<div class='goodcode'></div>

```lisp
;; This does the same thing while avoiding the copy
(reduce #'+ frobs :key #'acc :initial-value 0)
```

这更可取，因为它不会产生额外的 cons 操作，也不会在那些该限制较小的实现上
超出 `CALL-ARGUMENTS-LIMIT`，
从而可能在长列表上摧毁栈（我们希望避免代码中
不必要的不可移植性）。

然而，你必须小心，不要以不必要地提升计算复杂度
级别的方式使用 `REDUCE`。例如，
`(REDUCE 'STRCAT ...)` 在适当的实现下仅为 *O(n\^2)*，而
*O(n)*。此外，`(REDUCE 'APPEND ...)` 同样是 *O(n\^2)*，除非你指定
`:FROM-END T`。在这种情况下，你不得使用 `REDUCE`，也不得使用
 `(APPLY 'STRCAT ...)` 或 `(APPLY 'APPEND ...)`。相反，你必须使用
来自合适库（你或许需要为其贡献代码）的恰当抽象，
它能在不将实现细节强加给用户的情况下正确处理这些情况。
例如可参见 `UIOP:REDUCE/STRCAT`。

### NCONC 与 MAPCAN

-   不要使用 `NCONC` 或 `MAPCAN`。
    -   也不要使用 loop 的 `NCONC` 特性。
    -   优先使用 `APPEND`，或使用更好的数据结构。
    -   对于底层、对性能极其关键的代码可作例外。

你几乎永远不应使用 `NCONC`。当你不依赖任何副作用时，应使用 `APPEND`。
当你需要更新变量时，应使用 `ALEXANDRIA:APPENDF`。你大概不应依赖
对当前 `CONS` 单元 `CDR` 所做的操作（有人或许认为规范
暗示但未保证这一点）；如果确实这样做了，你必须在显眼的
注释中说明 `NCONC` 的使用；并且你大概应当
重新考虑自己的
数据表示策略。

进一步说，你应避免 `MAPCAN` 或 `LOOP` 的 `NCONC` 特性。你
应分别改用 `ALEXANDRIA:MAPPEND` 与 `LOOP` 的 `APPEND`
特性。

`NCONC` 很少是个好主意，因为其时间复杂度级别并不优于
 `APPEND`，在常见的、没有其他方共享该被副作用修改的列表的情况下，其空间复杂度级别也不优于 `APPEND`，
而其缺陷复杂度级别则远高于 `APPEND`。


如果 `APPEND` 相对于 `NCONC` 带来的微小性能损失成为你程序的瓶颈，
那说明你遇到了大问题，并且很可能用错了数据
结构：你应当使用具有常数时间追加的序列（参见
Okasaki 的著作，并将其加入 lisp-interface-library），或者更简单地，你
应当把数据累积到一棵树中，待累积阶段完成后在线性
时间内将其展平一次。

你只能在底层的、对性能有要求的函数中使用 `NCONC`、`MAPCAN` 或 `LOOP` 的 `NCONC` 特性，
这类函数须以列表作为数据结构、且因已知这些列表很短而
经过审查，同时当该函数
或表达式在其契约中明确要求所累积的结果
只返回全新列表（特别地，它不能是常量
引用或反引用表达式）。即便如此，此类原语的使用也必须
罕见，并附带合理的文档说明。

## 常见陷阱

### 格式化条件指令

-   使用 `FORMAT` 条件指令时要小心。参数
    很容易忘记。

无参数，例如 `"~[Siamese~;Manx~;Persian~] Cat"` \
接受一个格式参数，应为整数。用它来选择子句。
子句编号从零开始。如果数字超出范围，则什么也不打印。
你可以在最后一个 `";"` 前加上 `":"` 来提供默认值。例如在
`";"` 前加上 `":"` 来提供默认值。例如在
会打印 `"Alley"`。

`:` 参数，例如 `"~:[Siamese~;Manx~]"` \
接受一个格式参数。如果它是 `NIL`，使用第一个子句，否则使用
第二个子句。

@` 参数，例如 "~@[Siamese ~a~]" \
如果下一个格式参数为真，则使用该选择，但不消耗
该参数。如果为假，则消耗一个格式参数且不打印任何内容。（通常
子句会使用该格式参数。）

`#` 参数，例如 `"~#[ none~; ~s~; ~s and ~s~]"` \
使用要格式化的参数个数作为选择子句的编号。在其他所有方面
与无参数相同。以下是完整的复杂示例：
`"Items:~#[ none~; ~S~; ~S and ~S~:;~@{~#[~; and~] ~S~^ ,~}~]."`

### 比较运算符

-   比较对象时，你应使用合适的谓词。
    -   另请参阅风格指南中
        [Comparison Operators](lispguide.md#comparison-operators) 关于风格规则的
        说明。

Lisp 提供了四个通用的相等性谓词：`EQ`、`EQL`、`EQUAL` 与
`EQUALP`，它们在语义上有细微差别。此外，Lisp 还提供了
类型特定的谓词 `=`、`CHAR=`、`CHAR-EQUAL`、`STRING=` 与
`STRING-EQUAL`。务必弄清其中的区别！

你应当使用 `EQL` 来比较对象和符号的*同一性*。

你不得使用 `EQ` 来比较数字或字符。两个
 `EQL` 的数字或字符，Common Lisp 并不要求它们是 `EQ`。

对于区分大小写的字符比较，你应使用 `CHAR=`，对于
不区分大小写的字符比较，应使用 `CHAR-EQUAL`。

对于区分大小写的字符串比较，你应使用 `STRING=`，对于
不区分大小写的字符串比较，应使用 `STRING-EQUAL`。

在字符串上使用 `SEARCH` 时，一个常见的错误是将 `STRING=` 或
`STRING-EQUAL` 作为 `:TEST` 函数传入。`:TEST` 函数接收
两个序列元素进行比较。如果序列是字符串，则 `:TEST` 函数
会在两个字符上被调用，因此正确的测试应为 `CHAR=` 或 `CHAR-EQUAL`。
如果你使用 `STRING=` 或 `STRING-EQUAL`，结果虽如你所预期，但在
某些 Lisp 实现中会慢得多。例如，CCL（至少截至 2008 年 8 月）
在每次比较时都会创建一个单字符字符串，这非常
耗费性能。

你不得对浮点数使用精确比较，因为浮点运算模糊的特性可能在数值上
产生微小的「误差」。你应当将绝对值与某个阈值
进行比较。

你必须使用 `=` 来比较数字，除非你的确希望 `0`、`0.0` 与
 `-0.0` 比较为不相等，此时你应使用 `EQL`。但话说回来，你
通常不应在浮点数上使用精确比较。

金额应当使用十进制（有理数）来表示，以避免浮点运算的
复杂性与舍入误差。诸如
[wu-decimal](https://web.archive.org/web/20210423223211/https://wukix.com/lisp-decimals)
（[source](https://github.com/Wukix/wu-decimal)）之类的库可能对你有帮助；同样地，如果
该库不能令人满意，请参阅上文关于
[使用库](#using-libraries) 的介绍。

### CASE 与 ECASE

-   仅对数字、字符与符号使用 `CASE` 和 `ECASE`。
-   不要使用多余的单引号。
-   使用 `OTHERWISE` 而非 `T`。

你应当只使用 `CASE` 和 `ECASE` 来比较数字、字符或符号
（包括布尔值与关键字）。事实上，`CASE` 使用 `EQL` 进行比较，因此
字符串、路径名与结构体可能不会按你期望的方式比较，并且 `1`
会与 `1.0` 不同。

你不得在 `CASE` 形式中使用多余的单引号。这是一个常见的
错误：

<div class='badcode'></div>

```lisp
(ecase x
  ('bar :bar) ; Bad: catches QUOTE
  ('baz :baz)) ; Bad: also would catch QUOTE
```

<div class='goodcode'></div>

```lisp
(ecase x
  ((bar) :bar) ; Better: won't match QUOTE
  ((baz) :baz)) ; Better: same reason
```

 ` 'BAR` 即 `(QUOTE BAR)`，意味着如果
`X` 是 `QUOTE`，该分支就会被执行……第二个分支同理（不过 `QUOTE` 会被
第一个子句捕获）。这不太可能是你真正想要的结果。

在 `CASE` 形式中，当你意指「若其他分支均失败则执行本分支」时，必须使用 `otherwise` 而非 `t`。当你意指「匹配
符号 T」而非「匹配任意值」时，必须使用 `((t) ...)`。当你意指「匹配
符号 NIL」而非「不匹配任何值」时，也必须使用 `((nil) ...)`。


因此，如果你希望将布尔值 `NIL` 与 `T` 分别映射到符号
 ` :BAR` 与 `:QUUX`，应当避免前一种写法，而采用后一种写法：

<div class='badcode'></div>

```lisp
(ecase x ; Bad: has no actual error case!
  (nil :bar)) ; Bad: matches nothing
  (t :quux)) ; Bad: matches anything
```

<div class='goodcode'></div>

```lisp
(ecase x ; Better: will actually catch non-booleans
  ((nil) :bar)) ; Better: matches NIL
  ((t) :quux)) ; Better: matches T
```

### 定义常量

-   你必须使用恰当的定义形式来定义常量值。

我们主要使用的 Lisp 系统 SBCL 非常挑剔，每当一个常量被重新定义为与其先前设置
不 `EQL` 的值时，就会发出一个条件信号。
在定义非数字、
字符或符号（包括布尔值与关键字）的变量时，你不得使用 `DEFCONSTANT`。相反，应始终
使用项目所推荐的替代方案。

<div class='badcode'></div>

```lisp
;; Two strings or lists with the same content might not be eql
(defconstant +google-url+ "https://www.google.com/")
(defconstant +valid-colors+ '(red green blue))
```

开源库可以使用 `ALEXANDRIA:DEFINE-CONSTANT` 来定义数字、字符与符号（包括布尔值与关键字）
之外的常量。你
可以使用 `:TEST` 关键字参数来指定一个相等性谓词。

<div class='goodcode'></div>

```lisp
;; Better, for Open-Source code:
(alexandria:define-constant +google-url+ "https://www.google.com/"
                            :test #'string=)
(alexandria:define-constant +valid-colors+ '(red green blue))
```

注意，在使用如 SBCL 或 CMUCL 这类会进行优化的实现时，以这种方式定义
常量会阻止其后的任何重新定义，除非 `UNINTERN`
该符号并重新编译它的所有客户。这可能会让在 REPL 上调试
或部署实时代码升级变得「有趣」。如果在考虑到计划内与计划外的代码
补丁之后，你的「常量」在服务器进程的整个生命周期内
可能并非始终不变，你就应当考虑改用 `DEFPARAMETER` 或 `DEFVAR`，或者
某种基于未来某个实现全局词法变量的库（而非 `DEFCONSTANT`）
构建的 `DEFINE-CONSTANT` 变体。在这些情况下，你可以保留
`+plus+` 约定，以表明该参数意图作为常量。



另请注意，`LOAD-TIME-VALUE` 或许能帮你免去定义
常量的需要。

### EVAL-WHEN

-   使用 `EVAL-WHEN` 时，你几乎总应使用全部
    `(:compile-toplevel :load-toplevel :execute)`。

Lisp 的求值发生在多个时点，其中一些是相互交错的。在编写宏时要注意
这一点。
[EVAL-WHEN considered harmful to your mental health](https://fare.livejournal.com/146698.html)。

综上所述那篇文章，除非你在进行真正高级的
宏编程，否则 `EVAL-WHEN` 中唯一有效的组合就是包含全部
 `(eval-when (:compile-toplevel :load-toplevel :execute) ...)` 

你必须使用 `(eval-when (:compile-toplevel :load-toplevel :execute) ...)` 
来定义将在宏中使用的函数、类型、类、常量、变量等。


省略 `:execute` 通常是个错误，因为这会阻止 `LOAD` 源代码
而非 fasl。省略 `:load-toplevel` 通常也是个错误
（除非是为了修改例如读取表与编译期设置），因为这会
阻止 `LOAD` 未来的文件，或交互式编译依赖于
编译期所产生效果的代码，除非当前文件是在
同一 Lisp 会话中 `COMPILE-FILE` 的。

关于变量，请注意：由于宏可能在运行展开后代码的同一进程中被展开，也可能不会，你不得依赖编译期
与运行期效果在另一时刻是可见或不可见的。然而
在宏中使用变量仍有合理的场景：


-   某些变量可能保存某种新定义所用的字典及其他元数据。如果此类元数据需在运行期和/或
    其他文件中可见，你必须确保该宏展开为这样的代码：除了在编译期完成注册外，
    还要在加载期将定义注册到那些元数据结构中。通常，你的
    顶层定义会展开为执行注册操作的代码。如果你的
    代码不在顶层展开，有时可以使用 `LOAD-TIME-VALUE` 来达到良好效果。在极端情况下，你可能
    不得不使用 `ASDF-FINALIZERS:EVAL-AT-TOPLEVEL`。



-   某些变量可能保存仅在编译期、于同一文件中使用的临时数据，并可在文件编译结束时清理。
    这类预定义变量包括 `*readtable*` 或保存当前优化设置的编译器内部
    变量。你通常可以使用 `ASDF` 的 `:AROUND-COMPILE` 钩子来管理
    这些既有及新增的变量。


### 路径名

-   Common Lisp 的路径名十分棘手。请注意其中的陷阱。使用 `UIOP`。

在 Common Lisp 中正确地处理路径名出人意料地困难。

`ASDF 3` 附带了一个可移植性库 `UIOP`，它让在 Common Lisp 中以可移植且
正确的方式处理路径名变得*容易得多*。你应当在适当时
使用它。

首先，要注意 Common Lisp 路径名语法（取决于你所使用的实现与操作系统）
与你所用操作系统的原生路径名语法之间的差异。Lisp
语法可能涉及对特殊字符（如 `#\.`、`#\*` 等）的转义，
此外，在字符串内部还需转义 `#\\ ` 与 `#\"`。相比之下，你的
操作系统的其他系统编程语言（shell、C、脚本
语言）可能只有一层对字符串的转义。可使用
`UIOP:NATIVE-NAMESTRING` 与 `UIOP:PARSE-NATIVE-NAMESTRING` 在
Lisp 与操作系统的路径名表示之间进行转换（在 SBCL
和 CCL 等良好实现上，这些函数工作良好，但在其他实现上，它们可能退回到
 `NAMESTRING` 与 `PARSE-NAMESTRING`，并且无法正确转义
通配符字符）。


其次，使用 `MERGE-PATHNAMES` 时，要警惕对 `HOST` 组件的处理，
这在非 Unix 平台（甚至在某些 Unix 实现上）都至关重要。你大概应当使用
 `UIOP:MERGE-PATHNAMES*` 或 `UIOP:SUBPATHNAME`，而非 `MERGE-PATHNAMES`，
尤其是当你的相对路径名预期受 Unix 或 Windows 方式影响时；
否则你可能会遇到奇怪的缺陷：在某些实现上，将相对路径名与绝对路径名合并时，
会用创建相对路径名时 `*DEFAULT-PATHNAME-DEFAULTS*` 的值中的主机
覆盖绝对路径名的主机。



第三，要注意 `DIRECTORY` 在处理通配符、子目录、符号链接等方面
在不同实现间并不具有可移植性。在这方面，`UIOP` 提供了
若干常见抽象来处理路径名，但做得并不完美。若需要完整的可移植方案，
可使用 IOLib——尽管其对 Windows 的支持相对滞后。


`LOGICAL-PATHNAME` 并非一种可移植的抽象，不应在可移植代码中使用。
许多实现在支持它们时存在缺陷；即便支持，SBCL 对其实现得非常好，
但会严格强制标准所允许的字符限制，从而限制了其适用场景。
其他实现允许此类路径名中出现任意字符，但这样做并不符合规范，
并且在许多方面彼此仍不兼容。你应当使用其他路径名抽象，
例如 `ASDF:SYSTEM-RELATIVE-PATHNAME`，或底层的 `UIOP:SUBPATHNAME`
与 `UIOP:PARSE-UNIX-NAMESTRING`。



最后，要注意路径可能会在你为应用程序构建 Lisp 镜像的时间，
与你从该镜像运行应用程序的时间之间发生变化。
你应当小心地重置镜像，以遗忘无关的构建期路径，
并根据当前环境变量重新初始化任何搜索路径。例如，`ASDF` 要求你
使用 `UIOP:CLEAR-CONFIGURATION` 重置其路径。`UIOP` 提供了在镜像被
转储前调用函数的钩子，用以重置或 `makunbound` 相关变量。


### SATISFIES

-   在类型说明符中使用 `SATISFIES` 子句时必须小心。

大多数 Common Lisp 实现无法基于 `SATISFIES` 类型进行优化，但
许多实现提供基于形如
`(AND FOO (SATISFIES BAR-P))` 类型的简单优化，其中 `AND` 子句的第一项描述
对象的结构（不含任何 `SATISFIES`），而第二项则是
`SATISFIES`。

<div class='badcode'></div>

```lisp
; Can't optimize
(deftype prime-number () (satisfies prime-number-p))
```

<div class='goodcode'></div>

```lisp
;; Can optimize based on the known type
(deftype prime-number () (and integer (satisfies prime-number-p))
```

然而，在 `DEFTYPE` 语言中，`AND` 并非像在表达式语言中那样是自左向右的短路
操作符；它是一个对称的连接符，允许对子项重新排序，并且
不保证短路求值。
因此，在上例中，你不能依赖对 `INTEGER` 性的测试
来防止向函数 `PRIME-NUMBER-P` 传入非整数
参数以检验其是否为该类型的实例。实现可能会、并且某些实现
*确实会*在编译期调用由 `SATISFIES` 指定的函数，来测试
各种相关对象。

正因如此，在 `SATISFIES` 子句中指定的任何函数都必须接受任意类型的对象作为参数，
并且必须在 `EVAL-WHEN` 中定义（以及它所使用的任何变量或所调用的函数）：


<div class='badcode'></div>

```lisp
;; Doesn't check if argument is an integer, and the function isn't defined at
;; compile time.
(defun prime-number-p (n)
  (let ((m (abs n)))
    (if (<= m *prime-number-cutoff*)
        (small-prime-number-p m)
        (big-prime-number-p m))))
```

<div class='goodcode'></div>

```lisp
;; Works when called at compile-time or passed a non-integer argument.
(eval-when (:compile-toplevel :load-toplevel :execute)
  (defun prime-number-p (n)
    (when (integerp n) ; Better
      (let ((m (abs n)))
        (if (<= m *prime-number-cutoff*)
            (small-prime-number-p m)
            (big-prime-number-p m))))))
```

特别地，上述意味着，Common Lisp 标准中所使用的
[example](https://www.lispworks.com/documentation/HyperSpec/Body/t_satisf.htm)
示例是有误的：`(and integer (satisfies evenp))` 并非一个安全、
符合规范的类型说明符，因为当传入非整数参数时，`EVENP` 会抛出
错误，而非返回 `NIL`。

最后，当你的 `DEFTYPE` 代码展开为带有一个动态生成函数的 `SATISFIES` 时，存在一个陷阱：


-   你无法控制实现何时会或不会展开一个 `DEFTYPE`。
-   展开本身不能包含函数定义或表达式语言中的任何代码。

-   你无法控制展开何时被使用，它可能发生在
    一个并未展开该定义的不同的进程中。

因此，你不能在类型展开时仅通过 `EVAL` 将该函数的创建作为展开的副作用。
解决方案是改用 `ASDF-FINALIZERS:EVAL-AT-TOPLEVEL`。请参阅关于
[EVAL](lispguide.md#eval) 的讨论中最后一点。


Common Lisp 难以令人满意。
