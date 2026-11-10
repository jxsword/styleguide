# Google 的 Haskell 风格指南

修订版 1.01

<!-- mdformat off -->
* TOC
{:toc}
<!-- mdformat on -->

<a id="Background"></a>

## 背景

Haskell 是一种成熟的、通用的、纯函数式语言。它以
强大的静态类型系统（支持类型推断）、惰性（严格来说，
是“非严格”的）执行语义、高阶函数、参数化
多态、类型类以及单子（monadic）效应而著称。

Haskell 的语法相当简洁，而且你在风格上可能做出的大多数选择，
通常都与你希望表达代码的语义
紧密相关。因此，本指南的规范性往往比其他大多数指南要弱一些，因为
在编写 Haskell 代码时可以随意做出的选择更少了。

由 Google 开发的开源项目应当符合本指南中的
要求。

<a id="Structure"></a>

## 结构

<a id="Haddock"></a>

### Haddock

模块以及所有导出的顶层元素都应有 Haddock。

Haddock 应当紧接在其所描述的元素之前。它无需重复
参数名或类型，因为这些在声明中一目了然。

使用完整的句子；以大写字母开头并使用正确的标点。

**例外：** 极其简单的类型同义词或其他非常明显的声明
无需包含任何 Haddock。

<div class='goodcode'></div>

```haskell
type Forest p a = [Tree p a]    -- simple enough to not need Haddock

-- | Returns values in the Forest from entries that cover the given prefix.
-- The value list is ordered from most general to most specific entries.
forestLookup :: (Prefix p) => p -> Forest p a -> [a]
```

在 Haddock 中，内联链接应节制使用。链接是受鼓励的，但
无需为所有 API 名称都添加链接。在以下情况下添加链接：

*   用户可能确实想要点击它来获取更多信息（由你
    判断），且
*   仅针对注释中每个 API 名称的首次出现（无需
    重复添加链接）。

<a id="Exports"></a>

### 导出

*   所有模块都应当有显式的导出列表。
*   像所有列表一样格式化，在 `module` 之后另起一行开始。
*   如果逻辑相关，可以在一行内放置多个导出项。
*   顺序应当有条理——也就是 Haddock 中展示的顺序。

除以上规则外，不要以“方便”为由重新导出模块。
不过，在以下两种情况下重新导出模块是可以接受的：

*   可以从 `Internal` 模块重新导出那些原本
    不会被导出的内容。
*   可以有一个 "package" 模块，它只做一件事：
    从同一 package 中导出公共模块。

**例外：** 当大部分导出定义是由 Template Haskell 生成时，
可以不使用显式的导出列表，因为在导出列表中
显式命名它们会适得其反。

<a id="Imports"></a>

### 导入

*   导入可以拆分为由单个空行分隔的若干组。
*   推荐：将导入拆分为两组：外部模块与内部模块。
*   在每组内部，导入必须按完整的模块名按字母顺序排列。
*   导入可以是限定的（qualified），也可以是针对特定元素的。两者同时出现
    是可以的。
*   同一 package 中的导入可以整组导入，但
    不推荐这样做。

一般来说，使用模块名的最后一个组成部分作为限定名。

对相关的模块使用相同的前缀是可以接受的。

**例外：** 有些模块设计为可以合理地不带导入列表地导入，
例如 `Data.Bits`，这是可以接受的。

对于以下模块，使用非常短的限定导入名是可以接受的，
因为它们在 Haskell 源码中被广泛使用：

```haskell
import qualified Data.ByteString as BS
import qualified Data.ByteString.Lazy as BL
import qualified Data.HashMap.Strict as HM    -- or Data.HashMap.Lazy as needed
import qualified Data.HashSet as HS
import qualified Data.Map as M
import qualified Data.Set as S
import qualified Data.Text as T
import qualified Data.Text.Lazy as TL
```

将这些规则综合起来：

<div class='goodcode'></div>

```haskell
import Data.Bits                             -- okay for some modules
import Data.Maybe (mapMaybe, maybeToList)    -- better to list what you use...
import qualified Data.Ratio as Ratio         -- ...or import qualified
import qualified Data.Text as T              -- short name allowed for this
import qualified Data.Text.Encoding as T     -- reuse name for related modules
import qualified Data.Text.IO as T
import qualified Text.Parsec as Parsec
import qualified Text.Parsec.Expr as Parsec

import AnInternalProject.Data.WhoopTree      -- okay to import all, but discouraged
```

