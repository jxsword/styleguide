# Google Vimscript 指南

*   Nate Soares
*   Artemis Sparks
*   David Barnett

<!-- mdformat on -->

## 背景

这是深入的 vimscript 指南。如果你只是一个想编写插件的普通用户，
那么[简略风格指南](./vimscriptguide.md)适合你。

这份相当详尽的指南深入探讨了理由与澄清。它
提供了一套理想化的规则，这些规则对于普通脚本编写者来说
过于严苛而不宜强推。

它面向那些想知道简略指南中某些决策缘由、
并希望了解安全使用 vimscript 一二之法的
用户。

郑重警告：Vimscript 是一个令人抓狂的深渊。当你凝视它时，它也在
凝视你。请谨慎前行。

<!-- mdformat off -->
* TOC
{:toc}
<!-- mdformat on -->

## 可移植性

Vim 具有高度可配置性。用户可以更改许多默认设置，
包括大小写敏感性、正则表达式规则、替换规则
等等。为了让你的 vimscript 对所有用户都能正常工作，请遵循以下
准则：

*   始终用 `\m`、`\v`、`\M` 或 `\V` 之一为正则表达式添加前缀
    （优先选择最简洁的写法）

    *   用户可以更改正则表达式的全局“magic 级别”。这
        会改变正则表达式中原子的解析方式，包括 `.`、`*` 和
        `{`。
    *   即使你的正则表达式不包含受 `magic` 设置影响的字符，
        也必须用 magic 控制原子之一为其添加前缀。这样做可以让你的
        正则表达式面向未来，避免其他开发者修改它时
        忘记添加控制原子。
    *   在“magic 级别”不起作用的语境下使用正则表达式时（例如调用
        `substitute()`），这一做法是推荐但不强制的，因为它能让模式
        自成一体，并使其在其他语境下复用时也
        面向未来。
    *   如果你对于该使用哪种类型的正则表达式没有偏好，
        优先选择能让你的正则表达式最简洁的那种。

*   在脚本中避免使用 `:s[ubstitute]`。

    *   `:substitute` 会移动光标。
    *   当匹配不存在时，`:substitute` 会输出一条错误消息。
    *   `g` 标志的含义取决于 `gdefault` 设置。如果你
        确实要使用 `:substitute`，必须先保存 `gdefault`，将其设为 `0` 或 `1`，
        执行替换，然后再恢复它。
    *   想要一种安全方式在缓冲区中替换文本的脚本作者，
        建议使用 `maktaba#buffer#Replace`。

*   对字符串始终使用区分大小写的运算符（`=~#` 和 `=~?`，绝不要使用
    `=~`）。

    *   这也适用于 `!~ == != > >= < <= is` 和 `isnot`。
    *   这仅适用于字符串。`==` 和 `>=` 用于数字是没问题的，但
        `==#` 和 `>=#` 必须用于比较可能是字符串的值。
    *   `=~` 及其同类运算符的行为依赖于 `ignorecase`
        设置。
    *   当你明确想要遵循用户的 `ignorecase` 设置时，
        可以打破这一规则。但你要准备好为你的理由辩护。

*   当把正则表达式作为函数参数使用时，为其添加
    `\c` 或 `\C` 前缀。

    *   这会强制显式匹配或忽略大小写。
    *   当使用指定大小写敏感性的运算符（如 `=~#`）
        比较正则表达式时，这一做法是推荐但不强制的。
    *   当你的正则表达式在匹配语法、外部 API、
        外部消息以及大多数其他情况时，这一规则适用。
    *   在匹配缓冲区中的文本时不适用。当匹配缓冲区中的
        文本时，你应当遵循 `ignorecase` 设置。
    *   每当你明确想要遵循 `ignorecase` 设置时，
        也可以忽略这一规则。请准备好为你的理由辩护。

*   始终使用 `normal!` 而非 `normal`。

    *   如果省略 `!`，该命令会使用用户的按键映射，
        你将完全无法预知你的宏会做什么。

*   始终使用 `noremap` 系列命令。

    *   你的插件通常不应引入映射，但如果引入了，
        `map` 命令会遵循用户已有的映射，从而可能
        做出任何事情。

