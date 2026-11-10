# Google Vimscript 风格指南

*   Nate Soares
*   Artemis Sparks
*   David Barnett

<!-- mdformat on -->

## 背景

这是 vimscript 风格指南的精简版，因为 vimscript 本身
就是一门随意的语言。提交 vim 插件代码时，必须遵守
这些规则。有关 vimscript 细节的澄清、理由与解释，
请参阅[详尽版指南](./vimscriptfull.md)。

<!-- mdformat off -->
* TOC
{:toc}
<!-- mdformat on -->

## 可移植性

把 vimscript 写对并不容易。许多命令都依赖于用户的设置。
遵循这些指南，有望使你的脚本具备可移植性。

### 字符串

优先使用单引号字符串

在 vimscript 中，双引号字符串的语义不同，你很可能
并不需要它们（它们会破坏正则表达式）。

当需要使用转义序列（例如 `"\n"`）时，或者在确定无
影响且需要嵌入单引号时，才使用双引号字符串。

### 字符串匹配

优先使用 `=~#` 或 `=~?` 运算符族，而不是 `=~` 族。

匹配行为取决于用户的 ignorecase 与 smartcase 设置，
也取决于你是用 `=~`、`=~#` 还是 `=~?` 运算符族
进行比较。比较字符串时应显式使用 `=~#` 和 `=~?`
运算符族，除非你确实需要遵循用户的大小写敏感
设置。

### 正则表达式

所有正则表达式都加上 `\m\C` 前缀。

除大小写敏感设置外，正则表达式行为还取决于用户的
nomagic 设置。要让正则表达式表现得如同设置了
nomagic 和 noignorecase，请给所有正则加上 `\m\C` 前缀。

只要是有意且明确的，也可以使用其他 magic 级别
（`\v`）和大小写设置（`\c`）。

### 危险命令

避免带有意外副作用的命令。

避免使用 `:s[ubstitute]`，因为它会移动光标并打印
错误消息。优先使用更适合脚本的函数（例如 `search()`）。

对许多 vim 命令而言，都有副作用更小的函数能完成
同样的事。内置函数列表见 `:help function-list`。

### 脆弱的命令

避免依赖用户设置的命令。

始终使用 `normal!` 而不是 `normal`。后者依赖于用户的
按键映射，可能做出任何事情。

避免使用 `:s[ubstitute]`，因为它的行为取决于多项局部设置。

此处未列出的其他命令同理。

### 捕获异常

匹配错误码，而不是错误文本。

错误文本可能依赖于区域设置。

## 通用指南

### 消息提示

尽量少向用户发送消息。

吵闹的脚本令人厌烦。仅在以下情况下向用户发送消息：

*   一个长时间运行的进程已启动。
*   发生了错误。

### 类型检查

尽可能使用严格而显式的检查。

Vimscript 在处理某些类型时存在不安全、不直观的行为。
例如 `0 == 'foo'` 求值为 true。

尽可能使用严格的比较运算符。与字符串字面量比较时，
使用 `is#` 运算符。否则，优先使用
`maktaba#value#IsEqual` 或显式检查 `type()`。

使用变量前显式检查其类型。使用 `maktaba#ensure` 中的
函数，或检查 `maktaba#value` 或 `type()` 并抛出你自己的
错误。

对可能改变类型的变量使用 `:unlet`，尤其是在循环
内部赋值的变量。

### Python

谨慎使用。

仅在 python 提供关键功能时才使用它，例如编写
多线程代码时。

### 其他语言

改用 vimscript。

避免使用 ruby、lua 等其他脚本语言。我们无法保证
最终用户的 vim 在编译时支持非 vimscript 的
语言。

### 样板代码