<a id="Pragmas"></a>

### 编译指示（Pragmas）

GHC 选项与 `LANGUAGE` 编译指示应放在文件的最顶部。

*   在顶部放一个 `{-# OPTIONS_GHC ... #-}` 指令（如果需要的话）
*   在此之后，为每个语言扩展放一个 `{-# LANGUAGE ... #-}` 指令，
    按排序顺序排列（如果需要的话）

 `OPTIONS_GHC` 指令只应被用于与源文件相关的特定选项，
例如针对测试代码的 `-fno-warn-orphans`。通用的
编译选项（如 `-O2`）应放在 `.cabal` 文件中。

由 `LANGUAGE` 编译指示启用的特性，应当始终在需要它们的每个源文件中
列出，而绝不应通过 `.cabal` 文件中的标志全局开启。这样，未来的开发者
在阅读代码时就能清楚哪些语言扩展
正在生效。

 `INLINE`、`INLINEABLE` 以及类似的编译指示，只有在你已经
测试过它们确实能改善你关心场景下的速度时才应使用。使用时，
它们应当紧接在其所适用的声明之后。

以下 GHC 语言扩展没有争议，可以在需要时
加以使用。话虽如此，也要考虑使用该扩展是否能按比例地
改善代码，以抵消它给未来读者带来的额外负担：

*   `DeriveDataTypeable`, `DeriveGeneric`, `DeriveFunctor`, `DeriveFoldable`,
    and `DeriveTraversable`
*   `BangPatterns`
*   `CPP`
*   `FlexibleContexts`
*   `ForeignFunctionInterface`
*   `GADTs`
*   `GeneralizedNewtypeDeriving`
*   `MagicHash`
*   `MultiParamTypeClasses`
*   `NamedFieldPuns`
*   `OverloadedStrings`
*   `PatternGuards`
*   `Rank2Types`, `RankNTypes`
*   `RecordWildCards` and `DisambiguateRecordFields`
*   `ScopedTypeVariables`
*   `TemplateHaskell`
*   `TupleSections`
*   `TypeFamilies`
*   `ViewPatterns`

其他 GHC 扩展应当避免，因为它们可能稳定也可能不稳定，
会增加读者了解它们的负担，并可能强迫客户端使用它们。

<a id="Warnings"></a>

### 警告

代码应当能够干净地通过编译，且不产生来自 GHC 的任何警告。

当传入 `-Wall` 参数时，GHC 会发出非常有用的警告。代码
应当能够同时以 `-Wall` 和 `-Werror` 编译，确保警告不会被忽略。

（在 GHCi 中，你可以通过将 `:set -Wall ...` 添加到你的
 `~/.ghc/ghci.conf` 文件中来获得相同的效果。）

在极少数情况下，当有必要在某个既不包含相应类声明、也不包含
相应类型声明的模块中声明实例时，可以通过在该相关文件
顶部添加 `{-# OPTIONS_GHC -fno-warn-orphans #-}` 这一行来抑制
关于孤儿实例的警告。

<a id="Style"></a>

## 风格

<a id="Layout"></a>

### 布局

使用布局，而不是大括号和分号。

除单行代码外，使用布局而不是大括号和分号。这样
代码更清晰。

<a id="Type_Declarations"></a>

### 类型声明

所有顶层函数都应当有类型声明。

尽管 Haskell 支持类型推断，但所有顶层函数都应当
包含类型声明。至少，类型声明能提供
良好的文档。

在合理的情况下，使用尽可能多态的类型。

<a id="Comments"></a>

### 注释

除编译指示外，或当注释必须位于一行中间时，所有注释
都使用 `--`。

如果在破折号之前的行上有文本，那么破折号之前应当
至少有两空格。如果在破折号之后有文本，那么
破折号之后应当有一空格。

如 Haddock 一节所述，所有顶层元素都应当有一个位于其前的、
用于 Haddock 的注释。其目的是解释函数的
用途，而不是其实现。

实现应当能从代码中清晰看出，但代码中的注释
应当用于解释那些非显而易见的原因——为什么某件事要这样做，
或者它为何特别棘手。

<a id="if_then_else"></a>

### if…then…else

考虑优先使用守卫（guards）和模式匹配，而不是 `if`…`then`…`else`。

一般来说，在函数外层，模式匹配和守卫比嵌套的
 `if` 和 `case` 结构更清晰。不过，在其他地方 `if`