*   使用 `catch` 时，匹配错误码而非错误文本。

    *   错误文本可能依赖于区域设置。
    *   参见 `:help error-messages`。

总之，要使所有命令和函数免受用户设置的影响。

## 语言指南

*   行续接：**是**

    *   支持 vi 兼容模式的插件必须按**勘误部分**所述
        保存并恢复兼容性选项，以便行
        续接正常工作。

*   异常：**是，但须谨慎**

    *   在抛出的异常消息中始终使用错误码。
    *   优先使用 `maktaba` 中的 `maktaba#error` 错误码。
    *   退而使用 vim 错误码。参见 `:help error-messages`。
    *   使用 `maktaba#error#Message` 生成自定义错误消息。
    *   公共用户命令和函数应在错误传到用户之前捕获并回显已知错误
        （通过 echomsg 或 `maktaba#error#Shout`）。

        <div class='goodcode'></div>

        ```
        try
          call somelibrary#FuncThatCanFail()
        catch /ERROR(NotFound):/
          call maktaba#error#Shout('Failed to do thing: %s', v:exception)
        endtry
        ```

    *   建议库函数向调用者抛出异常，而不是自行回显，以便
        调用者能够管理错误状况。始终在 vimdoc 文档注释中
        使用 `@throws` 指令来记录抛出的错误。

*   全局变量：**仅作为配置使用**

    *   参见插件指南。

*   消息输出：**尽可能少。**

    *   吵闹的脚本令人讨厌。
    *   当发生错误时通知用户。
    *   当一项耗时较长的操作开始
        工作时，通知用户。
    *   除此之外避免输出消息。

*   类型检查：**尽可能使用严格且显式的检查。**

    *   Vimscript 在处理某些类型时具有不安全、不直观的行为。
        例如，`0 == 'foo'` 的求值结果为真。
    *   尽可能使用严格比较运算符。与字符串字面量比较时，
        使用 `is#` 运算符。否则，优先使用
        `maktaba#value#IsEqual` 或显式检查 `type()`。
    *   在使用变量之前显式检查其类型。使用
        `maktaba#ensure` 中的函数，或者检查 `maktaba#value` 或 `type()` 并抛出
        你自己的错误。
    *   对于可能改变类型的变量，尤其是
        循环内赋值的变量，使用 `:unlet`。

*   FuncRef：**大多数情况下不使用。**

    *   FuncRef 的命名限制执行得不一致。（函数
        可以拥有 FuncRef 无法拥有的名称。）
    *   FuncRef 被重新赋值的能力不一致（在 Vim 7.2 及
        更早版本中，必须在赋值前先 unlet 一个 FuncRef）。
    *   在大多数需要 FuncRef 的情况下，字符串同样管用：
        只需传入你本来用于创建 FuncRef 的那个字符串即可。
    *   考虑改用 `maktaba#function` 来创建和
        操作函数的句柄。

*   Python：**谨慎使用**

    *   不利于代码复用，因为嵌入在 Python 插件中的 Python 代码
        很难在插件之间共享。
    *   使用 Python 会引入 Python 语言版本依赖，这些依赖
        很可能过时。
    *   例外：对于需要在后台执行工作的插件功能，
        使用 Python 是合理的，因为 vimscript 做不到这一点。

*   Ruby：**否**

    *   我们无法假定 Ruby 的互操作性。
    *   你不应依赖用户所安装的
        Ruby 语言版本。

*   Lua：**否**

    *   原因与 Ruby 相同。

*   字典函数：**鼓励使用**

    *   Vimscript 可以将函数附加到字典上。这类函数
        可以访问 `self` 参数，该参数用于访问字典状态。
    *   在 Python 中你会使用类的地方，使用它们。
    *   不要过度使用这一特性；它对辅助函数
        或 API 函数并无必要，仅适用于封装对象。

所有其他语言特性都可以随意使用。

## 结构

*   所提供的功能应当打包为模块化插件。

    *   你插件中的每个函数都应当是专属于该插件的。
    *   通用工具函数应当抽象为库插件。
    *   使用 `maktaba` 管理依赖。

