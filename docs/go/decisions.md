<!--* toc_depth: 3 *-->

# Go 风格决策

https://google.github.io/styleguide/go/decisions

[概览](index) | [指南](guide) | [决策](decisions) |
[最佳实践](best-practices)

<!--

-->

{% raw %}

**注意：** 本文是阐述 Google [Go Style](index) 的系列文档之一。
本文档是**[规范性的](index#normative) 但并非
[权威的](index#canonical)**，并且从属于
[核心风格指南](guide)。更多信息请参阅[概览](index#about)。

<a id="about"></a>

## 关于

本文档收录各项风格决策，旨在统一并为
Go 可读性导师所给出的建议提供标准的
指导、解释与示例。

本文档**并未穷尽一切**，会随时间不断扩充。若
[核心风格指南](guide) 与此处给出的建议相抵触，**以风格
指南为准**，并应据此更新本文档。

全套 Go Style 文档请参阅
[概览](https://google.github.io/styleguide/go#about)。

以下各节已从风格决策移至
指南的其他部分：

*   **MixedCaps**：参见 [guide#mixed-caps](guide#mixed-caps)
    <a id="mixed-caps"></a>

*   **Formatting**：参见 [guide#formatting](guide#formatting)
    <a id="formatting"></a>

*   **Line Length**：参见 [guide#line-length](guide#line-length)
    <a id="line-length"></a>

<a id="naming"></a>

## 命名

[核心风格指南](guide#naming) 中的命名一节给出了命名的
总体指导。以下各节针对命名中的具体方面作进一步
说明。

<a id="underscores"></a>

### 下划线

Go 中的名称通常不应包含下划线。这一原则有
三处例外：

1.  仅由生成的代码导入的包名可以包含
    下划线。关于如何选择多词包名，更多细节
    请参见[包名](#package-names)。
1.  `*_test.go` 文件中的 Test、Benchmark 和 Example
    函数名可以包含下划线。
1.  与操作系统或 cgo 交互的底层库可以
    复用标识符，[`syscall`] 便是如此。预计这种情况
    在大多数代码库中都非常罕见。

**注意：** 源代码的文件名并非 Go 标识符，不必
遵循这些约定。它们可以包含下划线。

[`syscall`]: https://pkg.go.dev/syscall#pkg-constants

<a id="package-names"></a>

### 包名

<a id="TOC-PackageNames"></a>

在 Go 中，包名必须简洁，且只使用小写字母和数字
（例如 [`k8s`]、[`oauth2`]）。多词包名应保持完整不拆分，
并全部小写（例如用 [`tabwriter`] 而非 `tabWriter`、`TabWriter` 或
`tab_writer`）。

应避免选择可能被常用局部变量名[shadowed]的
包名。例如，`usercount` 是比 `count` 更好的包名，
因为 `count` 是常用的变量名。

Go 包名不应带有下划线。如果需要导入名称中
含下划线的包（通常来自生成的代码或第三方代码），
则必须在导入时将其重命名为适合在 Go 代码中使用的名称。

这一规则有一处例外：仅由生成的代码导入的包名
可以包含下划线。具体示例包括：

*   使用 `_test` 后缀编写单元测试，只检验包
    的已导出 API（package `testing` 称这些测试为
    ["black box tests"](https://pkg.go.dev/testing)）。例如，包
    `linkedlist` 必须把其黑盒单元测试定义在名为
    `linkedlist_test`（而非 `linked_list_test`）的包中

*   对于指定功能测试或集成测试的包，使用下划线
    及 `_test` 后缀。例如，链表的服务
    集成测试可命名为 `linked_list_service_test`

*   使用 `_test` 后缀编写
    [包级文档示例](https://go.dev/blog/examples)

[`tabwriter`]: https://pkg.go.dev/text/tabwriter
[`k8s`]: https://pkg.go.dev/k8s.io/client-go/kubernetes
[`oauth2`]: https://pkg.go.dev/golang.org/x/oauth2
[shadowed]: best-practices#shadowing

应避免使用 `util`、`utility`、`common`、`helper`、
`model`、`testhelper` 之类缺乏信息量的包名，以免包的
使用者想要在[导入时重命名](#import-renaming)。请参见：

*   [关于所谓「utility packages」的指导](best-practices#util-packages)
*   [Go Tip #97: What's in a Name](https://google.github.io/styleguide/go/index.html#gotip)
*   [Go Tip #108: The Power of a Good Package Name](https://google.github.io/styleguide/go/index.html#gotip)

当导入的包被重命名时（例如
`import foopb "path/to/foo_go_proto"`），该包的局部名称必须
遵守上述规则，因为局部名称决定了文件中如何引用
包内的符号。若同一导入在多个文件中被重命名，
尤其是在同一个或相邻的包中，应尽可能使用
相同的局部名称以保持一致。

> **注意：** 以下情形不受此规则约束：
>
> *   生成的 Protocol Buffer API
> *   标准库与操作系统对接的接口，例如
>     https://pkg.go.dev/syscall#pkg-constants
>
> **人工编写的代码适用更高的标准。**

另见：[关于包名的 Go 博客文章](https://go.dev/blog/package-names)。

<a id="receiver-names"></a>

### 接收者名称

<a id="TOC-ReceiverNames"></a>

[Receiver] 变量名必须：

*   简短（通常为一到两个字母）
*   是该类型本身的缩写
*   对该类型的每个接收者都保持一致
*   不用下划线；若未使用则省略名称

较长的名称                   | 更好的名称
--------------------------- | -------------------------
`func (tray Tray)`          | `func (t Tray)`
`func (info *ResearchInfo)` | `func (ri *ResearchInfo)`
`func (this *ReportWriter)` | `func (w *ReportWriter)`
`func (self *Scanner)`      | `func (s *Scanner)`

[Receiver]: https://golang.org/ref/spec#Method_declarations

<a id="constant-names"></a>

### 常量名

常量名必须与 Go 中所有其他名称一样使用 [MixedCaps]。（[Exported]
常量以大写开头，而未导出的常量以
小写开头。）即便这与其他语言中的约定相悖，也依然适用。
常量名不应由其值派生，而应说明
该值所表示的含义。

<div class='goodcode'></div>

```go
const MaxPacketSize = 512

const (
    ExecuteBit = 1 << iota
    WriteBit
    ReadBit
)
```

[MixedCaps]: guide#mixed-caps
[Exported]: https://tour.golang.org/basics/3

不要使用非 MixedCaps 的常量名，也不要使用带 `K` 前缀的常量。

<div class='badcode'></div>

```go
const MAX_PACKET_SIZE = 512
const kMaxBufferSize = 1024
const KMaxUsersPergroup = 500
```

应依据常量的作用而非其值来命名。如果某个常量
除了其值之外并无作用，那么就没有必要
将它定义为常量。

<div class='badcode'></div>

```go
const Twelve = 12

const (
    UserNameColumn = "username"
    GroupColumn    = "group"
)
```

> **注意：** 以下情形不受此规则约束：
>
> *   生成的 Protocol Buffer API
> *   标准库与操作系统对接的接口，例如
>     https://pkg.go.dev/syscall#pkg-constants
>
> **人工编写的代码适用更高的标准。**

<a id="initialisms"></a>

### 首字母缩略词

<a id="TOC-Initialisms"></a>

名称中作为首字母缩略词或缩写词的单词（例如 `URL` 和 `NATO`）应
保持相同的大小写。`URL` 应写作 `URL` 或 `url`（如 `urlPony` 或
`URLPony`），绝不可写作 `Url`。一般规则是，标识符（例如 `ID` 和 `DB`）
的大小写也应与其在英语散文中的用法相近。

*   对于含多个首字母缩略词的名称（例如 `XMLAPI`，因为它包含 `XML`
    和 `API`），同一个缩略词内的每个字母应保持一致的大小写，
    但名称中各缩略词之间不必采用相同的大小写。
*   对于含带小写字母的缩略词的名称（例如 `DDoS`、
    `iOS`、`gRPC`），缩略词应按标准散文中的写法呈现，
    除非为了 [exportedness] 需要改动首字母。
    在这些情况下，整个缩略词应保持同样的大小写（例如 `ddos`、
    `IOS`、`GRPC`）。

[exportedness]: https://golang.org/ref/spec#Exported_identifiers

<!-- Keep this table narrow. If it must grow wider, replace with a list. -->

英语用法     | 作用域      | 正确     | 不正确
------------- | ---------- | -------- | --------------------------------------
XML API       | 导出的     | `XMLAPI` | `XmlApi`, `XMLApi`, `XmlAPI`, `XMLapi`
XML API       | 未导出的   | `xmlAPI` | `xmlapi`, `xmlApi`
iOS           | 导出的     | `IOS`    | `Ios`, `IoS`
iOS           | 未导出的   | `iOS`    | `ios`
gRPC          | 导出的     | `GRPC`   | `Grpc`
gRPC          | 未导出的   | `gRPC`   | `grpc`
DDoS          | 导出的     | `DDoS`   | `DDOS`, `Ddos`
DDoS          | 未导出的   | `ddos`   | `dDoS`, `dDOS`
ID            | 导出的     | `ID`     | `Id`
ID            | 未导出的   | `id`     | `iD`
DB            | 导出的     | `DB`     | `Db`
DB            | 未导出的   | `db`     | `dB`
Txn           | 导出的     | `Txn`    | `TXN`

> **注意：** 以下情形不受此规则约束：
>
> *   生成的 Protocol Buffer API
> *   标准库与操作系统对接的接口，例如
>     https://pkg.go.dev/syscall#pkg-constants
>
> **人工编写的代码适用更高的标准。**

<a id="getters"></a>

### getter

<a id="TOC-Getters"></a>

函数名与方法名不应使用 `Get` 或 `get` 前缀，除非
底层概念本身就使用「get」一词（例如 HTTP GET）。应优先
直接用名词开头，例如用 `Counts` 而非 `GetCounts`。

如果函数需要执行复杂的计算或发起远程
调用，可以用 `Compute` 或 `Fetch` 之类的词替代 `Get`，
以便让读者明白该函数调用可能耗时，并且
可能阻塞或失败。

> **注意：** 以下情形不受此规则约束：
>
> *   生成的 Protocol Buffer API
> *   标准库与操作系统对接的接口，例如
>     https://pkg.go.dev/syscall#pkg-constants
>
> **人工编写的代码适用更高的标准。**

<a id="variable-names"></a>

### 变量名

<a id="TOC-VariableNames"></a>

一般的经验法则是，名称的长度应与其作用域的
大小成正比，与该作用域内的使用次数成反比。
在文件作用域创建的变量可能需要多个单词，而仅
作用于单个内层块的变量可能只需一个单词，甚至
一两个字符，以保持代码清晰并避免多余的
信息。

下面给出一个粗略的基准。这些数字指引并非严格规则。
请根据上下文、[clarity] 和 [concision] 自行判断。

*   小作用域是指执行一两个小操作的作用域，比如
    1-7 行。
*   中等作用域是指几个小操作或一个较大的操作，比如 8-15 行。
*   大作用域是指一个或几个较大的操作，比如 15-25 行。
*   超大作用域是指跨度超过一页的任何作用域（比如超过
    25 行）。

[clarity]: guide#clarity
[concision]: guide#concision

某个名称在小作用域内可能十分清晰（例如用 `c` 表示计数器），
但在更大的作用域中就可能不够用，需要补充说明，
以便在代码稍后处提醒读者它的用途。若某个作用域中
变量很多，或者变量表示的是相近的值或概念，
可能就需要比该作用域所暗示的更长的变量名。

概念的具体性同样有助于让变量名保持简洁。
例如，假设只使用了一个数据库，那么像 `db` 这样
通常只留给极小作用域的短变量名，即使作用域
非常大也依然十分清晰。在这种情况下，按作用域大小
来看，单词 `database` 或许也可以接受，但并非必需，
因为 `db` 是该词非常常见的简写，几乎没有其他
解释。

局部变量的名称应反映它所包含的内容以及在当前上下文中的
使用方式，而不是值的来源。例如，
最佳局部变量名往往与结构体字段或 Protocol Buffer
字段名并不相同。

一般而言：

*   像 `count` 或 `options` 这样的单词名称是很好的起点。
*   可以添加额外的词来区分相近的名称，例如
    `userCount` 和 `projectCount`。
*   不要单纯为了少打字而删去字母。例如 `Sandbox`
    优于 `Sbx`，对导出的名称尤其如此。
*   在大多数变量名中省略 [types and type-like words]。
    *   对于数值，`userCount` 是比 `numUsers` 或
        `usersInt` 更好的名称。
    *   对于切片，`users` 是比 `userSlice` 更好的名称。
    *   若作用域中同一值有两种版本，加上类似类型的
        限定词是可以接受的，例如可以把输入存放在
        `ageString` 中，而用 `age` 表示解析后的值。
*   省略那些从 [surrounding context] 即可看出的词。例如，在
    `UserCount` 方法的实现中，名为 `userCount` 的局部变量
    很可能多余；`count`、`users` 甚至 `c` 都同样
    可读。

[types and type-like words]: #repetitive-with-type
[surrounding context]: #repetitive-in-context

<a id="v"></a>

#### 单字母变量名

单字母变量名有助于减少[重复](#repetition)，但也可能
让代码无谓地晦涩。应只在完整单词一目了然、
且写出完整单词会显得重复时才
使用。

一般而言：

*   对于 [method receiver variable]，首选一个或两个字母的
    名称。
*   为常见类型使用熟悉的变量名通常很有帮助：
    *   用 `r` 表示 `io.Reader` 或 `*http.Request`
    *   用 `w` 表示 `io.Writer` 或 `http.ResponseWriter`
*   单字母标识符可用作整型循环变量，尤其是
    索引（例如 `i`）和坐标（例如 `x` 和 `y`）。
*   当作用域很短时，缩写也可以作为循环标识符，
    例如 `for _, n := range nodes { ... }`。

[method receiver variable]: #receiver-names

<a id="repetition"></a>

### 重复

<!--
Note to future editors:

Do not use the term "stutter" to refer to cases when a name is repetitive.
-->

一段 Go 源代码应避免不必要的重复。常见来源之一是
重复的名称，这类名称往往包含多余的词，或重复了
其上下文或类型。如果相同或相似的代码片段在相近位置
多次出现，代码本身也可能变得无谓地重复。

重复命名可能有多种形式，包括：

<a id="repetitive-with-package"></a>

#### 包名与导出的符号名

为导出的符号命名时，包名在你的包之外始终可见，
因此应减少或消除两者之间的冗余信息。如果某个包
只导出一个类型，且该类型以包本身命名，那么若需要
构造函数，其规范名称应为 `New`。

> **示例：** 重复的名称 -> 更好的名称
>
> *   `widget.NewWidget` -> `widget.New`
> *   `widget.NewWidgetWithName` -> `widget.NewWithName`
> *   `db.LoadFromDatabase` -> `db.Load`
> *   `goatteleportutil.CountGoatsTeleported` -> `gtutil.CountGoatsTeleported`
>     或 `goatteleport.Count`

<a id="repetitive-with-type"></a>

#### 变量名与类型

编译器始终知道变量的类型，而且在大多数情况下，
读者通过变量的使用方式也能清楚其类型。只有当
同一个值在同一作用域中出现两次时，才有必要
明确变量的类型。

重复的名称                     | 更好的名称
----------------------------- | ----------------------
`var numUsers int`            | `var users int`
`var nameString string`       | `var name string`
`var primaryProject *Project` | `var primary *Project`

如果一个值以多种形式出现，可以用 `raw`、`parsed` 之类的
额外单词，或用其底层表示来加以区分：

<div class='goodcode'></div>

```go
limitRaw := r.FormValue("limit")
limit, err := strconv.Atoi(limitRaw)
```

<div class='goodcode'></div>

```go
limitStr := r.FormValue("limit")
limit, err := strconv.Atoi(limitStr)
```

<a id="repetitive-in-context"></a>

#### 外部上下文与局部名称

包含其周围上下文信息的名称往往只会徒增噪声，
并无益处。包名、方法名、类型名、函数名、
导入路径甚至文件名都能提供上下文，自动为其中的
所有名称加上限定。

<div class='badcode'></div>

```go
// In package "ads/targeting/revenue/reporting"
type AdsTargetingRevenueReport struct{}

func (p *Project) ProjectName() string
```

<div class='goodcode'></div>

```go
// In package "ads/targeting/revenue/reporting"
type Report struct{}

func (p *Project) Name() string
```

<div class='badcode'></div>

```go
// In package "sqldb"
type DBConnection struct{}
```

<div class='goodcode'></div>

```go
// In package "sqldb"
type Connection struct{}
```

<div class='badcode'></div>

```go
// In package "ads/targeting"
func Process(in *pb.FooProto) *Report {
    adsTargetingID := in.GetAdsTargetingID()
}
```

<div class='goodcode'></div>

```go
// In package "ads/targeting"
func Process(in *pb.FooProto) *Report {
    id := in.GetAdsTargetingID()
}
```

重复通常应在符号使用者的语境中评估，
而不应孤立地看待。例如，下面的代码中有许多名称
在某些情况下或许没问题，但在上下文里显得多余：

<div class='badcode'></div>

```go
func (db *DB) UserCount() (userCount int, err error) {
    var userCountInt64 int64
    if dbLoadError := db.LoadFromDatabase("count(distinct users)", &userCountInt64); dbLoadError != nil {
        return 0, fmt.Errorf("load user count: %s", dbLoadError)
    }
    userCount = int(userCountInt64)
    return userCount, nil
}
```

相反，那些从上下文或用法即可看出的名称信息
往往可以省略：

<div class='goodcode'></div>

```go
func (db *DB) UserCount() (int, error) {
    var count int64
    if err := db.Load("count(distinct users)", &count); err != nil {
        return 0, fmt.Errorf("load user count: %s", err)
    }
    return int(count), nil
}
```

<a id="commentary"></a>

## 注释

围绕注释的各项约定（包括该注释什么、采用何种
风格、如何提供可运行示例等）旨在改善阅读
公开 API 文档时的体验。更多信息请参阅
[Effective Go](http://golang.org/doc/effective_go.html#commentary)
以了解更多。

最佳实践文档中关于 [documentation conventions] 的章节
对此作了进一步讨论。

**最佳实践：** 在开发和代码评审期间使用 [doc preview]，
以查看文档和可运行示例是否有用、是否按你期望
的方式呈现。

**提示：** Godoc 几乎不使用特殊格式；列表和代码片段
通常应缩进以避免自动换行。除缩进之外，
一般应避免使用修饰。

[doc preview]: best-practices#documentation-preview
[documentation conventions]:  best-practices#documentation-conventions

<a id="comment-line-length"></a>

### 注释行长度

Go 中的注释没有固定的 [line length]。

[line length]: guide#line-length

长注释行应换行，以确保源码在不自动
换行的工具中仍可读。若拿不准在哪里换行，
80 或 100 列是常见的选择。不过，这并非硬性
界限；有些情况下拆开长字面文本反而有害。
对于换行发生的具体列宽没有要求。
应尽量在同一文件内保持[一致](guide#consistency)。

关于注释的更多内容，请参阅 [post from The Go Blog on documentation]。

[post from The Go Blog on documentation]: https://blog.golang.org/godoc-documenting-go-code

<div class='goodcode'></div>

```text
// This is a comment paragraph.
// The length of individual lines doesn't matter in Godoc;
// but the choice of wrapping makes it easy to read on narrow screens.
//
// Don't worry too much about the long URL:
// https://supercalifragilisticexpialidocious.example.com:8080/Animalia/Chordata/Mammalia/Rodentia/Geomyoidea/Geomyidae/
//
// Similarly, if you have other information that is made awkward
// by too many line breaks, use your judgment and include a long line
// if it helps rather than hinders.
```

应避免把大量文字挤在单独一行里的注释，这会带来
糟糕的阅读体验。

<div class='badcode'></div>

```text
// This is a comment paragraph. While some code editors and viewers will wrap the paragraph for the reader, others will display a very long line that will overflow most windows and require users to scroll horizontally. In addition, even on a screen capable of displaying the entire line, it is easier to read a narrower paragraph than very wide one.
//
// Don't worry too much about the long URL:
// https://supercalifragilisticexpialidocious.example.com:8080/Animalia/Chordata/Mammalia/Rodentia/Geomyoidea/Geomyidae/
```

<a id="doc-comments"></a>

### 文档注释

<a id="TOC-DocComments"></a>

所有顶层的导出名称都必须有文档注释，行为或含义
不明显的未导出类型或函数声明也应如此。这些注释
应是 [full sentences]，并以所描述的对象的名称开头。
可以在名称前加冠词（"a"、"an"、"the"），使其读起来
更自然。

<div class='goodcode'></div>

```go
// A Request represents a request to run a command.
type Request struct { ...

// Encode writes the JSON encoding of req to w.
func Encode(w io.Writer, req *Request) { ...
```

文档注释会出现在 [Godoc](https://pkg.go.dev/) 中，并由 IDE
呈现，因此应面向所有使用该包的人来撰写。

[full sentences]: #comment-sentences

文档注释作用于紧随其后的符号；若出现在结构体中，
则作用于该组字段。

<div class='goodcode'></div>

```go
// Options configure the group management service.
type Options struct {
    // General setup:
    Name  string
    Group *FooGroup

    // Dependencies:
    DB *sql.DB

    // Customization:
    LargeGroupThreshold int // optional; default: 10
    MinimumMembers      int // optional; default: 2
}
```

**最佳实践：** 如果为未导出的代码编写文档注释，应遵循与
导出代码相同的惯例（即以未导出的名称开头）。
这样日后只要在注释和代码中把未导出的名称替换为
新导出的名称，便可轻松将其导出。

<a id="comment-sentences"></a>

### 注释句子

<a id="TOC-CommentSentences"></a>

完整句子形式的注释应像标准英语句子一样大写并
加标点。（作为例外，若其他方面表意清楚，也可以
以未大写的标识符名称开头。这类情形最好只出现在
段落开头。）

句子片段形式的注释在标点和大小写上没有
这类要求。

[Documentation comments] 应始终是完整句子，因此也应
始终大写并加标点。简单的行尾注释（尤其是结构体
字段的注释）可以是简单短语，默认以字段名作为
主语。

<div class='goodcode'></div>

```go
// A Server handles serving quotes from the collected works of Shakespeare.
type Server struct {
    // BaseDir points to the base directory under which Shakespeare's works are stored.
    //
    // The directory structure is expected to be the following:
    //   {BaseDir}/manifest.json
    //   {BaseDir}/{name}/{name}-part{number}.txt
    BaseDir string

    WelcomeMessage  string // displayed when user logs in
    ProtocolVersion string // checked against incoming requests
    PageLength      int    // lines per page when printing (optional; default: 20)
}
```

[Documentation comments]: #doc-comments

<a id="examples"></a>

### 示例

<a id="TOC-Examples"></a>

包应清楚地记录其预期用法。尽量提供
[runnable example]；示例会显示在 Godoc 中。可运行示例
应放在测试文件中，而非生产源文件中。参见此示例（[Godoc]、[source]）。

[runnable example]: http://blog.golang.org/examples
[Godoc]: https://pkg.go.dev/time#example-Duration
[source]: https://cs.opensource.google/go/go/+/HEAD:src/time/example_test.go

如果无法提供可运行示例，也可以在代码注释中给出
示例代码。与注释中的其他代码和命令行片段一样，
它应遵循标准的格式约定。

<a id="named-result-parameters"></a>

### 具名结果参数

<a id="TOC-NamedResultParameters"></a>

为参数命名时，应考虑函数签名在 Godoc 中的呈现
方式。函数本身的名称与结果参数的类型往往
已经足够清楚。

<div class='goodcode'></div>

```go
func (n *Node) Parent1() *Node
func (n *Node) Parent2() (*Node, error)
```

如果函数返回两个或更多相同类型的参数，加上名称
会很有帮助。

<div class='goodcode'></div>

```go
func (n *Node) Children() (left, right *Node, err error)
```

如果调用方必须对特定的结果参数采取行动，为其命名
有助于提示该行动是什么：

<div class='goodcode'></div>

```go
// WithTimeout returns a context that will be canceled no later than d duration
// from now.
//
// The caller must arrange for the returned cancel function to be called when
// the context is no longer needed to prevent a resource leak.
func WithTimeout(parent Context, d time.Duration) (ctx Context, cancel func())
```

在上面的代码中，取消是调用方必须采取的一项特定
操作。然而，若结果参数只写成 `(Context, func())`，
"cancel function" 指的是什么就不清楚了。

当名称会造成[不必要的重复](#repetitive-with-type)时，
请勿使用具名结果参数。

<div class='badcode'></div>

```go
func (n *Node) Parent1() (node *Node)
func (n *Node) Parent2() (node *Node, err error)
```

不要为了避免在函数内部声明变量而给结果参数
命名。这种做法以实现上略微简洁为代价，换来
不必要的 API 冗长。

[Naked returns] 仅在很小的函数中可以接受。一旦函数
达到中等规模，就应显式写出返回值。同样地，
不要仅仅因为能使用裸返回就给结果参数命名。
[清晰](guide#clarity) 始终比在函数里省下几行
更重要。

如果某个结果参数的值必须在延迟闭包中修改，
那么为其命名始终是可以接受的。

> **提示：** 在函数签名中，类型往往比名称更清晰。
> [GoTip #38: Functions as Named Types] 就说明了这一点。
>
> 在上面的 [`WithTimeout`] 中，真实代码在结果参数列表里
> 使用 [`CancelFunc`] 而非原始的 `func()`，几乎不费
> 力气便可写出文档。

[Naked returns]: https://tour.golang.org/basics/7
[GoTip #38: Functions as Named Types]: https://google.github.io/styleguide/go/index.html#gotip
[`WithTimeout`]: https://pkg.go.dev/context#WithTimeout
[`CancelFunc`]: https://pkg.go.dev/context#CancelFunc

<a id="package-comments"></a>

### 包注释

<a id="TOC-PackageComments"></a>

包注释必须紧挨在 package 子句上方，注释与包名之间
不得有空行。示例：

<div class='goodcode'></div>

```go
// Package math provides basic constants and mathematical functions.
//
// This package does not guarantee bit-identical results across architectures.
package math
```

每个包必须有且仅有一个包注释。如果一个包由
多个文件组成，应恰好有一个文件带有包注释。

`main` 包的注释形式略有不同：BUILD 文件中 `go_binary`
规则的名称取代了包名的位置。

<div class='goodcode'></div>

```go
// The seed_generator command is a utility that generates a Finch seed file
// from a set of JSON study configs.
package main
```

只要二进制文件的名称与 BUILD 文件中的写法完全一致，
其他注释风格也可以。当二进制名称是第一个词时，
即使它与命令行调用中的拼写并不严格一致，
也必须将其首字母大写。

<div class='goodcode'></div>

```go
// Binary seed_generator ...
// Command seed_generator ...
// Program seed_generator ...
// The seed_generator command ...
// The seed_generator program ...
// Seed_generator ...
```

提示：

*   示例命令行调用和 API 用法都是有用的文档。
    为符合 Godoc 格式，请缩进包含代码的注释行。

*   如果没有明显的主文件，或者包注释特别长，
    可以把文档注释放在一个名为 `doc.go` 的文件中，
    该文件只包含该注释和 package 子句。

*   可以使用多行注释代替多个单行注释。
    这主要在文档中含有便于从源文件复制粘贴的
    段落时有用，例如示例命令行（针对二进制文件）
    和模板示例。

    <div class='goodcode'></div>

    ```go
    /*
    The seed_generator command is a utility that generates a Finch seed file
    from a set of JSON study configs.

        seed_generator *.json | base64 > finch-seed.base64
    */
    package template
    ```

*   面向维护者、且适用于整个文件的注释通常
    放在 import 声明之后。它们不会显示在 Godoc 中，
    也不受上述包注释规则的约束。

<a id="imports"></a>

## 导入

<a id="TOC-Imports"></a>

<a id="import-renaming"></a>

### 导入重命名

包导入通常不应重命名，但有些情况下必须重命名，
或者重命名能提升可读性。

导入包的局部名称必须遵循
[关于包命名的指导](#package-names)，包括禁止使用下划线
和大写字母。应尽量保持[一致](guide#consistency)：
对同一个导入包始终使用相同的
局部名称。

为避免与其他导入发生名称冲突，导入的包*必须*
重命名。（由此可推知，[好的包名](#package-names)
本不应需要重命名。）发生名称冲突时，应优先
重命名最局部的或项目特有的导入。

生成的 Protocol Buffer 包*必须*重命名，以去掉
名称中的下划线，其局部名称还必须带 `pb` 后缀。
更多信息请参阅
[proto 与 stub 最佳实践](best-practices#import-protos)。

<div class='goodcode'></div>

```go
import (
    foosvcpb "path/to/package/foo_service_go_proto"
)
```

最后，对于导入的、非自动生成的包，如果其名称
缺乏信息量（例如 `util` 或 `v1`），*可以*重命名。
请谨慎使用：若使用该包的代码已提供足够的上下文，
则不要重命名。可能时，应优先重构该包本身，改用更合适的名称。

<div class='goodcode'></div>

```go
import (
    core "github.com/kubernetes/api/core/v1"
    meta "github.com/kubernetes/apimachinery/pkg/apis/meta/v1beta1"
)
```

如果需要导入的包，其名称与你想使用的常见局部变量名
冲突（例如 `url`、`ssh`），而你又希望重命名
该包，首选做法是使用 `pkg` 后缀（例如 `urlpkg`）。
请注意，局部变量有可能遮蔽包；只有当此类变量
处于作用域内、而该包仍需被使用时，
才有必要进行这种重命名。

<a id="import-grouping"></a>

### 导入分组

导入应按以下顺序分为若干组：

1.  标准库包

1.  其他（项目和 vendored）包

1.  Protocol Buffer 导入（例如 `foopb "path/to/foo_go_proto"`）

1.  用于[副作用](https://go.dev/doc/effective_go#blank_import)的导入
    （例如 `_ "path/to/package"`）

<div class='goodcode'></div>

```go
package main

import (
    "fmt"
    "hash/adler32"
    "os"

    "github.com/dsnet/compress/flate"
    "golang.org/x/text/encoding"
    "google.golang.org/protobuf/proto"

    foopb "myproj/foo/proto/proto"

    _ "myproj/rpc/protocols/dial"
    _ "myproj/security/auth/authhooks"
)
```

<a id="import-blank"></a>

### 空白导入（`import _`）

<a id="TOC-ImportBlank"></a>

仅为副作用而导入的包（使用 `import _ "package"`
语法）只能在 main 包中导入，或者在需要它们的
测试中导入。

此类包的一些示例包括：

*   [time/tzdata](https://pkg.go.dev/time/tzdata)

*   图像处理代码中的 [image/jpeg](https://pkg.go.dev/image/jpeg)

应避免在库包中使用空白导入，即使该库间接
依赖它们也是如此。把副作用导入限制在 main 包中
有助于控制依赖，也便于编写依赖不同导入的测试，
而不会产生冲突或白白增加构建开销。

以下情形是此规则仅有的例外：

*   可以使用空白导入来绕过 [nogo static checker] 中
    对被禁用导入的检查。

*   在使用 `//go:embed` 编译指令的源文件中，可以
    对 [embed](https://pkg.go.dev/embed) 包使用空白导入。

**提示：** 如果你创建的库包在生产环境中间接依赖了
副作用导入，请记录其预期用法。

[nogo static checker]: https://github.com/bazelbuild/rules_go/blob/master/go/nogo.rst

<a id="import-dot"></a>

### 点导入（`import .`）

<a id="TOC-ImportDot"></a>

`import .` 形式是一项语言特性，允许把另一个包导出的
标识符不加限定地带入当前包。更多内容请参阅
[语言规范](https://go.dev/ref/spec#Import_declarations)。

**不要**在 Google 代码库中使用这一特性；它会让人更难
判断某项功能来自何处。

<div class='badcode'></div>

```go
package foo_test

import (
    "bar/testutil" // also imports "foo"
    . "foo"
)

var myThing = Bar() // Bar defined in package foo; no qualification needed.
```

<div class='goodcode'></div>

```go
package foo_test

import (
    "bar/testutil" // also imports "foo"
    "foo"
)

var myThing = foo.Bar()
```

<a id="errors"></a>

## 错误

<a id="returning-errors"></a>

### 返回错误

<a id="TOC-ReturningErrors"></a>

使用 `error` 表示函数可能失败。按照惯例，`error` 是
最后一个结果参数。

<div class='goodcode'></div>

```go
func Good() error { /* ... */ }
```

返回 `nil` 错误是惯用的方式，用来表示一次本可能
失败的操作已成功。如果函数返回错误，除非另有
明确说明，调用方必须把所有非错误返回值视为
未指定。通常这些非错误返回值是其零值，但
不能想当然。

<div class='goodcode'></div>

```go
func GoodLookup() (*Result, error) {
    // ...
    if err != nil {
        return nil, err
    }
    return res, nil
}
```

返回错误的导出函数应使用 `error` 类型来返回。
具体错误类型容易引发微妙的缺陷：具体的 `nil` 指针
可能被包装进接口，从而变成非 nil 值（参见
[Go FAQ 中关于该问题的条目][nil error]）。

<div class='badcode'></div>

```go
func Bad() *os.PathError { /*...*/ }
```

**提示：** 接受 [`context.Context`] 参数的函数通常应
返回 `error`，以便调用方判断函数运行期间
context 是否被取消。

[nil error]: https://golang.org/doc/faq#nil_error

<a id="error-strings"></a>

### 错误字符串

<a id="TOC-ErrorStrings"></a>

错误字符串不应大写（除非以导出名称、专有名词或
首字母缩略词开头），也不应以标点结尾。这是因为
错误字符串在打印给用户之前，通常会出现在
其他上下文中。

<div class='badcode'></div>

```go
err := fmt.Errorf("Something bad happened.")
```

<div class='goodcode'></div>

```go
err := fmt.Errorf("something bad happened")
```

另一方面，完整显示消息的风格（日志、测试失败、
API 响应或其他 UI）视情况而定，但通常应大写，
除非直接引用未导出的标识符（例如在
[测试失败](#identify-the-function) 中）。

<div class='goodcode'></div>

```go
log.Infof("Operation aborted: %v", err)
log.Errorf("Operation aborted: %v", err)
t.Errorf("Op(%q) failed unexpectedly; err=%v", args, err)
t.Errorf("arrangeInputs(%q) = %v, want %v", args, got, want)
t.Fatalf("Connection failed: %v", err)
```

<a id="handle-errors"></a>

### 处理错误

<a id="TOC-HandleErrors"></a>

遇到错误的代码应有意识地选择如何处理它。
用 `_` 变量丢弃错误通常并不合适。
如果函数返回错误，请执行以下之一：

*   立即处理并解决该错误。
*   把错误返回给调用方。
*   在特殊情形下，调用 [`log.Fatal`]，或者（万不得已时）
    `panic`。

**注意：** `log.Fatalf` 并非标准库中的 log。请参见 [#logging]。

在极少数适合忽略或丢弃错误的情形下（例如
调用文档注明永不失败的 [`(*bytes.Buffer).Write`]），
应附上注释说明这样做为何安全。

<div class='goodcode'></div>

```go
var b *bytes.Buffer

n, _ := b.Write(p) // never returns a non-nil error
```

关于错误处理的更多讨论和示例，请参阅
[Effective Go](http://golang.org/doc/effective_go.html#errors) 和
[最佳实践](best-practices.md#error-handling)。

[`(*bytes.Buffer).Write`]: https://pkg.go.dev/bytes#Buffer.Write

<a id="in-band-errors"></a>

### 带内错误

<a id="TOC-In-Band-Errors"></a>

在 C 及类似语言中，函数常通过返回 -1、
null 或空字符串来表示错误或缺失结果。这被称为
带内错误处理。

<div class='badcode'></div>

```go
// Lookup returns the value for key or -1 if there is no mapping for key.
func Lookup(key string) int
```

未检查带内错误值可能导致缺陷，并把错误
归咎于错误的函数。

<div class='badcode'></div>

```go
// The following line returns an error that Parse failed for the input value,
// whereas the failure was that there is no mapping for missingKey.
return Parse(Lookup(missingKey))
```

Go 对多返回值的支持提供了更好的解决方案（参见
[Effective Go section on multiple returns]）。与其要求调用方
检查带内错误值，不如让函数返回一个额外的值，
用以表明其余返回值是否有效。在无需解释时，
这个返回值可以是 error 或布尔值，并且应是
最后一个返回值。

<div class='goodcode'></div>

```go
// Lookup returns the value for key or ok=false if there is no mapping for key.
func Lookup(key string) (value string, ok bool)
```

这一 API 可防止调用方错误地写出 `Parse(Lookup(key))`；
由于 `Lookup(key)` 有 2 个输出，这会引发编译期错误。

以这种方式返回错误有助于形成更健壮、更明确的错误处理：

<div class='goodcode'></div>

```go
value, ok := Lookup(key)
if !ok {
    return fmt.Errorf("no value for %q", key)
}
return Parse(value)
```

某些标准库函数（例如 `strings` 包中的函数）会返回
带内错误值。这极大简化了字符串处理代码，代价是
要求程序员更加细心。一般而言，Google 代码库中的
Go 代码应返回额外的值来表示错误。

[Effective Go section on multiple returns]: http://golang.org/doc/effective_go.html#multiple-returns

<a id="indent-error-flow"></a>

### 缩进错误处理流程

<a id="TOC-IndentErrorFlow"></a>

在继续处理其余代码之前先处理错误。这能让读者
迅速找到正常路径，从而提升代码的可读性。
同样的逻辑也适用于任何先测试条件、再以终止条件
结束的块（例如 `return`、`panic`、`log.Fatal`）。

终止条件未满足时才会运行的代码应出现在 `if`
块之后，而不应缩进放在 `else` 子句中。

<div class='goodcode'></div>

```go
if err != nil {
    // error handling
    return // or continue, etc.
}
// normal code
```

<div class='badcode'></div>

```go
if err != nil {
    // error handling
} else {
    // normal code that looks abnormal due to indentation
}
```

> **提示：** 如果某个变量要在超过几行代码中使用，
> 通常就不值得采用带初始化语句的 `if` 风格。在这种情况下，
> 通常更好的做法是把声明移出来，使用标准的 `if`
> 语句：
>
> <div class='goodcode'></div>
>
> ```go
> x, err := f()
> if err != nil {
>   // error handling
>   return
> }
> // lots of code that uses x
> // across multiple lines
> ```
>
> <div class='badcode'></div>
>
> ```go
> if x, err := f(); err != nil {
>   // error handling
>   return
> } else {
>   // lots of code that uses x
>   // across multiple lines
> }
> ```

参见 [Go Tip #1: Line of Sight] 以及
[TotT：通过减少嵌套来降低代码复杂度](https://testing.googleblog.com/2017/06/code-health-reduce-nesting-reduce.html)
以了解更多细节。

[Go Tip #1: Line of Sight]: https://google.github.io/styleguide/go/index.html#gotip

<a id="language"></a>

## 语言

<a id="literal-formatting"></a>

### 字面量格式

Go 拥有异常强大的[composite literal syntax]，借助它可以
在单个表达式中表达深层嵌套的复杂值。在可行的情况下，
应优先使用该字面量语法，而不是逐字段地构建值。
`gofmt` 对字面量的格式化通常相当出色，但为了保持
这些字面量的可读性与可维护性，还需要遵循一些
额外的规则。

[composite literal syntax]: https://golang.org/ref/spec#Composite_literals

<a id="literal-field-names"></a>

#### 字段名

对于在当前包之外定义的类型，结构体字面量必须
指定**字段名**。

*   为来自其他包的类型加上字段名。

    <div class='goodcode'></div>

    ```go
    // https://pkg.go.dev/encoding/csv#Reader
    r := csv.Reader{
      Comma: ',',
      Comment: '#',
      FieldsPerRecord: 4,
    }
    ```

    结构体中字段的位置以及全部字段（在省略字段名时
    这两者都必须正确）通常不被视为结构体公开 API
    的一部分；指定字段名是为了避免
    不必要的耦合。

    <div class='badcode'></div>

    ```go
    r := csv.Reader{',', '#', 4, false, false, false, false}
    ```

*   对于包内的局部类型，字段名是可选的。

    <div class='goodcode'></div>

    ```go
    okay := Type{42}
    also := internalType{4, 2}
    ```

    如果能让代码更清晰，仍应使用字段名，而且这样做
    非常常见。例如，字段数量很多的结构体几乎总是
    应该用字段名来初始化。

    <div class='goodcode'></div>

    ```go
    okay := StructWithLotsOfFields{
      field1: 1,
      field2: "two",
      field3: 3.14,
      field4: true,
    }
    ```

<a id="literal-matching-braces"></a>

#### 花括号匹配

一对花括号的右半部分应始终与左花括号处于具有相同
缩进量的行上。单行字面量必然具备这一性质。当字面量
跨越多行时，保持这一性质可使字面量的花括号匹配与
函数和 `if` 语句等常见 Go 语法结构的花括号匹配
保持一致。

这一方面最常见的错误是，在多行结构体字面量中把右花括号
与某个值放在同一行。这种情况下，该行应以逗号结尾，
右花括号应出现在下一行。

<div class='goodcode'></div>

```go
good := []*Type{{Key: "value"}}
```

<div class='goodcode'></div>

```go
good := []*Type{
    {Key: "multi"},
    {Key: "line"},
}
```

<div class='badcode'></div>

```go
bad := []*Type{
    {Key: "multi"},
    {Key: "line"}}
```

<div class='badcode'></div>

```go
bad := []*Type{
    {
        Key: "value"},
}
```

<a id="literal-cuddled-braces"></a>

#### 紧贴的花括号

对于切片和数组字面量，只有在同时满足以下两个条件时，
才允许去掉花括号之间的空白（即让它们「紧贴」）。

*   [缩进匹配](#literal-matching-braces)
*   内部值也是字面量或 proto 构建器（即不是变量或
    其他表达式）

<div class='goodcode'></div>

```go
good := []*Type{
    { // Not cuddled
        Field: "value",
    },
    {
        Field: "value",
    },
}
```

<div class='goodcode'></div>

```go
good := []*Type{{ // Cuddled correctly
    Field: "value",
}, {
    Field: "value",
}}
```

<div class='goodcode'></div>

```go
good := []*Type{
    first, // Can't be cuddled
    {Field: "second"},
}
```

<div class='goodcode'></div>

```go
okay := []*pb.Type{pb.Type_builder{
    Field: "first", // Proto Builders may be cuddled to save vertical space
}.Build(), pb.Type_builder{
    Field: "second",
}.Build()}
```

<div class='badcode'></div>

```go
bad := []*Type{
    first,
    {
        Field: "second",
    }}
```

<a id="literal-repeated-type-names"></a>

#### 重复的类型名

切片和 map 字面量中可以省略重复的类型名。这
有助于减少杂乱。适合显式重复类型名的合理场景是：
处理项目中不常见的复杂类型时，当重复的类型名
位于相隔很远的行上，可以提醒读者
当前所处的上下文。

<div class='goodcode'></div>

```go
good := []*Type{
    {A: 42},
    {A: 43},
}
```

<div class='badcode'></div>

```go
repetitive := []*Type{
    &Type{A: 42},
    &Type{A: 43},
}
```

<div class='goodcode'></div>

```go
good := map[Type1]*Type2{
    {A: 1}: {B: 2},
    {A: 3}: {B: 4},
}
```

<div class='badcode'></div>

```go
repetitive := map[Type1]*Type2{
    Type1{A: 1}: &Type2{B: 2},
    Type1{A: 3}: &Type2{B: 4},
}
```

**提示：** 如果想移除结构体字面量中重复的类型名，可以
运行 `gofmt -s`。

<a id="literal-zero-value-fields"></a>

#### 零值字段

在不损失清晰性的前提下，结构体字面量中可以省略
[Zero-value] 字段。

设计良好的 API 常采用零值构造以提升可读性。例如，
省略下面结构体中的三个零值字段，可以把注意力
集中到唯一被指定的选项上。

[Zero-value]: https://golang.org/ref/spec#The_zero_value

<div class='badcode'></div>

```go
import (
  "github.com/golang/leveldb"
  "github.com/golang/leveldb/db"
)

ldb := leveldb.Open("/my/table", &db.Options{
    BlockSize: 1<<16,
    ErrorIfDBExists: true,

    // These fields all have their zero values.
    BlockRestartInterval: 0,
    Comparer: nil,
    Compression: nil,
    FileSystem: nil,
    FilterPolicy: nil,
    MaxOpenFiles: 0,
    WriteBufferSize: 0,
    VerifyChecksums: false,
})
```

<div class='goodcode'></div>

```go
import (
  "github.com/golang/leveldb"
  "github.com/golang/leveldb/db"
)

ldb := leveldb.Open("/my/table", &db.Options{
    BlockSize: 1<<16,
    ErrorIfDBExists: true,
})
```

表驱动测试中的结构体往往能从 [explicit field names] 中
受益，尤其是当测试结构体并不简单时。当相关字段与
测试用例无关时，这让编写者可以完全省略零值字段。
例如，成功的测试用例应省略任何与错误或失败
相关的字段。在零值对于理解测试用例必不可少的
情况下，例如测试零值或 `nil` 输入时，应指定
字段名。

[explicit field names]: #literal-field-names

**简洁**

```go
tests := []struct {
    input      string
    wantPieces []string
    wantErr    error
}{
    {
        input:      "1.2.3.4",
        wantPieces: []string{"1", "2", "3", "4"},
    },
    {
        input:   "hostname",
        wantErr: ErrBadHostname,
    },
}
```

**显式**

```go
tests := []struct {
    input    string
    wantIPv4 bool
    wantIPv6 bool
    wantErr  bool
}{
    {
        input:    "1.2.3.4",
        wantIPv4: true,
        wantIPv6: false,
    },
    {
        input:    "1:2::3:4",
        wantIPv4: false,
        wantIPv6: true,
    },
    {
        input:    "hostname",
        wantIPv4: false,
        wantIPv6: false,
        wantErr:  true,
    },
}
```

<a id="nil-slices"></a>

### nil 切片

在大多数情况下，`nil` 与空切片在功能上没有区别。
`len` 和 `cap` 等内置函数在 `nil` 切片上的行为
符合预期。

<div class='goodcode'></div>

```go
import "fmt"

var s []int         // nil

fmt.Println(s)      // []
fmt.Println(len(s)) // 0
fmt.Println(cap(s)) // 0
for range s {...}   // no-op

s = append(s, 42)
fmt.Println(s)      // [42]
```

如果把空切片声明为局部变量（尤其是当它可能成为
返回值的来源时），优先使用 nil 初始化，以降低
调用方引入缺陷的风险。

<div class='goodcode'></div>

```go
var t []string
```

<div class='badcode'></div>

```go
t := []string{}
```

不要创建迫使客户端区分 nil 与
空切片的 API。

<div class='goodcode'></div>

```go
// Ping pings its targets.
// Returns hosts that successfully responded.
func Ping(hosts []string) ([]string, error) { ... }
```

<div class='badcode'></div>

```go
// Ping pings its targets and returns a list of hosts
// that successfully responded. Can be empty if the input was empty.
// nil signifies that a system error occurred.
func Ping(hosts []string) []string { ... }
```

在设计接口时，避免区分 `nil` 切片与非 `nil` 的零长度
切片，因为这可能导致难以察觉的编程错误。通常的做法
是使用 `len` 检查是否为空，而不是
`== nil`。

以下实现把 `nil` 和零长度切片都当作「空」：

<div class='goodcode'></div>

```go
// describeInts describes s with the given prefix, unless s is empty.
func describeInts(prefix string, s []int) {
    if len(s) == 0 {
        return
    }
    fmt.Println(prefix, s)
}
```

而不是把这种区别作为 API 的一部分：

<div class='badcode'></div>

```go
func maybeInts() []int { /* ... */ }

// describeInts describes s with the given prefix; pass nil to skip completely.
func describeInts(prefix string, s []int) {
  // The behavior of this function unintentionally changes depending on what
  // maybeInts() returns in 'empty' cases (nil or []int{}).
  if s == nil {
    return
  }
  fmt.Println(prefix, s)
}

describeInts("Here are some ints:", maybeInts())
```

进一步的讨论请参见 [in-band errors]。

[in-band errors]: #in-band-errors

<a id="indentation-confusion"></a>

### 缩进混淆

如果换行会让该行剩余部分与缩进的代码块对齐，
就应避免这样的换行。如果无法避免，请留出一个空格，
把块中的代码与折行后的内容分隔开。

<div class='badcode'></div>

```go
if longCondition1 && longCondition2 &&
    // Conditions 3 and 4 have the same indentation as the code within the if.
    longCondition3 && longCondition4 {
    log.Info("all conditions met")
}
```

具体准则与示例请参见以下章节：

*   [函数格式](#func-formatting)
*   [条件语句与循环](#conditional-formatting)
*   [字面量格式](#literal-formatting)

<a id="func-formatting"></a>

### 函数格式

函数或方法声明的签名应保持在一行之内，以避免
[缩进混淆](#indentation-confusion)。

函数参数列表可能构成 Go 源文件中最长的一些行。
然而，它们位于缩进发生变化之前，因此很难以一种
不会让后续行看起来像是函数体一部分的方式
来换行，容易造成混淆：

<div class='badcode'></div>

```go
func (r *SomeType) SomeLongFunctionName(foo1, foo2, foo3 string,
    foo4, foo5, foo6 int) {
    foo7 := bar(foo1)
    // ...
}
```

关于缩短那些本会带有大量参数的函数的调用处，
可参见[最佳实践](best-practices#funcargs)中的几种做法。

把局部变量提取出来往往可以缩短行宽。

<div class='goodcode'></div>

```go
local := helper(some, parameters, here)
good := foo.Call(list, of, parameters, local)
```

同样地，不应仅仅因为行长就把函数和方法调用
拆开。

<div class='goodcode'></div>

```go
good := foo.Call(long, list, of, parameters, all, on, one, line)
```

<div class='badcode'></div>

```go
bad := foo.Call(long, list, of, parameters,
    with, arbitrary, line, breaks)
```

尽可能避免针对具体函数参数添加行内注释。
应改用[选项结构体](best-practices#option-structure)，
或在函数文档中补充更多细节。

<div class='goodcode'></div>

```go
good := server.New(ctx, server.Options{Port: 42})
```

<div class='badcode'></div>

```go
bad := server.New(
    ctx,
    42, // Port
)
```

如果 API 无法改动，或者某处调用比较特殊（无论
调用是否过长），只要有助于理解该调用，
总是允许添加换行。

<div class='goodcode'></div>

```go
canvas.RenderHeptagon(fillColor,
    x0, y0, vertexColor0,
    x1, y1, vertexColor1,
    x2, y2, vertexColor2,
    x3, y3, vertexColor3,
    x4, y4, vertexColor4,
    x5, y5, vertexColor5,
    x6, y6, vertexColor6,
)
```

注意，上例中的各行并不是在某个固定列边界处折行，
而是按顶点坐标与颜色分组。

函数内的长字符串字面量不应为了行长而拆开。
对于包含此类字符串的函数，可以在格式字符串之后
添加换行，并把参数放在下一行或后续行。
换行位置最好依据输入的语义分组来决定，
而不是纯粹依据行长。

<div class='goodcode'></div>

```go
log.Warningf("Database key (%q, %d, %q) incompatible in transaction started by (%q, %d, %q)",
    currentCustomer, currentOffset, currentKey,
    txCustomer, txOffset, txKey)
```

<div class='badcode'></div>

```go
log.Warningf("Database key (%q, %d, %q) incompatible in"+
    " transaction started by (%q, %d, %q)",
    currentCustomer, currentOffset, currentKey, txCustomer,
    txOffset, txKey)
```

<a id="conditional-formatting"></a>

### 条件语句与循环

`if` 语句不应折行；多行的 `if` 子句可能导致
[缩进混淆](#indentation-confusion)。

<div class='badcode'></div>

```go
// The second if statement is aligned with the code within the if block, causing
// indentation confusion.
if db.CurrentStatusIs(db.InTransaction) &&
    db.ValuesEqual(db.TransactionKey(), row.Key()) {
    return db.Errorf(db.TransactionError, "query failed: row (%v): key does not match transaction key", row)
}
```

如果不需要短路行为，可以直接把布尔操作数
提取出来：

<div class='goodcode'></div>

```go
inTransaction := db.CurrentStatusIs(db.InTransaction)
keysMatch := db.ValuesEqual(db.TransactionKey(), row.Key())
if inTransaction && keysMatch {
    return db.Error(db.TransactionError, "query failed: row (%v): key does not match transaction key", row)
}
```

也可能还有其他可以提取的局部变量，尤其是当
条件本身已经很重复时：

<div class='goodcode'></div>

```go
uid := user.GetUniqueUserID()
if db.UserIsAdmin(uid) || db.UserHasPermission(uid, perms.ViewServerConfig) || db.UserHasPermission(uid, perms.CreateGroup) {
    // ...
}
```

<div class='badcode'></div>

```go
if db.UserIsAdmin(user.GetUniqueUserID()) || db.UserHasPermission(user.GetUniqueUserID(), perms.ViewServerConfig) || db.UserHasPermission(user.GetUniqueUserID(), perms.CreateGroup) {
    // ...
}
```

包含闭包或多行结构体字面量的 `if` 语句应确保
[花括号匹配](#literal-matching-braces)，以避免
[缩进混淆](#indentation-confusion)。

<div class='goodcode'></div>

```go
if err := db.RunInTransaction(func(tx *db.TX) error {
    return tx.Execute(userUpdate, x, y, z)
}); err != nil {
    return fmt.Errorf("user update failed: %s", err)
}
```

<div class='goodcode'></div>

```go
if _, err := client.Update(ctx, &userpb.UserUpdateRequest{
    ID:   userID,
    User: user,
}); err != nil {
    return fmt.Errorf("user update failed: %s", err)
}
```

同样地，不要试图在 `for` 语句中生硬地插入换行。
如果没有优雅的重构方式，尽可以让这一行
保持较长：

<div class='goodcode'></div>

```go
for i, max := 0, collection.Size(); i < max && !collection.HasPendingWriters(); i++ {
    // ...
}
```

不过，通常还是有办法的：

<div class='goodcode'></div>

```go
for i, max := 0, collection.Size(); i < max; i++ {
    if collection.HasPendingWriters() {
        break
    }
    // ...
}
```

`switch` 和 `case` 语句也应保持在一行之内。

<div class='goodcode'></div>

```go
switch good := db.TransactionStatus(); good {
case db.TransactionStarting, db.TransactionActive, db.TransactionWaiting:
    // ...
case db.TransactionCommitted, db.NoTransaction:
    // ...
default:
    // ...
}
```

<div class='badcode'></div>

```go
switch bad := db.TransactionStatus(); bad {
case db.TransactionStarting,
    db.TransactionActive,
    db.TransactionWaiting:
    // ...
case db.TransactionCommitted,
    db.NoTransaction:
    // ...
default:
    // ...
}
```

如果行过长，应缩进所有 case，并用空行把它们
分隔开，以避免[缩进混淆](#indentation-confusion)：

<div class='goodcode'></div>

```go
switch db.TransactionStatus() {
case
    db.TransactionStarting,
    db.TransactionActive,
    db.TransactionWaiting,
    db.TransactionCommitted:

    // ...
case db.NoTransaction:
    // ...
default:
    // ...
}
```

在把变量与常量比较的条件式中，应把变量值放在
相等运算符的左侧：

<div class='goodcode'></div>

```go
if result == "foo" {
  // ...
}
```

而不是采用常量在前这种不够清晰的写法
（[“Yoda 风格条件式”](https://en.wikipedia.org/wiki/Yoda_conditions)）：

<div class='badcode'></div>

```go
if "foo" == result {
  // ...
}
```

<a id="copying"></a>

### 复制

<a id="TOC-Copying"></a>

为避免意外的别名及类似缺陷，复制来自其他包的
结构体时要小心。例如，`sync.Mutex` 等同步对象
绝不能复制。

`bytes.Buffer` 类型包含一个 `[]byte` 切片，并且作为对
小字符串的优化，还包含一个小字节数组，切片可能指向它。
如果复制 `Buffer`，副本中的切片可能与原对象中的数组
形成别名，导致后续方法调用产生出乎意料的效果。

一般而言，如果类型 `T` 的方法与指针类型 `*T` 关联，
就不要复制 `T` 类型的值。

<div class='badcode'></div>

```go
b1 := bytes.Buffer{}
b2 := b1
```

调用以值作为接收者的方法可能掩盖复制行为。
设计 API 时，如果结构体含有不应被复制的字段，
通常应接收并返回指针类型。

以下做法是可以接受的：

<div class='goodcode'></div>

```go
type Record struct {
  buf bytes.Buffer
  // other fields omitted
}

func New() *Record {...}

func (r *Record) Process(...) {...}

func Consumer(r *Record) {...}
```

但以下做法通常是错误的：

<div class='badcode'></div>

```go
type Record struct {
  buf bytes.Buffer
  // other fields omitted
}


func (r Record) Process(...) {...} // Makes a copy of r.buf

func Consumer(r Record) {...} // Makes a copy of r.buf
```

这条准则同样适用于复制 `sync.Mutex`。

<a id="dont-panic"></a>

### 不要使用 panic

<a id="TOC-Don-t-Panic"></a>

不要用 `panic` 处理常规错误。应改用 `error` 和多个
返回值。请参见 [Effective Go section on errors]。

在 `package main` 和初始化代码中，对于应当终止程序的
错误（例如配置无效），可考虑使用 [`log.Exit`]，因为在许多
这类情况下，堆栈跟踪对读者并无帮助。请注意
[`log.Exit`] 会调用 [`os.Exit`]，任何 defer 函数都不会执行。

对于表示「不可能」状况的错误，即本应在代码评审
和/或测试中发现的缺陷，函数可以合理地返回
错误或调用 [`log.Fatal`]。

另见[何时可以接受 panic](best-practices.md#when-to-panic)。

**注意：** `log.Fatalf` 并非标准库中的 log。请参见 [#logging]。

[Effective Go section on errors]: http://golang.org/doc/effective_go.html#errors
[`os.Exit`]: https://pkg.go.dev/os#Exit

<a id="must-functions"></a>

### Must 函数

失败时终止程序的设置辅助函数遵循 `MustXYZ`
（或 `mustXYZ`）命名惯例。一般而言，它们只应在
程序启动早期调用，而不应用于用户输入之类
更适合常规 Go 错误处理的场合。

这种情况常出现在专门在
[包初始化时](https://golang.org/ref/spec#Package_initialization)
为初始化包级变量而调用的函数上
（例如 [template.Must](https://golang.org/pkg/text/template/#Must) 和
[regexp.MustCompile](https://golang.org/pkg/regexp/#MustCompile)）。

<div class='goodcode'></div>

```go
func MustParse(version string) *Version {
    v, err := Parse(version)
    if err != nil {
        panic(fmt.Sprintf("MustParse(%q) = _, %v", version, err))
    }
    return v
}

// Package level "constant". If we wanted to use `Parse`, we would have had to
// set the value in `init`.
var DefaultVersion = MustParse("1.2.3")
```

同样的惯例也可用于仅终止当前测试的测试辅助函数
（使用 `t.Fatal`）。这类辅助函数在创建测试值时
往往很方便，例如用于[表驱动测试](#table-driven-tests)的
结构体字段，因为返回错误的函数无法直接赋给结构体字段。

<div class='goodcode'></div>

```go
func mustMarshalAny(t *testing.T, m proto.Message) *anypb.Any {
  t.Helper()
  any, err := anypb.New(m)
  if err != nil {
    t.Fatalf("mustMarshalAny(t, m) = %v; want %v", err, nil)
  }
  return any
}

func TestCreateObject(t *testing.T) {
  tests := []struct{
    desc string
    data *anypb.Any
  }{
    {
      desc: "my test case",
      // Creating values directly within table driven test cases.
      data: mustMarshalAny(t, mypb.Object{}),
    },
    // ...
  }
  // ...
}
```

在这两种情况下，这一模式的价值在于辅助函数可以
在「值」上下文中调用。不应在难以确保错误会被捕获的
地方，或在错误本应被[检查](#handle-errors)的上下文中
（例如许多请求处理程序里）调用这类辅助函数。
对于常量输入，这让测试可以轻松确保 `Must` 参数
格式正确；对于非常量输入，则让测试能够验证错误
被[妥善处理或传播](best-practices#error-handling)。

在测试中使用 `Must` 函数时，通常应把它们
[标记为测试辅助函数](#mark-test-helpers)，并在出错时调用 `t.Fatal`
（更多相关考量请参见
[测试辅助函数中的错误处理](best-practices#test-helper-error-handling)）。

在可以进行[普通错误处理](best-practices#error-handling)时
（包括经过一些重构之后），
就不应使用它们：

<div class='badcode'></div>

```go
func Version(o *servicepb.Object) (*version.Version, error) {
    // Return error instead of using Must functions.
    v := version.MustParse(o.GetVersionString())
    return dealiasVersion(v)
}
```

<a id="goroutine-lifetimes"></a>

### goroutine 生命周期

<a id="TOC-GoroutineLifetimes"></a>

启动 goroutine 时，要明确它们何时退出、是否会退出。

goroutine 可能因阻塞在 channel 的发送或接收上而泄漏。
即使没有其他 goroutine 持有该 channel 的引用，
垃圾回收器也不会终止阻塞在 channel 上的 goroutine。

即便 goroutine 没有泄漏，在不再需要它们时仍让其
在后台运行，也可能引发其他微妙且难以诊断的问题。
向已关闭的 channel 发送数据会触发 panic。

<div class='badcode'></div>

```go
ch := make(chan int)
ch <- 42
close(ch)
ch <- 13 // panic
```

在「结果不再需要之后」修改仍在使用的输入可能导致
数据竞争。让 goroutine 任意长时间地在后台运行，
可能导致内存用量不可预测。

并发代码应写得让 goroutine 的生命周期一目了然。
这通常意味着把与同步相关的代码限制在
单个函数的作用域内，并把逻辑提取到
[synchronous functions] 中。如果并发仍不明显，
务必记录 goroutine 何时退出以及为何退出。

遵循 context 使用最佳实践的代码往往有助于把这一点
讲清楚。惯例上用 [`context.Context`] 来管理：

<div class='goodcode'></div>

```go
func (w *Worker) Run(ctx context.Context) error {
    var wg sync.WaitGroup
    // ...
    for item := range w.q {
        // process returns at latest when the context is cancelled.
        wg.Add(1)
        go func() {
            defer wg.Done()
            process(ctx, item)
        }()
    }
    // ...
    wg.Wait()  // Prevent spawned goroutines from outliving this function.
}
```

上述做法还有其他变体，使用 `chan struct{}` 之类的
原始信号 channel、同步变量、
[条件变量][rethinking-slides] 等等。关键在于
让后续维护者能清楚看到 goroutine 的结束点。

相比之下，下面的代码对其启动的 goroutine 何时结束
毫不在意：

<div class='badcode'></div>

```go
func (w *Worker) Run() {
    // ...
    for item := range w.q {
        // process returns when it finishes, if ever, possibly not cleanly
        // handling a state transition or termination of the Go program itself.
        go process(item)
    }
    // ...
}
```

这段代码看起来似乎没问题，但存在几个潜在问题：

*   这段代码在生产环境中可能存在未定义行为，程序
    也可能无法干净地终止，即便操作系统会释放资源。

*   由于代码的生命周期不确定，很难对它进行
    有意义的测试。

*   如上所述，代码可能会泄漏资源。

另见：

*   [不要在不知道如何停止的情况下启动 goroutine][cheney-stop]
*   「Rethinking Classical Concurrency Patterns」：[幻灯片][rethinking-slides]、
    [视频][rethinking-video]
*   [When Go programs end]
*   [Documentation Conventions: Contexts]

[synchronous functions]: #synchronous-functions
[cheney-stop]: https://dave.cheney.net/2016/12/22/never-start-a-goroutine-without-knowing-how-it-will-stop
[rethinking-slides]: https://drive.google.com/file/d/1nPdvhB0PutEJzdCq5ms6UI58dp50fcAN/view
[rethinking-video]: https://www.youtube.com/watch?v=5zXAHh5tJqQ
[When Go programs end]: https://changelog.com/gotime/165
[Documentation Conventions: Contexts]: best-practices.md#documentation-conventions-contexts

<a id="interfaces"></a>

### 接口

<a id="TOC-Interfaces"></a>

在出现[实际需求](guide#simplicity)之前，不要创建接口。
关注所需的行为，而不只是「service」或
「repository」之类的抽象命名模式。

*   不要仅仅为了抽象或测试就把 RPC 客户端包装进
    新的手写接口。
    请改用[使用真实传输](best-practices#use-real-transports)
    （[testing RPC]）。

*   不要仅为测试而定义后门或导出某个接口的
    [test double] 实现。应优先通过真实实现的
    [public API] 进行测试。

*   当使用真实实现进行测试不切实际时，可以提供
    测试专用的配置或测试替身。这些测试设施
    应放在专门的包中（例如类似
    [spannertest]）。

接口应设计得足够小，以便实现和组合
（[GoTip #78: Minimal Viable Interfaces]）。应为接口编写恰当的文档，
包括其契约、边界情况和预期错误。如果接口类型
仅在包内部使用，应保持不导出。

接口应由使用方定义（而不是由实现该接口的包定义），
以确保它只包含实际用到的方法。
如果接口本身就是产品（一种通用协议），提供方包可以导出该接口，
以避免接口被反复重新定义而膨胀。

有一条经验法则：函数应以接口作为参数，但返回
具体类型（[GoTip #49: Accept Interfaces, Return Concrete Types]）。
返回具体类型让调用方能够访问该特定实现的
每个公开方法和字段，而不只是预先选定的接口中
定义的方法子集。调用方仍可把该具体结果传给任何
其他接受接口的函数。有时为了封装而返回接口是
可接受的（例如 `error` 接口），某些构造也是如此，
例如命令、链式调用、工厂以及
[策略](https://en.wikipedia.org/wiki/Strategy_pattern) 模式。

关于接口的更深入讨论，请参见
[最佳实践关于接口的章节](best-practices#interfaces)。

[GoTip #78: Minimal Viable Interfaces]: https://google.github.io/styleguide/go/index.html#gotip
[GoTip #49: Accept Interfaces, Return Concrete Types]: https://google.github.io/styleguide/go/index.html#gotip
[testing RPC]: https://codelabs.developers.google.com/grpc/getting-started-grpc-go#3
[test double]: https://abseil.io/resources/swe-book/html/ch13.html
[spannertest]: https://pkg.go.dev/cloud.google.com/go/spanner/spannertest
[public API]: https://abseil.io/resources/swe-book/html/ch12.html#test_via_public_apis

<a id="generics"></a>

### 泛型

在满足业务需求的前提下允许使用泛型（正式名称为
「[Type Parameters]」）。在许多应用中，使用
现有语言特性（切片、map、接口等）的传统做法同样
有效，且不会带来额外的复杂性，因此要警惕过早使用。
请参见关于[最少机制](guide#least-mechanism)的讨论。

引入使用泛型的导出 API 时，务必提供恰当的
文档。强烈建议附上能说明动机的可运行 [examples]。

不要仅仅因为实现的算法或数据结构不关心其
成员元素的类型就使用泛型。如果实际只实例化
一种类型，起初应让代码在该类型上工作，
完全不使用泛型。日后添加多态会很容易，
相比之下，移除后来发现并不必要的抽象
要困难得多。

不要使用泛型来发明领域专用语言（DSL）。尤其要
避免引入可能给读者带来沉重负担的错误处理框架。
应优先采用既有的[错误处理](#errors)实践。
在测试方面，要特别警惕引入
[断言库](#assert) 或导致[测试失败](#useful-test-failures)
信息变得不那么有用的框架。

一般而言：

*   [Write code, don't design types]。出自 Robert Griesemer
    与 Ian Lance Taylor 在 GopherCon 上的演讲。
*   如果若干类型共享一个有用的统一接口，可以考虑
    用该接口来建模解决方案。可能并不需要泛型。
*   否则，与其依赖 `any` 类型和过度的
    [类型切换](https://tour.golang.org/methods/16)，不如考虑使用泛型。

另见：

*   Ian Lance Taylor 的演讲 [Using Generics in Go]

*   Go 网站上的 [Generics tutorial]

[Generics tutorial]: https://go.dev/doc/tutorial/generics
[Type Parameters]: https://go.dev/design/43651-type-parameters
[Using Generics in Go]: https://www.youtube.com/watch?v=nr8EpUO9jhw
[Write code, don't design types]: https://www.youtube.com/watch?v=Pa_e9EeCdy8&t=1250s

<a id="pass-values"></a>

### 传值

<a id="TOC-PassValues"></a>

不要仅仅为了节省几个字节就把指针作为函数参数传递。
如果函数自始至终只以 `*x` 的形式读取参数 `x`，
则该参数不应是指针。常见情形包括传递指向字符串
的指针（`*string`）或指向接口值的指针（`*io.Reader`）。
在这两种情况下，值本身大小固定，可以直接传递。

这条建议不适用于大型结构体，甚至不适用于可能
变大的小型结构体。特别是，protocol buffer 消息
通常应按指针而非按值处理。指针类型满足
`proto.Message` 接口（`proto.Marshal`、`protocmp.Transform`
等均接受该接口），而且 protocol buffer 消息可能相当大，
并且往往会随时间变得更大。

<a id="receiver-type"></a>

### 接收者类型

<a id="TOC-ReceiverType"></a>

[method receiver] 既可以按值传递，也可以按指针传递，
就像普通的函数参数一样。两者之间的选择取决于该方法
应属于哪个 [method set(s)]。

[method receiver]: https://golang.org/ref/spec#Method_declarations
[method set(s)]: https://golang.org/ref/spec#Method_sets

**正确性优先于速度或简洁性。** 有些情况下必须使用
指针值。在另一些情况下，若不清楚代码将如何增长，
可为大型类型选择指针或以此为未来留出余地，而对简单的
[plain old data] 使用值。

下面的列表更详细地说明了每种情况：

*   如果接收者是切片，且方法不会重新切片或重新分配
    该切片，则使用值而不是指针。

    <div class='goodcode'></div>

    ```go
    type Buffer []byte

    func (b Buffer) Len() int { return len(b) }
    ```

*   如果方法需要修改接收者，接收者必须是指针。

    <div class='goodcode'></div>

    ```go
    type Counter int

    func (c *Counter) Inc() { *c++ }

    // See https://pkg.go.dev/container/heap.
    type Queue []Item

    func (q *Queue) Push(x Item) { *q = append([]Item{x}, *q...) }
    ```

*   如果接收者是包含[无法安全复制](#copying)字段的
    结构体，应使用指针接收者。常见的例子
    是 [`sync.Mutex`] 和其他同步类型。

    <div class='goodcode'></div>

    ```go
    type Counter struct {
        mu    sync.Mutex
        total int
    }

    func (c *Counter) Inc() {
        c.mu.Lock()
        defer c.mu.Unlock()
        c.total++
    }
    ```

    **提示：** 查看类型的 [Godoc]，了解复制它是安全
    还是不安全。

*   如果接收者是「大」结构体或数组，指针接收者可能
    更高效。传递结构体相当于把它的所有字段或
    元素都作为参数传给方法。如果这看起来太大而不宜
    [按值传递](#pass-values)，指针是不错的选择。

*   对于将与其他修改接收者的函数并发调用或运行的
    方法，若不希望这些修改对你的方法可见，则使用值；
    否则使用指针。

*   如果接收者是结构体或数组，且其中任一元素是指向
    可能被修改对象的指针，优先使用指针接收者，以便
    向读者明确表达可变性的意图。

    <div class='goodcode'></div>

    ```go
    type Counter struct {
        m *Metric
    }

    func (c *Counter) Inc() {
        c.m.Add(1)
    }
    ```

*   如果接收者是无需修改的 [built-in type]（例如整数
    或字符串），则使用值。

    <div class='goodcode'></div>

    ```go
    type User string

    func (u User) String() { return string(u) }
    ```

*   如果接收者是 map、函数或 channel，则使用值而
    不是指针。

    <div class='goodcode'></div>

    ```go
    // See https://pkg.go.dev/net/http#Header.
    type Header map[string][]string

    func (h Header) Add(key, value string) { /* omitted */ }
    ```

*   如果接收者天然是值类型的「小」数组或结构体，
    没有可变字段也没有指针，则值接收者通常是
    正确的选择。

    <div class='goodcode'></div>

    ```go
    // See https://pkg.go.dev/time#Time.
    type Time struct { /* omitted */ }

    func (t Time) Add(d Duration) Time { /* omitted */ }
    ```

*   拿不准时，使用指针接收者。

一般准则是，尽量让某个类型的方法要么全部是指针
方法，要么全部是值方法。

**注意：** 关于向函数传值还是传指针是否会影响性能，
存在大量错误说法。编译器既可以选择传递指向栈上值的
指针，也可以选择在栈上复制值，但在大多数情况下，
这些考量不应压倒代码的可读性与正确性。
当性能确实重要时，务必先用贴近实际的基准测试
对两种做法做性能分析，再判定哪一种
做法更优。

[plain old data]: https://en.wikipedia.org/wiki/Passive_data_structure
[`sync.Mutex`]: https://pkg.go.dev/sync#Mutex
[built-in type]: https://pkg.go.dev/builtin

<a id="switch-break"></a>

### `switch` 与 `break`

<a id="TOC-SwitchBreak"></a>

不要在 `switch` 子句末尾使用不带目标标签的 `break`
语句；它们是多余的。与 C 和 Java 不同，Go 中的
`switch` 子句会自动跳出，需要 `fallthrough` 语句
才能实现 C 风格的行为。如果想说明空子句的用途，
请使用注释，而不是 `break`。

<div class='goodcode'></div>

```go
switch x {
case "A", "B":
    buf.WriteString(x)
case "C":
    // handled outside of the switch statement
default:
    return fmt.Errorf("unknown value: %q", x)
}
```

<div class='badcode'></div>

```go
switch x {
case "A", "B":
    buf.WriteString(x)
    break // this break is redundant
case "C":
    break // this break is redundant
default:
    return fmt.Errorf("unknown value: %q", x)
}
```

> **注意：** 如果 `switch` 子句位于 `for` 循环内，在
> `switch` 中使用 `break` 并不会退出外层的 `for` 循环。
>
> ```go
> for {
>   switch x {
>   case "A":
>      break // exits the switch, not the loop
>   }
> }
> ```
>
> 要跳出外层循环，请在 `for` 语句上使用标签：
>
> ```go
> loop:
>   for {
>     switch x {
>     case "A":
>        break loop // exits the loop
>     }
>   }
> ```

<a id="synchronous-functions"></a>

### 同步函数

<a id="TOC-SynchronousFunctions"></a>

同步函数直接返回结果，并在返回前完成所有回调
或 channel 操作。应优先使用同步函数，而非
异步函数。

同步函数把 goroutine 限制在一次调用之内。这有助于
推断其生命周期，并避免泄漏和数据竞争。
同步函数也更容易测试，因为调用方可以传入输入并
检查输出，无需轮询或同步。

如有必要，调用方可以在单独的 goroutine 中调用该函数
来引入并发。然而，在调用方一侧移除不必要的并发
相当困难（有时甚至不可能）。

另见：

*   Bryan Mills 的演讲「Rethinking Classical Concurrency Patterns」：
    [幻灯片][rethinking-slides]、[视频][rethinking-video]

<a id="type-aliases"></a>

### 类型别名

<a id="TOC-TypeAliases"></a>

使用*类型定义* `type T1 T2` 来定义新类型。使用
[*type alias*] `type T1 = T2` 来引用已有类型而不定义
新类型。类型别名很少见；其主要用途是帮助把包
迁移到新的源码位置。不需要时不要使用类型别名。

[*type alias*]: http://golang.org/ref/spec#Type_declarations

<a id="use-percent-q"></a>

### 使用 %q

<a id="TOC-UsePercentQ"></a>

Go 的格式化函数（`fmt.Printf` 等）提供了 `%q` 动词，
它会把字符串打印在双引号之内。

<div class='goodcode'></div>

```go
fmt.Printf("value %q looks like English text", someText)
```

优先使用 `%q`，而不是用 `%s` 手动实现同样的效果：

<div class='badcode'></div>

```go
fmt.Printf("value \"%s\" looks like English text", someText)
// Avoid manually wrapping strings with single-quotes too:
fmt.Printf("value '%s' looks like English text", someText)
```

在面向人的输出中，如果输入值可能为空或包含控制字符，
建议使用 `%q`。悄无声息的空字符串很难被察觉，
而 `""` 则一眼就能看出来。

<a id="use-any"></a>

### 使用 any

Go 1.18 引入了 `any` 类型，它是 `interface{}` 的 [alias]。
由于它是别名，`any` 在许多场合与 `interface{}` 等价，
在其他场合也可通过显式转换轻松互换。在新代码中
优先使用 `any`。

[alias]: https://go.googlesource.com/proposal/+/master/design/18130-type-alias.md

## 常用库

<a id="flags"></a>

### 标志

<a id="TOC-Flags"></a>

Google 代码库中的 Go 程序使用
[standard `flag` package] 的内部变体。它的接口类似，但能与
Google 内部系统良好互操作。Go 二进制文件中的标志名应优先
使用下划线分隔单词，而保存标志值的变量
应遵循标准的 Go 命名风格（[mixed caps]）。具体来说，标志
名应使用 snake case，变量名应使用与之对应的
camel case 名称。

<div class='goodcode'></div>

```go
var (
    pollInterval = flag.Duration("poll_interval", time.Minute, "Interval to use for polling.")
)
```

<div class='badcode'></div>

```go
var (
    poll_interval = flag.Int("pollIntervalSeconds", 60, "Interval to use for polling in seconds.")
)
```

标志只能在 `package main` 或等价位置定义。

通用包应通过 Go API 来配置，而不是穿透到
命令行接口；不要让导入某个库就附带导出新的
标志。也就是说，优先使用显式的函数参数或结构体
字段赋值，极少情况下、且须经最严格审查，
才使用导出的全局变量。在极少数确有必要
打破这条规则的情况下，标志名必须清楚地指明
它所配置的包。

如果标志是全局变量，请把它们放在紧随 import 部分
之后的独立 `var` 组中。

关于创建带子命令的 [complex CLIs] 的最佳实践，
还有更多讨论。

另见：

*   [本周提示 #45：避免使用标志，尤其是在库代码中][totw-45]
*   [Go 提示 #10：配置结构体与标志](https://google.github.io/styleguide/go/index.html#gotip)
*   [Go 提示 #80：依赖注入原则](https://google.github.io/styleguide/go/index.html#gotip)

[standard `flag` package]: https://golang.org/pkg/flag/
[mixed caps]: guide#mixed-caps
[complex CLIs]: best-practices#complex-clis
[totw-45]: https://abseil.io/tips/45

<a id="logging"></a>

### 日志

Google 代码库中的 Go 程序使用标准 [`log`] 包的一个变体。
它的接口相似但更强大，并且能与 Google 内部系统
良好互操作。该库的开源版本
以 [package `glog`] 形式提供，Google 的开源项目可以使用它，但
本指南通篇将其称为 `log`。

**注意：** 对于异常的程序退出，该库使用 `log.Fatal` 附带堆栈跟踪中止，
使用 `log.Exit` 则在不附带堆栈跟踪的情况下停止。它没有
标准库那样的 `log.Panic` 函数。

**提示：** `log.Info(v)` 等价于 `log.Infof("%v", v)`，其他
日志级别同理。在无需格式化时，优先使用
非格式化版本。

另见：

*   关于[记录错误日志](best-practices#error-logging)与
    [自定义详细级别](best-practices#vlog)的最佳实践
*   何时以及如何使用 log 包来
    [终止程序](best-practices#checks-and-panics)

[`log`]: https://pkg.go.dev/log
[`log/slog`]: https://pkg.go.dev/log/slog
[package `glog`]: https://pkg.go.dev/github.com/golang/glog
[`log.Exit`]: https://pkg.go.dev/github.com/golang/glog#Exit
[`log.Fatal`]: https://pkg.go.dev/github.com/golang/glog#Fatal

<a id="contexts"></a>

### 上下文

<a id="TOC-Contexts"></a>

[`context.Context`] 类型的值跨越 API 与进程边界传递安全
凭据、追踪信息、截止时间以及取消信号。与 Google 代码库中
使用线程局部存储的 C++ 和 Java 不同，Go 程序在从传入的
RPC 和 HTTP 请求到传出请求的整条函数调用链上，显式地
传递上下文。

[`context.Context`]: https://pkg.go.dev/context

当把 [`context.Context`] 传给函数或方法时，它始终是第一个
参数。

```go
func F(ctx context.Context /* other arguments */) {}
```

例外情况如下：

*   在 HTTP 处理程序中，上下文来自
    [`req.Context()`](https://pkg.go.dev/net/http#Request.Context)。
*   在流式 RPC 方法中，上下文来自流。

    使用 gRPC 流式传输的代码，通过生成的服务器类型中的
    `Context()` 方法获取上下文，该类型实现了 `grpc.ServerStream`。
    请参见 [gRPC 生成代码文档](https://grpc.io/docs/languages/go/generated-code/)。

*   在测试函数中（例如 `TestXXX`、`BenchmarkXXX`、`FuzzXXX`），
    上下文来自
    [`(testing.TB).Context()`](https://pkg.go.dev/testing#TB.Context)。

*   在其他入口函数中（此类函数的示例见下文），
    使用 [`context.Background()`]。

    *   在二进制目标中：`main`
    *   在通用代码和库中：`init`

> **注意**：调用链中间的代码极少需要用
> [`context.Background()`] 创建自己的基础上下文。除非
> 调用方给出的上下文不对，否则始终优先从调用方获取上下文。
>
> 你可能会遇到某些服务器库（即 Google 的 Go 服务器
> 框架中 Stubby、gRPC 或 HTTP 的实现），它们会为
> 每个请求构造一个全新的上下文对象。这些上下文会
> 立即用传入请求的信息填充，因此当它们被传给请求
> 处理程序时，上下文所附带的值已经跨越网络边界、
> 从客户端调用方传播过来。此外，这些上下文的生命
> 周期与请求一致：请求完成时，上下文
> 即被取消。
>
> 除非你正在实现服务器框架，否则不应在库代码中用
> [`context.Background()`] 创建上下文。若已有可用的
> 上下文，应优先改用下文提到的上下文分离。如果你
> 认为确实需要在入口函数之外使用
> [`context.Background()`]，请先与 Google Go 风格
> 邮件列表讨论，再着手实现。

[`context.Context`] 在函数中排在首位的约定同样适用于
测试辅助函数。

<div class='goodcode'></div>

```go
func readTestFile(ctx context.Context, t *testing.T, path string) string {}
```

不要给结构体类型添加上下文字段。而应为该类型中
需要传递上下文的每个方法各添加一个上下文参数。
唯一的例外是：方法的签名必须与标准库中或 Google
无法控制的第三方库中的接口相匹配。这类情况非常
罕见，实现之前应先与 Google Go 风格邮件列表讨论，
并进行可读性评审。

在测试中，优先使用最内层的 [`(testing.TB).Context()`]，而不是
[`context.Background()`]，来提供测试或子测试所用的初始
[`context.Context`]。辅助函数、环境或测试替身的设置，以及
测试函数体中调用的其他需要上下文的函数，都应显式地
传入一个上下文。

**注意：** `(testing.TB).Context()` 产生的上下文会在传给
[`(testing.TB).Cleanup`] 的清理函数运行之前被取消。清理期间，
要么使用 [`context.Background()`]，要么用
[`context.WithoutCancel`] 保留测试上下文中的值。

[`context.WithoutCancel`]: https://pkg.go.dev/context#WithoutCancel
[`(testing.TB).Cleanup`]: https://pkg.go.dev/testing#TB.Cleanup
[`(testing.TB).Context()`]: https://pkg.go.dev/testing#TB.Context

Google 代码库中，若某些代码必须启动在父上下文被取消之后
仍能运行的后台操作，可使用内部包来实现分离。关于
开源替代方案的讨论，请关注
[issue #40221](https://github.com/golang/go/issues/40221)。

由于上下文是不可变的，把同一个上下文传给共享相同截止时间、
取消信号、凭据、父追踪等信息的多个调用，
是完全可以的。

另见：

*   [Contexts and structs]

[`context.Background()`]: https://pkg.go.dev/context/#Background
[Contexts and structs]: https://go.dev/blog/context-and-structs

<a id="custom-contexts"></a>

#### 自定义上下文

不要创建自定义上下文类型，也不要在函数签名中使用
[`context.Context`] 以外的接口。这条规则
没有例外。

设想一下，如果每个团队都有自定义上下文，那么从包 `p`
到包 `q` 的每次函数调用，都必须确定如何把 `p.Context`
转换为 `q.Context`，而且要对所有包 `p` 和 `q` 的组合都
这样做。这对人来说既不现实又容易出错，也会让那些
添加上下文参数的自动化重构几乎无法进行。

如果有需要在各处传递的应用数据，就把它放进参数、
接收者、全局变量中，如果它确实属于上下文，就放进
`Context` 值里。创建自己的上下文类型是不可接受的，
因为这会削弱 Go 团队让 Go 程序在生产环境中正常工作的能力。

<a id="crypto-rand"></a>

### crypto/rand

<a id="TOC-CryptoRand"></a>

不要用 `math/rand` 包生成密钥，即便是一次性密钥也不行。
如果不设置种子，生成器完全可预测。即便用
`time.Nanoseconds()` 设置种子，熵也只有几个比特。应改用
`crypto/rand` 的 Reader；如果需要文本，就输出为十六进制或 base64。

<div class='goodcode'></div>

```go
import (
    "crypto/rand"
    // "encoding/base64"
    // "encoding/hex"
    "fmt"

    // ...
)

func Key() string {
    buf := make([]byte, 16)
    if _, err := rand.Read(buf); err != nil {
        log.Fatalf("Out of randomness, should never happen: %v", err)
    }
    return fmt.Sprintf("%x", buf)
    // or hex.EncodeToString(buf)
    // or base64.StdEncoding.EncodeToString(buf)
}
```

**注意：** `log.Fatalf` 并非标准库中的 log。请参见 [#logging]。

<a id="useful-test-failures"></a>

## 有用的测试失败信息

<a id="TOC-UsefulTestFailures"></a>

应当做到无需阅读测试的源码就能诊断出测试失败的原因。
测试失败时应给出有用的消息，详细说明：

*   导致失败的原因
*   哪些输入导致了错误
*   实际结果
*   预期结果

下文列出了为实现这一目标而约定的具体惯例。

<a id="assert"></a>

### 断言库

<a id="TOC-Assert"></a>

不要创建「断言库」作为测试辅助工具。

断言库是这样一类库：它们试图在测试内部把校验与
失败消息的生成合二为一（不过其他测试辅助函数也可能
有同样的陷阱）。关于测试辅助函数与断言库之间的区别，
请参见[最佳实践](best-practices#test-functions)。

<div class='badcode'></div>

```go
var obj BlogPost

assert.IsNotNil(t, "obj", obj)
assert.StringEq(t, "obj.Type", obj.Type, "blogPost")
assert.IntEq(t, "obj.Comments", obj.Comments, 2)
assert.StringNotEq(t, "obj.Body", obj.Body, "")
```

断言库往往要么过早终止测试（如果 `assert` 调用了
`t.Fatalf` 或 `panic`），要么遗漏有关测试哪些部分
做对了的相关信息：

<div class='badcode'></div>

```go
package assert

func IsNotNil(t *testing.T, name string, val any) {
    if val == nil {
        t.Fatalf("Data %s = nil, want not nil", name)
    }
}

func StringEq(t *testing.T, name, got, want string) {
    if got != want {
        t.Fatalf("Data %s = %q, want %q", name, got, want)
    }
}
```

复杂的断言函数往往无法提供
[useful failure messages] 以及测试函数中已有的上下文。
断言函数和断言库太多，会导致开发者体验碎片化：
我该用哪个断言库，它又该输出什么风格的输出格式
等等？碎片化造成不必要的困惑，对库维护者和大规模
改动的作者尤其如此，他们还要负责修复潜在的下游
破坏。与其为测试创造一门领域专用语言，不如直接
使用 Go 本身。

断言库常常把比较与相等性检查抽取出来。应优先改用
[`cmp`] 和 [`fmt`] 之类的标准库：

<div class='goodcode'></div>

```go
var got BlogPost

want := BlogPost{
    Comments: 2,
    Body:     "Hello, world!",
}

if !cmp.Equal(got, want) {
    t.Errorf("Blog post = %v, want = %v", got, want)
}
```

对于更贴近特定领域的比较辅助函数，优先返回一个值或
错误，以便用于测试的失败消息，而不是传入 `*testing.T`
再调用它的错误报告方法：

<div class='goodcode'></div>

```go
func postLength(p BlogPost) int { return len(p.Body) }

func TestBlogPost_VeritableRant(t *testing.T) {
    post := BlogPost{Body: "I am Gunnery Sergeant Hartman, your senior drill instructor."}

    if got, want := postLength(post), 60; got != want {
        t.Errorf("Length of post = %v, want %v", got, want)
    }
}
```

**最佳实践：** 如果 `postLength` 并不简单，直接对它进行
测试、独立于任何使用它的测试，是合理的。

另见：

*   [相等性比较与差异](#types-of-equality)
*   [打印差异](#print-diffs)
*   关于测试辅助函数与断言辅助函数之间的区别，请参见
    [最佳实践](best-practices#test-functions)
*   [Go FAQ] 中关于 [testing frameworks] 的章节，以及对其刻意不予采用的立场

[useful failure messages]: #useful-test-failures
[`fmt`]: https://golang.org/pkg/fmt/
[marking test helpers]: #mark-test-helpers
[Go FAQ]: https://go.dev/doc/faq
[testing frameworks]: https://go.dev/doc/faq#testing_framework

<a id="identify-the-function"></a>

### 标明函数

在大多数测试中，失败消息应包含发生失败的函数的名称，
即便从测试函数名看起来已显而易见。具体来说，
失败消息应写成 `YourFunc(%v) = %v, want %v`，
而不是仅仅写成 `got %v, want %v`。

<a id="identify-the-input"></a>

### 标明输入

在大多数测试中，如果函数输入较短，失败消息就应
包含这些输入。如果输入的相关特征并不明显（例如
输入很大或不透明），就应为测试用例取一个描述
所测内容的名字，并把该描述作为错误消息的一部分
打印出来。

<a id="got-before-want"></a>

### 先写实际值，再写期望值

测试输出应先包含函数返回的实际值，再打印期望值。
打印测试输出的标准格式是 `YourFunc(%v) = %v, want %v`。
在需要写「actual」和「expected」的地方，分别
改用「got」和「want」这两个词。

对于差异，方向性不那么明显，因此在失败消息中加入
一个说明以辅助解读很重要。请参见
[section on printing diffs]。无论在失败消息中采用哪种
差异顺序，都应把它作为失败消息的一部分明确标示出来，
因为现有代码在顺序上并不一致。

[section on printing diffs]: #print-diffs

<a id="compare-full-structures"></a>

### 完整结构比较

如果函数返回结构体（或切片、数组、map 等任何带有
多个字段的数据类型），应避免编写逐字段手工比较
结构体的测试代码。而应构造出你期望函数返回的
数据，再用
[deep comparison] 直接比较。

**注意：** 如果数据中含有会掩盖测试意图的无关字段，
则本条不适用。

如果结构体需要按近似（或某种等价的语义）相等性来比较，
或者它含有无法进行相等性比较的字段（例如某个字段是
`io.Reader`），那么用 [`cmpopts`] 的选项（如
[`cmpopts.IgnoreInterfaces`]）来调整 [`cmp.Diff`] 或
[`cmp.Equal`] 的比较，也许就能满足需求
（[示例](https://play.golang.org/p/vrCUNVfxsvF)）。

如果函数返回多个返回值，比较之前无需把它们包装进
结构体。只需逐个比较各个返回值并
打印出来即可。

<div class='goodcode'></div>

```go
val, multi, tail, err := strconv.UnquoteChar(`\"Fran & Freddie's Diner\"`, '"')
if err != nil {
  t.Fatalf(...)
}
if val != `"` {
  t.Errorf(...)
}
if multi {
  t.Errorf(...)
}
if tail != `Fran & Freddie's Diner"` {
  t.Errorf(...)
}
```

[deep comparison]: #types-of-equality
[`cmpopts`]: https://pkg.go.dev/github.com/google/go-cmp/cmp/cmpopts
[`cmpopts.IgnoreInterfaces`]: https://pkg.go.dev/github.com/google/go-cmp/cmp/cmpopts#IgnoreInterfaces

<a id="compare-stable-results"></a>

### 比较稳定的结果

避免比较那些可能依赖于你无法掌控的包的输出
稳定性的结果。测试应改为比较语义上相关、稳定
且不受依赖变化影响的信息。对于返回格式化字符串
或序列化字节的功能，通常不能安全地假定其输出
是稳定的。

例如，[`json.Marshal`] 可能改变（过去也确实改变过）
它输出的具体字节。若 `json` 包改变了序列化字节的
方式，对 JSON 字符串做字符串相等性比较的测试就可能
失效。更稳健的测试应解析 JSON 字符串的内容，
并确保它在语义上等价于某个预期的数据结构。

[`json.Marshal`]: https://golang.org/pkg/encoding/json/#Marshal

<a id="keep-going"></a>

### 继续执行

测试应尽可能继续执行，即便发生失败也要继续，以便在
一次运行中打印出所有失败的检查。这样，修复失败测试的
开发者就不必每修完一个缺陷就重新运行测试，
才能发现下一个缺陷。

报告不匹配时，优先调用 `t.Error` 而不是 `t.Fatal`。
比较函数输出的若干不同属性时，对每一项比较
都使用 `t.Error`。

<div class='goodcode'></div>

```go
gotMean, gotVariance, err := MyDistribution(input)
if err != nil {
  t.Fatalf("MyDistribution(%v) returned unexpected error: %v", input, err)
}
if diff := cmp.Diff(wantMean, gotMean); diff != "" {
  t.Errorf("MyDistribution(%v) returned unexpected difference in mean value (-want +got):\n%s", input, diff)
}
if diff := cmp.Diff(wantVariance, gotVariance); diff != "" {
  t.Errorf("MyDistribution(%v) returned unexpected difference in variance value (-want +got):\n%s", input, diff)
}
```

调用 `t.Fatal` 主要用于在后续失败将变得毫无意义、
甚至会误导排查者时，报告某种意外状况（例如错误或
输出不匹配）。请注意下面的代码先调用 `t.Fatalf`，
*然后*才调用 `t.Errorf`：

<div class='goodcode'></div>

```go
gotEncoded := Encode(input)
if gotEncoded != wantEncoded {
  t.Fatalf("Encode(%q) = %q, want %q", input, gotEncoded, wantEncoded)
  // It doesn't make sense to decode from unexpected encoded input.
}
gotDecoded, err := Decode(gotEncoded)
if err != nil {
  t.Fatalf("Decode(%q) returned unexpected error: %v", gotEncoded, err)
}
if gotDecoded != input {
  t.Errorf("Decode(%q) = %q, want %q", gotEncoded, gotDecoded, input)
}
```

对于表驱动测试，可考虑使用子测试，并使用 `t.Fatal`
而不是 `t.Error` 加 `continue`。另见
[Go 提示 #25：子测试：精简你的测试](https://google.github.io/styleguide/go/index.html#gotip)。

**最佳实践：** 关于何时该使用 `t.Fatal` 的更多讨论，
请参见[最佳实践](best-practices#t-fatal)。

<a id="types-of-equality"></a>

### 相等性比较与差异

`==` 运算符依据 [language-defined comparisons] 判定
相等性。标量值（数字、布尔值等）按值比较，但只有
部分结构体和接口能以这种方式比较。指针则按它们
是否指向同一变量来比较，而不是按所指值的相等性
来比较。

[`cmp`] 包能够比较 `==` 无法妥善处理的更复杂数据结构，
例如切片。用 [`cmp.Equal`] 做相等性比较，用
[`cmp.Diff`] 获得便于人阅读的对象差异。

<div class='goodcode'></div>

```go
want := &Doc{
    Type:     "blogPost",
    Comments: 2,
    Body:     "This is the post body.",
    Authors:  []string{"isaac", "albert", "emmy"},
}
if !cmp.Equal(got, want) {
    t.Errorf("AddPost() = %+v, want %+v", got, want)
}
```

作为通用的比较库，`cmp` 可能不知道如何比较某些类型。
例如，只有传入 [`protocmp.Transform`] 选项，它才能比较
protocol buffer 消息。

<!-- The order of want and got here is deliberate. See comment in #print-diffs. -->

<div class='goodcode'></div>

```go
if diff := cmp.Diff(want, got, protocmp.Transform()); diff != "" {
    t.Errorf("Foo() returned unexpected difference in protobuf messages (-want +got):\n%s", diff)
}
```

虽然 `cmp` 包不属于 Go 标准库，但它由 Go 团队维护，
应当能长期给出稳定的相等性结果。它是用户可配置的，
应能满足大多数比较需求。

[language-defined comparisons]: http://golang.org/ref/spec#Comparison_operators
[`cmp`]: https://pkg.go.dev/github.com/google/go-cmp/cmp
[`cmp.Equal`]: https://pkg.go.dev/github.com/google/go-cmp/cmp#Equal
[`cmp.Diff`]: https://pkg.go.dev/github.com/google/go-cmp/cmp#Diff
[`protocmp.Transform`]: https://pkg.go.dev/google.golang.org/protobuf/testing/protocmp#Transform

现有代码可能会使用下面这些较老的库，并且为了保持
一致性，可以继续沿用：

*   [`pretty`] 会生成美观的差异报告。不过，它
    相当刻意地把具有相同视觉表示的值视为相等。
    具体来说，`pretty` 不会发现 nil 切片与空切片
    之间的区别，对字段相同但接口实现不同的情况
    也不敏感，而且可以用嵌套 map 作为与结构体值
    比较的基础。它还会在生成差异之前把整个值
    序列化成字符串，因此不适合用来比较大的值。
    默认情况下它会比较未导出的字段，这使它对
    依赖中实现细节的变化很敏感。因此，在
    protobuf 消息上使用 `pretty` 并不
    合适。

[`pretty`]: https://pkg.go.dev/github.com/kylelemons/godebug/pretty

新代码应优先使用 `cmp`；在切实可行的情况下，
也值得考虑把旧代码更新为使用 `cmp`。

较旧的代码可能使用标准库的 `reflect.DeepEqual`
函数来比较复杂结构。不应使用 `reflect.DeepEqual`
检查相等性，因为它对未导出字段及其他实现细节的
变化很敏感。使用 `reflect.DeepEqual` 的代码
应更新为上述某个库。

**注意：** `cmp` 包是为测试而设计的，而非用于生产环境。
因此，当它怀疑某次比较执行得不正确时，可能会 panic，
以便指导用户如何改进测试、使其不那么脆弱。鉴于
cmp 动辄 panic 的倾向，它不适合用于生产代码，
因为一次意外的 panic 可能是致命的。

<a id="level-of-detail"></a>

### 详细程度

适用于大多数 Go 测试的惯用失败消息是
`YourFunc(%v) = %v, want %v`。不过，有些情况可能需要
更多或更少的细节：

*   执行复杂交互的测试也应描述这些交互。例如，如果
    同一个 `YourFunc` 被调用多次，要指出是哪一次调用
    导致测试失败。如果需要了解系统的额外状态，
    就把它写进失败输出（或至少写进日志）。
*   如果数据是带有大量样板代码的复杂结构体，只在
    消息中描述重要部分是可以接受的，但不要过度
    掩盖数据。
*   设置阶段的失败不需要同样程度的细节。如果测试
    辅助函数要填充 Spanner 表，而 Spanner 已宕机，
    你大概不必写出原本打算存入数据库的测试输入。
    `t.Fatalf("Setup: Failed to set up test database: %s", err)`
    通常就足以帮助定位问题。

**提示：** 让失败模式在开发阶段就触发。检查失败
消息具体是什么样，以及维护者能否有效地
处理该失败。

以下是一些清晰地重现测试输入与输出的技巧：

*   打印字符串数据时，[`%q` 往往很有用](#use-percent-q)，
    可以强调该值很重要，也更容易发现异常值。
*   打印（较小的）结构体时，`%+v` 可能比 `%v` 更有用。
*   较大值的校验失败时，[打印差异](#print-diffs)
    可以让失败更容易理解。

<a id="print-diffs"></a>

### 打印差异

如果函数返回很大的输出，测试失败时阅读失败消息的人
可能很难找出差异。与其同时打印返回值和期望值，
不如生成一份差异。

计算这类值的差异时，优先使用 `cmp.Diff`，对新测试
和新代码尤其如此，但也可以使用其他工具。关于各函数
优缺点的指导，请参见 [types of equality]。

*   [`cmp.Diff`]

*   [`pretty.Compare`]

可以用 [`diff`] 包比较多行字符串或字符串列表。
也可以把它作为构造其他类型差异的基础模块。

[types of equality]: #types-of-equality
[`diff`]: https://pkg.go.dev/github.com/kylelemons/godebug/diff
[`pretty.Compare`]: https://pkg.go.dev/github.com/kylelemons/godebug/pretty#Compare

在失败消息中补充一些文字，说明差异的方向。

<!--
The reversed order of want and got in these examples is intentional, as this is
the prevailing order across the Google codebase. The lack of a stance on which
order to use is also intentional, as there is no consensus which is
"most readable."


-->

*   使用 `cmp`、`pretty` 和 `diff` 包时（若向函数
    传入 `(want, got)`），类似 `diff (-want +got)` 的
    说明很合适，因为你加到格式字符串里的 `-` 和 `+`
    会与差异行开头实际出现的 `-` 和 `+` 相对应。
    如果传入 `(got, want)`，正确的说明则应改为
    `(-got +want)`。

*   `messagediff` 包使用不同的输出格式，因此在使用它时
    （若向函数传入 `(want, got)`），`diff (want -> got)`
    这条消息是合适的，因为箭头的方向会与
    「modified」行中箭头的方向一致。

差异会跨越多行，因此在打印差异之前，
应先打印一个换行。

<a id="test-error-semantics"></a>

### 测试错误语义

当单元测试执行字符串比较，或使用原生的 `cmp` 来检查
特定输入是否返回特定种类的错误时，你可能会发现，
一旦这些错误消息将来被改写，测试就会变得脆弱。
由于这可能把单元测试变成变更检测器
（参见 [TotT：变更检测器测试有害][tott-350] ），
不要用字符串比较来检查函数返回的错误类型。
不过，用字符串比较来检查来自被测包的错误消息
是否满足某些属性是允许的，例如是否包含
参数名。

Go 中的错误值通常包含一部分供人阅读的内容，
以及一部分供语义控制流使用的内容。测试应只
检验能够被可靠观察到的语义信息，而不是用于
人工调试的展示信息，因为后者常常会在将来
发生变化。关于构造带语义含义的错误的指导，
请参见[关于错误的最佳实践](best-practices#error-handling)。
如果语义信息不足的错误来自你无法掌控的依赖，
应考虑向该依赖的负责人提 bug 以帮助改进 API，
而不是依赖解析错误消息。

在单元测试中，通常只关心错误是否发生。
若是如此，只要在预期出错时检验错误是否为非 nil
就足够了。如果想检验该错误在语义上与另一个错误
相匹配，可考虑使用 [`errors.Is`]，或配合
[`cmpopts.EquateErrors`] 使用 `cmp`。

> **注意：** 如果测试使用了 [`cmpopts.EquateErrors`]，
> 但其所有 `wantErr` 值都是 `nil` 或 `cmpopts.AnyError`，
> 那么使用 `cmp` 属于[多余的机制](guide#least-mechanism)。
> 把 want 字段改成 `bool` 即可简化代码，随后用 `!=`
>
> <div class='goodcode'></div>
>
> ```go
> err := f(test.input)
> if gotErr := err != nil; gotErr != test.wantErr {
>     t.Errorf("f(%q) = %v, want error presence = %v", test.input, err, test.wantErr)
> }
> ```

另见
[Go 提示 #13：设计便于检查的错误](https://google.github.io/styleguide/go/index.html#gotip)。

[tott-350]: https://testing.googleblog.com/2015/01/testing-on-toilet-change-detector-tests.html
[`cmpopts.EquateErrors`]: https://pkg.go.dev/github.com/google/go-cmp/cmp/cmpopts#EquateErrors
[`errors.Is`]: https://pkg.go.dev/errors#Is

<a id="test-structure"></a>

## 测试结构

<a id="subtests"></a>

### 子测试

Go 标准测试库提供了 [define subtests] 的机制。
这为设置与清理、控制并行度以及测试过滤带来了灵活性。
子测试可能很有用（对表驱动测试尤其如此），但并非
必须使用。另见
[Go 博客关于子测试的文章](https://blog.golang.org/subtests)。

子测试不应依赖其他用例的执行来获得成功或初始状态，
因为子测试应当能够单独运行，无论是通过
`go test -run` 标志，还是通过 Bazel 的 [test filter] 表达式。

[define subtests]: https://pkg.go.dev/testing#hdr-Subtests_and_Sub_benchmarks
[test filter]: https://bazel.build/docs/user-manual#test-filter

<a id="subtest-names"></a>

#### 子测试名称

为子测试取名时，要使其在测试输出中可读，并在命令行上
对使用测试过滤的用户有用。用 `t.Run` 创建子测试时，
第一个参数用作该测试的描述性名称。为确保阅读日志的人
能看懂测试结果，应选择在转义之后仍然有用、可读的
子测试名称。把子测试名称更多地当作函数标识符，
而不是一段散文式的描述。

测试运行器会把空格替换为下划线，并对不可打印字符
进行转义。为确保测试日志与源码之间准确对应，
建议避免在子测试名称中使用这些字符。

如果测试数据适合用更长的描述，可考虑把描述放在
单独的字段中（也许用 `t.Log` 打印，或与失败消息
一起输出）。

子测试可通过传给 [Go test runner] 的标志或 Bazel 的
[test filter] 单独运行，因此要选择既具描述性又易于输入的名称。

> **警告：** 斜杠字符在子测试名称中尤其不友好，
> 因为它们具有 [special meaning for test filters]。
>
> > <div class='badcode'></div>
>
> ```sh
> # Assuming TestTime and t.Run("America/New_York", ...)
> bazel test :mytest --test_filter="Time/New_York"    # Runs nothing!
> bazel test :mytest --test_filter="Time//New_York"   # Correct, but awkward.
> ```

为了[identify the inputs]，请把函数的输入写进测试的
失败消息中，这样测试运行器就不会对其转义。

<div class='goodcode'></div>

```go
func TestTranslate(t *testing.T) {
    data := []struct {
        name, desc, srcLang, dstLang, srcText, wantDstText string
    }{
        {
            name:        "hu=en_bug-1234",
            desc:        "regression test following bug 1234. contact: cleese",
            srcLang:     "hu",
            srcText:     "cigarettát és egy öngyújtót kérek",
            dstLang:     "en",
            wantDstText: "cigarettes and a lighter please",
        }, // ...
    }
    for _, d := range data {
        t.Run(d.name, func(t *testing.T) {
            got := Translate(d.srcLang, d.dstLang, d.srcText)
            if got != d.wantDstText {
                t.Errorf("%s\nTranslate(%q, %q, %q) = %q, want %q",
                    d.desc, d.srcLang, d.dstLang, d.srcText, got, d.wantDstText)
            }
        })
    }
}
```

以下是一些应当避免的做法示例：

<div class='badcode'></div>

```go
// Too wordy.
t.Run("check that there is no mention of scratched records or hovercrafts", ...)
// Slashes cause problems on the command line.
t.Run("AM/PM confusion", ...)
```

另见
[Go 提示 #117：子测试名称](https://google.github.io/styleguide/go/index.html#gotip)。

[Go test runner]: https://golang.org/cmd/go/#hdr-Testing_flags
[identify the inputs]: #identify-the-input
[special meaning for test filters]: https://blog.golang.org/subtests#:~:text=Perhaps%20a%20bit,match%20any%20tests

<a id="table-driven-tests"></a>

### 表驱动测试

当许多不同的测试用例可以用相似的测试逻辑来检验时，
就使用表驱动测试。

*   检验函数的实际输出是否等于预期输出时。
    例如大量的 [tests of `fmt.Sprintf`]，或下面的
    最小片段。
*   检验函数的输出是否始终符合同一组不变式时。
    例如 [tests for `net.Dial`]。

[tests of `fmt.Sprintf`]: https://cs.opensource.google/go/go/+/master:src/fmt/fmt_test.go
[tests for `net.Dial`]: https://cs.opensource.google/go/go/+/master:src/net/dial_test.go;l=318;drc=5b606a9d2b7649532fe25794fa6b99bd24e7697c

下面是表驱动测试的最小结构。如有需要，可以使用
不同的名称，或添加子测试、设置与清理函数等额外
设施。请始终牢记[有用的测试失败信息](#useful-test-failures)。

<div class='goodcode'></div>

```go
func TestCompare(t *testing.T) {
    compareTests := []struct {
        a, b string
        want int
    }{
        {"", "", 0},
        {"a", "", 1},
        {"", "a", -1},
        {"abc", "abc", 0},
        {"ab", "abc", -1},
        {"abc", "ab", 1},
        {"x", "ab", 1},
        {"ab", "x", -1},
        {"x", "a", 1},
        {"b", "x", -1},
        // test runtime·memeq's chunked implementation
        {"abcdefgh", "abcdefgh", 0},
        {"abcdefghi", "abcdefghi", 0},
        {"abcdefghi", "abcdefghj", -1},
    }

    for _, test := range compareTests {
        got := Compare(test.a, test.b)
        if got != test.want {
            t.Errorf("Compare(%q, %q) = %v, want %v", test.a, test.b, got, test.want)
        }
    }
}
```

**注意**：上面这个例子中的失败消息满足
[标明函数](#identify-the-function)以及
[标明输入](#identify-the-input)的准则。没有必要
[用编号标识行](#table-tests-identifying-the-row)。

当某些测试用例需要用与其他测试用例不同的逻辑来检验时，
编写多个测试函数是合适的做法，具体说明见
[GoTip #50: Disjoint Table Tests]。

当新增的测试用例很简单（例如基本的错误检查），且不会在
表驱动测试的循环体中引入带条件的代码流时，把它纳入
现有测试是允许的，不过使用这类逻辑要谨慎。今天看似
简单的东西，可能会逐渐演变成难以维护的
代码。

例如：

```go
func TestDivide(t *testing.T) {
    tests := []struct {
        dividend, divisor int
        want              int
        wantErr           bool
    }{
        {
            dividend: 4,
            divisor:  2,
            want:     2,
        },
        {
            dividend: 10,
            divisor:  2,
            want:     5,
        },
        {
            dividend: 1,
            divisor:  0,
            wantErr:  true,
        },
    }

    for _, test := range tests {
        got, err := Divide(test.dividend, test.divisor)
        if (err != nil) != test.wantErr {
            t.Errorf("Divide(%d, %d) error = %v, want error presence = %t", test.dividend, test.divisor, err, test.wantErr)
        }

        // In this example, we're only testing the value result when the tested function didn't fail.
        if err != nil {
            continue
        }

        if got != test.want {
            t.Errorf("Divide(%d, %d) = %d, want %d", test.dividend, test.divisor, got, test.want)
        }
    }
}
```

测试代码中更复杂的逻辑，例如基于测试设置中条件差异
（往往取决于表驱动测试的输入参数）的复杂错误检查，
当表中每一项都有针对输入的专门逻辑时，可能
[难以理解](guide#maintainability)。如果测试用例逻辑不同
但设置相同，那么在单个测试函数内使用一连串
[子测试](#subtests)可能更易读。测试辅助函数也有助于
简化测试设置，从而保持测试主体的可读性。

可以把表驱动测试与多个测试函数结合使用。例如，
既要检验函数的输出与预期输出完全一致，又要检验
函数对无效输入返回非 nil 错误时，最佳做法是编写两个
独立的表驱动测试函数：一个用于正常的非错误输出，
另一个用于错误输出。

[GoTip #50: Disjoint Table Tests]: https://google.github.io/styleguide/go/index.html#gotip

<a id="table-tests-data-driven"></a>

#### 数据驱动的测试用例

表驱动测试的行有时会变得很复杂，行中的取值决定了
测试用例内部的条件行为。测试用例之间的重复所带来的
额外清晰度，对于可读性而言是必要的。

<div class='goodcode'></div>

```go
type decodeCase struct {
    name   string
    input  string
    output string
    err    error
}

func TestDecode(t *testing.T) {
    // setupCodex is slow as it creates a real Codex for the test.
    codex := setupCodex(t)

    var tests []decodeCase // rows omitted for brevity

    for _, test := range tests {
        t.Run(test.name, func(t *testing.T) {
            output, err := Decode(test.input, codex)
            if got, want := output, test.output; got != want {
                t.Errorf("Decode(%q) = %v, want %v", test.input, got, want)
            }
            if got, want := err, test.err; !cmp.Equal(got, want) {
                t.Errorf("Decode(%q) err %q, want %q", test.input, got, want)
            }
        })
    }
}

func TestDecodeWithFake(t *testing.T) {
    // A fakeCodex is a fast approximation of a real Codex.
    codex := newFakeCodex()

    var tests []decodeCase // rows omitted for brevity

    for _, test := range tests {
        t.Run(test.name, func(t *testing.T) {
            output, err := Decode(test.input, codex)
            if got, want := output, test.output; got != want {
                t.Errorf("Decode(%q) = %v, want %v", test.input, got, want)
            }
            if got, want := err, test.err; !cmp.Equal(got, want) {
                t.Errorf("Decode(%q) err %q, want %q", test.input, got, want)
            }
        })
    }
}
```

在下面的反例中，请注意在用例设置里很难区分每个
测试用例使用的是哪种 `Codex`。（高亮部分违背了
[TotT：数据驱动陷阱！][tott-97] 中的建议。）

<div class='badcode'></div>

```go
type decodeCase struct {
  name   string
  input  string
  codex  testCodex
  output string
  err    error
}

type testCodex int

const (
  fake testCodex = iota
  prod
)

func TestDecode(t *testing.T) {
  var tests []decodeCase // rows omitted for brevity

  for _, test := tests {
    t.Run(test.name, func(t *testing.T) {
      var codex Codex
      switch test.codex {
      case fake:
        codex = newFakeCodex()
      case prod:
        codex = setupCodex(t)
      default:
        t.Fatalf("Unknown codex type: %v", codex)
      }
      output, err := Decode(test.input, codex)
      if got, want := output, test.output; got != want {
        t.Errorf("Decode(%q) = %q, want %q", test.input, got, want)
      }
      if got, want := err, test.err; !cmp.Equal(got, want) {
        t.Errorf("Decode(%q) err %q, want %q", test.input, got, want)
      }
    })
  }
}
```

[tott-97]: https://testing.googleblog.com/2008/09/tott-data-driven-traps.html

<a id="table-tests-identifying-the-row"></a>

#### 标识行

不要用测试在测试表中的索引来替代为测试命名或
打印输入。没人愿意翻遍你的测试表、逐条数出条目，
只为弄清是哪个测试用例在失败。

<div class='badcode'></div>

```go
tests := []struct {
    input, want string
}{
    {"hello", "HELLO"},
    {"wORld", "WORLD"},
}
for i, d := range tests {
    if strings.ToUpper(d.input) != d.want {
        t.Errorf("Failed on case #%d", i)
    }
}
```

在测试结构体中添加测试描述，并把它与失败消息
一起打印。使用子测试时，子测试名称应能有效
标识对应的行。

**重要：** 尽管 `t.Run` 会限定输出与执行的作用域，
你仍必须始终[identify the input]。表驱动测试的行名
必须遵循 [subtest naming] 准则。

[identify the input]: #identify-the-input
[subtest naming]: #subtest-names

<a id="mark-test-helpers"></a>

### 测试辅助函数

测试辅助函数是执行设置或清理任务的函数。测试辅助
函数中发生的所有失败都应视为环境的失败（而不是
被测代码的问题）——例如，由于本机没有更多空闲端口，
测试数据库无法启动。

如果传入 `*testing.T`，请调用 [`t.Helper`]，把测试
辅助函数中的失败归因到调用该辅助函数的那一行。
该参数应排在 [context](#contexts) 参数（若存在）之后、
其余所有参数之前。

<div class='goodcode'></div>

```go
func TestSomeFunction(t *testing.T) {
    golden := readFile(t, "testdata/golden-result.txt")
    // ... tests against golden ...
}

// readFile returns the contents of a data file.
// It must only be called from the same goroutine as started the test.
func readFile(t *testing.T, filename string) string {
    t.Helper()
    contents, err := runfiles.ReadFile(filename)
    if err != nil {
        t.Fatal(err)
    }
    return string(contents)
}
```

当这种模式掩盖了测试失败与导致失败的条件之间的联系时，
就不要使用它。具体来说，关于
[断言库](#assert) 的准则仍然适用，且不应使用 [`t.Helper`]
来实现这类库。

**提示：** 关于测试辅助函数与断言辅助函数之间的区别，
请参见[最佳实践](best-practices#test-functions)。

尽管上面说的是 `*testing.T`，但大部分建议同样适用于
基准测试和模糊测试的辅助函数。

[`t.Helper`]: https://pkg.go.dev/testing#T.Helper

<a id="test-package"></a>

### 测试包

<a id="TOC-TestPackage"></a>

<a id="test-same-package"></a>

#### 同包测试

测试可以定义在与被测代码相同的包中。

要在同一个包中编写测试：

*   把测试放在 `foo_test.go` 文件中
*   测试文件使用 `package foo`
*   不要显式导入被测包

<div class='goodcode'></div>

```build
go_library(
    name = "foo",
    srcs = ["foo.go"],
    deps = [
        ...
    ],
)

go_test(
    name = "foo_test",
    size = "small",
    srcs = ["foo_test.go"],
    library = ":foo",
    deps = [
        ...
    ],
)
```

同包中的测试可以访问包内未导出的标识符。
这可能带来更好的测试覆盖率和更简洁的测试。请注意，
测试中声明的任何 [examples] 都不会带有用户在自己的
代码中所需的包名。

[`library`]: https://github.com/bazelbuild/rules_go/blob/master/docs/go/core/rules.md#go_library
[examples]: #examples

<a id="test-different-package"></a>

#### 异包测试

把测试定义在与被测代码相同的包中，并不总是合适，
有时甚至不可能。这种情况下，使用带 `_test` 后缀的
包名。这是对[包名](#package-names)中「不使用下划线」
规则的一个例外。例如：

*   如果某个集成测试没有明显所属的目标库

    <div class='goodcode'></div>

    ```go
    package gmailintegration_test

    import "testing"
    ```

*   如果在同一个包中定义测试会导致循环依赖

    <div class='goodcode'></div>

    ```go
    package fireworks_test

    import (
      "fireworks"
      "fireworkstestutil" // fireworkstestutil also imports fireworks
    )
    ```

<a id="use-package-testing"></a>

### 使用 `testing` 包

Go 标准库提供了 [`testing` package]。这是 Google 代码库中
Go 代码唯一允许使用的测试框架。具体而言，
[断言库](#assert) 和第三方测试框架都
不被允许。

`testing` 包为编写良好的测试提供了一套精简但完整的
功能：

*   顶层测试
*   基准测试
*   [可运行示例](https://blog.golang.org/examples)
*   子测试
*   日志
*   失败与致命失败

这些功能被设计为与核心语言特性（如
[composite literal] 和 [if-with-initializer] 语法）协同工作，
让测试编写者能够写出 [clear, readable, and maintainable tests]。

[`testing` package]: https://pkg.go.dev/testing
[composite literal]: https://go.dev/ref/spec#Composite_literals
[if-with-initializer]: https://go.dev/ref/spec#If_statements

<a id="non-decisions"></a>

## 未作规定之事

风格指南无法为所有事项列举出正面的规定，也无法
穷举所有它不表态的事项。尽管如此，下面列出几项
可读性社区此前曾讨论过、
但尚未达成共识的事项。

*   **用零值初始化局部变量**。`var i int` 与 `i := 0`
    等价。另见 [initialization best practices]。
*   **空复合字面量与 `new` 或 `make`**。`&File{}` 与 `new(File)`
    等价。`map[string]bool{}` 与 `make(map[string]bool)` 也
    一样。另见 [composite declaration best practices]。
*   **`cmp.Diff` 调用中 `got`、`want` 的参数顺序**。保持
    局部一致，并在失败消息中[附上说明](#print-diffs)。
*   **非格式化字符串用 `errors.New` 还是 `fmt.Errorf`**。
    `errors.New("foo")` 与 `fmt.Errorf("foo")` 可以互换使用。

如果出现特殊情况再次涉及这些事项，可读性导师
可能会给出可选的意见，但一般而言，作者可以自由
选择在当前情形下自己偏好的风格。

当然，如果风格指南未涵盖的内容确实需要更多讨论，
欢迎作者提问——既可以在具体的评审中提出，
也可以在内部留言板上提出。

[composite declaration best practices]: https://google.github.io/styleguide/go/best-practices#vardeclcomposite
[initialization best practices]: https://google.github.io/styleguide/go/best-practices#vardeclinitialization

<!--

-->

{% endraw %}
