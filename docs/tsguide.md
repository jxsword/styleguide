<div class="numbered"></div>

# TS/JS 风格指南

本指南基于 Google 内部的 TypeScript 风格指南，但进行了
轻微调整以移除 Google 内部的章节。Google 的内部
环境对 TypeScript 的约束不同于你在 Google 之外可能
遇到的约束。这里的建议对于那些编写代码并打算
将其导入 Google 的作者特别有用，但在你的外部环境
中可能并不适用。

此版本没有自动部署流程，因为它是由志愿者
按需推送的。

<!-- mdformat off -->
* TOC
{:toc}
<!-- mdformat on -->

<div class="numbered"></div>

<a id="introduction"></a>

## 简介

<div class="numbered"></div>

<a id="terminology-notes"></a>

### 术语说明

本风格指南在使用 [RFC 2119](https://tools.ietf.org/html/rfc2119)
术语时，采用 *must*、*must not*、*should*、*should not*、
和 *may* 这些短语。*prefer* 与 *avoid* 分别对应 *should* 与 *should
not*。祈使句和陈述句具有规范性，
对应 *must*。

<div class="numbered"></div>

<a id="guide-notes"></a>

### 指南说明

给出的所有示例均为**非规范性的**，仅用于说明
风格指南的规范性语言。也就是说，虽然示例采用 Google
风格，但它们未必展示了表达代码的*唯一*优雅方式。
示例中可选项格式化选择不得作为规则强制执行。

<div class="numbered"></div>

<a id="source-file-basics"></a>

## 源文件基础

<a id="file-encoding"></a>

<div class="numbered"></div>

<a id="file-encoding-utf-8"></a>

### 文件编码：UTF-8

源文件以 **UTF-8** 编码。

<a id="special-characters"></a>

<div class="numbered"></div>

<a id="whitespace-characters"></a>

#### 空白字符

除了行终止符序列之外，ASCII 水平空格字符
（0x20）是源文件中任何位置出现的唯一空白字符。
这意味着字符串字面量中的所有其他空白字符都
必须被转义。

<div class="numbered"></div>

<a id="special-escape-sequences"></a>

#### 特殊转义序列

对于任何拥有特殊转义序列（`\'`、`\"`、`\\ `、`\b`、
`\f`、`\n`、`\r`、`\t`、`\v`）的字符，应使用该序列而非
对应的数字转义（例如 `\x0a`、`\u000a` 或 `\u{a}`）。绝不
使用遗留八进制转义。

<div class="numbered"></div>

<a id="non-ascii-characters"></a>

#### 非 ASCII 字符

对于其余非 ASCII 字符，使用实际的 Unicode 字符（例如
`∞`）。对于不可打印字符，可以使用等效的十六进制或
Unicode 转义（例如 `\u221e`）并附上解释性注释。

<div class='goodcode'></div>

```ts
// Perfectly clear, even without a comment.
const units = 'μs';

// Use escapes for non-printable characters.
const output = '\ufeff' + content;  // byte order mark
```

<div class='badcode'></div>

```ts
// Hard to read and prone to mistakes, even with the comment.
const units = '\u03bcs'; // Greek letter mu, 's'

// The reader has no idea what this is.
const output = '\ufeff' + content;
```

<a id="modules"></a>
<a id="source-organization"></a>

<div class="numbered"></div>

<a id="source-file-structure"></a>

## 源文件结构

文件由以下内容组成，**按顺序排列**：

1.  版权信息（如有）
2.  带有 `@fileoverview` 和/或其他文件级 JSDoc 标签的 JSDoc（如有）。
3.  导入语句（如有）
4.  文件的实现

**恰好一个空行**分隔每一个存在的章节。

<div class="numbered"></div>

<a id="file-copyright"></a>

### 版权信息

如果文件中需要包含许可证或版权信息，请在文件顶部的
JSDoc 中添加。

<a id="file-fileoverview"></a>
<a id="jsdoc-top-file-level-comments"></a>

<div class="numbered"></div>

<a id="fileoverview"></a>

### `@fileoverview` JSDoc

一个文件可以拥有一个顶级的 `@fileoverview` JSDoc。如果
存在，它可以提供对文件内容、用途或其依赖项信息的
描述。换行的行不进行缩进。

示例：

<div class='goodcode'></div>

```ts
/**
 * @fileoverview Description of file. Lorem ipsum dolor sit amet, consectetur
 * adipiscing elit, sed do eiusmod tempor incididunt.
 */
```

<div class="numbered"></div>

<a id="imports"></a>

### 导入语句

ES6 和 TypeScript 中有四种导入语句变体：

<!-- mdformat off -->

| 导入类型                     | 示例                             | 用于               |
| ---------------------------- | -------------------------------- | ------------------ |
| module[^module_import]       | `import * as foo from '...';`    | TypeScript 导入    |
| named[^destructuring_import] | `import {SomeThing} from '...';` | TypeScript 导入    |
| default                      | `import SomeThing from '...';`   | 仅用于需要它们的其他外部代码 |
| side-effect                  | `import '...';`                  | 仅用于导入那些在加载时产生副作用的库（例如自定义元素） |

<!-- mdformat on -->

<div class='goodcode'></div>

```ts
// Good: choose between two options as appropriate (see below).
import * as ng from '@angular/core';
import {Foo} from './foo';

// Only when needed: default imports.
import Button from 'Button';

// Sometimes needed to import libraries for their side effects:
import 'jasmine';
import '@polymer/paper-button';
```

[^module_import]: Namespace imports are often called 'module imports'
[^destructuring_import]: named imports are sometimes called 'destructuring
    imports' because they use similar syntax to destructuring assignments.

<div class="numbered"></div>

<a id="import-paths"></a>

#### 导入路径

TypeScript 代码*必须*使用路径来导入其他 TypeScript 代码。路径*可以*
是相对的，即 `.` 或 `..` 开头，或者基于根目录，例如
`root/path/to/file`。

代码*应该*使用相对导入（`./foo`）而非绝对导入
`path/to/foo`，当引用同一（逻辑）项目内的文件时，因为这允许
移动项目而不会引入这些导入的变更。

请考虑限制父级步数（`../../../`）的数量，因为它们会使
模块和路径结构难以理解。

<div class='goodcode'></div>

```ts
import {Symbol1} from 'path/from/root';
import {Symbol2} from '../parent/file';
import {Symbol3} from './sibling';
```

<!-- Keep the previous id for backwards compatibility with links. -->

<a id="module-versus-destructuring-import"></a>

<div class="numbered"></div>

<a id="namespace-versus-named-imports"></a>

#### 命名空间导入与具名导入

命名空间导入与具名导入均可使用。

对于文件中频繁使用或名称清晰的标识符，优先使用具名导入，
例如 Jasmine 的 `describe` 和 `it`。具名导入可以
根据需要用 `as` 取更清晰的别名。

当从大型 API 使用许多不同标识符时，优先使用命名空间导入。尽管
使用了 `*` 字符，命名空间导入不同于其他语言中
所见的“通配符”导入。相反，命名空间导入为模块的所有导出
命名，模块中的每个导出标识符都成为该模块名称的
一个属性。对于像 `Model` 或 `Controller` 这样具有通用名称的导出
标识符，命名空间导入可以在无需声明别名的情况下
提升可读性。

<div class='badcode'></div>

```ts
// Bad: overlong import statement of needlessly namespaced names.
import {Item as TableviewItem, Header as TableviewHeader, Row as TableviewRow,
  Model as TableviewModel, Renderer as TableviewRenderer} from './tableview';

let item: TableviewItem|undefined;
```

<div class='goodcode'></div>

```ts
// Better: use the module for namespacing.
import * as tableview from './tableview';

let item: tableview.Item|undefined;
```

<div class='badcode'></div>

```ts
import * as testing from './testing';

// Bad: The module name does not improve readability.
testing.describe('foo', () => {
  testing.it('bar', () => {
    testing.expect(null).toBeNull();
    testing.expect(undefined).toBeUndefined();
  });
});
```

<div class='goodcode'></div>

```ts
// Better: give local names for these common functions.
import {describe, it, expect} from './testing';

describe('foo', () => {
  it('bar', () => {
    expect(null).toBeNull();
    expect(undefined).toBeUndefined();
  });
});
```

<div class="numbered"></div>

<a id="jspb-import-by-path"></a>

##### 特殊情况：Apps JSPB protos

Apps JSPB protos 必须使用具名导入，即使会导致较长的导入
行。

此规则的存在是为了提升构建性能并便于消除死代码，因为
`.proto` 文件通常包含许多并非全部同时需要的 `message`。
通过利用解构导入，构建系统可以对 Apps JSPB 消息创建更细粒度的
依赖关系，同时保留基于路径导入的
易用性。

<div class='goodcode'></div>

```ts
// Good: import the exact set of symbols you need from the proto file.
import {Foo, Bar} from './foo.proto';

function copyFooBar(foo: Foo, bar: Bar) {...}
```

<div class="numbered"></div>

<a id="renaming-imports"></a>

#### 重命名导入

代码*应该*通过命名空间导入或重命名导出本身来修复名称冲突。代码
*可以*在需要时重命名导入
（`import {SomeThing as SomeOtherThing}`）。

以下三个示例中重命名会有所帮助：

1.  如果需要避免与其他导入标识符发生冲突。
2.  如果导入的标识符名称是自动生成的。
3.  如果导入的标识符名称本身不够清晰，重命名可以
    提升代码清晰度。例如，使用 RxJS 时，将 `from` 函数
    重命名为 `observableFrom` 可能更易读。

<div class="numbered"></div>

<a id="exports"></a>

### 导出

在所有代码中使用具名导出：

<div class='goodcode'></div>

```ts
// Use named exports:
export class Foo { ... }
```

不要使用默认导出。这能确保所有导入遵循统一的
模式。

<div class='badcode'></div>

```ts
// Do not use default exports:
export default class Foo { ... } // BAD!
```

为什么？

默认导出不提供权威名称，这使得集中维护
变得困难，而代码所有者获得的收益相对较少，包括潜在的
可读性下降：

<div class='badcode'></div>

```ts
import Foo from './bar';  // Legal.
import Bar from './bar';  // Also legal.
```

具名导出的好处在于，当导入语句尝试导入未声明的
内容时会报错。在 `foo.ts` 中：

<div class='badcode'></div>

```ts
const foo = 'blah';
export default foo;
```

而在 `bar.ts` 中：

<div class='badcode'></div>

```ts
import {fizz} from './foo';
```

产生 `error TS2614: Module '"./foo"' has no exported member 'fizz'.` 而
`bar.ts`：

<div class='badcode'></div>

```ts
import fizz from './foo';
```

产生 `fizz === foo`，这可能出乎意料且难以调试。

此外，默认导出会促使人们将所有内容放入一个庞大的
对象中以统一命名：

<div class='badcode'></div>

```ts
export default class Foo {
  static SOME_CONSTANT = ...
  static someHelpfulFunction() { ... }
  ...
}
```

采用上述模式，我们拥有了文件作用域，可将其用作命名空间。我们
还拥有一个或许多余的二级作用域（类 `Foo`），它可以在
其他文件中被模糊地同时用作类型和值。

相反，优先使用文件作用域进行命名，以及使用具名导出：

<div class='goodcode'></div>

```ts
export const SOME_CONSTANT = ...
export function someHelpfulFunction()
export class Foo {
  // only class stuff here
}
```

<div class="numbered"></div>

<a id="export-visibility"></a>

#### 导出可见性

TypeScript 不支持限制导出标识符的可见性。
只导出在模块之外使用的标识符。通常应尽量缩减
模块的导出 API 表面积。

<div class="numbered"></div>

<a id="mutable-exports"></a>

#### 可变导出

无论技术层面是否支持，可变导出都可能产生难以理解和
调试的代码，尤其是在跨多个模块重新导出时。对此风格点
的一种转述是：不允许 `export let`。

<div class='badcode'></div>

```ts
export let foo = 3;
// In pure ES6, foo is mutable and importers will observe the value change after a second.
// In TS, if foo is re-exported by a second file, importers will not see the value change.
window.setTimeout(() => {
  foo = 4;
}, 1000 /* ms */);
```

如果需要在外部可访问且可变的绑定，应*该*
改用显式的 getter 函数。

<div class='goodcode'></div>

```ts
let foo = 3;
window.setTimeout(() => {
  foo = 4;
}, 1000 /* ms */);
// Use an explicit getter to access the mutable export.
export function getFoo() { return foo; };
```

对于有条件地导出两个值中任意一个的常见模式，请先
进行条件检查，然后再导出。确保所有导出在模块的
主体执行完毕后均为最终值。

<div class='goodcode'></div>

```ts
function pickApi() {
  if (useOtherApi()) return OtherApi;
  return RegularApi;
}
export const SomeApi = pickApi();
```

<a id="static-containers"></a>

<div class="numbered"></div>

<a id="container-classes"></a>

#### 容器类

不要为了命名而创建带有静态方法或属性的容器类，
仅出于命名的目的。

<div class='badcode'></div>

```ts
export class Container {
  static FOO = 1;
  static bar() { return 1; }
}
```

相反，导出单独的常量和函数：

<div class='goodcode'></div>

```ts
export const FOO = 1;
export function bar() { return 1; }
```

<div class="numbered"></div>

<a id="import-export-type"></a>

### 导入与导出类型

<div class="numbered"></div>

<a id="import-type"></a>

#### 导入类型

当导入的标识符仅用作类型时，可以使用 `import type {...}`。
对于值，请使用常规导入：

<div class='goodcode'></div>

```ts
import type {Foo} from './foo';
import {Bar} from './foo';

import {type Foo, Bar} from './foo';
```

为什么？

TypeScript 编译器会自动处理这种区分，并且不会为类型引用
插入运行时加载。那么为何要标注类型导入呢？

TypeScript 编译器可以运行于两种模式：

-   在开发模式下，我们通常希望快速迭代循环。编译器
    在没有完整类型信息的情况下转译为 JavaScript。这会快得多，
    但在某些情况下需要 `import type`。
-   在生产模式下，我们需要正确性。编译器会对所有内容
    进行类型检查，并确保 `import type` 被正确运用。

注意：如果需要强制进行运行时加载以获得副作用，请使用 `import '...';`。
参见 [导入语句](#imports)。

<div class="numbered"></div>

<a id="export-type"></a>

#### 导出类型

重新导出类型时，请使用 `export type`，例如：

<div class='goodcode'></div>

```ts
export type {AnInterface} from './foo';
```

为什么？

`export type` 有助于在逐文件转译中实现类型的重新导出。
参见
[`isolatedModules` docs](https://www.typescriptlang.org/tsconfig#exports-of-non-value-identifiers)。

`export type` 似乎也可用于避免为某个 API 导出值标识符。
但它同样不能提供保证：下游代码仍可能通过
不同的路径导入某个 API。更好地拆分并保证 API 的类型
与值用法的做法，是实际上将标识符拆分为例如
`UserService` 和 `AjaxUserService`。这样更不易出错，也能更好地
表达意图。

<div class="numbered"></div>

<a id="dynamic-import-type"></a>

#### 动态 `import()` 类型

不要在类型注解中使用 `import()` 函数。

<div class='badcode'></div>

```ts
let f: import('./foo').Foo;
```

如果需要确保导入始终从生成的 JavaScript 中省略，
请改用 `import type`。

<div class='goodcode'></div>

```ts
import type {Foo} from './foo';
```

<a id="namespaces-vs-modules"></a>

<div class="numbered"></div>

<a id="use-modules-not-namespaces"></a>

#### 使用模块而非命名空间

TypeScript 支持两种组织代码的方法：*命名空间*和*模块*，
但命名空间是被禁止的。也就是说，你的代码*必须*通过
`import {foo} from 'bar';` 形式的导入和导出引用其他文件中的代码

你的代码*不得*使用 `namespace Foo { ... }` 结构。`namespace`
仅在与外部第三方代码对接时才*可以*使用。要对代码进行语义
命名，请使用单独的文件。

代码*不得*使用 `require`（即 `import x = require('...');`）进行导入。
请使用 ES6 模块语法。

<div class='badcode'></div>

```ts
// Bad: do not use namespaces:
namespace Rocket {
  function launch() { ... }
}

// Bad: do not use <reference>
/// <reference path="..."/>

// Bad: do not use require()
import x = require('mydep');
```

> NB: TypeScript `namespace`s used to be called internal modules and used to use
> the `module` keyword in the form `module Foo { ... }`. Don't use that either.
> Always use ES6 imports.

<a id="language-rules"></a>

<div class="numbered"></div>

<a id="language-features"></a>

## 语言特性

本节界定了哪些特性可以使用或不得使用，以及对其使用的
任何附加约束。

本风格指南未讨论的语言特性*可以*使用，不作任何
使用建议。

<a id="features-local-variable-declarations"></a>

<div class="numbered"></div>

<a id="local-variable-declarations"></a>

### 局部变量声明

<a id="variables"></a>
<a id="features-use-const-and-let"></a>

<div class="numbered"></div>

<a id="use-const-and-let"></a>

#### 使用 const 和 let

始终使用 `const` 或 `let` 声明变量。默认使用 `const`，除非
变量需要被重新赋值。绝不使用 `var`。

<div class='goodcode'></div>

```ts
const foo = otherValue;  // Use if "foo" never changes.
let bar = someValue;     // Use if "bar" is ever assigned into later on.
```

`const` 和 `let` 是块级作用域的，如同大多数其他语言中的变量。
JavaScript 中的 `var` 是函数作用域的，这可能导致难以理解的
缺陷。不要使用它。

<div class='badcode'></div>

```ts
var foo = someValue;     // Don't use - var scoping is complex and causes bugs.
```

变量*不得*在其声明之前使用。

<a id="features-one-variable-per-declaration"></a>

<div class="numbered"></div>

<a id="one-variable-per-declaration"></a>

#### 每个声明一个变量

每个局部变量声明只声明一个变量：诸如
<code class="badcode">let a = 1, b = 2;</code> 这样的声明不被使用。

<a id="features-array-literals"></a>

<div class="numbered"></div>

<a id="array-literals"></a>

### 数组字面量

<a id="features-arrays-ctor"></a>

<div class="numbered"></div>

<a id="array-constructor"></a>

#### 不要使用 `Array` 构造函数

*不要*使用 `Array()` 构造函数，无论是否带 `new`。它的用法
令人困惑且自相矛盾：

<!--
Silencing a CommonTypos warning for incorrect array constructor usage.
common_typos_disable
-->

<div class='badcode'></div>

```ts
const a = new Array(2); // [undefined, undefined]
const b = new Array(2, 3); // [2, 3];
```

<!-- common_typos_enable -->

相反，始终使用方括号表示法来初始化数组，或使用 `from` 以
特定大小初始化一个 `Array`：

<div class='goodcode'></div>

```ts
const a = [2];
const b = [2, 3];

// Equivalent to Array(2):
const c = [];
c.length = 2;

// [0, 0, 0, 0, 0]
Array.from<number>({length: 5}).fill(0);
```

<a id="features-arrays-non-numeric-properties"></a>

<div class="numbered"></div>

<a id="do-not-define-properties-on-arrays"></a>

#### 不要在数组上定义属性

不要在数组上定义或使用非数字属性（`length` 除外）。
请改用 `Map`（或 `Object`）。

<a id="features-arrays-destructuring"></a>

<div class="numbered"></div>

<a id="array-destructuring"></a>

#### 数组解构

数组字面量可用于赋值左侧以执行解构（例如在从单个数组或
可迭代对象中解包多个值时）。可以包含一个末尾“剩余”元素
（`...` 与变量名之间无空格）。未使用的元素应
予以省略。

<div class='goodcode'></div>

```ts
const [a, b, c, ...rest] = generateResults();
let [, b,, d] = someArray;
```

解构也可用于函数参数。始终将 `[]` 指定为
默认值，如果解构的数组参数是可选的，并在左侧
提供默认值：

<div class='goodcode'></div>

```ts
function destructured([a = 4, b = 2] = []) { … }
```

不允许：

<div class='badcode'></div>

```ts
function badDestructuring([a, b] = [4, 2]) { … }
```

提示：对于将多个值（解）打包进函数的参数或返回值，在可能时
优先使用对象解构而非数组解构，因为它允许为各个元素命名
并为每个元素指定不同的类型。

<a id="features-object-literals"></a>

<div class="numbered"></div>

<a id="object-literals"></a>

### 对象字面量

<a id="features-objects-ctor"></a>

<div class="numbered"></div>

<a id="object-constructor"></a>

#### 不要使用 `Object` 构造函数

`Object` 构造函数是被禁止的。请改用对象字面量
（`{}` 或 `{a: 0, b: 1, c: 2}`）。

<div class="numbered"></div>

<a id="iterating-objects"></a>

#### 遍历对象

使用 `for (... in ...)` 遍历对象容易出错。它会包含
原型链上可枚举的属性。

不要使用未经过滤的 `for (... in ...)` 语句：

<div class='badcode'></div>

```ts
for (const x in someObj) {
  // x could come from some parent prototype!
}
```

要么用 `if` 语句显式过滤，要么使用
`for (... of Object.keys(...))`。

<div class='goodcode'></div>

```ts
for (const x in someObj) {
  if (!someObj.hasOwnProperty(x)) continue;
  // now x was definitely defined on someObj
}
for (const x of Object.keys(someObj)) { // note: for _of_!
  // now x was definitely defined on someObj
}
for (const [key, value] of Object.entries(someObj)) { // note: for _of_!
  // now key was definitely defined on someObj
}
```

<a id="using-the-spread-operator"></a>

<div class="numbered"></div>

<a id="object-spread-syntax"></a>

#### 使用展开语法

使用展开语法 `{...bar}` 是创建对象浅拷贝的便捷简写
方式。在对象初始化中使用展开语法时，后面的
值会在相同的键处替换先前的值。

<div class='goodcode'></div>

```ts
const foo = {
  num: 1,
};

const foo2 = {
  ...foo,
  num: 5,
};

const foo3 = {
  num: 5,
  ...foo,
}

foo2.num === 5;
foo3.num === 1;
```

避免展开那些原型不同于 Object 原型的
对象（例如类定义、类实例、函数），因为其
行为不直观（只有可枚举的非原型属性会被浅拷贝）。

<div class='badcode'></div>

```ts
// Creates {0: 'a', 1: 'b', 2: 'c'} but has no length
const fooStrings = ['a', 'b', 'c'];
const ids = {...fooStrings};
```

<div class='goodcode'></div>

```ts
const options = {foo: 1, bar: 2};
const extended = {...options, baz: 3};
```

<a id="features-objects-computed-property-names"></a>

<div class="numbered"></div>

<a id="computed-property-names"></a>

#### 计算属性名

计算属性名（例如 `{['key' + foo()]: 42}`）是允许的，且
被视为字典风格（带引号）的键（即不得与
非引号键混用），除非计算属性是一个
[symbol](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol)
（例如 `[Symbol.iterator]`）。

<a id="features-objects-destructuring"></a>

<div class="numbered"></div>

<a id="object-destructuring"></a>

#### 对象解构

对象解构模式可用于赋值的左侧，以执行解构
并从单个对象中解包多个值。

解构后的对象也可用作函数参数，但应尽量保持
简单：仅一层不带引号的简写属性。更深的
嵌套层级和计算属性不得在参数解构中使用。请在解构
参数的左侧指定所有默认值（
`{str = 'some default'} = {}`，而非
<code class="badcode">{str} = {str: 'some default'}</code>），且如果
解构对象本身是可选项，它必须默认为 `{}`。

示例：

<div class='goodcode'></div>

```ts
interface Options {
  /** The number of times to do something. */
  num?: number;

  /** A string to do stuff to. */
  str?: string;
}

function destructured({num, str = 'default'}: Options = {}) {}
```

不允许：

<div class='badcode'></div>

```ts
function nestedTooDeeply({x: {num, str}}: {x: Options}) {}
function nontrivialDefault({num, str}: Options = {num: 42, str: 'default'}) {}
```

<a id="formatting-class-literals"></a>
<a id="features-classes"></a>

<div class="numbered"></div>

<a id="classes"></a>

### 类

<div class="numbered"></div>

<a id="class-declarations"></a>

#### 类声明

类声明*不得*以分号结尾：

<div class='goodcode'></div>

```ts
class Foo {
}
```

<div class='badcode'></div>

```ts
class Foo {
}; // Unnecessary semicolon
```

相比之下，含有类表达式的语句*必须*以
分号结尾：

<div class='goodcode'></div>

```ts
export const Baz = class extends Bar {
  method(): number {
    return this.x;
  }
}; // Semicolon here as this is a statement, not a declaration
```

<div class='badcode'></div>

```ts
exports const Baz = class extends Bar {
  method(): number {
    return this.x;
  }
}
```

类声明的花括号与其他类内容之间是否留有空行，
既不鼓励也不反对：

<div class='goodcode'></div>

```ts
// No spaces around braces - fine.
class Baz {
  method(): number {
    return this.x;
  }
}

// A single space around both braces - also fine.
class Foo {

  method(): number {
    return this.x;
  }

}
```

<div class="numbered"></div>

<a id="no-ctor-only-members"></a>

#### 不要创建仅在构造函数中使用的成员变量

如果一个变量只在构造函数中使用，那么可以把它迁移为
作用域限于构造函数体的变量，这会让你的类更
无状态，也便于未来的开发者理解。

有些类的方法只在构造函数中调用，并且
更新仅在类构造期间使用的部分类状态。出于
与上述相同的原因，这些部分类状态也应迁移为
构造函数内的局部变量。

<div class='badcode'></div>

```ts
class MyClass {
  // BAD: onlyUsedInCtor is only used in the constructor and nowhere else after
  // class initialization.
  private readonly onlyUsedInCtor = ...;
  private readonly otherDataStructure = ...;
  constructor(
    // BAD: Services only used in the constructor but kept after ctor execution.
    private readonly serviceA: ServiceA,
    private readonly serviceB: ServiceB,
    private readonly serviceC: ServiceC,
  ) {
    this.computeThing(
      this.serviceA.getA(), this.serviceB.getB(), this.serviceC.getC(),
    );
    this.otherDataStructure = computeOther(this.onlyUsedInCtor);
  }

  private computeThing(a: A, b: B, c: C) {
    this.onlyUsedInCtor = someFunctionOf(a, b, c);
  }
}
```

<div class='goodcode'></div>

```ts
class MyClass {
  private readonly otherDataStructure = ...;
  constructor(
    // GOOD: Services only used in constructor and dropped after ctor finishes.
    serviceA: ServiceA,
    serviceB: ServiceB,
    serviceC: ServiceC,
  ) {
    // GOOD: onlyUsedInCtor is a constructor-local variable.
    const onlyUsedInCtor =
      someFunctionOf(serviceA.getA(), serviceB.getB(), serviceC.getC());
    this.otherDataStructure = computeOther(onlyUsedInCtor);
  }
}
```

<div class="numbered"></div>

<a id="class-method-declarations"></a>

#### 类方法声明

类方法声明*不得*使用分号来分隔各个
方法声明：

<div class='goodcode'></div>

```ts
class Foo {
  doThing() {
    console.log("A");
  }
}
```

<div class='badcode'></div>

```ts
class Foo {
  doThing() {
    console.log("A");
  }; // <-- unnecessary
}
```

方法声明与前后代码之间应
用一个空行分隔：

<div class='goodcode'></div>

```ts
class Foo {
  doThing() {
    console.log("A");
  }

  getOtherThing(): number {
    return 4;
  }
}
```

<div class='badcode'></div>

```ts
class Foo {
  doThing() {
    console.log("A");
  }
  getOtherThing(): number {
    return 4;
  }
}
```

<a id="features-classes-overriding-tostring"></a>

<div class="numbered"></div>

<a id="overriding-tostring"></a>

##### 覆写 toString

可以覆写 `toString` 方法，但它必须始终成功，且绝不产生
可见的副作用。

提示：尤其要当心在 toString 中调用其他方法，因为
异常情况可能导致无限循环。

<a id="features-classes-static-methods"></a>

<div class="numbered"></div>

<a id="static-methods"></a>

#### 静态方法

<div class="numbered"></div>

<a id="avoid-private-static-methods"></a>

##### 避免使用私有静态方法

在不影响可读性的前提下，优先使用模块内的局部函数，而不是
私有静态方法。

<div class="numbered"></div>

<a id="avoid-static-method-dynamic-dispatch"></a>

##### 不要依赖动态分发

代码*不应*依赖静态方法的动态分发。静态方法
*应*只在基类本身（即直接定义该方法的类）上调用。
静态方法*不应*在含有动态实例的变量上调用，该实例
可能是构造函数或子类构造函数（若这样做，则*必须*
用 `@nocollapse` 定义），并且*不得*在未自行定义该方法的
子类上直接调用。

不允许：

<div class='badcode'></div>

```ts
// Context for the examples below (this class is okay by itself)
class Base {
  /** @nocollapse */ static foo() {}
}
class Sub extends Base {}

// Discouraged: don't call static methods dynamically
function callFoo(cls: typeof Base) {
  cls.foo();
}

// Disallowed: don't call static methods on subclasses that don't define it themselves
Sub.foo();

// Disallowed: don't access this in static methods.
class MyClass {
  static foo() {
    return this.staticField;
  }
}
MyClass.staticField = 1;
```

<div class="numbered"></div>

<a id="static-this"></a>

##### 避免使用静态 `this` 引用

代码*不得*在静态上下文中使用 `this`。

JavaScript 允许通过 `this` 访问静态字段。与其他
语言不同，静态字段也会被继承。

<div class='badcode'></div>

```ts
class ShoeStore {
  static storage: Storage = ...;

  static isAvailable(s: Shoe) {
    // Bad: do not use `this` in a static method.
    return this.storage.has(s.id);
  }
}

class EmptyShoeStore extends ShoeStore {
  static storage: Storage = EMPTY_STORE;  // overrides storage from ShoeStore
}
```

为什么？

这类代码通常令人意外：编写者可能没想到静态字段
可以通过 this 指针访问，也可能惊讶地发现它们
可以被覆写——这一特性并不常用。

这类代码还会助长一种反模式，即持有大量静态状态，
从而引发可测试性方面的问题。

<a id="disallowed-features-omitting-parents-with-new"></a>
<a id="features-classes-constructors"></a>

<div class="numbered"></div>

<a id="constructors"></a>

#### 构造函数

调用构造函数*必须*使用括号，即使不传入任何实参：

<div class='badcode'></div>

```ts
const x = new Foo;
```

<div class='goodcode'></div>

```ts
const x = new Foo();
```

省略括号可能导致难以察觉的错误。下面两行并
不等价：

<div class='goodcode'></div>

```js
new Foo().Bar();
new Foo.Bar();
```

没有必要提供空的构造函数，或只是简单委托给
父类的构造函数，因为如果未指定构造函数，ES2015 会提供
默认的类构造函数。但是，带有参数属性、可见性
修饰符或参数装饰器的构造函数，即使其函数体为空，
也*不应*省略。

<div class='badcode'></div>

```ts
class UnnecessaryConstructor {
  constructor() {}
}
```

<div class='badcode'></div>

```ts
class UnnecessaryConstructorOverride extends Base {
    constructor(value: number) {
      super(value);
    }
}
```

<div class='goodcode'></div>

```ts
class DefaultConstructor {
}

class ParameterProperties {
  constructor(private myService) {}
}

class ParameterDecorators {
  constructor(@SideEffectDecorator myService) {}
}

class NoInstantiation {
  private constructor() {}
}
```

构造函数与其上下相邻的代码之间都应用
一个空行分隔：

<div class='goodcode'></div>

```ts
class Foo {
  myField = 10;

  constructor(private readonly ctorParam) {}

  doThing() {
    console.log(ctorParam.getThing() + myField);
  }
}
```

<div class='badcode'></div>

```ts
class Foo {
  myField = 10;
  constructor(private readonly ctorParam) {}
  doThing() {
    console.log(ctorParam.getThing() + myField);
  }
}
```

<div class="numbered"></div>

<a id="class-members"></a>

#### 类成员

<div class="numbered"></div>

<a id="private-fields"></a>

##### 不使用 #private 字段

不要使用私有字段（也称为私有标识符）：

<div class='badcode'></div>

```ts
class Clazz {
  #ident = 1;
}
```

应改用 TypeScript 的可见性注解：

<div class='goodcode'></div>

```ts
class Clazz {
  private ident = 1;
}
```

为什么？

私有标识符在被 TypeScript 降级编译时会导致输出体积和性能
明显劣化，并且在 ES2015 之前不受支持。它们只能
降级到 ES2015，不能更低。同时，在使用静态类型检查
来强制可见性时，它们并不会带来明显的好处。

<div class="numbered"></div>

<a id="use-readonly"></a>

##### 使用 readonly

对于在构造函数之外从不被重新赋值的属性，应使用
`readonly` 修饰符标记（这些属性不必是深层不可变的）。

<div class="numbered"></div>

<a id="parameter-properties"></a>

##### 参数属性

与其把一个显而易见的初始值一路传递到类成员，不如使用
TypeScript 的
[参数属性](https://www.typescriptlang.org/docs/handbook/2/classes.html#parameter-properties)。

<div class='badcode'></div>

```ts
class Foo {
  private readonly barService: BarService;

  constructor(barService: BarService) {
    this.barService = barService;
  }
}
```

<div class='goodcode'></div>

```ts
class Foo {
  constructor(private readonly barService: BarService) {}
}
```

如果参数属性需要文档说明，
[请使用 `@param` JSDoc 标签](#parameter-property-comments)。

<div class="numbered"></div>

<a id="field-initializers"></a>

##### 字段初始化器

如果初始化某个类成员并不依赖构造函数参数或
参数属性，就在声明处初始化。这样有时可以
完全省去构造函数。

<div class='badcode'></div>

```ts
class Foo {
  private readonly userList: string[];

  constructor() {
    this.userList = [];
  }
}
```

<div class='goodcode'></div>

```ts
class Foo {
  private readonly userList: string[] = [];
}
```

由于 TypeScript 把这一模式转译为 JavaScript 的方式，
在字段初始化器中引用参数属性是可行的。这种转译
正在改变，以符合 JavaScript 的语言语义，届时在字段
初始化器中引用参数属性将成为 TypeScript 编译错误，
因此应避免使用这一模式。

<div class='badcode'></div>

```ts
class Foo {
  // BAD: references a property (`this.state`) that will be
  // initialized after this field.
  private readonly userList = initializeUserList(this.state);

  constructor(private readonly state: InitialState) {}
}
```

<div class='goodcode'></div>

```ts
class Foo {
  // GOOD: this must be initialized in the constructor
  private readonly userList: string[];

  // This might allow converting the parameter property into a normal
  // constructor parameter.
  constructor(state: InitialState) {
    this.userList = initializeUserList(state);
  }
}
```

提示：构造函数执行完毕后，切勿在实例上添加或删除属性，
因为这会严重妨碍 VM 对类的“形状”进行优化。对于可能稍后
才填充的可选字段，应显式初始化为 `undefined`，
以防止之后发生形状变化。

<div class="numbered"></div>

<a id="properties-used-outside-of-class-lexical-scope"></a>

##### 在类的词法作用域之外使用的属性

在其所属类的词法作用域之外被使用的属性，*不得*
使用 `private` 可见性，因为它们是在其所属类的
词法作用域之外被使用的。

例外：仅在模板中使用的 Angular 组件属性允许
使用 `private` 可见性。

根据所讨论属性的情况，酌情使用 `protected` 或 `public`。

TypeScript 代码*不得*使用 `obj['foo']` 来绕过属性的
可见性。

为什么？

当某个属性为 `private` 时，你就是在向自动化系统和
人类同时声明：对该属性的访问被限定在声明它的
类的方法之内，而它们会依赖这一点。例如，未使用代码
检查会把看似未被使用的私有属性标记出来，即使其他某个文件
设法绕过了可见性限制。

尽管看起来 `obj['foo']` 似乎能在 TypeScript 编译器中
绕过可见性，但调整构建规则就可能破坏这一模式，而且它还
违反了[优化兼容性](#optimization-compatibility)。

<a id="features-classes-getters-and-setters"></a>

<div class="numbered"></div>

<a id="classes-getters-and-setters"></a>

##### getter 和 setter

类成员的 getter 和 setter（也称为访问器）*可以*使用。
getter 方法*必须*是
[纯函数](https://en.wikipedia.org/wiki/Pure_function)（即结果
一致且无副作用：getter *不得*改变可观察状态）。
它们还可用来限制内部实现细节或冗长实现细节的
可见性（见下文）。

<div class='goodcode'></div>

```ts
class Foo {
  constructor(private readonly someService: SomeService) {}

  get someMember(): string {
    return this.someService.someVariable;
  }

  set someMember(newValue: string) {
    this.someService.someVariable = newValue;
  }
}
```

<div class='badcode'></div>

```ts
class Foo {
  nextId = 0;
  get next() {
    return this.nextId++; // Bad: getter changes observable state
  }
}
```

如果使用访问器来隐藏某个类属性，被隐藏的属性*可以*
加上任意完整单词作为前缀或后缀，例如 `internal` 或 `wrapped`。
使用这些私有属性时，应尽可能通过访问器访问其值。
一个属性的访问器中至少有一个*必须*不是空实现：不要
仅仅为了隐藏属性而定义“透传”访问器。
相反，应把该属性设为 public（或考虑把它设为 `readonly`，
而不是只定义一个没有 setter 的 getter）。

<div class='goodcode'></div>

```ts
class Foo {
  private wrappedBar = '';
  get bar() {
    return this.wrappedBar || 'bar';
  }

  set bar(wrapped: string) {
    this.wrappedBar = wrapped.trim();
  }
}
```

<div class='badcode'></div>

```ts
class Bar {
  private barInternal = '';
  // Neither of these accessors have logic, so just make bar public.
  get bar() {
    return this.barInternal;
  }

  set bar(value: string) {
    this.barInternal = value;
  }
}
```

*不得*使用 `Object.defineProperty` 定义 getter 和 setter，
因为这会妨碍属性重命名。

<a id="features-classes-computed-properties"></a>

<div class="numbered"></div>

<a id="class-computed-properties"></a>

##### 计算属性

只有当属性是 symbol 时，才可以在类中使用计算属性。
不允许使用字典风格的属性（即带引号的键或计算得到的
非 symbol 键）（参见
[不混用键类型的理由](#features-objects-mixing-keys)）。对于任何在逻辑上
可迭代的类，都应定义 `[Symbol.iterator]` 方法。除此之外，
应谨慎使用 `Symbol`。

提示：慎用其他任何内置 symbol（例如
`Symbol.isConcatSpreadable`），因为编译器不会为它们提供 polyfill，
因而在较旧的浏览器中无法工作。

<div class="numbered"></div>

<a id="visibility"></a>

#### 可见性

限制属性、方法乃至整个类型的可见性，有助于
保持代码解耦。

*   尽可能限制 symbol 的可见性。
*   考虑把私有方法改为同一文件中、任何类之外的
    非导出函数，并把私有属性移到一个单独的、
    非导出的类中。
*   TypeScript 的 symbol 默认是 public。切勿使用 `public` 修饰符，
    除非是在声明非 readonly 的 public 参数属性时（在
    构造函数中）。

<div class='badcode'></div>

```ts
class Foo {
  public bar = new Bar();  // BAD: public modifier not needed

  constructor(public readonly baz: Baz) {}  // BAD: readonly implies it's a property which defaults to public
}
```

<div class='goodcode'></div>

```ts
class Foo {
  bar = new Bar();  // GOOD: public modifier not needed

  constructor(public baz: Baz) {}  // public modifier allowed
}
```

另见[导出可见性](#export-visibility)。

<div class="numbered"></div>

<a id="disallowed-class-patterns"></a>

#### 禁止的类模式

<a id="features-classes-prototypes"></a>

<div class="numbered"></div>

<a id="class-prototypes"></a>

##### 不要直接操作 `prototype`

`class` 关键字比定义 `prototype` 属性能带来更清晰、
更易读的类定义。普通实现代码不应
操作这些对象。明确禁止使用 mixin，也禁止修改内置
对象的 prototype。

**例外**：框架代码（例如 Polymer 或 Angular）可能需要使用
`prototype`，不应为了回避它而采用更糟糕的变通做法。

<a id="features-functions"></a>

<div class="numbered"></div>

<a id="functions"></a>

### 函数

<div class="numbered"></div>

<a id="terminology"></a>

#### 术语

函数有许多不同的种类，彼此之间有细微差别。
本指南采用以下术语，与
[MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions) 保持一致：

*   “函数声明”：使用 `function` 关键字的声明（即并非
    表达式）
*   “函数表达式”：使用 `function` 关键字的表达式，通常
    用于赋值或作为参数传递
*   “箭头函数”：使用 `=>` 语法的表达式
*   “块体”：带花括号的箭头函数右侧部分
*   “简洁体”：不带花括号的箭头函数右侧部分

本节不涉及方法与类/构造函数。

<div class="numbered"></div>

<a id="function-declarations"></a>

#### 具名函数优先使用函数声明

定义具名函数时，函数声明优先于箭头函数或
函数表达式。

<div class='goodcode'></div>

```ts
function foo() {
  return 42;
}
```

<div class='badcode'></div>

```ts
const foo = () => 42;
```

例如，在需要显式类型注解时，*可以*使用
箭头函数。

<div class='goodcode'></div>

```ts
interface SearchFunction {
  (source: string, subString: string): boolean;
}

const fooSearch: SearchFunction = (source, subString) => { ... };
```

<a id="features-functions-nested-functions"></a>

<div class="numbered"></div>

<a id="nested-functions"></a>

#### 嵌套函数

嵌套在其他方法或函数中的函数，*可以*酌情使用函数
声明或箭头函数。尤其是在方法体中，
优先使用箭头函数，因为它们能访问外层的 `this`。

<a id="use-arrow-functions-in-expressions"></a>

<div class="numbered"></div>

<a id="function-expressions"></a>

#### 不要使用函数表达式

不要使用函数表达式，应改用箭头函数。

<div class='goodcode'></div>

```ts
bar(() => { this.doSomething(); })
```

<div class='badcode'></div>

```ts
bar(function() { ... })
```

**例外：** 函数表达式*仅当*代码必须动态重新绑定 `this` 时（但这种做法
[不被鼓励](#rebinding-this)），或者用于生成器函数（它们没有箭头语法）时，
*才*可以使用。

<a id="features-functions-arrow-functions"></a>
<a id="expression-bodies-vs-block-bodies"></a>

<div class="numbered"></div>

<a id="arrow-function-bodies"></a>

#### 箭头函数体

酌情使用带简洁体（即表达式）或块体的
箭头函数。

<div class='goodcode'></div>

```ts
// Top level functions use function declarations.
function someFunction() {
  // Block bodies are fine:
  const receipts = books.map((b: Book) => {
    const receipt = payMoney(b.price);
    recordTransaction(receipt);
    return receipt;
  });

  // Concise bodies are fine, too, if the return value is used:
  const longThings =
      myValues.filter((v) => v.length > 1000).map((v) => String(v));

  function payMoney(amount: number) {
    // function declarations are fine, but must not access `this`.
  }

  // Nested arrow functions may be assigned to a const.
  const computeTax = (amount: number) => amount * 0.12;
}
```

只有当函数的返回值确实被使用时，才使用简洁体。
此时块体可确保返回类型为 `void`，并防止潜在的
副作用。

<div class='badcode'></div>

```ts
// BAD: use a block body if the return value of the function is not used.
myPromise.then((v) => console.log(v));
// BAD: this typechecks, but the return value still leaks.
let f: () => void;
f = () => 1;
```

<div class='goodcode'></div>

```ts
// GOOD: return value is unused, use a block body.
myPromise.then((v) => {
  console.log(v);
});
// GOOD: code may use blocks for readability.
const transformed = [1, 2, 3].map((v) => {
  const intermediate = someComplicatedExpr(v);
  const more = acrossManyLines(intermediate);
  return worthWrapping(more);
});
// GOOD: explicit `void` ensures no leaked return value
myPromise.then((v) => void console.log(v));
```

提示：当结果不被使用时，可以用 `void` 运算符确保
带表达式体的箭头函数返回 `undefined`。

<div class="numbered"></div>

<a id="rebinding-this"></a>

#### 重新绑定 `this`

函数表达式和函数声明*不得*使用 `this`，除非它们
专门为了重新绑定 `this` 指针而存在。多数情况下，
使用箭头函数或显式参数即可避免重新绑定 `this`。

<div class='badcode'></div>

```ts
function clickHandler() {
  // Bad: what's `this` in this context?
  this.textContent = 'Hello';
}
// Bad: the `this` pointer reference is implicitly set to document.body.
document.body.onclick = clickHandler;
```

<div class='goodcode'></div>

```ts
// Good: explicitly reference the object from an arrow function.
document.body.onclick = () => { document.body.textContent = 'hello'; };
// Alternatively: take an explicit parameter
const setTextFn = (e: HTMLElement) => { e.textContent = 'hello'; };
document.body.onclick = setTextFn.bind(null, document.body);
```

优先使用箭头函数，而非其他绑定 `this` 的方式，例如
`f.bind(this)`、`goog.bind(f, this)` 或 `const self = this`。

<div class="numbered"></div>

<a id="functions-as-callbacks"></a>

#### 优先传递箭头函数作为回调

回调可能被调用时传入意料之外的实参，这些实参虽然能
通过类型检查，却仍会导致逻辑错误。

避免把具名回调传给高阶函数，除非你确信
两个函数的调用签名都稳定不变。尤其要当心
较少使用的可选参数。

<div class='badcode'></div>

```ts
// BAD: Arguments are not explicitly passed, leading to unintended behavior
// when the optional `decimals` argument gets the array indices 0, 1, and 2.
const strs = [1.23, 4.56, 7.89].map(googFormat.numericValueToString);
// > ['1', '4.6', '7.89'];
```

应改为优先传递一个把参数显式转发给具名回调的
箭头函数。

<div class='goodcode'></div>

```ts
// GOOD: Arguments are explicitly passed to the callback
const strs = [1.23, 4.56, 7.89].map((n) => googFormat.numericValueToString(n));
// > ['1.23', '4.56', '7.89']

// GOOD: Function is locally defined and is designed to be used as a callback
function dayFilter(element: string|null|undefined) {
  return element != null && element.endsWith('day');
}

const days = ['tuesday', undefined, 'juice', 'wednesday'].filter(dayFilter);
```

<div class="numbered"></div>

<a id="arrow-functions-as-properties"></a>

#### 作为属性的箭头函数

类通常*不应*包含初始化为箭头函数的属性。
箭头函数属性要求调用函数明白被调用方的 `this`
已经绑定，这加剧了对 `this` 究竟是什么的困惑，而且
使用这类处理器的调用点和引用看起来像是坏的（即需要
非局部的知识才能确定它们是正确的）。代码*应*始终
使用箭头函数来调用实例方法
（`const handler = (x) => { this.listener(x); };`），并且*不应*获取或
传递实例方法的引用
（~~`const handler = this.listener; handler(x);`~~）。

> 注意：在某些特定情形下，例如在模板中绑定函数时，
> 作为属性的箭头函数很有用，能写出可读性好得多的代码。
> 运用这条规则时请自行判断。另请参阅下文的
> [`Event Handlers`](#event-handlers) 一节。

<div class='badcode'></div>

```ts
class DelayHandler {
  constructor() {
    // Problem: `this` is not preserved in the callback. `this` in the callback
    // will not be an instance of DelayHandler.
    setTimeout(this.patienceTracker, 5000);
  }
  private patienceTracker() {
    this.waitedPatiently = true;
  }
}
```

<div class='badcode'></div>

```ts
// Arrow functions usually should not be properties.
class DelayHandler {
  constructor() {
    // Bad: this code looks like it forgot to bind `this`.
    setTimeout(this.patienceTracker, 5000);
  }
  private patienceTracker = () => {
    this.waitedPatiently = true;
  }
}
```

<div class='goodcode'></div>

```ts
// Explicitly manage `this` at call time.
class DelayHandler {
  constructor() {
    // Use anonymous functions if possible.
    setTimeout(() => {
      this.patienceTracker();
    }, 5000);
  }
  private patienceTracker() {
    this.waitedPatiently = true;
  }
}
```

<div class="numbered"></div>

<a id="event-handlers"></a>

#### 事件处理器

当无需卸载处理器时（例如事件由类自身发出），
事件处理器*可以*使用箭头函数。如果需要
卸载处理器，那么作为属性的箭头函数才是恰当的
做法，因为它们会自动捕获 `this`，并提供一个
稳定的引用以便卸载。

<div class='goodcode'></div>

```ts
// Event handlers may be anonymous functions or arrow function properties.
class Component {
  onAttached() {
    // The event is emitted by this class, no need to uninstall.
    this.addEventListener('click', () => {
      this.listener();
    });
    // this.listener is a stable reference, we can uninstall it later.
    window.addEventListener('onbeforeunload', this.listener);
  }
  onDetached() {
    // The event is emitted by window. If we don't uninstall, this.listener will
    // keep a reference to `this` because it's bound, causing a memory leak.
    window.removeEventListener('onbeforeunload', this.listener);
  }
  // An arrow function stored in a property is bound to `this` automatically.
  private listener = () => {
    confirm('Do you want to exit the page?');
  }
}
```

不要在安装事件处理器的表达式中使用 `bind`，因为它会
创建一个无法卸载的临时引用。

<div class='badcode'></div>

```ts
// Binding listeners creates a temporary reference that prevents uninstalling.
class Component {
  onAttached() {
    // This creates a temporary reference that we won't be able to uninstall
    window.addEventListener('onbeforeunload', this.listener.bind(this));
  }
  onDetached() {
    // This bind creates a different reference, so this line does nothing.
    window.removeEventListener('onbeforeunload', this.listener.bind(this));
  }
  private listener() {
    confirm('Do you want to exit the page?');
  }
}
```

<a id="features-functions-default-parameters"></a>

<div class="numbered"></div>

<a id="parameter-initializers"></a>

#### 参数初始化器

可选的函数参数*可以*带有默认初始化器，以便在实参
省略时使用。初始化器*不得*有任何可观察的副作用。
初始化器*应*尽可能简单。

<div class='goodcode'></div>

```ts
function process(name: string, extraContext: string[] = []) {}
function activate(index = 0) {}
```

<div class='badcode'></div>

```ts
// BAD: side effect of incrementing the counter
let globalCounter = 0;
function newId(index = globalCounter++) {}

// BAD: exposes shared mutable state, which can introduce unintended coupling
// between function calls
class Foo {
  private readonly defaultPaths: string[];
  frobnicate(paths = defaultPaths) {}
}
```

谨慎使用默认参数。当可选参数数量稍多、且没有
自然顺序时，优先使用
[解构](#features-objects-destructuring) 来创建
可读性更好的 API。

<a id="features-functions-rest-parameters"></a>
<a id="features-functions-spread-operator"></a>

<div class="numbered"></div>

<a id="rest-and-spread"></a>

#### 适时优先使用 rest 与 spread

使用 *rest* 参数，而不要访问 `arguments`。切勿把局部变量
或参数命名为 `arguments`，那会令人困惑地遮蔽内置名称。

<div class='goodcode'></div>

```ts
function variadic(array: string[], ...numbers: number[]) {}
```

使用函数 spread 语法，而不要使用 `Function.prototype.apply`。

<a id="features-functions-generators"></a>

<div class="numbered"></div>

<a id="formatting-functions"></a>

#### 函数的格式

不允许在函数体的开头或结尾留空行。

*可以*在函数体内有节制地使用单个空行，以便把语句
分成*逻辑分组*。

生成器应把 `*` 紧贴 `function` 和 `yield` 关键字，例如
`function* foo()` 和 `yield* iter`，而不是 ~~`function *foo()`~~ 或
~~`yield *iter`~~。

单参数箭头函数左侧的括号是推荐写法，但并非
强制要求。

不要在 rest 或 spread 语法的 `...` 后面加空格。

<div class='goodcode'></div>

```ts
function myFunction(...elements: number[]) {}
myFunction(...array, ...iterable, ...generator());
```

<div class="numbered"></div>

<a id="function-length"></a>

#### 函数长度

编写短小、职责单一的函数和类方法。

虽然对函数和方法的长度没有硬性限制，但如果超过
约 40 行，就应考虑能否在不破坏程序结构的前提下
将其拆分。

这并非精确的科学，但下面列出一些迹象，表明你的
方法可能过于复杂：

*   它有若干层嵌套。
*   它由几个互不相连的代码块组成，每块都需要一条
    注释来解释其作用。
*   它需要在不同位置处理不同类型的异常。
*   它无法一次性完整显示在你的屏幕上。

如果发现使用这样的函数很吃力、错误难以调试，
或者你想在多个不同上下文中复用其中的一部分，
就应考虑把函数拆成更小、更易管理的片段。请注意，
只使用一次的私有辅助方法或类并没有错；它们可以成为
提高代码可读性的有用手段。

<div class="numbered"></div>

<a id="features-this"></a>

### this

只在类的构造函数和方法、以及声明了显式 `this` 类型的函数中
使用 `this`（例如 `function func(this: ThisType, ...)`），或者在允许
使用 `this` 的作用域内定义的箭头函数中使用它。

切勿用 `this` 来引用全局对象、`eval` 的上下文、
事件的目标，或不必要地经 `call()`、`apply()` 调用的函数。

<div class='badcode'></div>

```ts
this.alert('Hello');
```

<div class="numbered"></div>

<a id="primitive-literals"></a>

### 基本类型字面量

<a id="features-string-literals"></a>

<div class="numbered"></div>

<a id="string-literals"></a>

#### 字符串字面量

<a id="features-strings-use-single-quotes"></a>

<div class="numbered"></div>

<a id="use-single-quotes"></a>

##### 使用单引号

普通字符串字面量用单引号（`'`）界定，而不用
双引号（`"`）。

例外：如果字符串中包含单引号字符，可以用双引号界定，
以避免对引号进行转义。

<a id="syntax-no-line-continuations"></a>
<a id="features-strings-no-line-continuations"></a>

<div class="numbered"></div>

<a id="no-line-continuations"></a>

##### 不使用续行

不要在普通字符串字面量或模板字符串字面量中使用*续行*（即在字符串字面量
内部以反斜杠结束一行）。尽管 ES5 允许这样做，但如果反斜杠之后
出现任何尾随空白，就可能导致难以排查的错误，而且对读者来说
也不够直观。

不允许：

<div class='badcode'></div>

```ts
const LONG_STRING = 'This is a very very very very very very very long string. \
    It inadvertently contains long stretches of spaces due to how the \
    continued lines are indented.';
```

而应写成

<div class='goodcode'></div>

```ts
const LONG_STRING = 'This is a very very very very very very long string. ' +
    'It does not contain long stretches of spaces because it uses ' +
    'concatenated strings.';
const SINGLE_STRING =
    'http://it.is.also/acceptable_to_use_a_single_long_string_when_breaking_would_hinder_search_discoverability';
```

<a id="features-strings-template-strings"></a>

<div class="numbered"></div>

<a id="template-literals"></a>

##### 模板字面量

优先使用模板字面量（以 `` ` `` 界定），而非复杂的字符串
拼接，尤其是在涉及多个字符串字面量时。模板字面量
可以跨多行。

如果模板字面量跨多行，则不必遵循外围代码块的
缩进，不过如果增加的空白无关紧要，也可以遵循
该缩进。

示例：

<div class='goodcode'></div>

```ts
function arithmetic(a: number, b: number) {
  return `Here is a table of arithmetic operations:
${a} + ${b} = ${a + b}
${a} - ${b} = ${a - b}
${a} * ${b} = ${a * b}
${a} / ${b} = ${a / b}`;
}
```

<a id="features-number-literals"></a>

<div class="numbered"></div>

<a id="number-literals"></a>

#### 数字字面量

数字可以用十进制、十六进制、八进制或二进制表示。十六进制、八进制和
二进制分别严格使用 `0x`、`0o` 和 `0b` 前缀，且字母小写。
除非前导零后面紧跟 `x`、`o` 或 `b`，否则一律不要
包含前导零。

<div class="numbered"></div>

<a id="type-coercion"></a>

#### 类型转换

TypeScript 代码*可以*使用 `String()` 和 `Boolean()`（注意：不加 `new`！）
函数、字符串模板字面量或 `!!` 来转换类型。

<div class='goodcode'></div>

```ts
const bool = Boolean(0);
const str = String(aNumber);
const bool2 = !!str;
const str2 = `result: ${bool2}`;
```

枚举类型（包括枚举类型与其他类型的联合）的值*不得*用 `Boolean()` 或
`!!` 转换为布尔值，而必须改用比较运算符进行
显式比较。

<div class='badcode'></div>

```ts
enum SupportLevel {
  NONE,
  BASIC,
  ADVANCED,
}

const level: SupportLevel = ...;
let enabled = Boolean(level);

const maybeLevel: SupportLevel|undefined = ...;
enabled = !!maybeLevel;
```

<div class='goodcode'></div>

```ts
enum SupportLevel {
  NONE,
  BASIC,
  ADVANCED,
}

const level: SupportLevel = ...;
let enabled = level !== SupportLevel.NONE;

const maybeLevel: SupportLevel|undefined = ...;
enabled = maybeLevel !== undefined && maybeLevel !== SupportLevel.NONE;
```

为什么？

在大多数情况下，枚举名在运行时映射到哪个数字或字符串值
并不重要，因为源代码中枚举类型的值都是按名称引用的。
因此，工程师习惯于不去考虑这一点，于是那些确实
*需要*考虑这一点的情况就不太可取，因为它们会令人
感到意外。枚举转换为布尔值正是这种情况；特别地，
默认情况下首个声明的枚举值为假值（因为它是 0），
而其余值均为真值，这很可能出人意料。阅读
使用枚举值的代码时，读者甚至可能不知道它是不是
首个声明的值。

不鼓励使用字符串拼接来强制转换成字符串，因为我们会检查加号
运算符的两个操作数类型是否匹配。

<div class="numbered"></div>

<a id="coercing-to-numbers"></a>

##### 转换为数字

数字解析可能以多种方式失败，并伴随许多出人意料的边界
情况，而各种解析数字的方法各有不同、有时甚至不一致的
行为（例如空白、空字符串、科学记数法、溢出为无穷大、
进制前缀等）。此外，在错误的层级进行解析往往是一种
代码异味。代码*必须*检查任何数值转换的输出，并显式
处理所有可能的、不会抛出异常的失败情况（例如处理
任何 `NaN` 结果）。

代码*不得*使用一元加号（例如 `+str`）或 `parseFloat` 将字符串
转换为数字。前者在代码评审中太容易被忽略，而后者会
静默地忽略输入字符串末尾的无效内容。这两种情况都应
改用 `Number`。

除非需要非十进制进制，否则代码*不得*使用 `parseInt`。在
这种情况下，解析前*必须*检查输入字符串的有效性（即所有字符
都是有效数字），以确保末尾的无效内容不会被静默忽略。
还必须检查输出是否为 `NaN`。

<div class='badcode'></div>

```ts
const x = +y;
const x1 = parseFloat(y1);
```

<div class='goodcode'></div>

```ts
const x = Number(y);
if (!isFinite(x)) throw new Error(...);
```

<a id="type-coercion-implicit"></a>

<div class="numbered"></div>

<a id="implicit-coercion"></a>

##### 隐式转换

不要在具有隐式布尔转换的条件子句中使用显式布尔
转换（具体来说，即 `if`、`for` 和 `while`
语句中的条件）。

<div class='badcode'></div>

```ts
const foo: MyInterface|null = ...;
if (!!foo) {...}
while (!!foo) {...}
```

<div class='goodcode'></div>

```ts
const foo: MyInterface|null = ...;
if (foo) {...}
while (foo) {...}
```

[与显式转换一样](#type-coercion)，枚举类型（包括枚举类型与其他类型的
联合）的值*不得*被隐式转换为布尔值，而必须改用比较运算符
进行显式比较。

<div class='badcode'></div>

```ts
enum SupportLevel {
  NONE,
  BASIC,
  ADVANCED,
}

const level: SupportLevel = ...;
if (level) {...}

const maybeLevel: SupportLevel|undefined = ...;
if (maybeLevel) {...}
```

<div class='goodcode'></div>

```ts
enum SupportLevel {
  NONE,
  BASIC,
  ADVANCED,
}

const level: SupportLevel = ...;
if (level !== SupportLevel.NONE) {...}

const maybeLevel: SupportLevel|undefined = ...;
if (maybeLevel !== undefined && maybeLevel !== SupportLevel.NONE) {...}
```

其他类型的值既可以被隐式转换为布尔值，也可以用比较运算符
进行显式比较：

<div class='goodcode'></div>

```ts
// Explicitly comparing > 0 is OK:
if (arr.length > 0) {...}
// so is relying on boolean coercion:
if (arr.length) {...}
```

<a id="features-control-structures"></a>

<div class="numbered"></div>

<a id="control-structures"></a>

### 控制结构

<a id="formatting-braces"></a>
<a id="formatting-braces-all"></a>

<div class="numbered"></div>

<a id="control-flow-statements-blocks"></a>

#### 控制流语句与代码块

控制流语句（`if`、`else`、`for`、`do`、`while` 等）始终对所包含的
代码使用花括号代码块，即使语句体中只有一条语句。
非空代码块的第一条语句必须另起一行。

<div class='goodcode'></div>

```ts
for (let i = 0; i < x; i++) {
  doSomethingWith(i);
}

if (x) {
  doSomethingWithALongMethodNameThatForcesANewLine(x);
}
```

<div class='badcode'></div>

```ts
if (x)
  doSomethingWithALongMethodNameThatForcesANewLine(x);

for (let i = 0; i < x; i++) doSomethingWith(i);
```

**例外：**能写在一行内的 `if` 语句*可以*省略代码块。

<div class='goodcode'></div>

```ts
if (x) x.doFoo();
```

<div class="numbered"></div>

<a id="assignment-in-control-statements"></a>

##### 控制语句中的赋值

尽量避免在控制语句内部对变量赋值。在控制语句内部，赋值
很容易被误认为相等性检查。

<div class='badcode'></div>

```ts
if (x = someFunction()) {
  // Assignment easily mistaken with equality check
  // ...
}
```

<div class='goodcode'></div>

```ts
x = someFunction();
if (x) {
  // ...
}
```

如果确实需要在控制语句内部赋值，请用额外的括号把
赋值括起来，以表明这是有意为之。

```ts
while ((x = someFunction())) {
  // Double parenthesis shows assignment is intentional
  // ...
}
```

<a id="features-for-loops"></a>

<div class="numbered"></div>

<a id="iterating-containers"></a>

##### 迭代容器

遍历数组时优先使用 `for (... of someArr)`。`Array.prototype.forEach`
和原生的 `for` 循环也同样允许：

<div class='goodcode'></div>

```ts
for (const x of someArr) {
  // x is a value of someArr.
}

for (let i = 0; i < someArr.length; i++) {
  // Explicitly count if the index is needed, otherwise use the for/of form.
  const x = someArr[i];
  // ...
}
for (const [i, x] of someArr.entries()) {
  // Alternative version of the above.
}
```

`for`-`in` 循环只能用于字典式对象（更多信息参见
[下文](#optimization-compatibility-for-property-access)）。不要
使用 `for (... in ...)` 遍历数组，因为它会违背直觉地给出
数组的索引（以字符串形式！），而不是值：

<div class='badcode'></div>

```ts
for (const x in someArray) {
  // x is the index!
}
```

`Object.prototype.hasOwnProperty` 应在 `for`-`in` 循环中使用，以排除
不需要的原型属性。可能时，优先使用 `for`-`of` 搭配 `Object.keys`、
`Object.values` 或 `Object.entries`，而非 `for`-`in`。

<div class='goodcode'></div>

```ts
for (const key in obj) {
  if (!obj.hasOwnProperty(key)) continue;
  doWork(key, obj[key]);
}
for (const key of Object.keys(obj)) {
  doWork(key, obj[key]);
}
for (const value of Object.values(obj)) {
  doWorkValOnly(value);
}
for (const [key, value] of Object.entries(obj)) {
  doWork(key, value);
}
```

<a id="formatting-grouping-parentheses"></a>

<div class="numbered"></div>

<a id="grouping-parentheses"></a>

#### 分组括号

只有当作者与评审者一致认为，没有这些括号代码也
不会有合理的被误解的可能，而且加上它们也不会让
代码更易读时，才可以省略可选的分组括号。
假定每位读者都熟记完整的运算符优先级表，
是*不*合理的。

不要在 `delete`、`typeof`、`void`、`return`、`throw`、`case`、
`in`、`of` 或 `yield` 之后的整个表达式外添加多余的括号。

<a id="exceptions"></a>
<a id="features-exceptions"></a>

<div class="numbered"></div>

<a id="exception-handling"></a>

#### 异常处理

异常是该语言的重要组成部分，只要出现异常情况
就应使用异常。

自定义异常是从函数传递额外错误信息的绝佳方式。
凡是原生 `Error` 类型不够用时，都应定义并
使用自定义异常。

优先抛出异常，而不是临时拼凑的错误处理方式（例如
传递错误容器引用类型，或返回带有错误
属性的对象）。

<div class="numbered"></div>

<a id="instantiate-errors-using-new"></a>

##### 使用 `new` 实例化错误

实例化异常时始终使用 `new Error()`，而不是直接调用
`Error()`。两种形式都会创建一个新的 `Error` 实例，但使用 `new`
与其他对象的实例化方式更为一致。

<div class='goodcode'></div>

```ts
throw new Error('Foo is not a valid bar.');
```

<div class='badcode'></div>

```ts
throw Error('Foo is not a valid bar.');
```

<div class="numbered"></div>

<a id="only-throw-errors"></a>

##### 只抛出错误

尽管 JavaScript 允许抛出任意值，但只有当抛出的值是 `Error`
时才会填充堆栈轨迹。**不要**抛出原始值
（包括字符串、数字、null 或 undefined），也不要抛出不是
`Error` 或其子类实例的对象。此限制同样适用于所有
可能抛出其参数的 API，包括 `Promise.reject` 或 `AbortSignal` 的
各种 `abort` 方法。

<div class='badcode'></div>

```ts
// bad: does not get a stack trace.
throw 'oh noes!';
// For promises
new Promise((resolve, reject) => void reject('oh noes!'));
Promise.reject();
Promise.reject('oh noes!');
// For abort signals
new AbortController().abort('my custom abort error');
AbortSignal.abort('my other custom abort error');
```

而应只抛出 `Error`（或其子类）：

<div class='goodcode'></div>

```ts
// Throw only Errors
throw new Error('oh noes!');
// ... or subtypes of Error.
class MyError extends Error {}
throw new MyError('my oh noes!');
// For promises
new Promise((resolve) => resolve()); // No reject is OK.
new Promise((resolve, reject) => void reject(new Error('oh noes!')));
Promise.reject(new Error('oh noes!'));
// For abort signals
new AbortController().abort();  // No reason is OK.
AbortSignal.abort();
new AbortController().abort(new Error('my custom abort error'));
AbortSignal.abort(new Error('my other custom abort error'));
```

注：不带参数调用 `AbortController#abort` 或 `AbortSignal.abort`
是有效的，因为默认会创建一个新的 "AbortError" `DOMException`
并赋给 `AbortSignal#reason`（参见
[MDN](https://developer.mozilla.org/en-US/docs/Web/API/AbortController/abort#reason)）。

<div class="numbered"></div>

<a id="catching-and-rethrowing"></a>

##### 捕获与重新抛出

捕获错误时，代码*应该*假定所有抛出的错误都是
`Error` 的实例。

<div class='goodcode'></div>

```ts
function assertIsError(e: unknown): asserts e is Error {
  if (!(e instanceof Error)) throw new Error("e is not an Error");
}

try {
  doSomething();
} catch (e: unknown) {
  // All thrown errors must be Error subtypes. Do not handle
  // other possible values unless you know they are thrown.
  assertIsError(e);
  displayError(e.message);
  // or rethrow:
  throw e;
}
```

除非确知所调用的 API 会违反上述规则抛出非 `Error`
类型，否则异常处理程序*不得*防御性地处理非 `Error` 类型。
在这种情况下，应附上注释，明确指出这些非 `Error`
值来自何处。

<div class='goodcode'></div>

```ts
try {
  badApiThrowingStrings();
} catch (e: unknown) {
  // Note: bad API throws strings instead of errors.
  if (typeof e === 'string') { ... }
}
```

为什么？

避免
[过度防御式编程](https://en.wikipedia.org/wiki/Defensive_programming#Offensive_programming)。
对大多数代码中根本不存在的问题反复设置同样的防线，
只会产生毫无用处的样板代码。

<a id="features-empty-catch-blocks"></a>

<div class="numbered"></div>

<a id="empty-catch-blocks"></a>

##### 空的 catch 代码块

捕获到异常后什么都不做，极少是正确的做法。当确实
适合在 catch 代码块中不采取任何行动时，应在注释中
解释这样做的正当理由。

<div class='goodcode'></div>

```ts
  try {
    return handleNumericResponse(response);
  } catch (e: unknown) {
    // Response is not numeric. Continue to handle as text.
  }
  return handleTextResponse(response);
```

不允许：

<div class='badcode'></div>

```ts
  try {
    shouldFail();
    fail('expected an error');
  } catch (expected: unknown) {
  }
```

提示：与某些其他语言不同，上面这样的写法根本行不通，
因为它会捕获 `fail` 抛出的错误。请改用 `assertThrows()`。

<a id="features-switch-statements"></a>
<a id="features-switch-default-case"></a>

<div class="numbered"></div>

<a id="error-cause"></a>

##### ErrorOptions 的 cause 必须是 Error 对象

为 ErrorOptions 参数传入实参时，`cause` 属性
必须用错误的子类型来初始化。这实际上会创建一条
带有有用堆栈轨迹的错误对象链。

<div class='goodcode'></div>

```ts
try {
  ...
} catch (e: unknown) {
  if (e instanceof Error) {
    throw new Error('Something went wrong', {cause: e});
  }
}
```

<div class='badcode'></div>

```ts
const status = doSomething();
if (status !== success) {
  throw new Error('doSomething failed', {cause: status});
}
```

如果 `cause` 的初始化式引用的是类型为 unknown 的 catch 子句变量，
则可以省略类型检查，因为我们的代码库假定你不可能抛出
`Error` 对象以外的任何东西。

<div class='goodcode'></div>

```ts
try {
  ...
} catch (e: unknown) {
  // No need to check the type of e.
  throw new Error('Something went wrong', {cause: e});
}
```

在 TypeScript 中，`Error` 类型恰好可以赋值给 `ErrorOptions`。
因此有可能不小心把错误对象作为 ErrorOptions 参数传入，
这很可能是代码中的缺陷。

<div class='badcode'></div>

```ts
try {
  ...
} catch (e: unknown) {
  if (e instanceof Error) {
    throw new Error('Something went wrong', e);
  }
}
```

<div class="numbered"></div>

<a id="switch-statements"></a>

#### switch 语句

所有 `switch` 语句*必须*包含 `default` 语句组，即使其中
没有任何代码。`default` 语句组必须放在最后。

<div class='goodcode'></div>

```ts
switch (x) {
  case Y:
    doSomethingElse();
    break;
  default:
    // nothing to do.
}
```

在 switch 代码块内，每个语句组要么以 `break` 或 `return`
语句突然终止，要么通过抛出异常终止。非空语句组
（`case ...`）*不得*向下贯穿（由编译器强制保证）：

<div class='badcode'></div>

```ts
switch (x) {
  case X:
    doSomething();
    // fall through - not allowed!
  case Y:
    // ...
}
```

允许空语句组向下贯穿：

<div class='goodcode'></div>

```ts
switch (x) {
  case X:
  case Y:
    doSomething();
    break;
  default: // nothing to do.
}
```

<a id="features-equality-checks"></a>
<a id="features-equality-checks-exceptions"></a>

<div class="numbered"></div>

<a id="equality-checks"></a>

#### 相等性检查

始终使用三等号（`===`）和不等号（`!==`）。双等号
运算符会引发容易出错的类型转换，既难以理解，
也会降低 JavaScript 虚拟机的实现速度。另请参见
[JavaScript 相等性表格](https://dorey.github.io/JavaScript-Equality-Table/)。

<div class='badcode'></div>

```ts
if (foo == 'bar' || baz != bam) {
  // Hard to understand behaviour due to type coercion.
}
```

<div class='goodcode'></div>

```ts
if (foo === 'bar' || baz !== bam) {
  // All good here.
}
```

**例外：**与字面量 `null` 值比较时，*可以*使用 `==` 和
`!=` 运算符，以同时涵盖 `null` 和 `undefined` 值。

<div class='goodcode'></div>

```ts
if (foo == null) {
  // Will trigger when foo is null or undefined.
}
```

<div class="numbered"></div>

<a id="type-and-non-nullability-assertions"></a>

#### 类型断言与非空断言

类型断言（`x as SomeType`）和非空断言（`y!`）都是
不安全的。二者只会让 TypeScript 编译器不再报错，却不会插入任何
运行时检查来印证这些断言，因此可能导致程序在
运行时崩溃。

因此，在没有明显或明确的理由时，你*不应该*使用
类型断言和非空断言。

不要采用以下写法：

<div class='badcode'></div>

```ts
(x as Foo).foo();

y!.bar();
```

当你想断言某个类型或非空性时，最佳做法是显式地
编写执行该检查的运行时检查代码。

<div class='goodcode'></div>

```ts
// assuming Foo is a class.
if (x instanceof Foo) {
  x.foo();
}

if (y) {
  y.bar();
}
```

有时，由于代码的某些局部特性，你可以确信断言形式
是安全的。在这种情况下，你*应该*补充说明，
解释为什么可以接受这种不安全的行为：

<div class='goodcode'></div>

```ts
// x is a Foo, because ...
(x as Foo).foo();

// y cannot be null, because ...
y!.bar();
```

如果类型断言或非空断言背后的理由显而易见，则注释
*可以*不必添加。例如，生成的 proto 代码始终可空，但在
代码上下文中也许众所周知某些字段总是由后端提供。
请自行判断。

<div class="numbered"></div>

<a id="type-assertions-syntax"></a>

##### 类型断言语法

类型断言*必须*使用 `as` 语法（而不是尖括号
语法）。这样在访问成员时会强制给断言加上括号。

<div class='badcode'></div>

```ts
const x = (<Foo>z).length;
const y = <Foo>z.length;
```

<div class='goodcode'></div>

```ts
// z must be Foo because ...
const x = (z as Foo).length;
```

<div class="numbered"></div>

<a id="double-assertions"></a>

##### 双重断言

根据
[TypeScript 手册](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#type-assertions)，
TypeScript 只允许把类型转换为其*更具体*或
*更宽泛*版本的类型断言。若添加（`x as Foo`）这样不满足
此条件的类型断言，将报错："Conversion of type 'X' to type
'Y' may be a mistake because neither type sufficiently overlaps with the other."

如果确信某个断言是安全的，可以执行*双重断言*。这
需要经由 `unknown` 转换，因为它比所有类型都更宽泛。

<div class='goodcode'></div>

```ts
// x is a Foo here, because...
(x as unknown as Foo).fooMethod();
```

使用 `unknown`（而不是 `any` 或 `{}`）作为中间类型。

<div class="numbered"></div>

<a id="type-assertions-and-object-literals"></a>

##### 类型断言与对象字面量

使用类型注解（`: Foo`）而非类型断言（`as Foo`）来指定
对象字面量的类型。这样，当接口的字段随时间发生变化时，
就能发现重构引入的缺陷。

<div class='badcode'></div>

```ts
interface Foo {
  bar: number;
  baz?: string;  // was "bam", but later renamed to "baz".
}

const foo = {
  bar: 123,
  bam: 'abc',  // no error!
} as Foo;

function func() {
  return {
    bar: 123,
    bam: 'abc',  // no error!
  } as Foo;
}
```

<div class='goodcode'></div>

```ts
interface Foo {
  bar: number;
  baz?: string;
}

const foo: Foo = {
  bar: 123,
  bam: 'abc',  // complains about "bam" not being defined on Foo.
};

function func(): Foo {
  return {
    bar: 123,
    bam: 'abc',   // complains about "bam" not being defined on Foo.
  };
}
```

<div class="numbered"></div>

<a id="keep-try-blocks-focused"></a>

#### 让 try 代码块保持精简

在不损害可读性的前提下，尽量减少 try 代码块中
的代码量。

<div class='badcode'></div>

```ts
try {
  const result = methodThatMayThrow();
  use(result);
} catch (error: unknown) {
  // ...
}
```

<div class='goodcode'></div>

```ts
let result;
try {
  result = methodThatMayThrow();
} catch (error: unknown) {
  // ...
}
use(result);
```

把不会抛出异常的代码行移出 try/catch 代码块，有助于读者
弄清哪个方法会抛异常。某些不会抛异常的内联调用
可以留在其中，因为为它们引入临时变量带来的额外复杂度
可能并不值得。

**例外：**如果 try 代码块位于循环内部，可能会有性能问题。
扩大 try 代码块以覆盖整个循环是可以的。

<div class="numbered"></div>

<a id="decorators"></a>

### 装饰器

装饰器是带有 `@` 前缀的语法，例如 `@MyDecorator`。

不要定义新的装饰器。只使用框架定义的装饰器：

-   Angular（例如 `@Component`、`@NgModule` 等）
-   Polymer（例如 `@property`）

为什么？

我们通常希望避免使用装饰器，因为它们曾是一项实验性特性，
此后已与 TC39 提案产生分歧，并且存在已知且不会
被修复的缺陷。

使用装饰器时，装饰器*必须*紧挨着它所修饰的符号，
两者之间不得有空行：

```ts
/** JSDoc comments go before decorators */
@Component({...})  // Note: no empty line after the decorator.
class MyComp {
  @Input() myField: string;  // Decorators on fields may be on the same line...

  @Input()
  myOtherField: string;  // ... or wrap.
}
```

<div class="numbered"></div>

<a id="disallowed-features"></a>

### 禁用的特性

<a id="disallowed-features-wrapper-objects"></a>

<div class="numbered"></div>

<a id="primitive-types-wrapper-classes"></a>

#### 基本类型的包装对象

TypeScript 代码*不得*实例化基本类型 `String`、`Boolean`
和 `Number` 的包装类。包装类有出人意料的行为，
例如 `new Boolean(false)` 求值为 `true`。

<div class='badcode'></div>

```ts
const s = new String('hello');
const b = new Boolean(false);
const n = new Number(5);
```

这些包装器可以作为函数来调用，用于强制转换（这比使用 `+`
或拼接空字符串更可取）或创建符号。更多信息请参见
[类型转换](#type-coercion)。

<a id="formatting-semicolons-are-required"></a>
<a id="disallowed-features-automatic-semicolon-insertion"></a>

<div class="numbered"></div>

<a id="automatic-semicolon-insertion"></a>

#### 自动分号插入

不要依赖自动分号插入（ASI）。请显式地用分号结束
所有语句。这可以避免因分号插入不当
而引发的缺陷。

<div class="numbered"></div>

<a id="enums"></a>

#### 常量枚举

代码*不得*使用 `const enum`；请改用普通的 `enum`。

为什么？

TypeScript 的枚举本身已不可被修改；`const enum` 则是一项
与优化相关的独立语言特性，它会使枚举对该模块的
JavaScript 使用者不可见。

<div class="numbered"></div>

<a id="debugger-statements"></a>

#### debugger 语句

生产代码中*不得*包含 debugger 语句。

<div class='badcode'></div>

```ts
function debugMe() {
  debugger;
}
```

<a id="disallowed-features-with"></a>

<div class="numbered"></div>

<a id="diallowed-features-with"></a>

#### `with`

不要使用 `with` 关键字。它会使代码更难理解，而且
[自 ES5 起就已在严格模式中被禁用](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/with)。

<a id="disallowed-features-dynamic-code-evaluation"></a>

<div class="numbered"></div>

<a id="dynamic-code-evaluation"></a>

#### 动态代码求值

不要使用 `eval` 或 `Function(...string)` 构造函数（代码加载器
除外）。这些特性有潜在危险，并且在使用严格
[内容安全策略](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)的环境中
根本无法工作。

<a id="disallowed-features-non-standard-features"></a>

<div class="numbered"></div>

<a id="non-standard-features"></a>

#### 非标准特性

不要使用非标准的 ECMAScript 或 Web Platform 特性。

这包括：

-   已被标记为弃用或已从 ECMAScript / Web Platform 中完全移除的
    旧特性（参见
    [MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Deprecated_and_obsolete_features)）
-   尚未标准化的新 ECMAScript 特性
    -   避免使用当前 TC39 工作草案中的特性，或正处于
        [提案流程](https://tc39.es/process-document/)中的特性
    -   只使用当前 ECMA-262 规范中定义的 ECMAScript
        特性
-   已提出但尚未完成的网络标准：
    -   尚未完成
        [提案流程](https://whatwg.org/faq#adding-new-features)的 WHATWG 提案。
-   非标准的语言“扩展”（例如某些外部转译器
    提供的那些）

面向特定 JavaScript 运行时的项目（例如仅支持最新版 Chrome、
Chrome 扩展、Node.JS、Electron）显然可以使用这些 API。在考虑
专有的、仅在部分浏览器中实现的 API 接口时要谨慎；
不妨考虑是否有某个通用库能替你把这层 API
接口抽象掉。

<a id="disallowed-features-modifying-builtin-objects"></a>

<div class="numbered"></div>

<a id="modifying-builtin-objects"></a>

#### 修改内置对象

绝不修改内置类型，无论是给它们的构造函数还是给它们的
原型添加方法。避免依赖会这样做的库。

除非绝对必要（例如第三方 API 要求），否则不要向全局对象
添加符号。

<a id="syntax"></a>
<a id="naming-rules-common-to-all-identifiers"></a>

<div class="numbered"></div>

<a id="naming"></a>

## 命名

<div class="numbered"></div>

<a id="identifiers"></a>

### 标识符

标识符*必须*只使用 ASCII 字母、数字、下划线（用于常量
和结构化的测试方法名），以及（极少情况下）'$' 符号。

<div class="numbered"></div>

<a id="naming-style"></a>

#### 命名风格

TypeScript 通过类型来表达信息，因此名称*不应该*用
类型中已包含的信息来修饰。（更多信息参见
[Testing Blog](https://testing.googleblog.com/2017/10/code-health-identifiernamingpostforworl.html)，
其中说明了不应包含哪些内容。）

这条规则的一些具体示例：

*   不要为私有属性或方法使用后置或前置的
    下划线。
*   不要为可选参数使用 `opt_` 前缀。
    *   对于访问器，参见下文的[访问器规则](#classes-getters-and-setters)。
*   不要对接口做特殊标记（~~`IMyInterface`~~ 或
    ~~`MyFooInterface`~~），除非在其环境中这是惯用的。
    为类引入接口时，给它起一个能说明该接口
    最初为何存在的名称（例如 `class TodoItem` 和
    `interface TodoItemStorage`，如果该接口表达了用于
    JSON 中存储/序列化的格式）。
*   给 `Observable` 加 `$` 后缀是一种常见的外部惯例，可以
    帮助消除可观察值与具体值之间的混淆。
    这一惯例是否有用，由各个团队自行判断，但在项目内部
    *应该*保持一致。

<a id="identifiers-abbreviations"></a>

<div class="numbered"></div>

<a id="descriptive-names"></a>

#### 描述性名称

名称*必须*具有描述性，让新读者也能一目了然。不要使用
对项目之外的读者而言含义模糊或不熟悉的缩写，也不要
通过删去单词内部的字母来缩写。

*   **例外：** 作用域不超过 10 行的变量，包括*不属于*
    导出 API 的参数，*可以*使用简短的（例如单字母）
    变量名。

<div class='goodcode'></div>

```ts
// Good identifiers:
errorCount          // No abbreviation.
dnsConnectionIndex  // Most people know what "DNS" stands for.
referrerUrl         // Ditto for "URL".
customerId          // "Id" is both ubiquitous and unlikely to be misunderstood.
```

<div class='badcode'></div>

```ts
// Disallowed identifiers:
n                   // Meaningless.
nErr                // Ambiguous abbreviation.
nCompConns          // Ambiguous abbreviation.
wgcConnections      // Only your group knows what this stands for.
pcReader            // Lots of things can be abbreviated "pc".
cstmrId             // Deletes internal letters.
kSecondsPerDay      // Do not use Hungarian notation.
customerID          // Incorrect camelcase of "ID".
```

<a id="naming-camel-case-defined"></a>

<div class="numbered"></div>

<a id="camel-case"></a>

#### 驼峰式命名

把名称中的缩写和首字母缩略词当作完整单词对待，即使用
`loadHttpUrl`，而不是 ~~`loadHTTPURL`~~，除非平台名称有此要求（例如
`XMLHttpRequest`）。

<div class="numbered"></div>

<a id="identifiers-dollar-sign"></a>

#### 美元符号

标识符通常*不应该*使用 `$`，除非第三方框架的命名
约定有此要求。关于把 `$` 用于 `Observable` 值的更多信息，
请参见[上文](#naming-style)。

<a id="naming-class-names"></a>
<a id="naming-method-names"></a>
<a id="naming-enum-names"></a>
<a id="naming-constant-names"></a>
<a id="naming-local-variable-names"></a>
<a id="naming-non-constant-field-names"></a>
<a id="naming-parameter-names"></a>

<div class="numbered"></div>

<a id="naming-rules-by-identifier-type"></a>

### 按标识符类型划分的规则

大多数标识符名称应根据标识符的类型，遵循下表中的
大小写形式。

<!-- mdformat off -->

| 风格            | 类别 |
| ---------------- | -------- |
| `UpperCamelCase` | class / interface / type / enum / decorator / type parameters / component functions in TSX / JSXElement type parameter |
| `lowerCamelCase` | variable / parameter / function / method / property / module alias |
| `CONSTANT_CASE`  | 全局常量值，包括枚举值。见下文[常量](#identifiers-constants)。 |
| `#ident`         | 从不使用私有标识符。 |

<!-- mdformat on -->

<a id="naming-template-parameter-names"></a>

<div class="numbered"></div>

<a id="identifiers-type-parameters"></a>

#### 类型参数

类型参数（如 `Array<T>` 中的）*可以*使用单个大写字符
（`T`）或 `UpperCamelCase`。

<div class="numbered"></div>

<a id="identifiers-test-names"></a>

#### 测试名称

xUnit 风格测试框架中的测试方法名*可以*用 `_`
分隔符来组织，例如 `testX_whenY_doesZ()`。

<div class="numbered"></div>

<a id="identifiers-underscore-prefix-suffix"></a>

#### 下划线（`_`）前缀/后缀

下划线前缀表示某个语法上必需的标识符不会被
使用。鼓励在下划线之后提供有意义的名称，但也允许
单独使用 `_`。

<div class='goodcode'></div>

```ts
(_projectId, api) => of(!params.disabledApis.includes(api));

[].filter((_, i) => i % 2 === 0);

for await (const _item of getAllTheThings()) {
  count++;
}

using _cleanupFoo = foo();
```

不要对末尾未使用的参数使用这种写法，这类参数应直接省略。

在专门打算被重写的方法上，允许保留末尾未使用的
参数。

<div class='badcode'></div>

```ts
[].filter((element, _index) => !element.hasSomeProperty());
```

<div class='goodcode'></div>

```ts
[].filter(element => !element.hasSomeProperty());
```

标识符不得把 `_` 用作后缀。

> 提示：如果只需要数组（或 TypeScript 元组）中的部分元素，可以
> 在解构语句中插入额外的逗号，以忽略
> 中间的元素：
>
> ```ts
> const [a, , b] = [1, 5, 10];  // a <- 1, b <- 10
> ```

<div class="numbered"></div>

<a id="identifiers-imports"></a>

#### 导入

模块命名空间导入采用 `lowerCamelCase`，而文件名采用 `snake_case`，
这意味着正确的导入在大小写风格上并不一致，例如

<div class='goodcode'></div>

```ts
import * as fooBar from './foo_bar';
```

有些库可能普遍使用违反这一命名方案的命名空间导入
前缀，但其在开源界压倒性的普遍使用，使这种违规
风格反而更易读。目前适用这一例外的库
只有：

*   [jquery](https://jquery.com/)，使用 `$` 前缀
*   [threejs](https://threejs.org/)，使用 `THREE` 前缀

<div class="numbered"></div>

<a id="identifiers-constants"></a>

#### 常量

**不可变**：`CONSTANT_CASE` 表示某个值*意图*上不应被
改变，并且*可以*用于技术上可被修改的值（即
未被深度冻结的值），以此向使用者表明它们不得被
修改。

<div class='goodcode'></div>

```ts
const UNIT_SUFFIXES = {
  'milliseconds': 'ms',
  'seconds': 's',
};
// Even though per the rules of JavaScript UNIT_SUFFIXES is
// mutable, the uppercase shows users to not modify it.
```

常量也可以是类的 `static readonly` 属性。

<div class='goodcode'></div>

```ts
class Foo {
  private static readonly MY_SPECIAL_NUMBER = 5;

  bar() {
    return 2 * Foo.MY_SPECIAL_NUMBER;
  }
}
```

**全局**：只有在模块层级声明的符号、模块层级类的静态字段，
以及模块层级枚举的值，才*可以*使用 `CONST_CASE`。如果某个
值在程序的生命周期中可以被实例化多次（例如
在函数内声明的局部变量，或嵌套在函数内的类的静态
字段），那么它*必须*使用 `lowerCamelCase`。
[局部作用域别名](#aliases)例外，应采用既有标识符的
格式。

如果某个值是实现某接口的箭头函数，那么它*可以*
声明为 `lowerCamelCase`。

<a id="naming-local-aliases"></a>

<div class="numbered"></div>

<a id="aliases"></a>

#### 别名

为既有符号创建局部作用域别名时，请沿用该既有
标识符的格式。局部别名*必须*与源标识符既有的命名和
格式保持一致。对于变量，局部别名请用 `const`；对于类
字段，请使用 `readonly` 属性。

> 注：如果只是为了让别名暴露给你所选框架中的模板，
> 记得还要正确应用
> [访问修饰符](#properties-used-outside-of-class-lexical-scope)。

<div class='goodcode'></div>

```ts
const {BrewStateEnum} = SomeType;
const CAPACITY = 5;

class Teapot {
  readonly BrewStateEnum = BrewStateEnum;
  readonly CAPACITY = CAPACITY;
}
```

<div class="numbered"></div>

<a id="type-system"></a>

## 类型系统

<div class="numbered"></div>

<a id="type-inference"></a>

### 类型推断

代码*可以*依赖由 TypeScript 编译器实现的类型推断，
用于所有类型表达式（变量、字段、返回类型等）。

<div class='goodcode'></div>

```ts
const x = 15;  // Type inferred.
```

当类型可以轻易推断出来时，省略类型注解：未导出的、以
`string`、`number` 或 `boolean` 字面量初始化的变量或参数。
在为了与 `isolatedDeclarations` 兼容而必需的导出符号上，
类型注解不被视为可以省略。

<div class='badcode'></div>

```ts
let count: number = 0;  // Bad: type annotation here is redundant

// Bad: Exported interpolation fails isolatedDeclarations.
export const PATH = `/users/${id}`;
```

<div class='goodcode'></div>

```ts
let count = 0;

// Good: Explicit type for isolatedDeclarations.
export const PATH: string = `/users/${id}`;
```

当显式泛型类型与类型注解重复而显得多余时，
同样应省略这些显式泛型类型。

<div class='badcode'></div>

```ts
// Bad: Specifying '<string>' twice is unnecessary.
const x: Set<string> = new Set<string>();
```

<div class='goodcode'></div>

```ts
const x = new Set<string>();             // Preferred when local
export const y: Set<string> = new Set(); // Annotation required for exports
```

对于更复杂的表达式，类型注解有助于提升程序的
可读性：

<div class='badcode'></div>

```ts
// Hard to reason about the type of 'value' without an annotation.
const value = await rpc.getSomeValue().transform();
```

<div class='goodcode'></div>

```ts
// Can tell the type of 'value' at a glance.
const value: string[] = await rpc.getSomeValue().transform();
```

是否需要添加注解由代码评审者决定。

<div class="numbered"></div>

<a id="return-types"></a>

#### 返回类型

函数和方法是否包含返回类型注解由代码作者决定。评审者
*可以*要求添加注解，以澄清难以理解的复杂返回
类型。项目*可以*制定本地策略，始终要求
写明返回类型，但这并非 TypeScript 的通用风格要求。

显式写出函数与方法的隐式返回值类型，有两点
好处：

-   更精确的文档，有助于代码的读者。
-   若日后代码改动改变了函数的返回类型，能更快
    地暴露潜在的类型错误。

<a id="null-vs-undefined"></a>

<div class="numbered"></div>

<a id="undefined-and-null"></a>

### Undefined 与 null

TypeScript 支持 `undefined` 和 `null` 类型。可空类型
可以用联合类型（`string|null`）构造，`undefined` 同理；
对于 `undefined` 与 `null` 的联合没有特殊语法。

TypeScript 代码可以用 `undefined` 或 `null` 表示值缺失，
并没有通用准则要求优先使用其中某一个。许多
JavaScript API 使用 `undefined`（例如 `Map.get`），而许多 DOM 和 Google API
使用 `null`（例如 `Element.getAttribute`），因此用哪个值表示
缺失取决于上下文。

<div class="numbered"></div>

<a id="nullableundefined-type-aliases"></a>

#### 可空 / undefined 类型别名

类型别名*不得*在联合类型中包含 `|null` 或 `|undefined`。
可空别名通常表明 null 值在应用程序中经过了
过多层级的传递，这会掩盖导致 `null` 的原始问题根源。
它们还会使人难以判断类或接口上的特定值
何时可能缺失。

相反，代码*必须*只在实际使用该别名时才添加 `|null` 或
`|undefined`。代码*应该*在 null 值产生处附近处理它们，
并使用以下技巧。

<div class='badcode'></div>

```ts
// Bad
type CoffeeResponse = Latte|Americano|undefined;

class CoffeeService {
  getLatte(): CoffeeResponse { ... };
}
```

<div class='goodcode'></div>

```ts
// Better
type CoffeeResponse = Latte|Americano;

class CoffeeService {
  getLatte(): CoffeeResponse|undefined { ... };
}
```

<a id="structural-types-vs-nominal-types"></a>

<div class="numbered"></div>

<a id="use-structural-types"></a>

### 使用结构化类型

TypeScript 的类型系统是结构化的，而非名义化的。
也就是说，若一个值至少具备某类型所要求的全部属性，
且这些属性的类型递归地匹配，则该值匹配该类型。

在提供基于结构化类型的实现时，应在符号声明处
显式写出类型（这样能实现更精确的类型检查和
错误报告）。

<div class='goodcode'></div>

```ts
const foo: Foo = {
  a: 123,
  b: 'abc',
}
```

<div class='badcode'></div>

```ts
const badFoo = {
  a: 123,
  b: 'abc',
}
```

使用接口而非类来定义结构化类型

<div class='goodcode'></div>

```ts
interface Foo {
  a: number;
  b: string;
}

const foo: Foo = {
  a: 123,
  b: 'abc',
}
```

<div class='badcode'></div>

```ts
class Foo {
  readonly a: number;
  readonly b: number;
}

const foo: Foo = {
  a: 123,
  b: 'abc',
}
```

为什么？

上面的 "badFoo" 对象依赖类型推断。可以向
"badFoo" 添加额外字段，其类型则根据对象本身推断得出。

把 "badFoo" 传给接收 "Foo" 的函数时，错误会出现在
函数调用处，而非对象声明处。在大型代码库中改动
接口的公开结构时，这一点同样有用。

```ts
interface Animal {
  sound: string;
  name: string;
}

function makeSound(animal: Animal) {}

/**
 * 'cat' has an inferred type of '{sound: string}'
 */
const cat = {
  sound: 'meow',
};

/**
 * 'cat' does not meet the type contract required for the function, so the
 * TypeScript compiler errors here, which may be very far from where 'cat' is
 * defined.
 */
makeSound(cat);

/**
 * Horse has a structural type and the type error shows here rather than the
 * function call.  'horse' does not meet the type contract of 'Animal'.
 */
const horse: Animal = {
  sound: 'niegh',
};

const dog: Animal = {
  sound: 'bark',
  name: 'MrPickles',
};

makeSound(dog);
makeSound(horse);
```

<a id="interfaces-vs-type-aliases"></a>

<div class="numbered"></div>

<a id="prefer-interfaces"></a>

### 优先使用接口而非类型字面量别名

TypeScript 支持
[类型别名](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#type-aliases)
来为类型表达式命名。它可用于命名基本类型、联合类型、
元组以及任何其他类型。

然而，在声明对象的类型时，应使用接口，而不是针对
对象字面量表达式使用类型别名。

<div class='goodcode'></div>

```ts
interface User {
  firstName: string;
  lastName: string;
}
```

<div class='badcode'></div>

```ts
type User = {
  firstName: string,
  lastName: string,
}
```

为什么？

这两种形式几乎等价，因此本着在两种等价形式中
只选其一以避免产生变化的原则，我们应当选定一种。
此外，还有
[值得关注的技术理由支持优先使用接口](https://ncjamieson.com/prefer-interfaces/)。
该页面引用了 TypeScript 团队负责人的话：“老实说，我的看法是，
凡是接口能表达的东西，就该一律用接口。既然在展示/性能
方面有这么多问题，类型别名并没有什么好处。”

<div class="numbered"></div>

<a id="arrayt-type"></a>

### `Array<T>` 类型

对于简单类型（仅含字母数字字符和点号），应使用数组的
语法糖 `T[]` 或 `readonly T[]`，而不是较长的
`Array<T>` 或 `ReadonlyArray<T>`。

对于简单类型的多维非 `readonly` 数组，应使用语法糖
形式（`T[][]`、`T[][][]` 等），而不是较长的形式。

对于任何更复杂的类型，使用较长的形式 `Array<T>`。

这些规则适用于每一层嵌套，即嵌套在更复杂类型中的
简单 `T[]` 仍应写作 `T[]`，也就是使用语法糖。

<div class='goodcode'></div>

```ts
let a: string[];
let b: readonly string[];
let c: ns.MyObj[];
let d: string[][];
let e: Array<{n: number, s: string}>;
let f: Array<string|number>;
let g: ReadonlyArray<string|number>;
let h: InjectionToken<string[]>;  // Use syntax sugar for nested types.
let i: ReadonlyArray<string[]>;
let j: Array<readonly string[]>;
```

<div class='badcode'></div>

```ts
let a: Array<string>;  // The syntax sugar is shorter.
let b: ReadonlyArray<string>;
let c: Array<ns.MyObj>;
let d: Array<string[]>;
let e: {n: number, s: string}[];  // The braces make it harder to read.
let f: (string|number)[];         // Likewise with parens.
let g: readonly (string | number)[];
let h: InjectionToken<Array<string>>;
let i: readonly string[][];
let j: (readonly string[])[];
```

<div class="numbered"></div>

<a id="indexable-key-string-type"></a>

### 可索引类型 / 索引签名（`{[key: string]: T}`）

在 JavaScript 中，常用对象充当关联数组（亦称 "map"、
"hash" 或 "dict"）。在 TypeScript 中，这类对象可以用
[索引签名](https://www.typescriptlang.org/docs/handbook/2/objects.html#index-signatures)
（`[k: string]: T`）来标注类型：

```ts
const fileSizes: {[fileName: string]: number} = {};
fileSizes['readme.txt'] = 541;
```

在 TypeScript 中，应为键提供有意义的标签。（该标签
仅用于文档，其他场合并不使用。）

<div class='badcode'></div>

```ts
const users: {[key: string]: number} = ...;
```

<div class='goodcode'></div>

```ts
const users: {[userName: string]: number} = ...;
```

> 与其使用上述形式，不如考虑改用 ES6 的 `Map` 和 `Set` 类型。
> JavaScript 对象有
> [出人意料的不良行为](http://2ality.com/2012/01/objects-as-maps.html)，
> 而 ES6 类型能更明确地表达你的意图。此外，`Map` 可以用
> `string` 之外的类型作为键，`Set` 也可以包含这类类型。

TypeScript 内置的 `Record<Keys, ValueType>` 类型允许构造
具有确定键集合的类型。它与关联数组的区别在于，其键
是静态已知的。相关建议参见
[下文](#mapped-conditional-types)。

<div class="numbered"></div>

<a id="mapped-conditional-types"></a>

### 映射类型与条件类型

TypeScript 的
[映射类型](https://www.typescriptlang.org/docs/handbook/2/mapped-types.html)
和
[条件类型](https://www.typescriptlang.org/docs/handbook/2/conditional-types.html)
允许基于其他类型指定新类型。TypeScript 的标准库
包含若干基于它们的类型运算符（`Record`、`Partial`、
`Readonly` 等）。

这些类型系统特性可以简洁地指定类型，并构造出
强大且类型安全的抽象。不过，它们也带有一些
缺点：

*   与显式指定属性和类型关系（例如使用接口和继承，
    参见下文的示例）相比，类型运算符要求读者
    在头脑中推演类型表达式。这会显著增加程序的
    阅读难度，尤其是与类型推断以及跨文件边界的
    表达式结合使用时。
*   映射类型与条件类型的求值模型，尤其是与类型推断
    结合时，规格并不完备，也并非总能被充分理解，
    而且在 TypeScript 编译器的不同版本间常有变化。代码可能
    “意外地”通过编译，或看似给出正确结果。这会增加
    使用类型运算符的代码未来的维护成本。
*   映射类型与条件类型在从复杂类型和/或推断类型
    派生类型时最为强大。但另一方面，这也正是它们最容易
    造成程序难以理解和维护的时候。
*   某些语言工具无法很好地处理这些类型系统特性。
    例如，IDE 的“查找引用”（以及由此进行的属性重命名重构）
    无法在 `Pick<T, Keys>` 类型中找到属性，Code Search 也不会
    为它们生成超链接。 *

风格建议如下：

*   始终使用能够表达代码的最简单的类型构造。
*   少许重复或冗长，往往比复杂类型表达式的长期
    成本低得多。
*   在满足上述考量的前提下，可以使用映射类型与条件类型。

例如，TypeScript 内置的 `Pick<T, Keys>` 类型允许通过
取另一个类型 `T` 的子集来创建新类型，但简单的接口继承往往
更易于理解。

```ts
interface User {
  shoeSize: number;
  favoriteIcecream: string;
  favoriteChocolate: string;
}

// FoodPreferences has favoriteIcecream and favoriteChocolate, but not shoeSize.
type FoodPreferences = Pick<User, 'favoriteIcecream'|'favoriteChocolate'>;
```

这等价于把 `FoodPreferences` 上的属性逐一写出：

```ts
interface FoodPreferences {
  favoriteIcecream: string;
  favoriteChocolate: string;
}
```

为减少重复，`User` 可以继承 `FoodPreferences`，或者
（也许更好）嵌套一个表示饮食偏好的字段：

<div class='goodcode'></div>

```ts
interface FoodPreferences { /* as above */ }
interface User extends FoodPreferences {
  shoeSize: number;
  // also includes the preferences.
}
```

在这里使用接口可以显式地体现属性的分组，改善 IDE
支持，便于更好地优化，并且可以说让代码更
易于理解。

<div class="numbered"></div>

<a id="any"></a>

### `any` 类型

TypeScript 的 `any` 类型是所有其他类型的超类型和子类型，
并且允许解引用所有属性。因此，`any` 很危险——它可能
掩盖严重的编程错误，而且使用它会削弱在一开始就拥有
静态类型所带来的价值。

**考虑*不*使用 `any`。**在想要使用 `any` 的情形下，
可以考虑以下做法之一：

-   [提供更具体的类型](#any-specific)
-   [使用 `unknown`](#any-unknown)
-   [抑制静态检查警告并说明原因](#any-suppress)

<div class="numbered"></div>

<a id="any-specific"></a>

#### 提供更具体的类型

使用接口、内联对象类型或类型别名：

<div class='goodcode'></div>

```ts
// Use declared interfaces to represent server-side JSON.
declare interface MyUserJson {
  name: string;
  email: string;
}

// Use type aliases for types that are repetitive to write.
type MyType = number|string;

// Or use inline object types for complex returns.
function getTwoThings(): {something: number, other: string} {
  // ...
  return {something, other};
}

// Use a generic type, where otherwise a library would say `any` to represent
// they don't care what type the user is operating on (but note "Return type
// only generics" below).
function nicestElement<T>(items: T[]): T {
  // Find the nicest element in items.
  // Code can also put constraints on T, e.g. <T extends HTMLElement>.
}
```

<div class="numbered"></div>

<a id="any-unknown"></a>

#### 优先使用 `unknown` 而非 `any`

`any` 类型允许赋值给任何其他类型，并可解引用其
任意属性。这种行为往往既不必要也不合意，代码
只是需要表明某个类型是未知的。在这种情况下应
使用内置类型 `unknown`——它既能表达这一概念，
又因不允许解引用任意属性而安全得多。

<div class='goodcode'></div>

```ts
// Can assign any value (including null or undefined) into this but cannot
// use it without narrowing the type or casting.
const val: unknown = value;
```

<div class='badcode'></div>

```ts
const danger: any = value /* result of an arbitrary expression */;
danger.whoops();  // This access is completely unchecked!
```

要安全地使用 `unknown` 值，可使用
[类型保护](https://www.typescriptlang.org/docs/handbook/advanced-types.html#type-guards-and-differentiating-types)

<div class="numbered"></div>

<a id="any-suppress"></a>

#### 抑制 `any` 静态检查警告

有时使用 `any` 是合理的，例如在测试中构造 mock
对象。在这种情况下，应添加注释抑制静态检查警告，
并说明其合理之处。

<div class='goodcode'></div>

```ts
// This test only needs a partial implementation of BookService, and if
// we overlooked something the test will fail in an obvious way.
// This is an intentionally unsafe partial mock
// tslint:disable-next-line:no-any
const mockBookService = ({get() { return mockBook; }} as any) as BookService;
// Shopping cart is not used in this test
// tslint:disable-next-line:no-any
const component = new MyComponent(mockBookService, /* unused ShoppingCart */ null as any);
```

<div class="numbered"></div>

<a id="empty-interface-type"></a>

### `{}` 类型

`{}` 类型也称为*空接口*类型，表示一个
不含任何属性的接口。空接口类型没有指定属性，
因此任何非 nullish 值都可以赋值给它。

<div class='badcode'></div>

```ts
let player: {};

player = {
  health: 50,
}; // Allowed.

console.log(player.health) // Property 'health' does not exist on type '{}'.
```

<div class='badcode'></div>

```ts
function takeAnything(obj:{}) {

}

takeAnything({});
takeAnything({ a: 1, b: 2 });
```

Google3 代码**不应该**在多数用例中使用 `{}`。`{}` 表示任何
非 nullish 的基本类型或对象类型，这很少是恰当的。请优先使用
以下描述性更强的类型之一：

*   `unknown` 可以容纳任何值，包括 `null` 或 `undefined`，
    通常更适合表示不透明的值。
*   `Record<string, T>` 更适合类字典对象，并且通过
    明确写出所含值的类型 `T` 来提供更好的类型安全
    （该类型本身也可以是 `unknown`）。
*   `object` 还排除了基本类型，只留下非 nullish 的函数和
    对象，但不对可能提供哪些属性作任何其他
    假设。

<div class="numbered"></div>

<a id="tuple-types"></a>

### 元组类型

如果你打算创建一个 Pair 类型，请改用元组类型：

<div class='badcode'></div>

```ts
interface Pair {
  first: string;
  second: string;
}
function splitInHalf(input: string): Pair {
  ...
  return {first: x, second: y};
}
```

<div class='goodcode'></div>

```ts
function splitInHalf(input: string): [string, string] {
  ...
  return [x, y];
}

// Use it like:
const [leftHalf, rightHalf] = splitInHalf('my string');
```

不过，为属性提供有意义的名称往往更清晰。

如果声明 `interface` 太过笨重，可以使用内联对象
字面量类型：

<div class='goodcode'></div>

```ts
function splitHostPort(address: string): {host: string, port: number} {
  ...
}

// Use it like:
const address = splitHostPort(userAddress);
use(address.port);

// You can also get tuple-like behavior using destructuring:
const {host, port} = splitHostPort(userAddress);
```

<div class="numbered"></div>

<a id="wrapper-types"></a>

### 包装器类型

有几种与 JavaScript 基本类型相关的类型*绝不应该*
使用：

-   `String`、`Boolean` 和 `Number` 与对应的基本类型
    `string`、`boolean` 和 `number` 的含义略有不同。始终
    使用小写版本。
-   `Object` 与 `{}` 和 `object` 都有相似之处，但稍宽松。
    若类型要包含除 `null` 和 `undefined` 之外的一切值，
    请使用 `{}`；若要进一步排除其他基本类型（即上述
    三种，外加 `symbol` 和 `bigint`），请使用小写的 `object`。

此外，切勿将包装器类型作为构造函数调用（即使用 `new`）。

<div class="numbered"></div>

<a id="return-type-only-generics"></a>

### 仅用于返回类型的泛型

避免创建带有仅用于返回类型的泛型的 API。使用
带有仅用于返回类型的泛型的既有 API 时，始终显式指定
泛型。

<a id="appendices-style-related-tools"></a>

<div class="numbered"></div>

<a id="toolchain-requirements"></a>

## 工具链要求

Google style 要求以特定方式使用若干工具，概述如下。

<a id="google-format"></a>
<a id="use-the-google3-formatter"></a>
<a id="source-code-formatting"></a>
<a id="appendices-clang-format"></a>
<a id="formatting"></a>
<a id="formatting-array-literals"></a>
<a id="formatting-block-indentation"></a>
<a id="formatting-column-limit"></a>
<a id="formatting-empty-blocks"></a>
<a id="formatting-function-expressions"></a>
<a id="formatting-nonempty-blocks"></a>
<a id="formatting-object-literals"></a>
<a id="formatting-one-statement-perline"></a>
<a id="formatting-statements"></a>
<a id="formatting-switch-statements"></a>
<a id="formatting-vertical-whitespace"></a>
<a id="formatting-whitespace"></a>

<div class="numbered"></div>

<a id="typescript-compiler"></a>

### TypeScript 编译器

所有 TypeScript 文件都必须通过标准工具链的类型检查。

<div class="numbered"></div>

<a id="ts-ignore"></a>

#### @ts-ignore

不要使用 `@ts-ignore`，也不要使用其变体 `@ts-expect-error` 或 `@ts-nocheck`。

为什么？

它们表面上似乎是“修复”编译器错误的简便方法，但
实际上，某个具体的编译器错误往往由更大的问题引起，
而那个问题可以更直接地修复。

例如，如果你用 `@ts-ignore` 来抑制某个类型错误，就
很难预测周边代码最终会看到什么类型。对于许多
类型错误，[如何最好地使用 `any`](#any) 中的建议很有用。

你可以在单元测试中使用 `@ts-expect-error`，不过通常*不应该*。
`@ts-expect-error` 会抑制所有错误。很容易意外地过度匹配，
从而抑制更严重的错误。可考虑以下做法之一：

-   在测试需要在运行时处理未经检查的值的 API 时，
    添加向预期类型或 `any` 的强制转换，并附上解释性注释。
    这样可把错误抑制限制在单个表达式内。
-   抑制静态检查警告并说明原因，类似于
    [抑制 `any` 静态检查警告](#any-suppress)。

<a id="appendices-conformance-framework"></a>

<div class="numbered"></div>

<a id="conformance"></a>

### 一致性

Google TypeScript 包含若干*一致性框架*，
[tsetse](https://tsetse.info) 和 [tsec](https://github.com/google/tsec)。

这些规则通常用于强制执行关键限制（例如定义
全局变量，这可能破坏代码库）以及安全模式（例如使用
`eval` 或给 `innerHTML` 赋值），或者更宽松地用于提升代码质量。

Google-style TypeScript 必须遵守所有适用的全局或框架局部
一致性规则。

<a id="jsdoc"></a>
<a id="formatting-comments"></a>

<div class="numbered"></div>

<a id="comments-documentation"></a>

## 注释与文档

<div class="numbered"></div>

<a id="jsdoc-vs-comments"></a>

#### JSDoc 与普通注释

注释分为两类：JSDoc（`/** ... */`）和非 JSDoc 的普通
注释（`// ...` 或 `/* ... */`）。

*   使用 `/** JSDoc */` 注释来撰写文档，即代码用户
    应当阅读的注释。
*   使用 `// line comments` 作为实现注释，即只
    涉及代码自身实现的注释。

JSDoc 注释能被工具（例如编辑器和文档生成器）
理解，而普通注释只面向其他人类读者。

<a id="formatting-block-comment-style"></a>

<div class="numbered"></div>

<a id="multi-line-comments"></a>

#### 多行注释

多行注释的缩进级别与外围代码相同。它们
*必须*使用多个单行注释（`//` 风格），而不是块注释风格
（`/* */`）。

<div class='goodcode'></div>

```ts
// This is
// fine
```

<div class='badcode'></div>

```ts
/*
 * This should
 * use multiple
 * single-line comments
 */

/* This should use // */
```

注释不应被由星号或其他字符绘制的方框包围。

<div class="numbered"></div>

<a id="jsdoc-general-form"></a>

### JSDoc 通用形式

JSDoc 注释的基本格式如下例所示：

<div class='goodcode'></div>

```ts
/**
 * Multiple lines of JSDoc text are written here,
 * wrapped normally.
 * @param arg A number to do something to.
 */
function doSomething(arg: number) { … }
```

或如下面这个单行示例：

<div class='goodcode'></div>

```ts
/** This short jsdoc describes the function. */
function doSomething(arg: number) { … }
```

如果单行注释溢出为多行，则*必须*使用
多行风格，让 `/**` 和 `*/` 各自独占一行。

许多工具会从 JSDoc 注释中提取元数据，以执行代码校验和
优化。因此，这些注释*必须*格式良好。

<div class="numbered"></div>

<a id="jsdoc-markdown"></a>

### Markdown

JSDoc 用 Markdown 书写，不过在必要时*可以*包含 HTML。

这意味着解析 JSDoc 的工具会忽略纯文本格式，因此如果
你这样写：

<div class='badcode'></div>

```ts
/**
 * Computes weight based on three factors:
 *   items sent
 *   items received
 *   last timestamp
 */
```

它会被渲染成这样：

```
Computes weight based on three factors: items sent items received last timestamp
```

应当改写为 Markdown 列表：

<div class='goodcode'></div>

```ts
/**
 * Computes weight based on three factors:
 *
 * - items sent
 * - items received
 * - last timestamp
 */
```

<div class="numbered"></div>

<a id="jsdoc-tags"></a>

### JSDoc 标签

Google style 只允许使用 JSDoc 标签的一个子集。多数标签必须
独占一行，且标签位于行首。

<div class='goodcode'></div>

```ts
/**
 * The "param" tag must occupy its own line and may not be combined.
 * @param left A description of the left param.
 * @param right A description of the right param.
 */
function add(left: number, right: number) { ... }
```

<div class='badcode'></div>

```ts
/**
 * The "param" tag must occupy its own line and may not be combined.
 * @param left @param right
 */
function add(left: number, right: number) { ... }
```

<div class="numbered"></div>

<a id="jsdoc-line-wrapping"></a>

### 换行

换行的块标签缩进四个空格。换行的描述文本*可以*
与前面几行的描述对齐，但这种水平对齐
并不推荐。

<div class='goodcode'></div>

```ts
/**
 * Illustrates line wrapping for long param/return descriptions.
 * @param foo This is a param with a particularly long description that just
 *     doesn't fit on one line.
 * @return This returns something that has a lengthy description too long to fit
 *     in one line.
 */
exports.method = function(foo) {
  return 5;
};
```

在换行书写 `@desc` 或 `@fileoverview` 描述时不要缩进。

<div class="numbered"></div>

<a id="document-all-top-level-exports-of-modules"></a>

### 为模块的所有顶层导出编写文档

使用 `/** JSDoc */` 注释向代码用户传达信息。
避免只是重复属性或参数的名称。你也*应该*
为所有目的无法从名称立即看出的属性和方法（无论是否
导出/公开）编写文档，具体由评审者判断。

**例外：**仅为了供工具消费而导出的符号，例如
@NgModule 类，不需要注释。

<div class="numbered"></div>

<a id="jsdoc-class-comments"></a>

### 类的注释

类的 JSDoc 注释应为读者提供足够的信息，使其
了解如何以及何时使用该类，并说明正确使用该类
所需的其他注意事项。构造函数上的文字描述可以
省略。

<div class="numbered"></div>

<a id="method-and-function-comments"></a>

### 方法与函数的注释

如果方法、参数和返回值的描述从方法其余的 JSDoc
或从方法名称与类型签名中即可看出，则可以省略。

方法描述以一个描述方法行为的动词短语开头。
该短语不是祈使句，而是以第三人称书写，
仿佛前面隐含了 "This method ..."。

<div class="numbered"></div>

<a id="parameter-property-comments"></a>

### 参数属性的注释

一个
[参数属性](https://www.typescriptlang.org/docs/handbook/2/classes.html#parameter-properties)
是指以 `private`、`protected`、`public` 或 `readonly`
之一为前缀的构造函数参数。参数属性同时声明
一个参数和一个实例属性，并隐式向其赋值。例如，
`constructor(private readonly foo: Foo)` 声明构造函数接受
一个参数 `foo`，同时还声明了一个私有的只读属性 `foo`，
并在执行构造函数其余部分之前，把该参数赋给
这个属性。

要为这些字段编写文档，请使用 JSDoc 的 `@param` 注解。
编辑器会在构造函数调用和属性访问处显示该描述。

<div class='goodcode'></div>

```ts
/** This class demonstrates how parameter properties are documented. */
class ParamProps {
  /**
   * @param percolator The percolator used for brewing.
   * @param beans The beans to brew.
   */
  constructor(
    private readonly percolator: Percolator,
    private readonly beans: CoffeeBean[]) {}
}
```

<div class='goodcode'></div>

```ts
/** This class demonstrates how ordinary fields are documented. */
class OrdinaryClass {
  /** The bean that will be used in the next call to brew(). */
  nextBean: CoffeeBean;

  constructor(initialBean: CoffeeBean) {
    this.nextBean = initialBean;
  }
}
```

<a id="omit-comments-that-are-redundant-with-typescript"></a>
<a id="do-not-use-override"></a>

<div class="numbered"></div>

<a id="jsdoc-type-annotations"></a>

### JSDoc 类型注解

JSDoc 类型注解在 TypeScript 源代码中是多余的。不要在
`@param` 或 `@return` 块中声明类型，也不要在
使用了 `implements`、`enum`、`private`、`override` 等
关键字的代码上写 `@implements`、`@enum`、`@private`、`@override` 等。

<div class="numbered"></div>

<a id="redundant-comments"></a>

### 让注释真正提供信息

对于未导出的符号，有时函数或参数的名称和类型
已经足够。不过，代码*通常*会从比单纯变量名
更多的文档中受益！

*   避免只是重复参数名称和类型的注释，例如

    <div class='badcode'></div>

    ```ts
    /** @param fooBarService The Bar service for the Foo application. */
    ```

*   由于这条规则，`@param` 和 `@return` 行仅在
    能提供信息时才需要，否则*可以*省略。

    <div class='goodcode'></div>

    ```ts
    /**
     * POSTs the request to start coffee brewing.
     * @param amountLitres The amount to brew. Must fit the pot size!
     */
    brew(amountLitres: number, logger: Logger) {
      // ...
    }
    ```

<a id="formatting-param-name-comments"></a>

<div class="numbered"></div>

<a id="comments-when-calling-a-function"></a>

#### 调用函数时的注释

当方法名和参数值不足以传达该参数的含义时，
应使用“参数名”注释。

在添加这类注释之前，可考虑重构该方法，使其改为
接收一个接口并对其进行解构，以大幅提升调用点的可读性。

“参数名”注释放在参数值之前，并包含
参数名以及 `=` 后缀：

<div class='goodcode'></div>

```ts
someFunction(obviousParam, /* shouldRender= */ true, /* name= */ 'hello');
```

既有代码可能使用旧式的参数名注释风格，把这些
注释放在参数值~之后~并省略 `=`。在同一文件内
为保持一致而继续使用该风格是可以接受的。

```ts
someFunction(obviousParam, true /* shouldRender */, 'hello' /* name */);
```

<div class="numbered"></div>

<a id="place-documentation-prior-to-decorators"></a>

### 将文档置于装饰器之前

当类、方法或属性同时带有 `@Component` 之类的装饰器和
JsDoc 时，请务必把 JsDoc 写在装饰器之前。

*   不要把 JsDoc 写在装饰器和被装饰的语句之间。

    <div class='badcode'></div>

    ```ts
    @Component({
      selector: 'foo',
      template: 'bar',
    })
    /** Component that prints "bar". */
    export class FooComponent {}
    ```

*   把 JsDoc 块写在装饰器之前。

    <div class='goodcode'></div>

    ```ts
    /** Component that prints "bar". */
    @Component({
      selector: 'foo',
      template: 'bar',
    })
    export class FooComponent {}
    ```

<div class="numbered"></div>

<a id="policies"></a>

## 策略

<a id="policies-be-consistent"></a>
<a id="policies-newly-added-code-use-google-style"></a>

<div class="numbered"></div>

<a id="consistency"></a>

### 一致性

对于本规范未明确规定的任何风格问题，请沿用
同一文件中其他代码已有的做法（“保持一致”）。如果
这样仍无法解决问题，可考虑仿照同一目录中的
其他文件。

全新的文件*必须*使用 Google Style，无论同一包中
其他文件采用了怎样的风格选择。向不符合 Google Style
的文件添加新代码时，建议先重新格式化已有代码，
但须遵循[下文](#reformatting-existing-code)中的建议。
如果不做这种重新格式化，新代码*应该*尽可能与同一
文件中的既有代码保持一致，但*不得*违反风格指南。

<a id="policies-code-not-in-google-style"></a>
<a id="policies-reformatting-existing-code"></a>

<div class="numbered"></div>

<a id="reformatting-existing-code"></a>

#### 重新格式化已有代码

你偶尔会在代码库中遇到并未严格遵循
Google Style 的文件。这些文件可能来自收购，也可能是
在 Google Style 就某个问题给出立场之前编写的，
也可能出于其他任何原因采用非 Google Style 的写法。

更新已有代码的风格时，请遵循以下指南。

1.  不要求把所有已有代码都改成符合当前的风格
    指南。重新格式化已有代码是在代码改动量与一致性
    之间做权衡。风格规则会随时间演进，这类为保持
    合规而做的微调会带来不必要的改动。不过，如果对
    某个文件进行了重大修改，就应让该文件符合
    Google Style。
1.  注意不要让顺手做的风格修正冲淡 CL 的重点。
    如果你发现自己做了很多对 CL 核心目标并不关键的
    风格改动，就把这些改动提到单独的 CL 中。

<a id="policies-deprecation"></a>

<div class="numbered"></div>

<a id="deprecation"></a>

### 弃用

用 `@deprecated` JSDoc 注解标记已弃用的方法、类或
接口。弃用注释必须包含简单、清晰的指引，
以便人们修改调用点。

<a id="policies-generated-code-mostly-exempt"></a>

<div class="numbered"></div>

<a id="generated-code"></a>

### 生成的代码：大多豁免

构建过程生成的源代码不必符合 Google Style。
不过，任何会被手写源代码引用的生成标识符
都必须遵循命名要求。作为一项特殊例外，
这类标识符允许包含下划线，这有助于
避免与手写标识符冲突。

<a id="goals"></a>

<div class="numbered"></div>

<a id="style-guide-goals"></a>

#### 风格指南的目标

一般来说，工程师通常最清楚自己的代码需要什么，
因此如果存在多种选择且取舍视情况而定，我们应该
让决策在本地做出。所以默认答案应是“省略它”。

以下几项是例外，也正是我们制定某些
全局规则的理由。请对照以下几点评估你的风格指南提案：

1.  **代码应避免已知会引发问题的模式，尤其是
    对语言新手而言。**

2.  **不同项目的代码应在无关的差异上保持一致。**

    当两种选项在表面上看等价时，我们应当考虑
    只选其一，以免毫无理由地朝不同方向演化，
    并避免在代码评审中产生无谓的争论。

    示例：

    -   名称的大小写风格。
    -   `x as T` 语法与等价的 `<T>x` 语法（不允许）。
    -   `Array<[number, number]>` 与 `[number, number][]`。

3.  **代码应当易于长期维护。**

    代码的存活时间通常长于原作者参与开发的时间，
    而 TypeScript 团队必须让 Google 的一切在未来正常运转。

    示例：

    -   我们用软件自动修改代码，因此代码会自动格式化，
        以便软件轻松满足空白规则。
    -   我们要求统一的一组编译器标志，这样给定的 TS 库
        就能假定一组特定的标志来编写，用户也始终能
        安全地使用一个共享库。
    -   代码必须导入它所使用的库（“严格依赖”），以便
        依赖项中的重构不会改变其使用者的依赖关系。
    -   我们要求用户编写测试。没有测试，我们就无法确信
        对语言所做的改动不会破坏用户。

4.  **代码评审者应专注于提升代码质量，而不是
    执行任意的规则。**

    如果能把你的规则实现为自动检查，这通常
    是个好兆头。这也支持原则 3。

    如果某件事真的无关紧要——比如它属于语言中
    某个冷僻角落，或者只是规避一个不太可能发生的缺陷——
    那大概就值得省略。