*   `plugin-names-like-this`

    *   插件名称应当描述性强且简洁。

*   每个插件必须由单个目录（或代码仓库）构成，与插件同名
    （如需要可带 “vim-” 前缀或 “.vim” 后缀）。

*   插件元数据应当用 addon-info.json 格式声明（详见
    [VAM 文档](https://goo.gl/CUXJZC)）。

*   函数应当放在你插件的 `autoload/` 子目录中。

    *   这样它们可以被延迟加载，从而加快启动速度。
    *   这有助于 vim 强制实施命名空间约定。

*   `plugin/` 或 `instant/` 目录中的每个文件都应当以以下
    样板代码开头

    <div class='goodcode'></div>

    ```
    let [s:plugin, s:enter] = maktaba#plugin#Enter(expand('<sfile>:p'))
    if !s:enter
      finish
    endif
    ```

    （这可以防止重入，并允许用户有选择地禁用
    某些功能。）

*   用户配置应当通过
    `instant/flags.vim` 中定义的插件标志来实现。

    *   使用 `call s:plugin.Flag('FLAGNAME', DEFAULT_VALUE)` 定义标志。
    *   用户可以使用 `:Glaive` 命令配置这些标志（参见
        [glaive](https://github.com/google/glaive)）。

*   命令、自动命令、映射以及设置更改应当出现在
    `plugin/` 或 `ftplugin/` 子目录中。

    *   所有命令都应当定义在 `plugin/commands.vim` 或 `ftplugin/`
        文件中。
    *   自动命令应当定义在 `plugin/autocmds.vim` 中，并且位于一个
        augroup 之内。
    *   映射应当定义在 `plugin/mappings.vim` 中，并且除非用户显式
        启用，否则默认禁用。
    *   如果插件配置了任何标准 vim 设置，这些设置应当在
        `plugin/settings.vim` 或 `instant/settings.vim` 中配置。

*   避免使用 `after/` 子目录。

    *   `after/` 应当为用户的保留空间。
    *   当插件使用 `after/` 时，
        用户很难添加自己的覆盖配置。

### 库与功能

将提供库的插件与提供命令的插件分开。

许多插件要么提供用户功能（命令、自动命令等），要么提供 API
（由 autoload 函数构成），但不会两者兼而有之。我们鼓励这种
分离，因为它允许其他插件引入一个库，而无需同时引入
会影响最终用户的命令、设置更改以及其他插件功能。

### 配置

不要覆盖用户的设置。尽可能提供可配置性：这正是
Vim 的精髓所在。

*   使用 maktaba 标志进行插件配置。用户可以使用
    `:Glaive` 命令配置它们。

*   在设置配置变量之前，先检查它们是否已存在。

    <div class='goodcode'></div>

    ```
    if !exists('g:myplugin_option')
      let g:myplugin_option = 1
    endif
    ```

## 风格指南

遵循全 Google 范围的风格约定。如有疑问，参照 Google Python 风格。

### 文档

使用 [vimdoc](https://github.com/google/vimdoc)。

提供由 [vimdoc](https://github.com/google/vimdoc) 生成的帮助文件。

在 .vim 文件中编写符合 vimdoc 标准的文档，并在 addon-info.json
文件中包含 “description” 和 “author” 等字段（参见
[VAM 文档](https://goo.gl/CUXJZC)）。

### 空白符

遵循全 Google 范围的约定。

*   使用两个空格进行缩进。
*   不要使用制表符。
*   运算符两侧使用空格，但命令的参数除外。

    *   在命令的运算符两侧使用空格通常是不合法的语法。Vimscript
        对这一点执行得并不一致。为安全起见，命令参数
        周围始终不要留空白。

        <div class='goodcode'></div>

        ```
        let s:variable = "concatenated " . "strings"
        command -range=% MyCommand
        ```

        <div class='badcode'></div>

        ```
        let s:variable="concatenated "."strings"
        command -range = % MyCommand
        ```

*   不要引入行尾空白。

    *   你不必特意去删除它。

*   将每行限制在 80 列宽以内。

*   续行缩进四个空格。

    <div class='goodcode'></div>

    ```
    let l:something = SomeReallyLongFunctionName(
        \ 'arg1', 0, ['XXXXX'], {'somekey': 9999999999})
    ```

*   不要浪费空白去对齐相似命令中的公共片段。这种对齐
    既难以维护，维护成本也高。

    <div class='goodcode'></div>

    ```
    command -bang MyCommand call myplugin#foo()
    command MyCommand2 call myplugin#bar()
    ```

    <div class='badcode'></div>

    ```
    command -bang MyCommand  call myplugin#foo()
    command       MyCommand2 call myplugin#bar()
    ```

#### 行续接

*   优先在语义边界处进行行续接。

    <div class='goodcode'></div>

    ```
    command SomeLongCommand
        \ call some#function()
    ```

    <div class='badcode'></div>

    ```
    command SomeLongCommand call
        \ some#function()
    ```

    请运用你的最佳判断。

*   在表示行续接的反斜杠之后放一个空格。

    *   续接多行命令时，如有必要可以用竖线替代这个
        空格，如下所示：

        <div class='goodcode'></div>

        ```
        autocommand BufEnter <buffer>
            \ if !empty(s:var)
            \|  call some#function()
            \|else
            \|  call some#function(s:var)
            \|endif
        ```

*   在可以避免的情况下，不要续接多行命令。优先使用
    函数调用。

#### 注释

*   在注释文本前的 `"` 之后放一个空格。

    <div class='goodcode'></div>

    ```
    " I am a line comment.
    call call(s:my_function)
    ```

*   不要使用行内注释。

    *   某些命令将它们视为注释，而另一些则视为未闭合的引号。
        存在许多边缘情况。它既难以写对，也
        难以维护。
    *   在你本想使用行内注释的地方，改为在上一行
        放置一条行注释。
    *   在注释中留空行时，空行也要
        包含引号。

        <div class='goodcode'></div>

        ```
        " I am one continuous
        "
        " comment block
        ```

### 变量

`plugin-names-like-this`、`FunctionNamesLikeThis`、`CommandNamesLikeThis`、
`augroup_names_like_this`、`variable_names_like_this`。为所有变量添加
其作用域前缀。

*   `variable_names_like_this`

    *   FuncRef 变量被视为函数，应当像函数一样命名。
    *   这种（病态的）约定由 vim 本身强制实施。

*   全局变量以 `g:` 为前缀

    *   Vimscript 允许你创建不带前缀的全局变量。
    *   将不带前缀的全局变量引入作用域
        是非常糟糕的做法。
    *   全局变量只应当用于插件配置。
    *   这不适用于 `autoload` 目录中定义的函数。

*   脚本局部变量以 `s:` 为前缀

    *   这可以防止插件之间的命名空间冲突。
    *   这也适用于脚本局部函数。

*   函数参数以 `a:` 为前缀

    *   这由 vim 本身强制实施。

*   函数局部变量以 `l:` 为前缀

    *   这并非由 vimscript 强制实施，但属于良好实践。
    *   它有助于你记住所有其他变量都必须
        添加作用域前缀。
    *   `l:` 可以区分函数局部变量与 vim 预定义变量。
        例如，`count` 指的是 `v:count`，而非 `l:count`。
    *   它让你的脚本能够面向未来，免受新引入的
        vim 预定义变量的影响。

*   vim 预定义变量以 `v:` 为前缀

    *   这并非由 vimscript 强制实施，但属于良好实践。
    *   它能提供上下文，说明这个（未声明的）变量
        来自何处。
    *   它提醒你该变量不可被赋值。

*   缓冲区局部或窗口局部变量以 `b:` 或 `w:` 为前缀

    *   这对于维护每缓冲区或每窗口状态的插件很有用。

### 字符串

优先使用单引号。

优先使用单引号字符串。具体而言，按优先级顺序：

*   正则表达式始终使用单引号。

    *   `'\s*'` 与 `"\s*"` 并不相同。
    *   单引号可以避免使用过多的反斜杠。
    *   在单引号字符串中，两个连续的单引号转义为一个单引号：
        `'example ('')'` 表示字符串 `example (')`。

*   如果你的字符串需要转义字符（`\n`、`\t` 等），
    使用双引号。

    *   转义字符无法在单引号字符串中表达。
    *   记住，正则表达式中的 `'\n'` 并不表示换行符，而是表示
        “\n”。只有当你想把被表示的字符本身（例如换行符）
        嵌入字符串时，才需要使用双引号。

*   如果你的字符串既不包含转义字符也不包含单引号，
    使用单引号字符串。

    *   Vimscript 中的大多数字符串都是正则表达式，因此
        这样能提供最大程度的一致性。

*   如果你的非正则字符串包含单引号但不包含双引号，
    使用双引号。

    *   如果没必要，不要费心转义字符串。
    *   这与 Python 的字符串规则类似。

*   如果你的字符串同时包含单引号和双引号，使用所需
    转义更少的那种引号风格。

    *   平局时优先使用单引号。

### 设置

优先使用长名称。在局部设置设置项。

*   优先使用内建设置的长名称（即优先用 `tabstop` 而非 `ts`）。
*   除非你明确想要设置全局设置，否则设置局部设置。

    *   使用 `setlocal` 和 `&l:` 而非 `set` 和 `&`。

## 使用指南

Vim 插件应当提供以下任意或全部内容：**命令**、
**自动命令**、**函数**、**状态行标志**以及**映射**。

### 命令

<div>

*   定义在 `plugin/commands.vim` 中。
*   CommandNamesLikeThis.
*   优先使用语义化名称而非统一前缀。
*   Do not use `[!]`
*   将逻辑提取到函数中。

</div>

*   `CommandNamesLikeThis`

*   命令应当定义在一个块中，彼此之间不留空白。

    *   以牺牲统一前缀为代价，对命令进行语义化命名。

        <div class='badcode'></div>

        ```
        command WhitespaceFixTrailing
        command WhitespaceFixIndentation
        ```

        <div class='goodcode'></div>

        ```
        command FixTrailingWhitespace
        command FixIndentation
        ```

*   使用不带叹号的 `command`。

    *   这会在启动时立即将命令名冲突告知用户。
    *   命令名冲突是一种错误，不应静默失败。
    *   插件已防止重入，因此单个 vim 会话
        不应尝试重新定义已定义的命令。

*   不要在命令中编写逻辑。

    *   改为委托给函数。
    *   在参数型参数（`<f-args>` 等）之前，先传入非参数型
        命令参数（`<bang>`、`<register>` 等）。
    *   否则变长参数函数将难以实现。

*   不要 autoload 命令。

    *   在被同一文件中的某个函数调用之前，
        autoload 的命令将不可用。
    *   打算在 .vimrc 中使用的命令，应当在使用 maktaba 的插件里
        定义于 `instant/commands.vim` 文件中，或者在非 maktaba
        插件中通过 autoload 函数显式安装。

<a id="commands-conventions"></a>

#### 约定

*   用 `'<bang>' == '!'` 将 `<bang>` 传给函数。

    *   该函数应当接收一个布尔型参数，而非字符串。

### 自动命令

<div>

*   定义在 `plugin/autocmds.vim` 中。
*   使用 augroup。
*   `augroup_names_like_this`。
*   先清空 augroup。
*   将逻辑提取到函数中。

</div>

*   所有自动命令都应当定义在 `plugin/autocmds.vim` 文件中。

    *   这允许用户通过
        `Glaive myplugin !plugin[autocmds]` 禁用你的自动命令。

*   在一个 `augroup` 块中声明所有自动命令。

    *   这允许你的自动命令通过 `autocmd!` 被清空。

    *   如果你的插件只有一个 `augroup`，那么 `augroup` 的名称应当与
        你的插件名称相同，将任何连字符替换为下划线。

    *   否则，`augroup` 名称应当以你的插件名称开头，
        后跟一个下划线。

*   不要在自动命令中编写逻辑。

    *   改为委托给函数。

*   创建新的 `augroup` 时，用 `autocmd!` 将其清空

    *   这让你的插件可以重入。

### 函数

<div>

*   FunctionNamesLikeThis.
*   Autoload 所有函数。
*   脚本局部函数以 `s:` 为前缀
*   Use `[!]`.
*   Use `[abort]`.

</div>

*   `FunctionNamesLikeThis`

    *   所有脚本局部函数以 `s:` 为前缀

*   不要提供全局函数。改为使用 autoload 函数。

*   在顶层函数之间放置两个空行。

*   用 `abort` 声明所有函数。

    *   如果你不这样做，函数的行为将取决于它是否在
        调用栈上的某个 `try..endtry` 块中被调用。
    *   `abort` 关键字强制函数行为保持一致。
    *   没有它，函数在发生错误后可能会（也可能不会）
        尝试继续执行。

*   使用带叹号的 `function!`。

    *   这让开发者能够重新 source 他们的脚本，并在
        不报错的情况下重载函数。
    *   函数名永远不应冲突，因为函数应当始终是脚本局部的，
        或者定义在 `autoload` 目录中。
    *   如果在 autoload 文件的任何函数中不使用叹号，当 vim 尝试
        重新 source 该文件时（例如，你引用了一个不存在的
        autoload 函数），将导致难以理解的错误。

*   使用 `...` 表示可选参数，而不要用于表示参数列表。

    *   Vimscript 函数最多接受 20 个参数。
    *   列表没有这样的长度限制。
    *   如果你用 `...` 来表示参数列表，当传入
        过多参数时，你的函数很可能会出错。

*   抛出异常，而不是打印错误。

    *   打印出来的错误无法被捕获。
    *   预期会出错的高层函数可以捕获它们并打印错误消息，但
        即便如此，这些函数在自身出错时也应当抛出自己的错误。

### 映射

<div>

*   在 `plugin/mappings.vim` 中提供选择启用的按键映射。
*   `<Plug>` 映射可以定义在 `plugin/plugs.vim` 中（与 mappings.vim 不同，
    plugs.vim 默认启用）。

</div>

*   在 `plugin/mappings.vim` 中定义按键映射，使用
    `maktaba#plugin#MapPrefix` 获取前缀。

    *   在特殊的 `plugin/mappings.vim` 文件中定义的映射默认会被
        禁用（由标准的 `maktaba#plugin#Enter()`
        样板代码实现）。
    *   用户可以使用 `Glaive myplugin plugin[mappings]` 启用按键映射。

*   使用 `<unique>` 创建所有映射。

    *   当用户存在映射冲突时，这会通知用户，而不是
        静默地覆盖他们已有的映射。

*   你可以在 `plugin/plugs.vim` 中使用 `<Plug>` 和你的插件名称
    来提供伪映射（与标准按键映射分开）。

    *   `<Plug>` 是一个无法被键入的序列。
    *   你可以像
        `noremap <Plug>namespace#MappingName some_key_sequence` 这样做，然后用户
        就可以用 `noremap <leader>x <Plug>namespace#MappingName` 来
        利用你的伪映射。
    *   伪映射**不应**放在 `plugin/mappings.vim` 中，否则
        它们将默认被禁用。
    *   这类伪映射应当命名为 `<Plug>` 后接你的插件名称、
        一个井号以及一个唯一的映射名称（像函数一样
        使用 CamelCase）。

*   始终使用 `noremap` 系列命令。绝不要使用 `map` 系列。

    *   `map` 依赖于用户已有的映射，并可能做出任何事情。

*   只对既产生移动又接受范围（range）的命令使用 `noremap`。

    *   `noremap` 会在普通模式、可视模式和 operator-pending 模式中创建映射。
    *   如果你不想要所有这些，请显式使用 `nnoremap`、`onoremap` 或
        `vnoremap`。

*   在映射中访问脚本局部变量时，始终使用 `<SID>` 替代
    `s:`。

    *   使用 `s:` 通常会失败，因为映射会尝试键入
        字面量的 s 和冒号。

## 约定

### 依赖检查

在 addon-info.json 中声明依赖，并使用 `maktaba`。

在 addon-info.json 中声明依赖，可以让符合规范的插件管理器
（如 VAM）确保依赖已安装。详见
[VAM 文档](https://goo.gl/CUXJZC)。

在依赖代码运行时调用 `maktaba#library#Require`，可以确保
依赖已安装，且其中不包含不安全的
非库文件。

### 状态行标志

使用 `<plugin-name>#status#Status()` 或其更细粒度的变体来
提供状态行标志。

以下是将状态行标志暴露给用户的约定。插件绝不应
修改用户的状态行，除非这正是该插件的唯一用途
（如 powerline 等）。

*   在 `<plugin-name>#status` 命名空间下提供 `Info`、`Alert`、`Warning` 和
    `Error` 函数。
*   `Info` 应当提供有关缓冲区状态的信息。
    *   示例：当前的 git 分支。
*   `Alert` 应当提供一个温和的提醒，表明缓冲区是非标准的。
    *   示例：readonly 设置已开启。
*   `Warning` 应当就缓冲区的当前状态提供一条警告。
    *   示例：文件已在别处被编辑。
*   `Error` 应当引起对缓冲区严重问题的注意。
    *   示例：文件未通过语法检查器。
*   遵循这些约定，用户可以轻松构建自己的状态行，
    按自己的喜好自定义详细程度和颜色。
*   所有函数都不应接受参数，并且应当返回空字符串或用方括号
    括起来的字符串，例如 `[Google]`。
    例如：
    *   尾部空白插件可能返回 `[$]`，如果文件
        包含尾部空白。
    *   散文写作插件在 vim 处于写作模式时可能返回 `[write]`。
*   考虑提供 `<plugin-name>#status#Status` 函数。
    *   它应当返回 `Error`、`Warning`、`Alert` 或
        `Info` 中第一个非空者。
    *   这对于那些只想要最相关标志、且
        没有彩色状态行的用户很有用。

## 禁用的命令

这些是只有少数插件才能使用的命令，通常
不应被你的插件使用。

*   Do not use `:match :2match` or `:3match`
    *   这些是为用户和 vim 本身保留的。
    *   使用 `matchadd()` 创建专属于你插件的匹配级别。
*   Do not use `echoerr`.
    *   `echoerr` 并不会打印你以为它会
        打印的红色错误消息。
    *   `echoerr` 会打印一条错误消息，以及关于
        `echoerr` 被调用位置的代码上下文。
    *   `echoerr` 最适合用于调试。
    *   如果你想要红色错误条，请将 `echohl` 与 `echomsg` 配合使用。
*   Use `echomsg` instead of `echo`.
    *   `echomsg` 消息可以通过 `:messages` 命令查看。
    *   `echo` 消息在重绘时会永久消失，这对那些
        未能及时读取消息的用户来说可能非常恼人。

## 布局

如适用，将 `plugin/` 文件按以下小节布局，
小节之间用两个空行分隔：

*   脚本常量声明
*   配置变量声明
*   其他声明（`commands.vim` 文件中的命令、
    `autocmds.vim` 文件中的自动命令等）

如适用，将 `autoload/` 文件按以下小节布局，
小节之间用两个空行分隔：

*   `maktaba#library#Require` calls
*   脚本局部变量
*   脚本局部函数
*   私有 autoload 函数
*   公有 autoload 函数

这是推荐的约定，并非强制。

## 推荐的快捷方式

使用以下快捷方式：

*   `catch` over `catch /.*/`
*   当返回值没有语义用途时，使用 `return` 而非 `return 0`。

## 勘误

本节探究 vimscript 中一些较为晦涩的角落，解释那些
你但愿不必知晓的语言怪癖。

### 兼容模式

如果你不支持 vi 兼容模式，请优雅地失败。

当设置了 `compatible` 时，许多 vim 功能不可用。最常影响
vimscript 作者的 vim 功能是行续接。

如果你希望你的插件在开启了 vi 兼容性的 vim 中正常工作，你需要
在每个插件文件的开头保存兼容性选项、清空
它们，并在每个插件文件的结尾恢复它们。详见 `:help use-cpo-save`
。

依赖 maktaba 的插件通常无需担心兼容模式，因为 maktaba
目前只是禁用它并打印一条警告。