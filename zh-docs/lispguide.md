# Google Common Lisp 风格指南

## 简介

本指南不是 Common Lisp 教程，而是针对 Common Lisp 代码的格式、
结构与风格取舍给出的建议。现有代码的维护者需要在这些
建议与保持现有代码内部一致性的收益之间做出
权衡。

我们欢迎就如何改进本指南提出建设性反馈。如果你在
本文档中发现错误，可以在
[GitHub issue 跟踪器](https://github.com/google/styleguide/issues)
中提交 bug。由于本仓库包含多种语言的风格指南，
请在 issue 标题中加上 “[Lisp]”。

<!-- mdformat off -->
* TOC
{:toc}
<!-- mdformat on -->

### 参考文献

-   关于 Google 内部高效的 Lisp 编程指南，请参阅
    [Google Lisp 高效编程指南](lispprogrammingguide.md)。

-   关于该语言的基础信息，请查阅
    [Practical Common Lisp](https://www.gigamonkeys.com/book/)。

-   关于语言参考，请查阅
    [Common Lisp HyperSpec](https://www.lispworks.com/documentation/HyperSpec/Front/index.htm)。

-   关于更详细的风格指导，不妨（有所保留地）参考
    [Peter Norvig 与 Kent Pitman 的风格指南](https://www.cs.umd.edu/~nau/cmsc421/norvig-lisp-style.pdf)。

## 现有代码

-   顺手修正旧代码。
-   不要在没有事先告知的情况下大规模修正风格。

很多 Lisp 代码是在这些指导原则出现之前编写的。你应当在
日常编码过程中遇到违规之处时顺手修正。仅当这类修正
易于实现、且不会显著增大改动规模时才这样做。在
这种情况下，可以考虑把风格修正拆分为单独的
改动。

不得在未告知其他开发者并与他们协调的情况下大规模
修正违规之处，以免让大型分支的合并变得比现在
更加困难。

## 格式

### 标点、拼写与语法

-   在注释和代码中使用正确的拼写。
-   在注释和文档中使用规范的语法。

留意标点、拼写与语法；写得好的注释
比写得差的注释更易读。

注释应当像叙述性文字一样易读，使用正确的大小写和
标点。很多情况下，完整句子比句子片段更易读。
较短的注释，例如位于代码行末尾的注释，有时可以
不那么正式，但你应当保持风格一致。

### 行长度

-   格式化源代码，使任何一行都不超过 100 个字符。

对行长度加以限制总比完全不限制要好。过去的老式
文本终端把 80 列定为标准，而如今允许 100 列
似乎更合适，因为良好的风格鼓励使用描述性的
变量名和函数名。

### 形式长度

-   优先使用短小且职责单一的顶层形式。

较长的顶层形式（例如函数和宏）有时是合适的，
因此对其长度不设硬性限制。如果某个函数或宏
超过约 40 行，请考虑能否在不破坏程序结构的
前提下将其拆分。

即便你的长形式目前工作得完美无缺，几个月后
修改它的人也可能加入新的行为。这可能导致
难以发现的 bug。让你的形式保持短小简单，
能使其他人更容易阅读和修改你的代码。

不要对修改现有代码心存畏惧。如果处理一个过长的
函数确实很困难——错误难以调试，或者其中一部分
要在多个不同场景中使用——请考虑把该函数拆分为
更小、更易于管理的片段。

### 缩进

-   使用空格而非制表符来缩进代码。
-   绑定形式的绑定数据应当：
    -   位于新行时缩进四个空格，或
    -   否则与第一个绑定数据形式对齐。
-   绑定形式的主体应当：
    -   位于新行时缩进两个空格，或
    -   否则与主体中的第一个形式对齐。
-   函数调用的参数应当
    -   位于新行时与调用本身对齐，或
    -   否则与第一个参数对齐。
-   函数和宏声明中的特殊参数（`&key`、`&optional`、
    ...）应当：
    -   位于新行时与特殊参数声明对齐，或
    -   否则与第一个特殊参数对齐。
-   尽量让函数的所有参数：
    -   在可能时放在同一行，或
    -   否则每行一个参数。
-   loop 形式的参数（loop 关键字）及其各自的参数应当
    是：
    -   第一个参数位于新行时缩进两个空格，或
    -   否则与第一个参数对齐。

Emacs 中的 Common Lisp 缩进由 cl-indent 库提供。
最新版本的 cl-indent 随
[SLIME](https://www.common-lisp.net/project/slime/)（位于
contrib/slime-cl-indent.el）。安装 SLIME 后，请配置 Emacs 自动
加载 SLIME，方法是使用
[这些说明](https://www.common-lisp.net/project/slime/doc/html/Loading-Contribs.html)，
并在调用 slime-setup 时把 slime-indentation 加入要加载的
contrib 库列表。

理想情况下，使用 SLIME 提供的默认缩进设置。如有必要，
可自定义缩进参数，以便在整个现有项目中保持一致的缩进
风格。参数可通过
define-common-lisp-style 中的 :variables 设置来自定义。
特定形式的缩进可通过
define-common-lisp-style 的 :indentation 设置来自定义。
这在创建行为类似宏或特殊运算符、且缩进方式不同于
标准函数调用（例如 defun、labels 或 let）的形式时尤其
有用。向 'lisp-mode-hook 添加一个 [钩子](https://www.gnu.org/software/emacs/manual/html_node/emacs/Hooks.html)，
使其调用 common-lisp-set-style，从而自动
设置合适的风格。

使用缩进让复杂的函数应用更易读。当某个
应用无法放在一行，或函数带有许多参数时，
可考虑在参数之间插入换行，使每个参数各占
一行。但不要以让人难以判断函数接受多少参数、
或某个参数形式从何处开始与结束的方式
插入换行。

<div class='badcode'></div>

```lisp
;; Ow, my eyes!
(do-something first-argument second-argument (lambda (x)
  (frob x)) fourth-argument last-argument)
```

<div class='goodcode'></div>

```lisp
;; This looks nicer.
(do-something first-argument
              second-argument
              (lambda (x) (frob x))
              fourth-argument
              last-argument)
```

按照惯例，绑定形式的主体在该形式之后缩进两个空格。
主体之前的任何绑定数据通常缩进四个空格。函数调用的
参数与第一个参数对齐；若第一个参数单独占一行，
则与函数名对齐。

<div class='goodcode'></div>

```lisp
(multiple-value-bind (a b c d)
    (function-returning-four-values x y)
  (declare (ignore c))
  (something-using a)
  (also-using b d))
```

必须把编辑器设置为不在所编辑的文件中插入制表符。
当不同编辑器对制表符代表多少空格意见不一时，会造成混乱。
在 Emacs 中，执行 `(setq-default indent-tabs-mode nil)`。

### 文件头

-   每个源文件都应以简短描述其
    内容作为开头。
-   在该描述之后加上 `in-package` 声明。
-   避免在文件级别使用 `(declaim (optimize ...))` 声明。
    确有需要时，把它放在 `in-package` 声明之后。

每个源文件都应以一段简短描述开头，
说明该文件的内容。

在该描述之后，每个文件都应以一个
`(in-package #:package-name)` 形式开始正式的代码。

在 `in-package` 形式之后，每个文件都应接上任何未被
`ASDF` 的 `:around-compile` 钩子覆盖的文件级
`(declaim (optimize ...))` 声明。请注意，应尽可能避免
使用文件级 `(declaim (optimize ...))` 声明，
而改用作用域更小的声明。

<div class='goodcode'></div>

```lisp
;;;; Variable length encoding for integers and floating point numbers.

(in-package #:varint)
(declaim #.*optimize-default*)
```

不应在文件顶部包含作者信息：版本控制能
提供更可靠的信息，而这样的标注只会带来
困惑与麻烦。事实上，加入该标注时的主要
作者，未必就是最终对该文件贡献最多的人，
更不一定是当下负责
该文件的那个人。

不应在单个源代码文件中包含版权信息。
拟作为独立文件分发的文件可以例外。

### 纵向空白

-   在所有顶层形式之间留一个空行
    -   对于简单（单行）且紧密相关的形式可以省略。

应在顶层形式（例如函数定义）之间留一个空行。
作为例外，同类且简单、紧密相关的定义形式之间
可以省略空行，例如一组相关的类型声明或
常量定义。

<div class='goodcode'></div>

```lisp
(defconstant +mix32+ #x12b9b0a1 "pi, an arbitrary number")
(defconstant +mix64+ #x2b992ddfa23249d6 "more digits of pi")

(defconstant +golden-ratio32+ #x9e3779b9 "the golden ratio")
(defconstant +golden-ratio64+ #xe08c1d668b756f82 "more digits of the golden ratio")

(defmacro incf32 (x y)
  "Like INCF, but for integers modulo 2**32"
  `(setf ,x (logand (+ ,x ,y) #xffffffff)))
(defmacro incf64 (x y)
  "Like INCF, but for integers modulo 2**64"
  `(setf ,x (logand (+ ,x ,y) #xffffffffffffffff)))
```

可以用空行分隔复杂函数的各个部分。不过一般而言，
应把大函数拆分为若干小函数，而不是试图通过增加
纵向空白来提升可读性。如果做不到，应使用
`;;` 注释说明函数中每个被分隔开的
部分各自的作用。

### 横向空白

-   不要在左括号之后或
    右括号之前插入空格。
-   在函数与宏的各个参数之间插入一个空格。
-   不要用空白来横向对齐形式。
-   不要让右括号孤立成行，除非用于闭合顶层 `eval-when`
    形式。

不得在左括号之后或
右括号之前插入横向空白。

不得把右括号单独放在一行。
连续出现的若干末尾右括号必须位于同一行。

<div class='badcode'></div>

```lisp
;; These parentheses pull more attention, hurting readability. This also isn't
;; conventional Lisp style.
    ( defun factorial ( limit )
      ( let (( product 1 ))
        ( loop for i from 1 upto limit
              do (setf product ( * product i ) ) )
        product
      )
    )
```

<div class='goodcode'></div>

```lisp
;; This is easier to read, and avoids a hanging-braces style that is not
;; conventionally used by Lisp programmers.
(defun factorial (limit)
  (let ((product 1))
    (loop for i from 1 upto limit
          do (setf product (* product i)))
    product))
```

形式之间应只使用一个空格。

不要用空格在连续多行的中间位置纵向对齐形式。
当代码具有某种重要、但除此之外不易看出的对称性，
且你希望加以强调时，可以例外。

<div class='badcode'></div>

```lisp
;; The cost of maintaining this sort of formatting and the inconsistent
;; horizontal spacing outweighs the readability benefit of vertical alignment.
(let* ((low    1)
       (high   2)
       (sum    (+ (* low low) (* high high))))
  ...)
```

<div class='goodcode'></div>

```lisp
;; Consistent horizontal spacing is preferred.
(let* ((low 1)
       (high 2)
       (sum (+ (* low low) (* high high))))
  ...)
```

如果嵌套形式跨越多行，必须将其对齐。

<div class='badcode'></div>

```lisp
;; Hard to visually grasp how deeply each form is nested.
(defun munge (a b c)
(* (+ a b)
c))
```

<div class='goodcode'></div>

```lisp
;; Indentation helps the reader parse the nesting of forms.
(defun munge (a b c)
  (* (+ a b)
     c))
```

对于围绕若干定义的 `eval-when` 形式，关于孤立
右括号的规则可以例外；此时应在闭合括号之后
加上 `; eval-when` 注释。

## 文档

### 文档字符串

-   只要语言允许，就使用文档字符串。
-   对所有顶层函数、类型、类、变量和
    宏都使用文档字符串。
-   记录函数的使用方法，包括其参数、返回值
    与副作用，而不是代码的工作原理。
-   当泛型函数的某个特化违反文档字符串所规定的契约时，
    要为该特化撰写文档。必须避免这种情况。

除非某段代码一眼就能看懂，否则都应使用
文档字符串（也称 docstring）为其撰写文档。

文档字符串是给使用你代码的程序员看的。它们可以从
函数、类型、类、变量和宏中提取出来，并由 IDE 之类的
编程工具显示，或通过 `(describe 'foo)` 之类的 REPL
查询显示；也可以基于它们生成 Web 文档或
其他参考资料。因此，文档字符串是记录 API 的
绝佳位置。它们应当描述如何使用代码（包括要避开
哪些陷阱），而不是代码如何工作（以及哪里还需
改进）——后者应写进注释里。

在定义顶层函数、类型、类、变量和宏时，
都应提供文档字符串。一般而言，只要语言允许，
就加上文档字符串。

对于函数，文档字符串应描述函数的契约：函数
做什么、各参数含义、返回什么值、函数可能
发出什么条件。它应在恰当的抽象层次上表述，
解释其意图含义，而不只是语法。在文档字符串中，
Lisp 符号（例如函数参数）的名称使用大写。
例如：
“LENGTH 的值必须是整数。”

<div class='goodcode'></div>

```lisp
(defun small-prime-number-p (n)
  "True if N, an integer, is a prime number."
  ...)

(defgeneric clear-table (table)
  (:documentation
    "Like clrhash, empties TABLE of all associations, and returns TABLE."))
```

较长的文档字符串可以先以一句简短的概要开头，
随后再展开文档字符串的主体内容。

当使用类型名称时，可以在其开头加上反引号、
结尾加上单引号来引用该符号。Emacs 会
高亮该类型，这种高亮会提示读者：M-.
将跳转到该符号的定义。

<div class='goodcode'></div>

```lisp
(defun bag-tag-expected-itinerary (bag-tag)
  "Return a list of `legacy-pnr-pax-segment' objects representing
  the expected itinerary of the `bag-tag' object, BAG-TAG."
  ...)
```

当某个特化对方法行为的影响超出了其泛型函数
文档字符串中的描述时，泛型函数的每个方法
都应单独撰写文档。

### 不显而易见的代码

-   做不显而易见的 bug 修复时，添加注释说明
    改动原因并引用 bug 编号。
-   编写复杂代码时，添加注释说明引入这种
    复杂性的必要性以及代码在做什么。
-   当代码还需后续工作时，加入 TODO。
-   对代码中领域特定语言（DSL）的任何声明
    与使用，都要特别仔细地撰写文档。

修复 bug 时，请判断修复后的代码所做之事是否
显然正确；若不显然，必须添加注释，说明这段代码
为何如此修复该 bug。如果有的话，也建议
附上 bug 编号。

注释是写给代码未来维护者的说明。即便你是唯一
会看到并改动这段代码的人，即便你长生不老、
永不离职，或者根本不在意自己离开后会发生什么
（甚至让代码在这种情况下自行销毁），给代码写
注释也仍可能对你有益。事实上，当你在数周、
数月或数年后重新审视自己的代码时，会发现
自己已与当初写下它的那个人判若两人，而你会
感激先前的自己让代码保持了可读性。

必须为任何复杂的代码写注释，让下一位开发者
能够理解发生了什么。（同样是“被卡车撞”原则。）

也可以把注释当作引导读者的手段，
让他们知道该到哪里去找什么。

对于使用晦涩形式完成某项任务的代码，必须
加上注释，说明该形式的用途及所完成的任务。

对于需要特别留意的注释，例如未完成的代码、TODO 项、
疑问、缺陷与危险，应加入 TODO 注释，指明问题的
类型、性质，以及关于如何处理的说明。

理想情况下，TODO 注释应引用 bug 编号：

```lisp
;; TODO(b/12345): use circular lists for fizzbuzz
```

不过，它也可以是用户名或电子邮件地址：

```lisp
;; TODO(user@example.com): Refactor to provide a better API.
```

其主要目的是提供一种途径，让查阅该 bug 或
该用户的人能找到更多信息。（通常应填自己的用户名。）

在 TODO 注释中指明时间或软件版本时要具体，日期使用
[YYYY-MM-DD](https://www.w3.org/TR/NOTE-datetime) 格式，以便
对此类日期进行自动化处理：

```lisp
;;--- TODO(username): Remove this code after release 1.7 or before 2012-11-30.
```

你应当把自己的 DSL 设计得让熟悉该领域的人
易于阅读和理解。

必须为你所有的 DSL 妥善撰写文档。

有时，你的 DSL 是为简洁而设计的。在这种情况下，
如果从上下文中不易一眼看出，务必说明每个程序的用途。

尤其要注意，使用正则表达式时（例如借助
`CL-PPCRE` 包），必须始终加上注释（通常是
前一行上的双分号注释），至少大致说明该正则
表达式做什么，或使用它的目的是什么。注释
不必逐条解释语法的每一处细节，但应让人
无需真正解析正则表达式就能跟上代码的逻辑。

### 注释分号

-   顶层形式的注释使用三个分号。
-   顶层形式内部的注释使用两个分号。
-   代码行末尾的注释使用一个分号。
-   在分号与注释文本之间留一个空格。

适用于整个文件或顶层形式的注释，
应以三个分号开头。

在顶层形式内部，若注释出现在各行之间，
应以两个分号开头。

如果注释是附带的补充说明且位于行尾，应使用
一个分号。应使用空格把注释与其所指的代码
分开，使注释更为醒目。应尽量让连续相关的
行尾注释纵向对齐。

<div class='goodcode'></div>

```lisp
;;; File-level comments or comments for large sections of code.

;;; Divisibility
;;; Comments that describe a group of definitions.

(defun divisorp (d n)
  (zerop (mod n d)))

(defun proper-divisors (n)
  ...)

(defun divisors (n)
  (cons n (proper-divisors n)))

;;; Prime numbers

(defun small-prime-number-p (n)
  (cond ((or (< n 2))
         nil)
        ((= n 2)   ; parenthetical remark here
         t)        ; continuation of the remark
        ((divisorp 2 n)
         nil)  ; different remark
        ;; Comment that applies to a section of code.
        (t
         (loop for i from 3 upto (sqrt n) by 2
               never (divisorp i n)))))
```

应在分号与注释文本之间留一个空格。

## 命名

### 符号准则

-   全部使用小写字母。
-   使用连字符分隔单词。
-   遵循关于
    [标点、拼写与语法](#punctuation-spelling-and-grammar) 的规则。
-   根据符号的意图而非其内容来命名。对于常见
    后缀，例如 `-P` 和 `-V`，可以例外；但在
    多数情况下应优先采用其他传达类型信息的
    方式（包括声明和类型专用的访问器函数）。
-   函数名、变量名和文件名应具有描述性；
    避免使用缩写。
-   作用域有限的变量可以自由缩写。

所有符号都使用小写。始终使用小写能让
符号名称的查找更容易，也更易读。

请注意，Common Lisp 会进行大小写转换，你的符号的
`symbol-name` 将是大写。由于这种大小写转换，
试图用大小写区分符号是行不通的，只会造成混乱。
虽然可以通过转义符号中的字符来强制小写，但
除非确实需要与第三方软件互操作，否则不应
使用这一能力。

在符号中的所有单词之间放置连字符。如果某个
标识符难以念出口，它很可能命名得很糟糕。

不得用 `"/"` 或 `"."` 代替 `"-"`，
除非你有充分记录、全局性的理由，
并且得到评审你提案的其他黑客的许可。

<div class='badcode'></div>

```lisp
;; Bad
(defvar *default-contextname* "main")  ; Words run together
(defvar *maximum-widget-cnt* 200)      ; Abbreviation to save two characters
```

<div class='goodcode'></div>

```lisp
;; Better
(defvar *default-context-name* "main") ; Words separated by dashes
(defvar *maximum-widget-count* 200)    ; Uses full words
```

Common Lisp 中有关于符号内标点使用的
[约定](https://www.cliki.net/Naming+conventions)。
不应在这些约定之外于符号中使用标点。

在合理范围内，尽可能取具有描述性的名称。
不必担心节省横向空间，因为让新读者能立刻
看懂你的代码要重要得多。

对于作用域较广的符号，不要使用有歧义的
缩写；例如 `defvar` 或 `defun` 定义的符号。
对于项目之外的读者不熟悉的缩写，以及领域
特定的缩写，应集中记录这些缩写。对于作用域
有限的符号，例如函数内部绑定的，可自由缩写。

<div class='badcode'></div>

```lisp
(defvar *n*)               ; Meaningless.
(defvar *nerr*)            ; Ambiguous abbreviation.
(defvar *n-comp-conns*)    ; Ambiguous abbreviation.
(defvar *wgc-connections*) ; Only your group knows what this stands for.
(defvar *pc-reader*)       ; Lots of things can be abbreviated "pc".
(defvar *cstmr-id*)        ; Deletes internal letters.
```

<div class='goodcode'></div>

```lisp
(defvar *price-count-reader*)  ; No abbreviation.
(defvar *num-errors*);         ; "num" is a widespread convention.
(defvar *num-dns-connections*) ; Most people know what "DNS" stands for.
```

应根据变量所代表的高层概念来命名，
而不是根据表示该概念时所用的
低层实现细节来命名。

因此，应避免在变量名中嵌入数据结构或聚合
类型名称，例如 `list`、`array` 或 `hash-table`，
除非你编写的是适用于任意列表、数组、哈希表等的
通用算法。此时把变量命名为 `list` 或 `array` 完全没问题。

事实上，每当协议中的对象出现一种新的意图时，
就应当用 `defclass` 或 `deftype` 引入新的
抽象数据类型。随后，以通用方式操作这类对象的
函数，所使用的变量名可以反映该抽象类型。

例如，若某个变量的值始终是一行（row）
（或者要么是一行、要么是 `nil`），把它叫作
`row` 或 `first-row` 之类是合适的。即使 `row`
已被 `deftype` 定义为 `string` 也无妨——正因为
你已把细节抽象掉，剩下的要点正是它是一行。
在这种情况下不应把变量命名为 `string`，
除非是在专门操作行内部细节以提供该抽象的低层函数中。

保持一致。如果某个变量在一个函数中名为 `row`，
而它的值被传给第二个函数，那么在后者中也
叫它 `row`，而不是比如 `value`（这是个真实案例）。

### 全局变量与常量

-   全局常量应以加号字符开头和结尾。
-   全局变量应以星号字符开头和结尾。

全局常量的名称应以加号字符开头和结尾。

全局变量的名称应以星号开头和结尾
（在此语境下也称 earmuffs）。

在某些项目中，正常情况下通常不应修改或绑定
（但在实验或特殊情形下可能修改或绑定）的参数，
应以美元符号开头（但不以它结尾）。如果项目中
存在这样的约定，应始终遵循；否则应
避免以这种方式命名变量。

Common Lisp 没有全局词法变量，因此采用一种
命名约定，以确保动态绑定的全局变量永远
不会与局部变量重名。可以用一个名称不同的
全局变量配合 `define-symbol-macro` 来伪造全局
词法变量。除非你先发布一个把它抽象掉的库，否则不应使用这一技巧。

<div class='goodcode'></div>

```lisp
(defconstant +hash-results+ #xbd49d10d10cbee50)
(defvar *maximum-search-depth* 100)
```

### 谓词命名

-   单词谓词名称使用结尾的 `"p"`。
-   多词谓词名称使用结尾的 `"-p"`。

返回广义布尔值的函数，名称应带
`"p"` 或 `"-p"` 结尾，以表明它们是布尔谓词。
`nil` 的值表示“假”，其他任何值表示“真”。
返回值除表达谓词的真假之外，不应有
其他含义。一般而言，函数名其余部分为单个
单词时用 `"p"`，多于一个单词时用 `"-p"`。

这一约定的理由见
[CLtL2 中关于谓词的章节](https://www.cs.cmu.edu/Groups/AI/html/cltl/clm/node69.html)。

除真值之外还返回有意义值的函数，例如
`cl:member`，即使其返回值可用作
[广义布尔值](https://www.lispworks.com/documentation/HyperSpec/Body/26_glo_g.htm#generalized_boolean)，
也不应以 `-p` 或 `p` 后缀命名。

布尔变量命名的建议约定是：如果没有其他
便于表达其布尔类型的名称，就同样给名称加上
“-p” 或 “p” 后缀。

### 省略库前缀

-   不要在符号名称中包含库名或包名
    作为前缀。

在包中为符号（外部或内部）命名时，不应把
包名作为前缀放进符号名称里。这样命名会让
客户包在使用包前缀限定该符号时很不方便，
因为包名会出现两次（一次作为包前缀，
另一次作为符号名称内的前缀）。

<div class='badcode'></div>

```lisp
(in-package #:varint)
(defun varint-length64 () ... )

(in-package #:client-code)
(defconst +padding+ (varint:varint-length64 +end-token+))  ; varint is repeated
```

<div class='goodcode'></div>

```lisp
(in-package #:varint)
(defun length64 () ... )

(in-package #:client-code)
(defconst +padding+ (varint:length64 +end-token+))  ; reads nicely with package
```

上述规则的一个例外是：对于那些否则会与使用
当前包的包中变量发生冲突的变量，
可在其名称中加入前缀。例如，`ASDF` 导出的
变量 `*asdf-verbose*` 只控制 `ASDF` 的详细程度，而非整个 Lisp 程序的。

对于对应标准、惯用 Lisp 表达式，且包名或其
一部分会出现在非前缀位置的符号，仍应把
该包名或其一部分写入名称。以下惯用 Lisp
表达式即为示例：

<div class='goodcode'></div>

```lisp
;; Definition of the FOOBAR concept.
(foobar:define-foobar ...)
;; Iterate over elements of FOOBAR.
(foobar:do-foobar ...)
;; Establish a lexical scope dealing with some aspect of FOOBAR.
(foobar:with-frobed-foobar ...)
;; Constructors.
(foobar:make-foobar ...)
(foobar:new-foobar ...)
```

<a id="package-names"></a>

### 包名

-   设计包名时应使其可直接用作符号前缀。
-   不要使用带点的分层包名（例如 `org.library.unit`）。

选择简洁、具有描述性的小写名称，需要时用
连字符（`-`）分隔单词（例如 `threadpool`
或 `concurrent-queue`），即便对 “http” 这类
众所周知的缩写也是如此。Common Lisp 的包
命名空间是扁平的，没有分层名称解析，点号
（`.`）对语言及其工具都没有特殊含义。多段
带点的名称直接用作符号前缀过于笨重，迫使
使用者添加 `:local-nicknames`（往往
使用 `pool` 或 `string` 这类泛泛的叶词，容易丢失上下文或与 `common-lisp` 符号冲突），同时在打印出的符号和回溯中留下长长的带点前缀。

包前缀应与这些包导出的符号名称相配。例如，
如果你有一个名为 `fifo` 的抽象，
且它位于第一类包中，函数会命名为
`fifo-add-to` 和 `fifo-clear-all` 之类。若把包名
设计成可用作前缀，名称会是 `add-to` 和 `clear-all`，因为调用方会这样写：

<div class='goodcode'></div>

```lisp
(fifo:add-to ...)
(fifo:clear-all ...)
```

下面展示了一种冗余、且可以说“丑陋”的符号命名方式。

<div class='badcode'></div>

```lisp
(fifo:fifo-clear-all ...)
```

包名优先使用单数而非复数：

<div class='goodcode'></div>

```lisp
(threadpool:schedule-task ...)
```

上面的写法比下面更易读：

<div class='badcode'></div>

```lisp
(threadpools:schedule-task ...)
```

### 文件名

-   Lisp 及相关源文件的名称使用连字符。
-   使用 “.lisp” 文件扩展名。C stub 使用 “-ci.cc”。

文件名应使用连字符（-）而非下划线（\_）。

文件名应尽可能与包名一致。采用每文件一个包的
策略时，文件名（不含 `.lisp`）应与包名一致
——例如 `threadpool.lisp` 定义 `threadpool` 包。

Lisp 文件名应以 “.lisp” 结尾。

包含外部函数接口 C stub 的源代码文件
应以 “-ci.cc” 后缀结尾。

## 代码结构与组织

### 包

-   使用包，并优先采用每文件一个包的设计。

Lisp 包用于划分命名空间。通常，每个系统
都有自己的命名空间。包有一组外部符号，
它们提供接口，使该包的功能可在别处使用。

一个包的内部符号绝不应被其他包引用。
也就是说，你永远不必使用双冒号 `::` 结构
（例如 `quake::hidden-function`）。如果编写
真正的生产代码需要用到双冒号，那就说明有问题，需要修正。

作为例外，单元测试可以使用被测包的内部符号。

`::` 结构在非常临时的 hack 以及 REPL 中
也很有用。但如果该符号确实属于包对外可见
定义的一部分，就应当把它导出。

有时为了允许某个 API 有多种实现，
需要暴露一些内部符号。与其导出这些内部符号，
不如创建第二个包来导出它们。第一个包供
普通用户使用，第二个包供实现及其扩展者使用。

-   设计包时应通过包限定符使用，而不是通过 `:use`。

如果新增一个库包，例如 `time`，应把它设计成
通过包前缀 `time:` 使用，而不是在使用方的
包定义里加上 `:use time`。相应地，应尽可能
避免导出重复包名的符号（`time:now` 与
`time:current-time`）。当然，完全避免重复是不可能的。
例如，你可能导出 `time:time` 类型，这没有问题。

内部实现包，以及众所周知、被广泛使用的“核心”包，
可以例外。包类型的选择将决定该包中
大多数外部符号的名称。

-   优先使用 `:import-from` 而非 `:use`。

在定义包并访问另一个被设计为无需包前缀
即可使用的包中的符号时，优先使用
`:import-from` 指令，而非 `:use` 指令。
`:import-from` 能让依赖关系更明确。不过，
如果要导入*许多*符号，则 `:use` 可能更合适。

-   不要使用包别名。

绝不能使用包别名。包别名往往是长包名的
简短版本，通常缩写为首字母缩略词。

<div class='badcode'></div>

```lisp
(defpackage :regression-test
  (:nicknames :rtest #-foo :rt))
```

这种做法会污染 Lisp 包名的全局命名空间，
而且很可能成为名称冲突的根源。此外，
不同用户可能在各自代码中使用不同的别名，
从而降低可读性，也削弱了那些不依赖
Lisp 包命名方案的自动化工具处理代码的能力。

-   优先遵循每文件一个包的设计原则，而不是在
    库中的多个文件之间共享同一个包。

    -   它减少了组织代码时需要推敲的概念数量。
        文件、包、命名空间、单元 ... 都具有
        一一对应的关系。
    -   它通过包定义中显式的依赖关系，直接
        记录文件/单元/包的结构。这既有利于
        人类读者，也有利于能从依赖关系中
        轻松推导出系统与构建信息的自动化工具。
    -   它在各代码单元之间强制形成分层的、
        无环的依赖关系。若两个这样的文件
        彼此循环依赖，就难以加载和编译其中已定义的包。
        这能改善软件的架构与设计。

-   不要遮蔽 `common-lisp` 符号。

你的包不得遮蔽（从而实际上重新定义）属于
Common Lisp 语言的符号，也就是 `common-lisp`
（别名 `cl`）包中的符号。存在某些例外，
但它们必须有充分理由，且极为罕见：

-   如果你显式地用一个更安全或功能
    更完备的版本替换某个 Common Lisp 符号。
-   如果你定义的包不打算被 “used”，且有充分
    理由导出与 Common Lisp 冲突的符号，
    例如 `log:error` 和 `log:warn` 等。

### CLOS

-   禁止新增对 CLOS 的使用；允许新增 print-object 方法

## 语言使用准则

### 以函数式为主的风格

-   仅在能带来更好/更清晰的代码时才使用副作用：

Lisp 最适合当作“大体函数式”的语言来使用。

避免修改局部变量，改为尝试重新绑定。

避免先创建对象再用 SETF 设置其槽。
更应在初始化期间就设置好槽。

让类尽可能不可变，也就是说，尽可能不要
为槽提供 setter 函数。（槽仍可通过 `with-slots` 设置。）

采用以函数式为主的风格，会让编写线程安全的
并发代码容易得多，也让代码更易于测试。
它还常常让代码更易于推理，因为在头脑中
跟踪程序状态是很困难的。

### 特殊变量

-   谨慎使用
    [特殊变量](https://www.lispworks.com/documentation/HyperSpec/Body/d_specia.htm#special)
    （例如由
    [`defvar`](https://www.lispworks.com/documentation/HyperSpec/Body/m_defpar.htm#defvar)
    定义的那些）。

谨慎使用特殊（动态绑定）变量，
并且只在不会让读代码的人感到意外、
且能带来显著好处的情况下使用。

事实上，每个特殊变量都构成一份状态。
开发者在试图理解代码做什么、怎么做时，
必须在头脑中跟踪所有相关变量的状态；
测试必须针对所有相关组合来编写和运行；
为了隔离某项活动，必须小心地在局部绑定
所有相关变量，包括间接使用的模块中的变量。
它们可能让宝贵信息无法在回溯中打印出来。
不仅每个新变量都有开销，而且随着这类变量
数量增加，变量之间的相互作用会让代码复杂度呈指数级上升。收益必须与成本相称。

不过请注意，特殊变量并不是 BASIC 或 C 意义上
的全局变量。由于特殊变量可以动态绑定到
局部值，它们比所有使用者必然相互干扰的
全局值单元强大得多。

适合作为特殊变量的，是那些可以自然地把
“当前的”用作前缀的事物，例如“当前的数据库
连接”或“当前的业务数据源”。就其余代码而言，
它们是单例，而且把它们作为显式参数传递，
往往并不会提升相关源代码的可读性或可维护性。

它们能让代码更易重构。如果你有一条
请求处理链，其中多层都作用于
“当前”请求，那么把请求对象显式传给每个
函数，就要求链上每个函数都带一个请求参数。
把代码抽取成新函数时，这些新函数往往
也得带上这个参数，从而让代码堆满样板代码。

把特殊变量当作每线程变量来对待。除非存在
对所有线程都有效的默认值，否则不要提供
默认的顶层绑定。每个需要该变量的控制线程
都应显式绑定它。这样，任何对该变量的
错误使用都会导致“变量未绑定”错误，
且每个线程都会看到该变量属于自己的值。
具有默认全局值的变量，通常应在线程创建时于局部重新绑定。

### 赋值

-   在同一个包内，保持包级赋值形式的一致。

处理赋值与副作用有若干种风格；在修改某个包时，
应始终沿用该包正在使用的那一种。开始
编写新包时，请选择一种合理的风格。

关于在单个形式中做多重赋值，有两种流派：第一种
风格把尽可能多的赋值归入同一个 `setf` 或 `psetf`
形式，从而尽量减少带有副作用的形式数量：

<div class='goodcode'></div>

```lisp
(setf foo bar
      baz quux)
```

第二种风格把赋值拆成尽可能多的独立 `setf`
（或 `setq`，见下文）形式，以便尽可能通过
grep `(setf (foo ...` 定位修改某类位置的形式：

```lisp
(setf foo bar)
(setf baz quux)
```

grep 模式实际上必须涵盖你在程序中可能用到的
所有修改位置的形式，这可能使该理由显得
有说服力，也可能变得毫无意义，取决于代码其余
部分的风格。请遵循所修改包中使用的约定。对新包，我们推荐第一种约定。

关于 `setf` 与 `setq`，有两种流派：第一种
把 `setq` 视为过时的实现细节，完全不用它，
改用 `setf`；第二种把 `setf` 视为多出一层的
复杂性，只要可能就避免使用它，改用 `setq`
（即当被赋值的位置是变量或符号宏时）。
请遵循所修改包中使用的约定。对新包，我们推荐第一种约定。

本着大体纯粹的函数式风格的精神（它让测试
与维护更轻松），我们建议你考虑如何用
最少的赋值来完成工作。

### 断言与条件

只使用 `assert`、`check-type` 和 `etypecase`
来检测内部 bug，并且要大量使用它们。

-   优先使用 `etypecase` 而非 `typecase`
-   使用 `error` 检查来自文件的输入。
-   如果函数会发出错误，请在其契约中说明。
-   优先用 `log` 记录警告，而非使用 `warn`。
-   绝不直接调用 `signal`，改用 `error`。
-   优先使用 `handler-bind` 而非 `restart`。
-   优先使用 `restart` 而非 `throw` 和 `catch`。
-   避免笼统地处理条件：
    -   与当前代码无关的错误应继续向上传播。
    -   避免笼统地处理 `serious-condition`。
-   绝不在 `unwind-protect` 的清理部分发出条件。
-   绝不通过重新发出条件来做清理。
-   绝不返回条件或错误值，而应用 ERROR 发出它。

只把 `assert` 用于检测内部 bug。代码应
用 `assert` 断言那些一旦失效就表明软件
自身出错的不变量。不正确的输入应在运行时
妥善处理，且不得导致断言被违反。
`assert` 失败的受众是开发者。不要用 `assert` 的
data-form 和 argument-form 来指定要发出的条件。
用它们打印调试信息是可以的（既然只用于调试，就不存在国际化问题）。

`check-type`、`etypecase` 也属于断言形式。
只要其中之一失败，就说明发现了 bug。对于
函数的输入，优先使用 `check-type` 而非 `(declare (type ...))`。

无效输入，例如读入但不符合预期格式的文件，
不应被视为违反断言。始终要检查输入是否有效，
若无效则采取适当措施，例如发出
应用特有的错误。

使用 `error` 发出与用户数据、请求、权限等
有关的问题，或向调用方报告“异常结果”。

始终用显式的条件类型调用 `error`；在生产
代码中绝不应只传一个字符串。这样便于国际化。

通过发出条件来报告异常结果的函数，应在
其契约（文档、文档字符串等中的文字描述）里
明确说明这一点。当函数发出其契约未规定的
条件时，那就是 bug。契约应清楚地规定
条件类。随后函数可以发出属于这些条件中
任一类之类型的任何条件。也就是说，
发出所记载条件类的子类实例是没有问题的。

代码不得调用 `signal`。请改用 `error`。

当可以使用 `restart` 机制时，
不要使用 `throw` 和 `catch`。

当可以使用 `handler-bind` 时，不要使用 `restart`。

不要笼统地处理所有条件，例如类型 `t`，
或使用 `ignore-errors`。相反，应让未知条件
传播到标准的最终处理程序去处理。

有少数场合适合处理所有条件，但很罕见。
问题在于，处理所有条件会掩盖程序 bug。
如果确实需要处理“所有条件”，则必须只处理
`error`，*而非* `t`，也不是 `serious-condition`。

`(error (make-condition 'foo-error ...))` 等价于
`(error 'foo-error ...)` ——代码必须使用更短的形式。

不要在 `unwind-protect` 的清理形式内部发出
条件，也不要以其他方式从处理程序之外的
清理处理程序中非局部退出，例如 `invoke-restart`。

不要通过重新发出条件来做清理。如果这样做，
且该条件未被处理，堆栈跟踪会停在重新发出
之处，把其余部分隐藏起来。而其余部分恰恰是我们真正关心的！

<div class='badcode'></div>

```lisp
(handler-case
  (catch 'ticket-at
    (etd-process-blocks))
  (error (c)
    (reset-parser-values)
      (error c)))  ; The origin of this error has been lost.
```

<div class='goodcode'></div>

```lisp
(unwind-protect
  (catch 'ticket-at
    (etd-process-blocks))
  (reset-parser-values))  ; The error passes through but cleanup still happens
```

不要把条件对象作为多值中的一员返回。
相反，应发出条件来表示异常结果。

应发出条件来表示异常结果，
而不是依赖特殊的返回类型。

### 类型检查与声明

-   在以下情况使用 `(declare (type ...))`：
    -   仅用于非 API 函数的契约，以及
    -   对低层内部函数做优化。
-   在以下情况使用 `check-type`：
    -   用作隐式参数的特殊变量，
    -   API 函数的契约，以及
    -   有助于发现输入 bug 的地方。

如果你的函数把某个特殊变量用作隐式参数，
最好为该特殊变量加上 `check-type`，
原因有二：提示读代码的人该变量被隐式
当作参数使用，同时也有助于发现 bug。

使用 `(declare (type ...))` 是最不可取的机制，
正如 Scott McKay 所说：

> 事实是，`(declare (type ...))` 会依据编译器在 speed、
> safety 等方面的设置而做不同的事。在某些编译器中，
> 当 speed 优先于 safety 时，`(declare (type ...))`
> 会告诉编译器“请假定这些变量具有这些类型”，
> *而不*生成任何类型检查。也就是说，如果某个
> 变量的值是 `1432`，而你把它声明为 `string` 类型，
> 编译器可能就直接把它当作字符串来用。
>
> 寓意：不要用 `(declare (type ...))` 来声明任何
> API 函数的契约，这并不合适。当然，可以用在
> “helper”函数上，但不要用在 API 函数上。

在内部低层函数中，若这些声明用于优化，
就使用恰当的声明。不过这样做时，请参阅
我们对
[不安全操作](lispprogrammingguide.md#unsafe-operations) 的建议。

## 元语言准则

### 宏

-   用宏来清晰地表达重复出现的模式。
-   当（可能是内联的）函数就够用时，不要写宏。
-   避免编写过于复杂的宏：
    -   宏形式应只处理语法。
    -   尽量减少宏展开后的代码，在适当之处
        把逻辑委托给实现函数（*call-with 风格*）
-   宏通常应保持卫生，只绑定由调用方提供
    或由 `gensym` 生成的符号。
-   清楚地记录宏中不卫生的方面与副作用。
-   宏的参数只求值一次。
-   对于带 `body` 形式的宏，即使没有参数，
    也应包含一个空的 `()`，以便将来扩展而不破坏调用方。
-   不要用普通宏来提升性能，应使用内联。
-   按需使用编译器宏来提升性能。
-   避免定义其他宏的宏。若必须使用，
    请仔细撰写文档。
-   编写读取宏之前，先取得开发者共识。
-   绝不让读取宏泄漏出使用它的系统。

宏通过提供语法抽象让代码更清晰。不过，
这是以语法复杂性为代价的，而且宏展开后的
形式不像函数那样易于单元测试和调试。

在函数就够用的地方绝不使用宏。也就是说，
如果你所写内容的语义符合函数的语义，
就把它写成函数而非宏。这条建议也适用于
用 `macrolet` 定义的局部宏；可能时改用 `flet` 或 `labels`。

尽可能复用已有的宏。只有当表达力上的
提升值得这份投入时，才编写复杂的宏。

复杂的宏应采用
[*call-with 风格*](http://random-state.net/log/3390120648.html)，
即把尽可能多的逻辑委托给一个（可能声明为
内联的）辅助函数。宏的 `&body` 参数通常会被
拼接到传给该辅助函数的 lambda 表达式体中。
实现函数的命名应遵循在外部名称前加 `%` 的
约定。例如，宏 `foo` 可以把一个 body lambda
及其他参数传给函数 `%foo`。

宏绑定的符号通常要么由调用方提供，
要么用 `gensym` 生成。由于 `gensym`
生成的是全新符号，这些符号不可能
出现在调用方传入的其他形式中。这可
防止宏展开后的代码执行时符号被意外
遮蔽（[*变量捕获*](https://www.bookshelf.jp/texi/onlisp/onlisp_10.html)）；
保持这一性质的宏称为*卫生的*。
给 `gensym` 的可选参数传入字符串，
可为生成的符号提供人类可读的名称。`alexandria:with-gensyms` 宏提供了生成此类符号的便捷方式。

如果宏在执行调用方提供的形式期间必须绑定
其他符号（例如全局变量），则其接口的这一
方面必须清楚地记录在文档中。宏展开中
非调用方传入的形式所产生的副作用也应清楚记录。

如果宏调用中含有将用于宏展开代码的形式，
该形式应只展开一次，且求值次数应符合
调用方的预期。把代码展开多次（尤其是
`&body` 形式）会使宏展开更难读、
二进制体积更大。`alexandria:once-only`
提供了一种便捷方式：求值用户提供的形式
并把它绑定到一个新生成的符号。采用 `call-with` 风格
更容易保持这一性质，因为形式可以在调用辅助函数时只求值一次。

如果某个形式需要在宏展开代码的多个分支中
求值，可以改为把它拼接到一个局部函数定义中，
让各分支都调用该函数。此时，应用 `flet`
给该局部函数一个唯一的 gensym 名称，并（若适用）声明 dynamic-extent。

编写带 body 的宏时，例如 `with-xxx` 宏，
即使没有任何参数，也应为它们留出位置。
例如，若定义 `with-lights-on`，不要把它写成这样：

<div class='badcode'></div>

```lisp
(defmacro with-lights-on (&body b)
  ...)

;; Example call
(with-lights-on
  ...)
```

相反，应在 body 参数之前加上一个空的参数列表：

<div class='goodcode'></div>

```lisp
;; Macro lambda list has empty parens before body argument
(defmacro with-lights-on (() &body b)
  ...)

;; Call has empty arguments list before body forms
(with-lights-on ()
  ...)
```

这样一来，日后就能添加可选参数或关键字参数，
而不必改动宏的所有使用处：

<div class='goodcode'></div>

```lisp
(defmacro with-lights-on ((&keyword install-new-bulbs-p) &body b)
  ...)

;; Calls that don't use the optional parameter don't need update
(with-lights-on ()
  ...)

;; Other calls can use the new parameter
(with-lights-on (:install-new-bulbs-p t)
  ...)
```

不得出于性能原因把函数改写成宏。如果
性能分析表明，代码作为函数体的一部分而非
内联展开会带来性能问题，请妥善记录需求
与分析结果，并使用 `(declaim (inline <function-name>))`。

也可以用编译器宏通过指定源到源的变换
来加快函数执行。请注意，它会干扰对
被优化函数的跟踪。

编写定义宏的宏（即生成宏的宏）时，
要特别清楚地撰写文档与注释，因为它们更难理解。

未经系统开发者达成共识，不得安装新的
读取宏。读取宏不得从使用它们的系统泄漏
到该系统的客户端，或同一项目中使用的
其他系统。必须使用 `cl-syntax` 或
`named-readtables` 之类的软件来控制读取宏的使用方式。
客户端应能自行选择是否使用与你相同的
读取宏：即便客户端不使用这些读取宏，你的系统也必须可用。

### 读取期求值

-   避免使用 `#.` 读取宏：
    -   优先使用 `eval-when` 和 `defconstant`。
-   避免读取期的副作用。

标准读取宏 `#.` 会读入一个对象、
对该对象求值，并让读取器返回结果值。

在其他惯用法够用的地方不得使用它，
例如用 `eval-when` 在编译期求值副作用、
用普通宏返回编译期计算出的表达式、
用 `load-time-value` 在加载期计算它。

读取期求值常被用作在编译期求值某物的快捷
方式（其实是“读取期”，但结果相同）。如果
使用它，该求值绝不能有任何副作用，
也绝不能依赖任何可变的全局状态。
应把 `#.` 视为强制进行“常量折叠”的手段：
足够聪明的编译器本可自行算出来，只是在
编译器不够聪明、且这一差别要紧时才用它。

`#.` 的另一用途是在既非表达式、也非
（准）引用的位置展开宏的等价物，例如
lambda 列表。不过，如果你发现自己大量
使用它，也许该改为定义宏，把 lambda 列表
的使用方替换成能识别某种扩展的形式。

每当打算使用 `#.` 时，都应考虑改用
`defconstant` 及其变体（可放在 `eval-when` 中），
给该值取一个能说明其含义的名称。

### EVAL

-   绝不在生产代码中于运行时使用 `eval`。

真正适合使用 `eval` 的场合少之又少，
因此必须与评审者商议；它很容易被误用。

如果代码在运行时操纵符号并需要取得
某个符号的值，请使用 `symbol-value`，而非 `eval`。

通常，你真正需要的是写一个宏，而不是使用 `eval`。

你可能会想用 `eval` 作为快捷方式，
在语言的安全子集中求值表达式。但相比于
构建专用求值器，正确检查并净化这类 `eval` 用法
的所有可能输入，往往需要更多审视。不得在运行时这样使用 `eval`。

允许使用 `eval` 的场合有：

-   交互式开发工具的实现。
-   构建基础设施。
-   测试框架中的后门。（生产代码中
    绝不能有此类后门。）
-   在编译期折叠常量的宏。
-   把定义登记到元数据结构的宏；登记形式
    有时既在编译期求值，也被包含进宏展开，
    因而能立即供其他宏使用。

请注意，在后一种情况下，如果该宏不会在顶层
使用，就可能无法把这些定义作为宏展开的
一部分提供出来。同样的现象也可能出现在
`deftype` 展开中，或宏所用的辅助函数中。
在这些情况下，你可能确实需要在宏中使用
`asdf-finalizers:eval-at-toplevel`。它不仅会在
宏展开时 `EVAL` 你的定义以便立即可用，
还会把该形式留存下来，供包含到
`(asdf-finalizers:final-forms)` 中，而你需要
把它放在被编译文件的末尾（或在该形式
被需要之前）。这样，无论加载未经编译的
fasl 还是在编译时，副作用都存在；两种情况中该形式都在加载期可用。`asdf-finalizers` 通过在遗漏时抛错来确保该形式存在。

### INTERN 与 UNINTERN

-   绝不在运行时使用 `intern` 或 `unintern`。

不得在运行时使用 `intern`。它不仅会 cons，
还会要么创建一个不会被回收的永久符号，
要么让人得以访问内部符号。这为内存泄漏、
拒绝服务攻击、对内部的未授权访问以及与其他符号的冲突提供了可乘之机。

不要仅仅为了与关键字比较就 `intern` 一个
字符串；请使用 `string=` 或 `string-equal`。

<div class='badcode'></div>

```lisp
(member (intern str :keyword) $keys)  ; intern has undesired side-effects
```

<div class='goodcode'></div>

```lisp
  (member str $keys :test #'string-equal)
;; Compares without interning
```

注意：当给定符号时，string-equal 使用 `symbol-name` 进行比较。

不得在运行时使用 `unintern`。它会破坏
依赖动态绑定的代码，也会让调试更困难。
不得在运行时动态 intern 任何新符号，因此也就无需动态 unintern 任何东西。

当然，可以在编译期、在某些宏的实现中
使用 `intern`。即便如此，通常更合适的做法是
使用其上的抽象，例如 `alexandria:symbolicate`
或 `alexandria:format-symbol` 来创建所需符号。

## 数据表示

### 使用 NIL

-   用 `nil` 表示假，或表示不可能为 `nil` 的未指定值。
-   用符号表示值的缺失，或表示
    可能为 `nil` 的未指定值。

`nil` 可以有几种不同的解释：

-   “假。”此时使用 `nil`。应使用
    运算符 `not` 或谓词函数 `null` 来检测假 `nil`。
-   “空列表。”此时使用 `nil`。当已知
    参数是正规列表时，应使用 `endp` 检测空列表，
    否则用 `null`。
-   表示某个值未指定。此时，如果代码中
    任何地方都没有歧义风险，可以使用 `nil`；
    否则应使用显式、具有描述性的符号。
-   表示已知某个值不存在。此时，
    应使用显式、具有描述性的符号，而非 `nil`。

不得在数据表示中引入会让调试代码的人
头疼的歧义。只要存在歧义风险，就应
为每种情形使用显式、具有描述性的符号
或关键字，而不是两者都用 `nil`。
如果确实用了 `nil`，务必把区别记录清楚。

在许多场合，与其把“我不知道”表示为某个
特定值，不如改用多值：一个表示已知的值
（如果有的话），另一个表示该值是否已知或已找到。

处理数据库类时请记住，`nil` 未必总是
映射到 `null`（反之亦然）！数据库的需求
可能与 Lisp 的需求不同。

### 列表

-   仅将列表用于同类元素构成的容器。
-   仅将列表用于顺序访问。
-   将列表用于在编译期或加载期会被转换为数据
    结构的字面常量。
-   优先使用正规列表（proper list），而非非正规列表（improper list）
-   使用 `first`、`second`、……和 `rest` 访问正规列表。
-   使用 `car` 和 `cdr` 访问非正规列表。
-   避免将列表用作集合，极小的集合除外。

尽管早在 1958 年，LISP 还是“LISt Processing”的缩写，但它的后继者
Common Lisp 自 1980 年代以来一直是一门具备现代数据结构的现代编程语言。
你必须在程序中使用恰当的数据结构。

不得在不适用的场合滥用内置的（单链表）`list` 数据结构，即便
Common Lisp 让它的使用变得格外容易。

除了作为同类元素的容器之外，应避免将列表
用于任何其他用途。

只有在列表的性能特征适合当前算法时，才必须使用列表：
即对列表的全部内容进行
顺序迭代。

适合使用列表的一个例外是：事先已知列表的规模会
一直非常小（比如少于 16 个元素）。

对于宏以及宏在编译期使用的函数，列表数据结构往往（但并非
总是）是合适的：的确，在 Common Lisp 中，源代码不仅
以列表形式传递，而且宏展开与编译过程通常也会一次性、
顺序地遍历整个源代码。（注意，高级宏系统并不直接使用
列表，而是使用能够追踪源代码位置与作用域的抽象语法
对象；不过，目前 Common Lisp 中尚不存在这样的
高级宏系统。）

适合使用列表的另一个例外，是用于引入那些在编译期或加载期
会被转换为更合适的数据结构的字面常量。最好用一个名字
相对较短的函数，从这类字面量构建出程序的
数据结构。

在列表并非恰当数据结构的众多情形下，诸如
[cl-containers](https://cliki.net/cl-containers) 或
[lisp-interface-library](https://cliki.net/lisp-interface-library) 等各种库
提供了大量不同的数据结构，应能满足你程序的全部基本需求。
如果现有库不能令人满意，请参阅关于
[使用库](lispprogrammingguide.md#using-libraries) 的说明。

在列表确为正确数据结构的场合，优先使用正规列表，而非
非正规列表。仅在作用域有限且性能至关重要的列表中
使用非正规列表。

对于正规列表：使用 `first` 访问列表的第一个元素，使用 `second`
访问第二个元素，依此类推。使用 `rest` 访问列表的尾部。使用
`endp` 检测列表是否到末尾。

对于非正规列表：使用 `car` 访问列表的第一个元素。使用 `cdr`
访问列表的尾部。使用 `consp` 检测列表是否到末尾。

作为例外，在手动解构列表时，你可以使用 `cdadr` 及其他变体，
而不必组合使用多个列表访问函数。在这种语境下，使用 `car`
和 `cdr` 来替代 `first` 和 `rest` 也说得通。不过请记住，
在这类情形下，改用 `destructuring-bind` 或
`optima:match` 之类更高级的构造，
也许更为恰当。

除关联表（alist）之外，这种情况应当很少见，因为在适用之处
你应使用结构体和类，需要树时则使用数据结构库。

把列表当作集合的表示是个坏主意，除非你确知这些列表
会很小，因为访问操作是 *O(n)* 而非 *O(log n)*。对于
任意大的集合，应使用平衡二叉树，例如借助
`lisp-interface-library`。

<div class='badcode'></div>

```lisp
(member foo (union list-1 list-2))  ; Slow O(n) best-case and creates a new list
```

<div class='goodcode'></div>

```lisp
(or (member foo list-1) (member foo list-2))  ; O(n) average-case
```

事实上，`union` 不仅会产生不必要的 cons 操作，在某些实现上
还可能是 *O(n\^2)*，即便为 *O(n)* 也相当慢。

### 数组

-   对需要非顺序访问的同构集合，使用数组。
-   在随机访问很重要的场合，使用数组。

`elt` 作用于列表时具有 *O(n)* 的行为。如果要对某个对象
进行随机元素访问，请改用数组和 `aref`。

例外是关键路径之外的代码，那里本就已知列表
很小。

### 结构体与类

-   对异构类型的组合，使用结构体或类。
-   对于返回多个、且不会立即被解构的值，使用结构体
    或类。

不得把列表当作在函数调用中传入传出多个不同类型、彼此
独立的值的手段。有时把列表当作一个临时的简易结构体会很
方便，例如“列表的第一个元素是 FOO，
第二个是 BAR”，但这种用法应尽量少，因为这类小约定
很难记住。只有在解构函数的参数列表，或构造一个
参数列表以便对其 `apply` 某个函数时，才可以
这样使用列表。

传递一个由若干异构类型的值所组成的对象的恰当方式，
是使用由 `defstruct` 或
`defclass` 定义的结构体。

只有当函数返回少量、且意在由调用方立即使用的值时，
才应使用多值，而不是把它们一并作为参数
传给后续的函数。

### 点对

-   少用点对，且仅用于表示恰好两个同类、紧密相关
    的值。
-   对点对使用 `car` 和 `cdr`。
-   对点对搭配使用 `null` 和 `nil`。

当用 cons 单元存放一对相关对象时，使用 `car` 和
`cdr`。在此语境下使用 `null` 来检测 `nil`。

## 正确的形式

对于众所周知的函数、宏和特殊形式，你必须遵循
正确的用法。

### 定义函数

-   避免使用 `&aux` 和 `&allow-other-keys`。
-   避免同时使用 `&optional` 和 `&key` 参数。
-   避免函数中绑定形式的过度嵌套
    -   应当把函数拆开。
    -   考虑使用 `nest` 宏。

应避免使用 `&allow-other-keys`，因为它会模糊函数的
契约（contract）。就调用方而言，几乎任何实际函数（无论
是否为泛型）都只允许一组固定的关键字，它们是其契约
的一部分。若你正在实现泛型函数的一个方法，且它
无需知晓某些关键字参数的值，就应当对所有未使用的
参数显式地 `(declare (ignore ...))`。
除非你明确想在以匹配该特定方法的实参调用泛型函数时，
对所有方法禁用允许关键字的检查，否则不得使用
`&allow-other-keys`。注意，泛型函数的契约属于
`defgeneric`，而非 `defmethod`；就泛型的调用方
而言，它基本上只是该泛型函数的一个
“实现细节”。

`&allow-other-keys` 适用的一种情形是：你编写一个包装器
函数，用来包装另一些可能变化的函数（在计算过程中
或开发期间变化），并以 `&REST` 参数传递一个 plist。

应避免使用 `&aux` 参数。

应避免同时使用 `&optional` 和 `&key` 参数，因为当只
指定了部分可选参数时，关键字参数便无法使用。当函数
同时具有 `&optional` 和 `&key` 参数时，不得为 `&optional`
参数设置非 `nil` 的默认值。

为使库达到最大的可移植性，`defmethod` 定义最好对
所有未使用的必需参数使用 `(declare (ignorable ...))`。
确实，有些实现若你对这些参数 `(declare (ignore ...))`，
就会发出警告；而另一些实现若你没有对它们
`(declare (ignore ...))`，也会发出警告。
`(declare (ignorable ...))` 在所有实现上都有效。

应避免函数内部绑定形式的过度嵌套。如果函数最终
出现大量嵌套，或许应把它拆成几个函数或宏。若它
确实是单一的概念单元，可考虑使用 `fare-utils:nest` 之类的
宏，至少减少所需的缩进量。在典型的、嵌套层次为 4 层
或更少的短函数里使用 `nest` 是不好的做法，但在
嵌套层次达到 10 层或更多的少见长函数中不用它，
同样是不好的做法。请自行判断，并
咨询评审者。

### \#'FUN vs. 'FUN

-   用 `#'FUN` 而非 `'FUN` 来引用函数，除非：
    -   要访问全局函数绑定，或
    -   需要动态链接。

前者读作 `(function fun)`，指向函数对象，
并采用词法作用域。后者读作 `(quote fun)`，指向
符号，调用该符号时会使用它的全局 `fdefinition`。

当使用那些接受函数实参的函数时（例如 `mapcar`、`apply`、
`:test` 和 `:key` 参数），应使用 `#'` 来引用函数，
而不仅仅是单引号。

一个例外是你明确需要动态链接，因为你预期
全局函数绑定会被更新。

另一个例外是你明确想访问全局函数绑定，并避开
可能的遮蔽性词法绑定。这种情况不应经常出现，因为
当你还要使用被遮蔽的函数时，遮蔽某个函数通常是个坏主意；
给词法函数换个名字即可。

必须使用不带函数引用 `#'` 记法的 `(lambda ...)`。
与 `#'symbol` 对比 `'symbol` 的情形不同，这里含义
并无变化。较短的宏形式会展开为函数引用形式，因此
更长的记法就没有必要了。

### 条件表达式

-   只有一个分支时，使用 `when` 和 `unless`。
-   有两个分支时，使用 `if`。
-   若某个子句会是 `progn`，就不要用 `if`，请改用下列
    形式之一。
-   相对于嵌套的 `if` 语句，优先使用 `cond`、`case` 或其变体。
-   在以下情况下优先使用 `and` 和 `or`：
    -   它们能让代码更简洁。
    -   除了 `or` 最后一个子句中可选的 `error` 之外，
        没有其他副作用。
-   相对于 `case` 和 `typecase`，优先使用 `ecase` 和 `etypecase`。
-   不要使用 `ccase` 或 `ctypecase`。
-   另请参阅 [陷阱](lispprogrammingguide.md#case-and-ecase) 一节，了解使用
    `case` 和 `ecase` 时常见的陷阱。

只有一个分支时使用 `when` 和 `unless`。有两个分支时
使用 `if`，有多个分支时使用 `cond`。

不过，不要用 `progn` 作为 `if` 的子句——改用 `cond`、`when` 或 `unless`。

注意，在 Common Lisp 中，当条件不满足时 `when` 和 `unless`
会返回 `nil`。你可以利用这一点。不过，若有特定理由
坚持返回值，也可以用 `if` 显式返回 `nil`。
类似地，你可以在 COND 的最后加入兜底子句 `(t nil)`，
或在 CASE 的最后加入 `(otherwise nil)`，以强调
条件表达式的返回值确实重要、且该分支确实
会被用到。当条件表达式仅用于副作用时，应省略
这个兜底子句。

当比使用 `if`、`cond`、`when` 或 `unless` 更简洁，且
不涉及副作用时，应优先使用 `and` 和 `or`。你也可以在
`or` 的最后一个子句中把 `error` 用作副作用。

相对于 `case` 和 `typecase`，应使用 `ecase` 和 `etypecase`。
最好尽早捕获错误的值。

<div class='badcode'></div>

```lisp
(case x ; Bad: silently returns NIL on mismatch
  ((bar) :bar)
  ((baz) :baz))
```

<div class='goodcode'></div>

```lisp
(ecase x ; Better: will error on mismatch
  ((bar) :bar)
  ((baz) :baz))
```

完全不应使用 `ccase` 或 `ctypecase`。至少，不应在
服务器进程中使用它们，除非你拥有相当健壮的错误处理
基础设施，并确保不会以此方式泄露敏感数据。它们
是为交互使用而设计的，若导致数据或控制权泄露给
攻击者，可能造成耐人寻味的破坏。

### 比较运算符

-   恰当地使用 `eq` 和 `eql`；在其他条件相同的情况下，
    对非性能关键的代码优先使用 `eql`。
-   对 `string=` 或 `string-equal` 使用 `:START` 和 `:END` 参数，
    而不要用 `subseq`。
-   使用 `zerop`、`plusp` 或 `minusp`，而不要与 `0` 或 `0.0` 比较。
-   另请参阅
    编程指南中的 [比较运算符](lispprogrammingguide.md#comparison-operators) 一节，
    了解正确用法。

在 `eq` 与 `eql` 之间选择时，除非你在编写性能关键的
底层代码，否则应使用 `eql`。`eql` 减少了一类令人难堪的
错误出现的机会（例如，若拿数字或字符来比较）。
相对 `eq` 可能有极小的性能代价，不过在 SBCL 下，它
常常会被完全编译优化掉。`eq` 等价于 `eql` 加上类型声明，
为优化而使用它时，应当像对待任何此类
[不安全操作](lispprogrammingguide.md#unsafe-operations) 一样。

此外，对 `string=` 或 `string-equal` 应使用 `:start` 和 `:end`
参数，而不要用 `subseq`；例如
`(string-equal (subseq s1 2 6) s2)` 应改为
`(string-equal s1 s2 :start1 2 :end1 6)`。这样更好，因为它
更清晰，而且不产生 cons。

应使用 `zerop`、`plusp` 或 `minusp`，而不要把某个值与
`0` 或 `0.0` 比较。

### 迭代

-   在简单情形下，优先使用 `dolist` 或 `dotimes` 形式，而非 `loop`。
-   在 `loop` 中优先使用 `with`，而非 `let` 绑定：
    -   除非 `let` 能让代码更清晰。
    -   也可用 `let` 来避免 `finally (return ...)` 形式。
-   不要在迭代宏的体里给迭代变量赋值。
-   通常，`loop` 关键字优先使用无修饰的符号，除非是
    为了一致性，或出现在宏展开中。

在不会用到 `loop` 的任何功能（如绑定、收集或
块返回）的简单情形下，应改用 `dolist` 或 `dotimes`
这类更简单的形式，而不是 `loop`。

当 `loop` 的 `with` 子句能省去一层 `let` 嵌套时，
就使用它。如果在 `loop` 之后返回某个被绑定变量更清晰，
也可以用 `let`，而不必用笨拙的 `finally (return ...)` 形式。

在 `dotimes` 的体中，不要给迭代变量赋值。

多数系统使用当前包中无修饰的符号作为 `loop` 关键字，
而不是 `keyword` 包中的 `:keywords`。应优先采用这种方式，
但以下情况除外：

*   这与周围代码所用的约定不符。
*   `loop` 形式由宏生成，且使用无修饰的关键字
    会导致宏展开更难读。

### I/O

-   使用日志工具，不要直接写入 `*standard-output*` 或
    `*error-output*`。
-   不要在供生产使用的接口中使用 `print-object`。
-   在单个 `format` 就够用的地方，不要使用多个 `write-` 形式。
-   输出单个字符时优先使用 `write-char`。
-   相对于 `(format nil "~A" value)`，优先使用 `princ-to-string`。
-   在格式字符串中使用 `~<NEWLINE>` 或 `~@<NEWLINE>`，以满足编辑器
    的行长限制。
-   使用 `"~:@(~A~)"` 或 `"~(~A~)"` 来改变格式控制
    参数的大小写。

编写服务器时，代码不得把输出发送到标准流，例如
`*standard-output*` 或 `*error-output*`。代码必须改用
恰当的日志框架来输出调试消息。我们是以服务器方式运行的，
所以没有控制台！

代码不得用 `print-object` 与用户交互——`print-object` 仅
用于调试目的。修改任何 `print-object` 方法都不得破坏
任何公共接口。

在单个 `format` 字符串就能胜任的地方，不要使用一连串
`write-xxx`。使用 format 便于将来在需要时把格式控制
字符串参数化。

应使用 `write-char` 输出一个字符，而不是用 `write-string`
输出只含单个字符的字符串。

不要使用 `(format nil "~A" value)`；
应改用 `princ-to-string`。

应在格式字符串中使用 `~<Newline>` 或 `~@<Newline>`，以免它们在
100 列的编辑器窗口中折行，或者用来缩进某些段落或子句，
使其更易读。

不应对格式控制参数使用 `string-upcase` 或 `string-downcase`；
而应使用 `"~:@(~A~)"` 或 `"~(~A~)"`。