可能更清晰。由你来判断。

<div class='badcode'></div>

```haskell
nth :: Int -> [a] -> Maybe a
nth i xs = if null xs || i < 0
    then Nothing
    else if i == 0
        then Just (head xs)
        else nth (i-1) (tail xs)
```

<div class='goodcode'></div>

```haskell
nth :: Int -> [a] -> Maybe a
nth i _     | i < 0 = Nothing
nth _ []            = Nothing
nth 0 (x:xs)        = Just x
nth i (_:xs)        = nth (i-1) xs
```

<a id="Idioms"></a>

## 惯用法

函数式编程催生了大量新的
编程惯用法。以下惯用法是受鼓励的：

<a id="Partial_Functions"></a>

### 偏函数

[Partial functions](https://www.haskell.org/haskellwiki/Partial_functions) 是指
那些并非对所有可能参数都有定义的函数。

极力避免使用来自 `Prelude` 和基库（base libraries）的偏函数。
常用例子有：`head`、`(!!)`、`minimum`、`fromJust` 和 `read`。

**例外：** 在模式匹配、守卫或紧邻的其他逻辑能够确定
这些函数被安全应用的情况下，
可以调用它们。

<div class='goodcode'></div>

```haskell
defaultChoice :: [String] -> String
defaultChoice [] = "beige"
defaultChoice opts = minimum opts
  -- okay because pattern match ensures non-empty

digitsReversed :: Integer -> Integer
digitsReversed i = (* signum i) . read . reverse . show $ abs i
  -- okay because show of a non-negative value only produces digits
```

不要编写偏函数。

**例外：** 如果模块内部的某个函数，由于该模块所维护的不变量
而绝不会到达某种情况，那么针对这些情况调用 `error`
是可以接受的，并且优先于返回不准确的结果，
或启发式地恢复不变量：

```haskell
data PTrie = PT { ptSubs :: [(String, PTrie)] }
  -- Invariant this module maintains: There is no non-empty prefix that is
  -- shared by any two sub-PTries of a given node.

insert :: String -> PTrie -> PTrie
insert s pt = case filter (not . null . greatestCommonPrefix s) $ ptSubs pt of
  [] -> ...   -- no node matches
  [a] -> ...  -- one node matches, need to recurse or split
  _ -> error "PTrie.insert PTrie has subs with a common prefix"
```

<a id="Point_Free"></a>

### 无点风格（Point-Free）

[Point-free style](http://www.haskell.org/haskellwiki/Haskell/Pointfree) 很好，
而且常常会催生出简洁的代码，这类代码关注的
是代码做了什么，而不是它对什么做的。

不过，要避免过度使用它。例如，不要仅仅为了处理多个参数
而使用扭曲的无点风格：

<div class='badcode'></div>

```haskell
f = (g .) . h       -- makes most of us puzzle it out
```

<div class='goodcode'></div>

```haskell
f x = g . h x       -- most readers will get this immediately
f x y = g $ h x y   -- depending on the functions, this may or may not be better
```

<a id="Combinators"></a>

### 组合子

被设计为组合子的库，会为其他
开发者提供非常强大的工具。可以学习的例子有 Parsec 和 PrettyPrint。

<a id="QuickCheck"></a>

### QuickCheck

测试应当尽可能用 QuickCheck 编写。这种测试形式
出奇地有效。对于需要显式测试的特殊情况，
使用 HUnit。用 Test Framework 将它们整合在一起。

经常需要编写 `Arbitrary` 的实例。它们应当放在
对应的 `_Test` 模块中。（并配以相应的选项来关闭
关于孤儿实例的警告。）这些实例应当确保各类情况的
权重相等，如果做不到，则要解释原因。

<a id="Naming"></a>

## 命名

<a id="General_Rules"></a>

### 通用规则

使用混合大小写的标识符，不带下划线。

Haskell 的命名规则相当严格，此处不再赘述，
因为语言本身会强制要求遵守。

应避免使用下划线，因为混合大小写是 Haskell 社区中的
主流风格。以下对下划线的使用是可以接受的：

*   一个未使用的参数或模式元素：`_`
*   一个需要更具描述性名称的未使用参数或模式匹配元素：
    `_sizeHint`。
*   用于标识一个 QuickCheck 属性、测试、测试组或测试模块：
    `prop_UnionIsAssociative`、`test_SetOperations` 或 `Data.MultiWaySet_Test`
*   当某事物的逻辑名称同时也是 Haskell 中的
    保留字时，附加一个下划线：`type_`。

使用常见的习惯用法，在名称后附加撇号（`'`）来表示
被改变的值，例如：`fib` 和 `fib'`。

使用常见的习惯用法，对列表使用复数形式：例如，针对列表的
模式匹配可以是 `(a:as)`。（另见下文「短变量」。）

<div class='badcode'></div>

```haskell
simpleMetricComputer :: Double -> Set Things -> Double
simpleMetricComputer _ things = ...
    -- it isn't clear what the first argument is

map :: (a -> b) -> [a] -> [b]
map _f [] = []
map f (a:as) = f a : map f as
    -- no need to name _f in first clause, as it is clear from the second clause
```

<div class='goodcode'></div>

```haskell
simpleMetricComputer :: Double -> Set Things -> Double
simpleMetricComputer _sizeHint things = ...
    -- clear what the first argument is for, and that it isn't used

map :: (a -> b) -> [a] -> [b]
map _ [] = []
map f (a:as) = f a : map f as
    -- first argument in first clause is clear from context and second clause
```

<a id="Short_Variables"></a>

### 短变量

简短的、单字母的变量名是可以的。

当变量名的作用域仅跨几行时，简短或单字母的
变量名是可以接受的，甚至是受鼓励的。一般来说，它们有助于
展现代码的结构。

<div class='badcode'></div>

```haskell
nextAfter :: Eq element => element -> [element] -> Maybe element
nextAfter match (current:next:remainder) =
    if current == match then Just next
                        else nextAfter match (next:remainder)
nextAfter _ _ = Nothing
```

<div class='goodcode'></div>

```haskell
nextAfter :: Eq a => a -> [a] -> Maybe a
nextAfter m (x:y:ys) =
    if x == m then Just y
              else nextAfter m (y:ys)
nextAfter _ _ = Nothing
```

<a id="Module_Names"></a>

### 模块

命名模块时使用单数形式。

使用 `Data.Map` 和 `Data.ByteString.Internal`，而不是
 `Data.Maps` 和 `Data.ByteString.Internals`。

<a id="Abbreviations"></a>

### 缩写

名称中的缩写应当采用混合大小写。

<div class='badcode'></div>

```haskell
HTTPResponse
IPBlock
```

<div class='goodcode'></div>

```haskell
HttpResponse
IpBlock
```

**例外：** 有少数情况，某个术语的特定大小写用法已有
相当多的先例。在这种情况下，保留特定的选择
是可以接受的。注意，这不适用于像 `HTTP` 这样全大写的事物——
它们全大写仅仅是因为它们是缩写。

<div class='goodcode'></div>

```haskell
GREoIPsec  -- acceptable because specific precedent for this form exists
```

<a id="Formatting"></a>

## 格式化

<a id="Vertical_Spacing"></a>

### 垂直间距

垂直空白应当节约使用，以便在单屏内能够
看到更多上下文。

一般来说，用一空行分隔声明就足够了。在模块导入与第一个顶层声明
之间，以及文件的各个主要部分之间（如果需要的话），
应当使用两空行。在 where 子句的各个声明之间不需要空行，
但如果有许多或较长的声明时，有时会
使用空行。

<div class='goodcode'></div>

```haskell
{-# OPTIONS_GHC -fno-warn-orphans #-}
{-# LANGUAGE TupleSections #-}

-- | Run-length encoding types and functions.
--
-- Run-length encoded sequences are a quick and efficient compression scheme
-- that is so on and so forth....

module RunLength
    ( RunList
    , rleEncode
    , relDecode
    ) where

import Data.List (replicate)


type RunList a = [(Int, a)]

-- | Run-length encode a sequence of elements.
rleEncode :: (Eq a) => [a] -> RunList a
rleEncode [] = []
rleEncode (a:as) = go 1 a as
  where
    go n a [] = [(n,a)]
    go n a (b:bs) | a == b    =         go (n+1) b bs
                  | otherwise = (n,a) : go 1     b bs
-- | Run-length decode a RunList.
rleDecode :: RunList a -> [a]
rleDecode = concatMap (uncurry replicate)
```

<a id="Horizontal_Spacing"></a>

### 水平间距

*   宽度为 80 列
*   不能有尾随空格

目标是让水平间距有助于展现
表达式的结构。使用水平间距来清晰地呈现各个子句之间的
结构关系，是可以接受的，甚至是受鼓励的。

<div class='goodcode'></div>

```haskell
-- | Run-length encode a sequence of elements.
rleEncode :: (Eq a) => [a] -> RunList a
rleEncode [] = []
rleEncode (a:as) = go 1 a as
  where                        -- see rules for "where" below
    go n a [] = [(n,a)]
    go n a (b:bs) | a == b    =         go (n+1) b bs
                  | otherwise = (n,a) : go 1     b bs
```

数据声明也应当遵从这些规则：

<div class='goodcode'></div>

```haskell
data Tree a = Branch a (Tree a) (Tree a)
            | Leaf

data HttpException
    = InvalidStatusCode Int
    | MissingContentHeader
```

<a id="Indentation"></a>

### 缩进

*   以 4 空格为间隔进行缩进
*   不使用制表符（tab）

由于缩进在 Haskell 中承担着重要的语义功能，
因此缩进以 4 空格为间隔。

表达式中续写到另一行的部分，应当比前一行的缩进
多缩进一个层级，而不是相对于它们所延续的
构造进行缩进。（不过，请参见前一节关于使用对齐来使
结构清晰的内容，并自行判断。）

<div class='goodcode'></div>

```haskell
arbitrary = arbitrary >>= \b -> if b
    then do
        cidr <- choose (0, 32)
        ip <- pick 32 cidr
        return $ makeBlock (IPv4 ip) cidr
    else do
        cidr <- choose (0, 64)
        hi <- pick 64 cidr
        lo <- pick 64 (cidr - 64)
        return $ makeBlock (IPv6 hi lo) cidr
```

<a id="Comment_Formatting"></a>

### 注释

*   使用 `--` 注释
*   在代码与注释之间使用 2 个或更多空格

使用 2 空格将行尾注释与代码分隔开。对
数据类型定义的注释进行对齐：

<div class='goodcode'></div>

```haskell
data CommandSummary = CommandSummary
    { ciName :: T.Text        -- ^ name and short summary on one line
    , ciSynopsis :: T.Text    -- ^ invocation template, like "foo [-f] file..."
    , ciOptions :: [([T.Text], T.Text)]
                              -- ^ a list of pairs of options synonyms and their
                              -- summary description
    }
```

<a id="Where"></a>

### where

为了将局部声明与主表达式分隔开，对 `where` 使用
*悬挂缩进*。对于所有其他用法（模块、类和
实例声明），使用尾随的 `where`。

```haskell
module Main.TestRouters
    ( TestPrefix, TestMetric(..)
    , prop_routeSameAsNaive
    ) where

class PrefixLength a where
    prefixLength :: a -> Int

instance Arbitrary TestMetric where
    arbitrary = arbitraryBoundedEnum
    shrink = shrinkNothing

updateFlowTable :: (Ord m, Eq p) =>
    FlowMod m p t -> FlowTable m p t -> FlowTable m p t
updateFlowTable u tbl = case u of
    AddFlow m p t -> let (cs,ds) = break ((<= m) . fst) (clean p)
                     in cs ++ (m, (p, t)) : ds
    DeleteFlow p  -> clean p
  where
    clean p = filter ((/= p) . fst . snd) tbl
```

<a id="Deriving"></a>

### deriving

 `deriving` 子句可以跟在声明之后，也可以独占一行。

```haskell
data Light = Stop | Slow | Go
    deriving (Eq, Ord, Enum, Bounded, Show)

newtype Max a = Max a deriving (Eq, Ord, Show)

data HttpStats
    = StatusOk
    | StatusRedirectMoved
    | StatusRedirectTemporary
    | StatusNotFound
    deriving (Eq, Show)

data Employee = Employee
    { empName :: String
    , empId :: Integer
    , empDepartment :: Integer
    } deriving (Eq, Ord, Show)
```

<a id="case_of"></a>

### case…of

 `of` 标记与 `case` 标记出现在同一行。缩进各个分支（cases）。

当有助于可读性时，对齐 `->` 箭头。

<div class='goodcode'></div>

```haskell
foobar = case something of
    Just j  -> foo
    Nothing -> bar
```

<a id="let_in"></a>

### let…in

 `in` 标记出现在带有 `let` 标记的那一行的下一行，
并与 `let` 对齐。

<div class='goodcode'></div>

```haskell
access add = let (s,a) = add `divMod` segmentSize
                 (p,b) = a `divMod` pageSize
             in getPageByte b . getSegmentPage p <$> getSegment s
```

如果较短，整个 `let` 表达式可以全部写在一行上：

<div class='goodcode'></div>

```haskell
formatItem x = let (a,b) = x `divMod` 1000 in show a ++ '/' : show b
```

<a id="if_then_else_2"></a>

### if…then…else

缩进 `then` 和 `else`。

 `then` 和 `else` 是相对于包含 `if` 的那一行的
缩进层级进行缩进的，而不是相对于 `if` 本身。

<div class='goodcode'></div>

```haskell
foo = if ....
    then ...
    else ...

foo = do
    someCode
    if condition
        then someMoreCode
        else someAlternativeCode

foo = bar $ \qux -> if predicate qux
    then doSomethingSilly
    else someOtherCode
```

同样的规则也适用于嵌套在内的 do 代码块：

<div class='goodcode'></div>

```haskell
foo = do
    instruction <- decodeInstruction
    skip <- load Memory.skip
    if skip == 0x0000
        then do
            execute instruction
            addCycles $ instructionCycles instruction
        else do
            store Memory.skip 0x0000
            addCycles 1
```

**例外：** 如果表达式很短，整个表达式
写在一行上是可以接受的：

<div class='goodcode'></div>

```haskell
adjective n = if odd n then "odd" else "even"
```

<a id="List_Formatting"></a>

### 列表格式化

对跨多行的列表，使用“前导逗号”列表格式。

被括号或大括号包围、并跨越多行的列表及其他构造，
应当格式化为：后续每一行以逗号开头，
并且结束的标点独占一行。这适用于导出列表、导入列表、
列表值、记录字段声明以及
记录值。

将多个值放在一行上是可以接受的，如果它们在逻辑上归为一组，
则用“逗号空格”分隔。

<div class='goodcode'></div>

```haskell
exceptions =
    [ InvalidStatusCode
    , MissingContentHeader
    , InternalServerError
    ]
```

<div class='goodcode'></div>

```haskell
data Person = Person
    { firstName :: !String  -- ^ First name
    , lastName  :: !String  -- ^ Last name
    , age       :: !Int     -- ^ Age
    } deriving (Eq, Show)
```

<div class='goodcode'></div>

```haskell
module CPU
    ( CpuState(..), powerOnState

    , zeroPage
    , bitN, bitV, bitD, bitI, bitZ, bitC

    , assignBit
    , assignZN

    , setZN, setAZN, setXZN, setYZN
    , setZVNbit, setACZVN, setCZN

    , fetch, store
    , clearBus
    , fetchIndirectAddr
    , nextPC, fetchPC

    , push, pull, pushAddr, pullAddr, pushP, pullP
    ) where
```

<a id="Operators_Punctuation"></a>

### 运算符与标点

在所有运算符两侧各使用一个空格。在逗号和分号后使用一个空格。
在反斜杠标记后不使用空格。

<div class='goodcode'></div>

```haskell
sumSqDelta = dSumSqDelta + delta' * (val' - mean)

(rib', fib') = process updates rib

\s -> s ++ reverse s      -- note: \ is not an operator, no trailing space

quarterlyIncome `mod` 10  -- treat identifiers used as an operator the same

foldr (*) 1 list          -- treat operator in parenthesis as an identifier
```

对于运算符区段（operator sections），不要在“未应用”的一侧添加空格：

<div class='goodcode'></div>

```haskell
map (++ " likes noodles") people
```

**例外：** 对于由单字符值组成的元组和常见操作，
当省略逗号或运算符后的空格能改善可读性时，
可以这样做：

<div class='goodcode'></div>

```haskell
swap (a,b) = (b,a)

foldl' (\v d -> 10*v + digitToInt d) 0

go n m (a:as) | m == a = go (n+1) m as
```

<a id="Parting_Words"></a>

## 临别赠言

运用常识，并*保持一致性*。

如果你在编辑代码，花几分钟看看你周围的代码，
弄清它的风格，并与之保持一致。

制定风格指南的意义在于，建立一套通用的编码词汇表，
这样人们就能专注于你要表达的内容，而不是你
表达的方式。我们在此提出全局性的风格规则，以便人们了解这套词汇表。
但局部风格同样重要。如果你添加到文件中的代码与周围的
现有代码看起来截然不同，那么这种不连续性会在读者阅读时
打乱他们的节奏。尽量避免这一点。

好了，关于写代码的描述已经说得够多了；代码本身要有趣得多。
玩得开心！