使用 [maktaba](https://github.com/google/maktaba)。

maktaba 消除了样板代码，包括：

*   插件创建
*   错误处理
*   依赖检查

### 插件布局

把功能组织成模块化的插件

把你的功能组织为一个插件，统一放在一个与
插件同名的目录（或代码仓库）中（如需要，
可加 "vim-" 前缀或 ".vim" 后缀）。应按需
拆分为 plugin/、autoload/ 等子目录，并以
addon-info.json 格式声明元数据（详见
[VAM 文档](https://goo.gl/CUXJZC)）。

### 函数

放在 autoload/ 目录中，定义时带 `[!]` 和 `[abort]`。

自动加载让函数按需加载，从而加快启动速度，
并强制实现函数命名空间。

脚本局部函数是可以的，但也应放在 autoload/ 中，
并由自动加载的函数调用。

非库类插件应暴露命令而非函数。命令逻辑应提取到
函数中并自动加载。

`[!]` 让开发者可以无报错地重新加载其函数。

`[abort]` 强制函数在遇到错误时中止。

### 命令

放在 plugin/commands.vim 中或 ftplugin/ 目录下，
定义时不带 `[!]`。

通用命令放在 `plugin/commands.vim` 中。特定文件类型的
命令放在 `ftplugin/` 中。

省略 `[!]` 可防止插件悄悄覆盖已有的命令。
命令冲突应由用户自行解决。

### 自动命令

把它们放在 `plugin/autocmds.vim` 中，并置于 augroup 内。

把所有自动命令都放在 augroup 中。

augroup 的名称应唯一。它要么就是插件名，要么
以插件名作为前缀。

在该 augroup 中定义新的自动命令之前，先用
`autocmd!` 清空该 augroup。这使插件可重入。

### 映射

把它们放在 `plugin/mappings.vim` 中，使用
`maktaba#plugin#MapPrefix` 获取前缀。

所有按键映射都应定义在 `plugin/mappings.vim` 中。

部分映射（参见 `:help using-<Plug>`。）应定义在
`plugin/plugs.vim` 中。

### 设置

局部地修改设置

使用 `:setlocal` 和 `&l:`，而不是 `:set` 和 `&`，
除非你有明确的理由不这么做。

## 风格

遵循 google 的风格约定。拿不准时，把 vimscript
风格当作 python 风格来对待。

### 空白

与 python 类似。

*   缩进使用两个空格
*   不要使用制表符
*   运算符两侧加空格

    这不适用于命令的参数。

    <div class='goodcode'></div>

    ```
    let s:variable = 'concatenated ' . 'strings'
    command -range=% MyCommand
    ```

*   不要引入尾随空白

    不必特意去清除它。

    在为用户输入预置命令的映射中，允许出现尾随
    空白，例如 `noremap <leader>gf :grep -f `。

*   把行宽限制在 80 列以内

*   续行缩进四个空格

    <div class='goodcode'></div>

    ```
    let l:something = SomeReallyLongFunctionName(
        \ 'arg1', 0, ['XXXXX'], {'somekey': 9999999999})
    ```

*   不要对齐命令的参数

    <div class='badcode'></div>

    ```
    command -bang MyCommand  call myplugin#foo()
    command       MyCommand2 call myplugin#bar()
    ```

    <div class='goodcode'></div>

    ```
    command -bang MyCommand call myplugin#foo()
    command MyCommand2 call myplugin#bar()
    ```

### 命名

一般使用 `plugin-names-like-this`、`FunctionNamesLikeThis`、
`CommandNamesLikeThis`、`augroup_names_like_this`、`variable_names_like_this`。
变量一律加上其作用域前缀。

#### plugin-names-like-this

保持简短而贴切。

#### FunctionNamesLikeThis

脚本局部函数加上 `s:` 前缀

自动加载的函数不得带作用域前缀。

不要创建全局函数。改用自动加载的函数。

#### CommandNamesLikeThis

命令名应简洁，优先于通用的命令前缀。

#### variable_names_like_this

就命名而言，augroup 名称也算作变量。

#### 所有变量都加上其作用域前缀。

*   全局变量用 `g:`
*   脚本局部变量用 `s:`
*   函数参数用 `a:`
*   函数局部变量用 `l:`
*   Vim 预定义变量用 `v:`
*   缓冲区局部或窗口局部变量用 `b:` 或 `w:`

必须始终使用 `g:`、`s:` 和 `a:`。

`b:` 和 `w:` 会改变变量的语义；当需要缓冲区局部
或窗口局部语义时使用它们。

为保持一致、面向未来并避免微妙的 bug，应使用
`l:` 和 `v:`。它们并非强制要求。在新代码中加上
它们，但不必特意为其他地方补上。
