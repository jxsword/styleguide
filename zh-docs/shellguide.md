<!--
AUTHORS:
Prefer only GitHub-flavored Markdown in external text.
See README.md for details.
-->

# Shell 风格指南

由众多 Google 员工撰写、修订并维护。

## 目录

<!-- mdformat off -->

章节                                                                              | 内容
------------------------------------------------------------------------------------ | --------
[背景](#s1-background)                                                         | [使用哪个 Shell](#s1.1-which-shell-to-use) - [何时使用 Shell](#s1.2-when-to-use-shell)
[Shell 文件与解释器调用](#s2-shell-files-and-interpreter-invocation) | [文件扩展名](#s2.1-file-extensions) - [SUID/SGID](#s2.2-suid-sgid)
[环境](#s3-environment)                                                       | [STDOUT vs STDERR](#s3.1-stdout-vs-stderr)
[注释](#s4-comments)                                                             | [文件头](#s4.1-file-header) - [函数注释](#s4.2-function-comments) - [实现注释](#s4.3-implementation-comments) - [TODO 注释](#s4.4-todo-comments)
[格式](#s5-formatting)                                                         | [缩进](#s5.1-indentation) - [行长度与长字符串](#s5.2-line-length-and-long-strings) - [管道](#s5.3-pipelines) - [控制流](#s5.4-control-flow) - [case 语句](#s5.5-case-statement) - [变量展开](#s5.6-variable-expansion) - [引用](#s5.7-quoting)
[特性与陷阱](#s6-features-and-bugs)                                           | [ShellCheck](#s6.1-shellcheck) - [命令替换](#s6.2-command-substitution) - [Test、`[… ]` 与 `[[… ]]`](#s6.3-tests) - [测试字符串](#s6.4-testing-strings) - [文件名的通配符展开](#s6.5-wildcard-expansion-of-filenames) - [Eval](#s6.6-eval) - [数组](#s6.7-arrays) - [通过管道传给 while](#s6.8-pipes-to-while) - [算术运算](#s6.9-arithmetic) - [别名](#s6.10-aliases)
[命名约定](#s7-naming-conventions)                                         | [函数名](#s7.1-function-names) - [变量名](#s7.2-variable-names) - [常量与环境变量名](#s7.3-constants-and-environment-variable-names) - [源文件名](#s7.4-source-filenames) - [使用局部变量](#s7.5-use-local-variables) - [函数的位置](#s7.6-function-location) - [main](#s7.7-main)
[调用命令](#s8-calling-commands)                                             | [检查返回值](#s8.1-checking-return-values) - [内置命令与外部命令](#s8.2-builtin-commands-vs-external-commands)
[如有疑问：保持一致](#s9-conclusion)                                       |

<!-- mdformat on -->

<a id="s1-background"></a>

## 背景

<a id="s1.1-which-shell-to-use"></a>

### 使用哪个 Shell

Bash 是唯一允许用于可执行文件的 shell 脚本语言。

可执行文件必须以 `#!/bin/bash` 和尽可能少的标志开头。使用 `set` 来设置
shell 选项，这样即便以 `bash script_name` 的方式调用脚本，也不会破坏
其功能。

把所有可执行的 shell 脚本都限定为 *bash*，让我们拥有一致的、且在所有机器上
都已安装的 shell 语言。特别地，这意味着通常无需刻意追求
POSIX 兼容性，也无需刻意回避
“bashisms”。

上述规则的唯一例外，是当你所要编写代码的目标环境迫使你不得不如此时。
例如，某些遗留操作系统或受限的执行环境可能要求某些脚本使用
纯粹的 Bourne shell。

<a id="s1.2-when-to-use-shell"></a>

### 何时使用 Shell

Shell 只应用于小型工具或简单的包装器脚本。

虽然 shell 脚本并不是一门开发语言，但 Google 内部到处都在用它编写
各类实用脚本。本风格指南更多是对这一用途的
认可，而非建议把它广泛用于
部署。

一些指导原则：

*   如果你主要是在调用其他工具，而数据处理工作相对较少，
    那么 shell 对这项任务来说是可以接受的选择。
*   如果性能很重要，请改用 shell 之外的其他方式。
*   如果你正在编写的脚本超过 100 行，或者用到了
    并不直观的控制流逻辑，你*立即*就应该用更结构化的
    语言重写它。请记住，脚本会不断变长。尽早重写
    脚本，以免日后付出更耗时的重写代价。
*   在评估代码的复杂度时（例如决定是否要换一门
    语言），请考虑代码是否容易被作者以外的
    其他人维护。

如果你想把已有的程序从 shell 迁移到一门正式的语言，却
不知从何下手，可以看看
[Deshell Playbook](https://github.com/google/deshell/blob/main/playbook.md)。它
会引导你采用一套稳妥的方法，平稳地替换生产代码。

<a id="s2-shell-files-and-interpreter-invocation"></a>

## Shell 文件与解释器调用

<a id="s2.1-file-extensions"></a>

### 文件扩展名

可执行文件应使用 `.sh` 扩展名，或者不带扩展名。

-   如果可执行文件会有一条构建规则来重命名源文件，那么
    优先使用 `.sh` 扩展名。这样你就能采用推荐的
    命名约定，例如源文件叫 `foo.sh`，而构建规则名为
    `foo`。
-   如果可执行文件会被直接加入用户的 `PATH`，那么优先
    不使用扩展名。执行程序时没必要知道它是用什么语言
    编写的，而且 shell 并不要求扩展名，所以对于会被用户
    直接调用的可执行文件，我们倾向于不带扩展名。同时，
    也请考虑是否更适合部署构建规则的产物，而不是直接
    部署源文件。
-   如果以上两种情况都不适用，那么两种选择都可以接受。

库文件必须使用 `.sh` 扩展名，且不应可执行。

<a id="s2.2-suid-sgid"></a>

### SUID/SGID

shell 脚本上*禁止*使用 SUID 和 SGID。

shell 存在太多安全问题，几乎不可能把它加固到足以允许
SUID/SGID 的程度。虽然 bash 确实让运行 SUID 变得困难，
但在某些平台上仍然可行，这正是我们要明确
禁用它的原因。

如需提升权限，请使用 `sudo`。

<a id="s3-environment"></a>

## 环境

<a id="s3.1-stdout-vs-stderr"></a>

### STDOUT vs STDERR

所有错误消息都应输出到 `STDERR`。

这样更容易把正常状态信息与实际问题区分开来。

建议使用一个函数来打印错误消息以及其他
状态信息。

<div class='goodcode'></div>

```shell
err() {
  echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $*" >&2
}

if ! do_something; then
  err "Unable to do_something"
  exit 1
fi
```

<a id="s4-comments"></a>

## 注释

<a id="s4.1-file-header"></a>

### 文件头

每个文件都应以对其内容的说明开头。

每个文件都必须有一个顶层注释，简要概述其内容。版权声明
和作者信息是可选的。

示例：

<div class='goodcode'></div>

```shell
#!/bin/bash
#
# Perform hot backups of Oracle databases.
```

<a id="s4.2-function-comments"></a>

### 函数注释

任何并非既显而易见又简短的函数，都必须带有函数头
注释。库中的任何函数无论长度或复杂度如何，都必须带有
函数头注释。

其他人应当能够仅通过阅读注释（以及随附的帮助信息，
如果有的话）就学会如何使用你的程序，或如何使用你库中的
函数，而无需阅读代码。

所有函数头注释都应按以下各项描述预期的 API 行为：

*   函数的描述。
*   Globals：所使用和修改的全局变量列表。
*   Arguments：接收的参数。
*   Outputs：输出到 STDOUT 或 STDERR 的内容。
*   Returns：除最后运行的命令的默认退出状态之外的
    返回值。

示例：

<div class='goodcode'></div>

```shell
#######################################
# Cleanup files from the backup directory.
# Globals:
#   BACKUP_DIR
#   ORACLE_SID
# Arguments:
#   None
#######################################
function cleanup() {
  …
}

#######################################
# Get configuration directory.
# Globals:
#   SOMEDIR
# Arguments:
#   None
# Outputs:
#   Writes location to stdout
#######################################
function get_dir() {
  echo "${SOMEDIR}"
}

#######################################
# Delete a file in a sophisticated manner.
# Arguments:
#   File to delete, a path.
# Returns:
#   0 if thing was deleted, non-zero on error.
#######################################
function del_thing() {
  rm "$1"
}
```

<a id="s4.3-implementation-comments"></a>

### 实现注释

为代码中棘手、不易理解、有趣或重要的部分添加注释。

这遵循 Google 通用的编码注释实践。不要给每处都加注释。
如果存在复杂的算法，或者你做了某些不同寻常的处理，
就加上一段简短的注释。

<a id="s4.4-todo-comments"></a>

### TODO 注释

对于临时性的代码、短期解决方案，或者够用但并不完美的
代码，请使用 TODO 注释。

这与
[C++ Guide](https://google.github.io/styleguide/cppguide.html#TODO_Comments) 中的约定一致。

`TODO` 中应包含全大写的字符串 `TODO`，其后跟上姓名、
电子邮件地址或其他标识符，指向对 `TODO` 所引用的问题
最了解情况的人。其主要目的是让 `TODO` 保持统一、可被搜索，
以便在需要时获知如何取得更多细节。`TODO` 并不表示
被提到的人承诺会修复该问题。因此当你创建 `TODO` 时，
给出的几乎总是你自己的名字。

示例：

<div class='goodcode'></div>

```shell
# TODO(username): Handle the unlikely edge cases (bug ####)
```

<a id="s5-formatting"></a>

## 格式

对于你正在修改的文件，应遵循其中已有的风格；而对于任何
新代码，则必须遵守以下要求。

<a id="s5.1-indentation"></a>

### 缩进

缩进 2 个空格。不要使用制表符。

在代码块之间使用空行以提升可读性。缩进为两个
空格。无论如何都不要使用制表符。对于已有文件，请保持
与原有缩进一致。

**例外：** 唯一允许使用制表符的情形，是 `<<-` 所引导的、
以制表符缩进的
[here-document](https://www.gnu.org/software/bash/manual/html_node/Redirections.html#Here-Documents) 的主体。

<a id="s5.2-line-length-and-long-strings"></a>

### 行长度与长字符串

最大行长度为 80 个字符。

如果必须写出超过 80 个字符的字面字符串，应尽可能
通过
[here document](https://www.gnu.org/software/bash/manual/html_node/Redirections.html#Here-Documents)
或嵌入的换行符来实现。

超过 80 个字符且无法合理拆分的单词是可以接受的，但只要
可能，这类内容就应单独占一行，或提取到一个
变量中。例如文件路径和 URL，尤其是当对它们做字符串匹配
（如 `grep`）对维护很有价值时。

<div class='goodcode'></div>

```shell
# DO use 'here document's
cat <<END
I am an exceptionally long
string.
END

# Embedded newlines are ok too
long_string="I am an exceptionally
long string."

long_file="/i/am/an/exceptionally/loooooooooooooooooooooooooooooooooooooooooooooooooooong_file"

long_string_with_long_file="i am including an exceptionally \
/very/long/file\
 in this long string."

# Long file converted into a shorter variable name with cleaner line breaking.
long_string_alt="i am an including an exceptionally ${long_file} in this long\
 string"
```

<div class='badcode'></div>

```shell
# Just because a line contains an exception doesn't mean the rest of the
# line shouldn't be wrapped like usual.

bad_long_string_with_long_file="i am including an exceptionally /very/long/file in this long string."
```

<a id="s5.3-pipelines"></a>

### 管道

如果管道无法全部放在一行内，则应每行拆分一段。

如果管道能全部放在一行内，就应写在一行。

否则，应按每行一个管道段来拆分，管道符置于
换行处，下一段管道缩进 2 个空格。应统一使用 `\ ` 来
表示续行。这既适用于用 `|` 串联的命令链，
也适用于用 `||` 和 `&&` 组合的逻辑表达式。

<div class='goodcode'></div>

```shell
# All fits on one line
command1 | command2

# Long commands
command1 \
  | command2 \
  | command3 \
  | command4
```

这有助于在区分管道与普通的命令长行续行时提升可读性，
尤其当同一行中两者同时出现时。

注释需要放在整个管道之前。如果注释和管道
都很长且复杂，那么值得考虑借助辅助函数把其中的底层
细节挪到别处。

<a id="s5.4-control-flow"></a>

<!-- section was previously titled "Loops" -->

<a id="s5.4-loops"></a>
<a id="loops"></a>

### 控制流

把 `; then` 和 `; do` 与 `if`、`for` 或 `while` 放在同一行。

shell 中的控制流语句稍有不同，但我们遵循与声明函数时使用花括号
相同的原则。也就是说：`; then` 和 `; do`
应与 `if`/`for`/`while`/`until`/`select` 放在同一行。`else`
应单独占一行，而结束语句（`fi` 和 `done`）应各自
单独占一行，并与起始语句垂直对齐。

示例：

<div class='goodcode'></div>

```shell
# If inside a function remember to declare the loop variable as
# a local to avoid it leaking into the global environment:
local dir
for dir in "${dirs_to_cleanup[@]}"; do
  if [[ -d "${dir}/${SESSION_ID}" ]]; then
    log_date "Cleaning up old files in ${dir}/${SESSION_ID}"
    rm "${dir}/${SESSION_ID}/"* || error_message
  else
    mkdir -p "${dir}/${SESSION_ID}" || error_message
  fi
done
```

虽然在 for 循环中可以
[省略 `in "$@"`](https://www.gnu.org/software/bash/manual/html_node/Looping-Constructs.html#index-for)，
但为清晰起见，我们建议始终把它写上。

<div class='goodcode'></div>

```shell
for arg in "$@"; do
  echo "argument: ${arg}"
done
```

<a id="s5.5-case-statement"></a>

### case 语句

*   各分支缩进 2 个空格。
*   单行分支需要在模式的右括号之后、`;;` 之前
    留一个空格。
*   较长或包含多条命令的分支应拆成多行，
    让模式、动作和 `;;` 各占一行。

匹配表达式相对 `case` 和 `esac` 缩进一级。
多行动作再缩进一级。通常无需给匹配表达式
加引号。模式表达式前不应加左括号。
避免使用 `;&` 和 `;;&` 标记。

<div class='goodcode'></div>

```shell
case "${expression}" in
  a)
    variable="…"
    some_command "${variable}" "${other_expr}" …
    ;;
  absolute)
    actions="relative"
    another_command "${actions}" "${other_expr}" …
    ;;
  *)
    error "Unexpected expression '${expression}'"
    ;;
esac
```

只要表达式仍然可读，简单命令可以与模式 <i>以及</i> `;;`
放在同一行。这通常适用于单字母选项的处理。
当动作无法放在一行内时，让模式单独占一行，然后是动作，
再让 `;;` 也单独占一行。当与动作放在同一行时，
在模式的右括号之后留一个空格，并在 `;;` 之前
再留一个空格。

<div class='goodcode'></div>

```shell
verbose='false'
aflag=''
bflag=''
files=''
while getopts 'abf:v' flag; do
  case "${flag}" in
    a) aflag='true' ;;
    b) bflag='true' ;;
    f) files="${OPTARG}" ;;
    v) verbose='true' ;;
    *) error "Unexpected option ${flag}" ;;
  esac
done
```

<a id="s5.6-variable-expansion"></a>

### 变量展开

按优先级排序：与既有代码保持一致；给变量加引号；
优先使用 `"${var}"` 而非 `"$var"`。

这些是强烈推荐但并非强制规定的准则。
尽管如此，它只是建议而非强制，并不意味着
可以轻视或淡化它。

它们按优先级顺序列出。

*   与既有代码中的写法保持一致。
*   给变量加引号，参见[下文的引用一节](#quoting)。
*   不要用花括号界定单字符的 shell 特殊变量 / 位置参数，
    除非确有必要或为了避免严重的混淆。

其他所有变量都优先使用花括号界定。

<div class='goodcode'></div>

```shell
# Section of *recommended* cases.

# Preferred style for 'special' variables:
echo "Positional: $1" "$5" "$3"
echo "Specials: !=$!, -=$-, _=$_. ?=$?, #=$# *=$* @=$@ \$=$$ …"

# Braces necessary:
echo "many parameters: ${10}"

# Braces avoiding confusion:
# Output is "a0b0c0"
set -- a b c
echo "${1}0${2}0${3}0"

# Preferred style for other variables:
echo "PATH=${PATH}, PWD=${PWD}, mine=${some_var}"
while read -r f; do
  echo "file=${f}"
done < <(find /tmp)
```

<div class='badcode'></div>

```shell
# Section of *discouraged* cases

# Unquoted vars, unbraced vars, brace-delimited single letter
# shell specials.
echo a=$avar "b=$bvar" "PID=${$}" "${1}"

# Confusing use: this is expanded as "${1}0${2}0${3}0",
# not "${10}${20}${30}
set -- a b c
echo "$10$20$30"
```

注意：在 `${var}` 中使用花括号*并不*是一种引用形式。“双引号”
也必须*同时*使用。

<a id="s5.7-quoting"></a>

### 引用

*   对于包含变量、命令替换、空格或 shell 元字符的字符串，
    始终加引号，除非确实需要谨慎地不加引号展开，或者它是
    shell 内部的整数（见下一点）。
*   对于由多个元素组成的列表，使用数组来安全地加引号，
    尤其是命令行标志。参见下文[数组](#arrays)。
*   可以选择给定义为整数的 shell 内部只读
    [特殊变量](https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html)
    加引号：`$?`、`$#`、`$$`、`$!`。为保持一致，倾向于
    给“具名的”内部整数变量（例如 PPID 等）加引号。
*   倾向于给作为“单词”的字符串加引号（相对于命令选项或
    路径名而言）。
*   留意 `[[ … ]]` 中模式匹配的引号规则。参见下文
    [Test、`[ … ]` 与 `[[ … ]]`](#tests) 一节。
*   使用 `"$@"`，除非有特定理由要用 `$*`，例如只是把参数
    追加到消息或日志中的某个字符串里。

<div class='goodcode'></div>

```shell
# 'Single' quotes indicate that no substitution is desired.
# "Double" quotes indicate that substitution is required/tolerated.

# Simple examples

# "quote command substitutions"
# Note that quotes nested inside "$()" don't need escaping.
flag="$(some_command and its args "$@" 'quoted separately')"

# "quote variables"
echo "${flag}"

# Use arrays with quoted expansion for lists.
declare -a FLAGS
FLAGS=( --foo --bar='baz' )
readonly FLAGS
mybinary "${FLAGS[@]}"

# It's ok to not quote internal integer variables.
if (( $# > 3 )); then
  echo "ppid=${PPID}"
fi

# "never quote literal integers"
value=32
# "quote command substitutions", even when you expect integers
number="$(generate_number)"

# "prefer quoting words", not compulsory
readonly USE_INTEGER='true'

# "quote shell meta characters"
echo 'Hello stranger, and well met. Earn lots of $$$'
echo "Process $$: Done making \$\$\$."

# "command options or path names"
# ($1 is assumed to contain a value here)
grep -li Hugo /dev/null "$1"

# Less simple examples
# "quote variables, unless proven false": ccs might be empty
git send-email --to "${reviewers}" ${ccs:+"--cc" "${ccs}"}

# Positional parameter precautions: $1 might be unset
# Single quotes leave regex as-is.
grep -cP '([Ss]pecial|\|?characters*)$' ${1:+"$1"}

# For passing on arguments,
# "$@" is right almost every time, and
# $* is wrong almost every time:
#
# * $* and $@ will split on spaces, clobbering up arguments
#   that contain spaces and dropping empty strings;
# * "$@" will retain arguments as-is, so no args
#   provided will result in no args being passed on;
#   This is in most cases what you want to use for passing
#   on arguments.
# * "$*" expands to one argument, with all args joined
#   by (usually) spaces,
#   so no args provided will result in one empty string
#   being passed on.
#
# Consult
# https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html and
# https://mywiki.wooledge.org/BashGuide/Arrays for more

(set -- 1 "2 two" "3 three tres"; echo $#; set -- "$*"; echo "$#, $@")
(set -- 1 "2 two" "3 three tres"; echo $#; set -- "$@"; echo "$#, $@")
```

<a id="s6-features-and-bugs"></a>

## 特性与陷阱

<a id="s6.1-shellcheck"></a>

### ShellCheck

[ShellCheck 项目](https://www.shellcheck.net/) 能识别 shell 脚本中常见的
缺陷与警告。建议对所有脚本都使用它，
无论大小。

<a id="s6.2-command-substitution"></a>

### 命令替换

使用 `$(command)`，而不要使用反引号。

嵌套的反引号需要用 `\ ` 对内层反引号转义。`$(command)` 这种
格式在嵌套时不会变化，而且更易读。

示例：

<div class='goodcode'></div>

```shell
# This is preferred:
var="$(command "$(command1)")"
```

<div class='badcode'></div>

```shell
# This is not:
var="`command \`command1\``"
```

<a id="s6.3-tests"></a>

<a id="tests"></a>

### Test、`[ … ]` 与 `[[ … ]]`

优先使用 `[[ … ]]`，而不是 `[ … ]`、`test` 和 `/usr/bin/[`。

`[[ … ]]` 能减少错误，因为在 `[[` 和 `]]` 之间不会发生路径名展开
或单词拆分。此外，`[[ … ]]` 支持模式和正则
表达式匹配，而 `[ … ]` 不支持。

<div class='goodcode'></div>

```shell
# This ensures the string on the left is made up of characters in
# the alnum character class followed by the string name.
# Note that the RHS should not be quoted here.
if [[ "filename" =~ ^[[:alnum:]]+name ]]; then
  echo "Match"
fi

# This matches the exact pattern "f*" (Does not match in this case)
if [[ "filename" == "f*" ]]; then
  echo "Match"
fi
```

<div class='badcode'></div>

```shell
# This gives a "too many arguments" error as f* is expanded to the
# contents of the current directory. It might also trigger the
# "unexpected operator" error because `[` does not support `==`, only `=`.
if [ "filename" == f* ]; then
  echo "Match"
fi
```

欲了解详尽的细节，请参阅
[Bash FAQ](https://tiswww.case.edu/php/chet/bash/FAQ) 中的 E14。

<a id="s6.4-testing-strings"></a>

### 测试字符串

尽可能使用引号，而不要使用填充字符。

Bash 足够聪明，能够处理测试中的空字符串。因此，考虑到这样
代码更易读，请针对空/非空字符串或空字符串进行测试，
而不要使用填充字符。

<div class='goodcode'></div>

```shell
# Do this:
if [[ "${my_var}" == "some_string" ]]; then
  do_something
fi

# -z (string length is zero) and -n (string length is not zero) are
# preferred over testing for an empty string
if [[ -z "${my_var}" ]]; then
  do_something
fi

# This is OK (ensure quotes on the empty side), but not preferred:
if [[ "${my_var}" == "" ]]; then
  do_something
fi
```

<div class='badcode'></div>

```shell
# Not this:
if [[ "${my_var}X" == "some_stringX" ]]; then
  do_something
fi
```

为免对所测试的内容产生混淆，请显式使用 `-z` 或 `-n`。

<div class='goodcode'></div>

```shell
# Use this
if [[ -n "${my_var}" ]]; then
  do_something
fi
```

<div class='badcode'></div>

```shell
# Instead of this
if [[ "${my_var}" ]]; then
  do_something
fi
```

为清晰起见，判断相等时请使用 `==` 而非 `=`，尽管两者都有效。
前者会促使你使用 `[[`，而后者容易与
赋值混淆。不过，`<` 和 `>` 在 `[[ … ]]` 中执行的是
字典序比较，使用时要小心。做数值比较请使用 `(( … ))`
或 `-lt` 和 `-gt`。

<div class='goodcode'></div>

```shell
# Use this
if [[ "${my_var}" == "val" ]]; then
  do_something
fi

if (( my_var > 3 )); then
  do_something
fi

if [[ "${my_var}" -gt 3 ]]; then
  do_something
fi
```

<div class='badcode'></div>

```shell
# Instead of this
if [[ "${my_var}" = "val" ]]; then
  do_something
fi

# Probably unintended lexicographical comparison.
if [[ "${my_var}" > 3 ]]; then
  # True for 4, false for 22.
  do_something
fi
```

<a id="s6.5-wildcard-expansion-of-filenames"></a>

### 文件名的通配符展开

对文件名做通配符展开时，请使用显式的路径。

由于文件名可能以 `-` 开头，用 `./*` 而不是 `*` 来展开通配符
要安全得多。

<div class='badcode'></div>

```shell
# Here's the contents of the directory:
# -f  -r  somedir  somefile

# Incorrectly deletes almost everything in the directory by force
psa@bilby$ rm -v *
removed directory: `somedir'
removed `somefile'
```

<div class='goodcode'></div>

```shell
# As opposed to:
psa@bilby$ rm -v ./*
removed `./-f'
removed `./-r'
rm: cannot remove `./somedir': Is a directory
removed `./somefile'
```

<a id="s6.6-eval"></a>

### Eval

应避免使用 `eval`。

Eval 在用于变量赋值时会篡改输入，并且它能在无法检查
所设置变量内容的情况下设置变量。

<div class='badcode'></div>

```shell
# What does this set?
# Did it succeed? In part or whole?
eval $(set_my_variables)

# What happens if one of the returned values has a space in it?
variable="$(eval some_function)"
```

<a id="s6.7-arrays"></a>

### 数组

应使用 Bash 数组来存储元素列表，以避免引号带来的
复杂问题。这一点尤其适用于参数列表。不要用数组
来实现更复杂的数据结构（参见上文
[何时使用 Shell](#when-to-use-shell)）。

数组存储的是有序的字符串集合，可以安全地展开为
供命令或循环使用的单个元素。

应避免用单个字符串承载多个命令参数，因为这会不可避免地
导致作者使用 `eval`，或试图在字符串内嵌套引号，
这样既得不到可靠、可读的结果，又会带来不必要的
复杂度。

<div class='goodcode'></div>

```shell
# An array is assigned using parentheses, and can be appended to
# with +=( … ).
declare -a flags
flags=(--foo --bar='baz')
flags+=(--greeting="Hello ${name}")
mybinary "${flags[@]}"
```

<div class='badcode'></div>

```shell
# Don’t use strings for sequences.
flags='--foo --bar=baz'
flags+=' --greeting="Hello world"'  # This won’t work as intended.
mybinary ${flags}
```

<div class='badcode'></div>

```shell
# Command expansions return single strings, not arrays. Avoid
# unquoted expansion in array assignments because it won’t
# work correctly if the command output contains special
# characters or whitespace.

# This expands the listing output into a string, then does special keyword
# expansion, and then whitespace splitting.  Only then is it turned into a
# list of words.  The ls command may also change behavior based on the user's
# active environment!
declare -a files=($(ls /directory))

# The get_arguments writes everything to STDOUT, but then goes through the
# same expansion process above before turning into a list of arguments.
mybinary $(get_arguments)
```

<a id="s6.7.1-arrays-pros"></a>

#### 数组的优点

*   使用数组可以在不引入令人困惑的引号语义的情况下表示列表。
    相反，不使用数组会导致人们误入歧途，试图在字符串内部
    嵌套引号。
*   数组能够安全地存储由任意字符串组成的序列/列表，
    包括含有空白字符的字符串。

<a id="s6.7.2-arrays-cons"></a>

#### 数组的缺点

使用数组可能带来脚本复杂度增长的风险。

<a id="s6.7.3-arrays-decision"></a>

#### 数组的决策

应使用数组来安全地创建并传递列表。特别是在
构建一组命令参数时，使用数组可避免令人困惑的引号
问题。请使用带引号的展开 – `"${array[@]}"` – 来访问数组。不过，
若需要更高级的数据操作，就应完全避免使用 shell 脚本；
参见[上文](#when-to-use-shell)。

<a id="s6.8-pipes-to-while"></a>

### 通过管道传给 while

优先使用进程替换或 `readarray` 内建命令（bash4+），而不是
通过管道传给 `while`。管道会创建子 shell，因此在管道中
修改的任何变量都不会传回父 shell。

通过管道传给 `while` 时隐含的子 shell 可能引入难以
排查的微妙缺陷。

<div class='badcode'></div>

```shell
last_line='NULL'
your_command | while read -r line; do
  if [[ -n "${line}" ]]; then
    last_line="${line}"
  fi
done

# This will always output 'NULL'!
echo "${last_line}"
```

使用进程替换同样会创建子 shell。不过，它允许
从子 shell 重定向到 `while`，而不必把 `while`（或任何其他
命令）放入子 shell 中。

<div class='goodcode'></div>

```shell
last_line='NULL'
while read line; do
  if [[ -n "${line}" ]]; then
    last_line="${line}"
  fi
done < <(your_command)

# This will output the last non-empty line from your_command
echo "${last_line}"
```

另一种做法是使用 `readarray` 内建命令把文件内容读入数组，
再遍历数组的内容。请注意（出于与上文相同的原因），
对 `readarray` 需要使用进程替换而非管道，但其优点是
循环所需的输入生成位于循环之前，
而不是之后。

<div class='goodcode'></div>

```shell
last_line='NULL'
readarray -t lines < <(your_command)
for line in "${lines[@]}"; do
  if [[ -n "${line}" ]]; then
    last_line="${line}"
  fi
done
echo "${last_line}"
```

> 注意：使用 for 循环遍历输出时要小心，例如
> `for var in $(...)`，因为输出是按空白字符而非按行拆分的。
> 有时你能确定这样做是安全的，因为输出不可能含有任何
> 意外的空白字符；但如果这一点并不明显，或者这样做并不能提升
> 可读性（例如 `$(...)` 中是一条很长的命令），那么 `while read` 循环或
> `readarray` 往往更安全、更清晰。

<a id="s6.9-arithmetic"></a>

### 算术运算

始终使用 `(( … ))` 或 `$(( … ))`，而不要使用 `let`、`$[ … ]` 或 `expr`。

绝不要使用 `$[ … ]` 语法、`expr` 命令或 `let` 内建命令。

`<` 和 `>` 在 `[[ … ]]` 表达式中并不执行数值比较
（它们执行的是字典序比较；参见
[测试字符串](#testing-strings)）。最好*完全*不要用 `[[ … ]]`
来做数值比较，而改用 `(( … ))`。

建议避免把 `(( … ))` 用作独立语句，并留意其表达式求值
为零的情况

-   尤其是在启用 `set -e` 时。例如，`set -e; i=0; (( i++ ))`
    会导致 shell 退出。

<div class='goodcode'></div>

```shell
# Simple calculation used as text - note the use of $(( … )) within
# a string.
echo "$(( 2 + 2 )) is 4"

# When performing arithmetic comparisons for testing
if (( a < b )); then
  …
fi

# Some calculation assigned to a variable.
(( i = 10 * j + 400 ))
```

<div class='badcode'></div>

```shell
# This form is non-portable and deprecated
i=$[2 * 10]

# Despite appearances, 'let' isn't one of the declarative keywords,
# so unquoted assignments are subject to globbing wordsplitting.
# For the sake of simplicity, avoid 'let' and use (( … ))
let i="2 + 2"

# The expr utility is an external program and not a shell builtin.
i=$( expr 4 + 4 )

# Quoting can be error prone when using expr too.
i=$( expr 4 '*' 4 )
```

抛开风格上的考量不谈，shell 内建的算术运算比 `expr`
快很多倍。

`${var}`（以及 `$var`）这样的形式在 `$(( … ))` 内部并不需要。
shell 会自行查找 `var`，省略 `${…}`
能让代码更简洁。这与前面要求始终使用花括号的规则
略有出入，因此这只是一条建议。

<div class='goodcode'></div>

```shell
# N.B.: Remember to declare your variables as integers when
# possible, and to prefer local variables over globals.
local -i hundred="$(( 10 * 10 ))"
declare -i five="$(( 10 / 2 ))"

# Increment the variable "i" by three.
# Note that:
#  - We do not write ${i} or $i.
#  - We put a space after the (( and before the )).
(( i += 3 ))

# To decrement the variable "i" by five:
(( i -= 5 ))

# Do some complicated computations.
# Note that normal arithmetic operator precedence is observed.
hr=2
min=5
sec=30
echo "$(( hr * 3600 + min * 60 + sec ))" # prints 7530 as expected
```

<a id="s6.10-aliases"></a>

## 别名

虽然别名在 `.bashrc` 文件中很常见，但脚本中应避免使用别名。
正如
[Bash manual](https://www.gnu.org/software/bash/manual/html_node/Aliases.html)
所指出的：

> 几乎在所有场景下，shell 函数都比别名更可取。

别名使用起来很麻烦，因为需要对其内容小心地加引号和
转义，而且错误可能很难察觉。

<div class='badcode'></div>

```shell
# this evaluates $RANDOM once when the alias is defined,
# so the echo'ed string will be the same on each invocation
alias random_name="echo some_prefix_${RANDOM}"
```

函数提供了别名功能的超集，应始终
优先使用。 .

<div class='goodcode'></div>

```shell
random_name() {
  echo "some_prefix_${RANDOM}"
}

# Note that unlike aliases function's arguments are accessed via $@
fancy_ls() {
  ls -lh "$@"
}
```

<a id="s7-naming-conventions"></a>

## 命名约定

<a id="s7.1-function-names"></a>

### 函数名

使用小写字母，用下划线分隔单词。独立的函数无需
置于命名空间中，但库可以通过给所有函数加上库名或包名前缀
来创建命名空间，并以 `::` 作为包分隔符。

请注意，某些场景（例如交互式 shell 中的自动补全）
并不适合以冒号分隔的名称，因此在这些场景下要避免
使用命名空间。

函数名之后必须有括号。关键字 `function` 是
可选的，但在整个项目中必须保持使用一致。

花括号必须与函数名在同一行（与 Google 的其他语言一致），
且函数名与括号之间不留空格。

<div class='goodcode'></div>

```shell
# Single function
my_func() {
  …
}

# Part of a package
mypackage::my_func() {
  …
}
```

当函数名后已有 “()” 时，关键字 `function` 是多余的，
但它有助于快速识别函数。

<a id="s7.2-variable-names"></a>

### 变量名

与函数名相同。

循环所用的变量名应与你所遍历的
变量采用类似的命名。

<div class='goodcode'></div>

```shell
for zone in "${zones[@]}"; do
  something_with "${zone}"
done
```

<a id="s7.3-constants-and-environment-variable-names"></a>
<a id="s7.5-read-only-variables"></a>

### 常量、环境变量与 readonly 变量

常量以及任何导出到环境中的变量都应使用大写，
用下划线分隔，并在文件顶部声明。

<div class='goodcode'></div>

```shell
# Constant
readonly PATH_TO_FILES='/some/path'

# Both constant and exported to the environment
declare -xr ORACLE_SID='PROD'
```

为清晰起见，建议使用 `readonly` 或 `export`，而不是等价的
`declare` 命令。你可以先后各写一条，例如：

<div class='goodcode'></div>

```shell
# Constant
readonly PATH_TO_FILES='/some/path'
export PATH_TO_FILES
```

可以在运行时或条件语句中设置常量，但应随即
将其设为 readonly。

<div class='goodcode'></div>

```shell
ZIP_VERSION="$(dpkg --status zip | sed -n 's/^Version: //p')"
if [[ -z "${ZIP_VERSION}" ]]; then
  ZIP_VERSION="$(pacman -Q --info zip | sed -n 's/^Version *: //p')"
fi
if [[ -z "${ZIP_VERSION}" ]]; then
  handle_error_and_quit
fi
readonly ZIP_VERSION
```

<a id="s7.4-source-filenames"></a>

### 源文件名

使用小写字母，如有需要可用下划线分隔单词。

这是为了与 Google 的其他代码风格保持一致：`maketemplate` 或
`make_template`，但不要用 `make-template`。

<a id="s7.5-use-local-variables"></a>
<a id="s7.6-use-local-variables"></a>

### 使用局部变量

用 `local` 声明函数专用的变量。

声明变量时使用 `local`，以确保局部变量只在函数及其
子函数中可见。这样可以避免污染全局命名空间，
也能避免无意中设置那些在函数之外
可能具有意义的变量。

当赋值来自命令替换时，声明与赋值必须是分开的
语句；因为 `local` 内建命令不会传递命令替换的
退出码。

<div class='goodcode'></div>

```shell
my_func2() {
  local name="$1"

  # Separate lines for declaration and assignment:
  local my_var
  my_var="$(my_func)"
  (( $? == 0 )) || return

  …
}
```

<div class='badcode'></div>

```shell
my_func2() {
  # DO NOT do this:
  # $? will always be zero, as it contains the exit code of 'local', not my_func
  local my_var="$(my_func)"
  (( $? == 0 )) || return

  …
}
```

<a id="s7.6-function-location"></a>
<a id="s7.7-function-location"></a>

### 函数的位置

把所有函数集中放在文件中紧接常量之后的位置。不要把
可执行代码藏在函数之间。这样做会让代码难以理解，
并在调试时带来令人头疼的意外。

如果文件中有函数，就把它们全部集中放在靠近文件顶部的位置。
在声明函数之前，只允许写 include、`set` 语句
以及常量的设置。

<a id="s7.7-main"></a>
<a id="s7.8-main"></a>

### main

对于长到至少还包含另一个函数的脚本，必须有一个名为
`main` 的函数。

为了便于找到程序的起点，请把主程序放进一个名为
`main` 的函数，并把它作为最靠下的函数。这既能与
代码库的其余部分保持一致，也让你能把更多变量定义为
`local`（如果主代码不是函数，就做不到这一点）。文件中
最后一行非注释内容应是对 `main` 的调用：

<div class='goodcode'></div>

```shell
main "$@"
```

显然，对于只是线性流程的短脚本，`main` 就多余了，
因此并不要求使用。

<a id="s8-calling-commands"></a>

## 调用命令

<a id="s8.1-checking-return-values"></a>

### 检查返回值

始终检查返回值，并给出信息明确的返回值。

对于未经管道的命令，为保持简洁，可使用 `$?`，或直接通过
`if` 语句检查。

示例：

<div class='goodcode'></div>

```shell
if ! mv "${file_list[@]}" "${dest_dir}/"; then
  echo "Unable to move ${file_list[*]} to ${dest_dir}" >&2
  exit 1
fi

# Or
mv "${file_list[@]}" "${dest_dir}/"
if (( $? != 0 )); then
  echo "Unable to move ${file_list[*]} to ${dest_dir}" >&2
  exit 1
fi
```

Bash 还提供了 `PIPESTATUS` 变量，可用于检查管道中
各部分的返回码。如果只需检查整个管道的成败，
那么以下写法是可以接受的：

<div class='goodcode'></div>

```shell
tar -cf - ./* | ( cd "${dir}" && tar -xf - )
if (( PIPESTATUS[0] != 0 || PIPESTATUS[1] != 0 )); then
  echo "Unable to tar files to ${dir}" >&2
fi
```

不过，由于一旦执行任何其他命令，`PIPESTATUS` 就会被
覆盖，因此如果你需要根据错误发生在管道中的哪个位置
采取不同的处理，就必须在运行该命令后立即把
`PIPESTATUS` 赋给另一个变量（别忘了 `[` 也是命令，
会清掉 `PIPESTATUS`）。

<div class='goodcode'></div>

```shell
tar -cf - ./* | ( cd "${DIR}" && tar -xf - )
return_codes=( "${PIPESTATUS[@]}" )
if (( return_codes[0] != 0 )); then
  do_something
fi
if (( return_codes[1] != 0 )); then
  do_something_else
fi
```

<a id="s8.2-builtin-commands-vs-external-commands"></a>

### 内置命令与外部命令

如果在调用 shell 内建命令与启动一个独立进程之间
可以选择，请选择内建命令。

我们倾向于使用内建功能，例如 `bash` 提供的
[*Parameter Expansion*](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html)，
因为它更高效、更健壮，也更可移植
（尤其是与 `sed` 之类的做法相比）。另请参见
[`=~` 操作符](https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html#index-_005b_005b)。

示例：

<div class='goodcode'></div>

```shell
# Prefer this:
addition="$(( X + Y ))"
substitution="${string/#foo/bar}"
if [[ "${string}" =~ foo:(\d+) ]]; then
  extraction="${BASH_REMATCH[1]}"
fi
```

<div class='badcode'></div>

```shell
# Instead of this:
addition="$(expr "${X}" + "${Y}")"
substitution="$(echo "${string}" | sed -e 's/^foo/bar/')"
extraction="$(echo "${string}" | sed -e 's/foo:\([0-9]\)/\1/')"
```

<a id="s9-conclusion"></a>

## 如有疑问：保持一致

在整个代码库中始终如一地使用同一种风格，让我们可以专注于其他
（更重要的）问题。一致性还便于实现自动化。很多情况下，那些
归因于“保持一致”的规则归根结底就是“随便选一个，别再
纠结了”；在这些地方允许灵活性所带来的潜在
价值，比不上人们为此争论所付出的代价。

不过，一致性也有其限度。当没有明确的技术论据、
也没有长期方向时，它是一个不错的决胜依据。一般不应
把一致性当作借口，用来在不考虑新风格好处、也不考虑
代码库随时间向更新风格收敛的趋势下，继续沿用
旧风格。
