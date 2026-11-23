# Google JavaScript 风格指南

> **重要：本指南已不再更新。Google 建议
> 迁移到 TypeScript，并遵循 <a href="tsguide.html">TypeScript
> 指南</a>。**

* TOC
{:toc}

<a id="introduction"></a>

## 1 简介

本文档是 Google 针对 JavaScript 编程语言源代码的编码标准的
**完整**定义。一个 JavaScript 源文件被描述为*符合 Google 风格*，
当且仅当它遵守本文所述的
规则。

与其他编程风格指南一样，本文涉及的问题不仅包括
格式方面的美观问题，还包括其他类型的约定或编码标准。
不过，本文档主要聚焦于我们普遍遵守的硬性规则，
避免给出无法明确强制执行的建议（无论由人工
还是工具）。

<a id="terminology-notes"></a>

### 1.1 术语说明

在本文档中，除非另有说明：

1.  术语 *comment* 始终指*实现*注释。我们不使用
    “文档注释”这一说法，而是用通用术语 “JSDoc”
    来同时指代 `/** …
    */` 中可供人阅读的文本和机器可读的注解。
2.  本风格指南在使用下列措辞时采用
    [RFC 2119](http://tools.ietf.org/html/rfc2119) 的术语：*must*、*must not*、*should*、*should
    not* 和 *may*。*prefer* 和 *avoid* 分别对应 *should* 和
    *should not*。祈使句和陈述句具有规定性，
    对应 *must*。

其他“术语说明”会在本文档中偶尔出现。

<a id="guide-notes"></a>

### 1.2 指南说明

本文档中的示例代码是**非规范性的**。也就是说，虽然示例
符合 Google 风格，但它们可能并未展示表示代码的*唯一*
符合风格的方式。示例中做出的可选格式选择不得被当作
规则来强制执行。

<a id="source-file-basics"></a>

## 2 源文件基础

<a id="file-name"></a>

### 2.1 文件名

文件名必须全部小写，可以包含下划线（`_`）或连字符
（`-`），但不能包含其他标点符号。请遵循你的项目所使用的
约定。文件名的扩展名必须是 `.js`。

<a id="file-encoding"></a>

### 2.2 文件编码：UTF-8

源文件一律采用 **UTF-8** 编码。

<a id="special-characters"></a>

### 2.3 特殊字符

<a id="whitespace-characters"></a>

#### 2.3.1 空白字符

除行终止符序列外，ASCII 水平空格字符
（0x20）是源文件中唯一可以出现的空白字符。
这意味着

1.  字符串字面量中的所有其他空白字符都要转义，且
2.  制表符**不得**用于缩进。

<a id="special-escape-sequences"></a>

#### 2.3.2 特殊转义序列

对于任何具有特殊转义序列的字符（`\'`、`\"`、`\\`、`\b`、
`\f`、`\n`、`\r`、`\t`、`\v`），都应使用该序列，而不是
对应的数字转义（例如 `\x0a`、`\u000a` 或 `\u{a}`）。绝不使用
遗留的八进制转义。

<a id="non-ascii-characters"></a>

#### 2.3.3 非 ASCII 字符

对于其余的非 ASCII 字符，可以使用实际的 Unicode 字符
（例如 `∞`）或等价的十六进制或 Unicode 转义（例如 `\u221e`），
仅取决于哪种方式让代码**更易于阅读和理解**。

> 提示：在使用 Unicode 转义时，有时即便使用了实际的
> Unicode 字符，加一条解释性注释也会很有帮助。

<div class='goodcode'></div>

```js
/* Best: perfectly clear even without a comment. */
const units = 'μs';

/* Allowed: but unnecessary as μ is a printable character. */
const units = '\u03bcs'; // 'μs'

/* Good: use escapes for non-printable characters with a comment for clarity. */
return '\ufeff' + content;  // Prepend a byte order mark.
```

<div class='badcode'></div>

```js
/* Poor: the reader has no idea what character this is. */
const units = '\u03bcs';
```

> 提示：绝不要仅仅因为担心某些程序可能无法正确处理非 ASCII 字符，
> 就降低代码的可读性。如果确实出现这种情况，说明那些
> 程序是**有缺陷的**，必须**修复**它们。

<a id="source-file-structure"></a>

## 3 源文件结构

所有新的源文件都应当是 `goog.module` 文件（即包含
`goog.module` 调用的文件），或者是 ECMAScript（ES）模块（使用 `import` 和 `export`
语句）。

文件由以下部分组成，**按顺序**排列：

1.  许可证或版权信息（如果存在）
2.  `@fileoverview` JSDoc（如果存在）
3.  `goog.module` 语句（如果是 `goog.module` 文件）
4.  ES `import` 语句（如果是 ES 模块）
5.  `goog.require` 和 `goog.requireType` 语句
6.  文件的实现

**恰好一个空行**用于分隔每个存在的部分，但文件的
实现之前可以有 1 个或 2 个空行。

<a id="file-copyright"></a>

### 3.1 许可证或版权信息（如果存在）

如果文件中应包含许可证或版权信息，就放在这里。

<a id="file-fileoverview"></a>

### 3.2 `@fileoverview` JSDoc（如果存在）

参见 [7.5 顶层/文件级注释](#jsdoc-top-file-level-comments) 中的格式
规则。

<a id="file-goog-module"></a>

### 3.3 `goog.module` 语句

所有 `goog.module` 文件必须在单独一行上声明恰好一个 `goog.module` 名称：
包含 `goog.module` 声明的行不得换行，因此是 80 列限制的
一个例外。

`goog.module` 的整个实参定义了命名空间。它是
包名（一个反映代码所在目录结构片段的标识符），
再加上可选的、它所定义的主类/枚举/接口，以 `lowerCamelCase` 形式
拼接在末尾。

示例：

<div class='goodcode'></div>

```js
goog.module('search.urlHistory.urlHistoryService');
```

<a id="naming-hierarchy"></a>

#### 3.3.1 层次结构

模块命名空间绝不能命名为另一个模块
命名空间的*直接*子级。

不允许：

<div class='badcode'></div>

```js
goog.module('foo.bar');   // 'foo.bar.qux' would be fine, though
goog.module('foo.bar.baz');
```

目录层次结构反映命名空间的层次结构，因此嵌套更深的
子级是上层父目录的子目录。请注意，这意味着
“parent” 命名空间组的所有者必然了解所有子命名空间，
因为它们位于同一目录中。

<a id="file-declare-legacy-namespace"></a>

#### 3.3.2 `goog.module.declareLegacyNamespace`

唯一的 `goog.module` 语句后面可以选择调用
`goog.module.declareLegacyNamespace();`。应尽可能避免
`goog.module.declareLegacyNamespace()`。

示例：

<div class='goodcode'></div>

```js
goog.module('my.test.helpers');
goog.module.declareLegacyNamespace();
goog.setTestOnly();
```

`goog.module.declareLegacyNamespace` 的存在是为了简化从
传统的基于对象层次结构的命名空间过渡，但附带一些命名
限制。由于子模块名称必须在父命名空间之后创建，该名称
**不得**是其他任何 `goog.module` 的子级或父级（例如，
`goog.module('parent');` 和
`goog.module('parent.child');` 不能同时安全地存在，
`goog.module('parent');` 和 `goog.module('parent.child.grandchild');` 也不能）。

<a id="file-goog-module-exports"></a>

#### 3.3.3 `goog.module` 导出

类、枚举、函数、常量以及其他符号都通过
`exports` 对象导出。导出的符号可以直接定义在 `exports`
对象上，也可以在局部声明后单独导出。只有当符号
打算在模块外部使用时才将其导出。未导出的模块局部
符号不声明为 `@private`。导出符号与模块局部符号之间
没有规定的顺序。

示例：

<div class='goodcode'></div>

```js
const /** !Array<number> */ exportedArray = [1, 2, 3];

const /** !Array<number> */ moduleLocalArray = [4, 5, 6];

/** @return {number} */
function moduleLocalFunction() {
  return moduleLocalArray.length;
}

/** @return {number} */
function exportedFunction() {
  return moduleLocalFunction() * 2;
}

exports = {exportedArray, exportedFunction};
```

<div class='goodcode'></div>

```js
/** @const {number} */
exports.CONSTANT_ONE = 1;

/** @const {string} */
exports.CONSTANT_TWO = 'Another constant';
```

不要将 `exports` 对象标注为 `@const`，因为编译器已经把它
当作常量处理。

<div class='badcode'></div>

```js
/** @const */
exports = {exportedFunction};
```

不要使用默认导出，因为它们不容易对应到 ES 模块的
语义。

<div class='badcode'></div>

```js
exports = FancyClass;
```

<a id="file-es6-modules"></a>
<a id="file-es-modules"></a>

### 3.4 ES 模块

ES 模块是使用 `import` 和 `export` 关键字的文件。

<a id="es6-module-imports"></a>
<a id="es-module-imports"></a>

#### 3.4.1 导入

导入语句不得换行，因此是 80 列限制
的一个例外。

<a id="es6-import-paths"></a>
<a id="esm-import-paths"></a>

##### 3.4.1.1 导入路径

ES 模块文件必须使用 `import` 语句来导入其他 ES 模块文件。
不要用 `goog.require` 导入另一个 ES 模块。

<div class='goodcode'></div>

```js
import './sideeffects.js';

import * as goog from '../closure/goog/goog.js';
import * as parent from '../parent.js';

import {name} from './sibling.js';
```

<a id="es6-import-paths-file-extension"></a>
<a id="esm-import-paths-file-extension"></a>

###### 3.4.1.1.1 导入路径中的文件扩展名

导入路径中的 `.js` 文件扩展名不是可选的，必须始终
包含。

<div class='badcode'></div>

```js
import '../directory/file';
```

<div class='goodcode'></div>

```js
import '../directory/file.js';
```

<a id="importing-the-same-file-multiple-times"></a>

##### 3.4.1.2 多次导入同一文件

不要多次导入同一个文件。这会让文件的全部导入
难以确定。

<div class='badcode'></div>

```js
// Imports have the same path, but since it doesn't align it can be hard to see.
import {short} from './long/path/to/a/file.js';
import {aLongNameThatBreaksAlignment} from './long/path/to/a/file.js';
```

<a id="naming-es6-imports"></a>
<a id="naming-esm-imports"></a>

##### 3.4.1.3 导入的命名

<a id="naming-module-imports"></a>

###### 3.4.1.3.1 模块导入的命名

模块导入名称（`import * as name`）是 `lowerCamelCase` 名称，
由被导入的文件名派生而来。

<div class='goodcode'></div>

```js
import * as fileOne from '../file-one.js';
import * as fileTwo from '../file_two.js';
import * as fileThree from '../filethree.js';
```

<div class='goodcode'></div>

```js
import * as libString from './lib/string.js';
import * as math from './math/math.js';
import * as vectorMath from './vector/math.js';
```

有些库可能普遍使用违反此命名方案的命名空间导入前缀，
但其在开源社区中压倒性的普遍用法让这种违规
风格更具可读性。目前唯一适用此例外的库是
[threejs](https://threejs.org/)，它使用 `THREE` 前缀。

<a id="naming-default-imports"></a>

###### 3.4.1.3.2 默认导入的命名

默认导入名称由被导入的文件名派生而来，并遵循
[6.2 按标识符类型的规则](#naming-rules-by-identifier-type) 中的规则。

<div class='goodcode'></div>

```js
import MyClass from '../my-class.js';
import myFunction from '../my_function.js';
import SOME_CONSTANT from '../someconstant.js';
```

注意：一般情况下不应出现这种情况，因为本风格指南禁止
默认导出，参见 [3.4.2.1 具名导出与默认导出](#named-vs-default-exports)。
默认导入仅用于导入不符合本风格指南的
模块。

<a id="naming-named-imports"></a>

###### 3.4.1.3.3 具名导入的命名

一般来说，通过具名导入（`import {name}`）引入的符号应保持
同名。避免给导入起别名（`import {SomeThing as SomeOtherThing}`）。
名称冲突应优先通过使用模块导入（`import *`）或重命名
导出本身来解决。

<div class='goodcode'></div>

```js
import * as bigAnimals from './biganimals.js';
import * as domesticatedAnimals from './domesticatedanimals.js';

new bigAnimals.Cat();
new domesticatedAnimals.Cat();
```

如果确实需要重命名具名导入，则应在得到的别名中使用
被导入模块文件名或路径中的组成部分。

<div class='goodcode'></div>

```js
import {Cat as BigCat} from './biganimals.js';
import {Cat as DomesticatedCat} from './domesticatedanimals.js';

new BigCat();
new DomesticatedCat();
```

<a id="es6-module-exports"></a>
<a id="es-module-exports"></a>

#### 3.4.2 导出

只有当符号打算在模块外部使用时才将其导出。
未导出的模块局部符号不声明为 `@private`。导出符号与
模块局部符号之间没有规定的顺序。

<a id="named-vs-default-exports"></a>

##### 3.4.2.1 具名导出与默认导出

所有代码都使用具名导出。可以把 `export` 关键字用于
声明，也可以使用 `export {name};` 语法。

不要使用默认导出。导入方模块必须为这些值指定名称，
这可能导致各模块之间命名不一致。

<div class='badcode'></div>

```js
// Do not use default exports:
export default class Foo { ... } // BAD!
```

<div class='goodcode'></div>

```js
// Use named exports:
export class Foo { ... }
```

<div class='goodcode'></div>

```js
// Alternate style named exports:
class Foo { ... }

export {Foo};
```

<a id="es6-exports-mutability"></a>
<a id="esm-exports-mutability"></a>

##### 3.4.2.2 导出的可变性

导出的变量不得在模块初始化之外被修改。

如果确实需要修改，也有其他做法，包括导出一个指向
带有可变字段的对象的常量引用，或者导出针对可变数据的
访问器函数。

<div class='badcode'></div>

```js
// Bad: both foo and mutateFoo are exported and mutated.
export let /** number */ foo = 0;

/**
 * Mutates foo.
 */
export function mutateFoo() {
  ++foo;
}

/**
 * @param {function(number): number} newMutateFoo
 */
export function setMutateFoo(newMutateFoo) {
  // Exported classes and functions can be mutated!
  mutateFoo = () => {
    foo = newMutateFoo(foo);
  };
}
```

<div class='goodcode'></div>

```js
// Good: Rather than export the mutable variables foo and mutateFoo directly,
// instead make them module scoped and export a getter for foo and a wrapper for
// mutateFooFunc.
let /** number */ foo = 0;
let /** function(number): number */ mutateFooFunc = (foo) => foo + 1;

/** @return {number} */
export function getFoo() {
  return foo;
}

export function mutateFoo() {
  foo = mutateFooFunc(foo);
}

/** @param {function(number): number} mutateFoo */
export function setMutateFoo(mutateFoo) {
  mutateFooFunc = mutateFoo;
}
```

<a id="es6-module-circular-dependencies"></a>
<a id="es-module-export-from"></a>

##### 3.4.2.3 export from

`export from` 语句不得换行，因此是 80 列限制的
一个例外。此规则适用于两种 `export from` 形式。

<div class='goodcode'></div>

```js
export {specificName} from './other.js';
export * from './another.js';
```

<a id="es-module-circular-dependencies"></a>

#### 3.4.3 ES 模块中的循环依赖

不要在 ES 模块之间制造循环，即便 ECMAScript
规范允许这样做。请注意，`import` 和 `export` 语句
都可能造成循环。

<div class='badcode'></div>

```js
// a.js
import './b.js';
```

<div class='badcode'></div>

```js
// b.js
import './a.js';

// `export from` can cause circular dependencies too!
export {x} from './c.js';
```

<div class='badcode'></div>

```js
// c.js
import './b.js';

export let x;
```

<a id="es6-module-closure-interop"></a>
<a id="es-module-closure-interop"></a>

#### 3.4.4 与 Closure 互操作

<a id="es6-module-referencing-goog"></a>
<a id="es-module-referencing-goog"></a>

##### 3.4.4.1 引用 goog

要引用 Closure 的 `goog` 命名空间，请导入 Closure 的 `goog.js`。

<div class='goodcode'></div>

```js
import * as goog from '../closure/goog/goog.js';

const {compute} = goog.require('a.name');

export const CONSTANT = compute();
```

`goog.js` 只导出全局 `goog` 中可在 ES 模块里使用的
一部分属性。

<a id="goog-require-in-es6-module"></a>
<a id="goog-require-in-es-module"></a>

##### 3.4.4.2 ES 模块中的 goog.require

`goog.require` 在 ES 模块中的行为与在 `goog.module` 文件中相同。
可以引入任何 Closure 命名空间符号（即由 `goog.provide` 或
`goog.module` 创建的符号），`goog.require` 会返回其值。

<div class='goodcode'></div>

```js
import * as goog from '../closure/goog/goog.js';
import * as anEsModule from './anEsModule.js';

const GoogPromise = goog.require('goog.Promise');
const myNamespace = goog.require('my.namespace');
```

<a id="closure-module-id-in-es6-module"></a>
<a id="closure-module-id-in-es-module"></a>

##### 3.4.4.3 在 ES 模块中声明 Closure 模块 ID

`goog.declareModuleId` 可在 ES 模块中使用，用于声明一个类似
`goog.module` 的模块 ID。这意味着该模块 ID 可以被
`goog.require`d、`goog.module.get`d 等，就像它是一个
未调用 `goog.module.declareLegacyNamespace` 的 `goog.module`。它不会
把该模块 ID 创建为全局可用的 JavaScript 符号。

对来自 `goog.declareModuleId` 的模块 ID，
`goog.require`（或 `goog.module.get`）始终返回模块对象
（就像它是 `import *`'d 一样）。因此，`goog.declareModuleId` 的
实参应始终以 `lowerCamelCaseName` 结尾。

注意：在 ES 模块中调用 `goog.module.declareLegacyNamespace` 是错误的，
它只能在 `goog.module` 文件中调用。没有直接的办法
把“legacy”命名空间与 ES 模块关联起来。

`goog.declareModuleId` 只应在原地升级 Closure 文件为 ES
模块时使用，且使用具名导出。

<div class='goodcode'></div>

```js
import * as goog from '../closure/goog.js';

goog.declareModuleId('my.esm');

export class Class {};
```

<a id="file-set-test-only"></a>

### 3.5 `goog.setTestOnly`

在 `goog.module` 文件中，`goog.module` 语句以及（如果存在）
`goog.module.declareLegacyNamespace()` 语句后面可以选择
调用 `goog.setTestOnly()`。

在 ES 模块中，`import` 语句后面可以选择调用
`goog.setTestOnly()`。

<a id="file-goog-require"></a>

### 3.6 `goog.require` 与 `goog.requireType` 语句

导入通过 `goog.require` 和 `goog.requireType` 语句完成。
由 `goog.require` 语句导入的名称既可用于代码，也可用于
类型注解；而由 `goog.requireType` 导入的名称只能用于
类型注解。

`goog.require` 和 `goog.requireType` 语句构成一个连续的代码块，
中间没有空行。该块位于 `goog.module` 声明之后，
[以一个空行分隔](#source-file-structure)。`goog.require` 或
`goog.requireType` 的整个实参是由单独文件中的 `goog.module`
定义的命名空间。`goog.require` 和 `goog.requireType` 语句不得
出现在文件的其他任何位置。

每个 `goog.require` 或 `goog.requireType` 都赋给一个常量
别名，或者解构为多个常量别名。这些别名是在类型注解或代码
中引用依赖的唯一可接受方式。任何地方都不得使用完全
限定的命名空间，除非作为 `goog.require` 或
`goog.requireType` 的实参。

**例外**：在 externs 文件中声明的类型、变量和函数在
类型注解和代码中必须使用其完全限定名称。

当 `goog.require` 被赋给单个常量别名时，该别名必须与
被导入模块命名空间的最后一个以点分隔的组成部分一致。

**例外**：在某些情况下，可以使用命名空间中额外的组成部分
构成更长的别名。得到的别名必须保留原标识符的
大小写，以便仍正确地标识其类型。更长的别名可用于
区分本来完全相同的别名，或者在能显著提升可读性时
使用。此外，必须使用更长的别名来避免遮蔽原生类型，
例如 `Element`、`Event`、`Error`、`Map` 和
`Promise`（更完整的列表参见 MDN 上的
[标准内置对象](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects)
以及 [Web APIs](https://developer.mozilla.org/en-US/docs/Web/API)）。

重命名解构别名时，冒号后必须跟一个空格，具体参见
[4.6.2 横向空白](#formatting-horizontal-whitespace)。

一个文件不应同时对同一命名空间包含 `goog.require` 和
`goog.requireType` 语句。如果导入的名称既用于代码又用于
类型注解，则应由单个 `goog.require` 语句导入。

如果导入某个模块只是为了其副作用，则该调用必须是
`goog.require`（而不是 `goog.requireType`），并且可以省略赋值。
必须用注释说明为何需要这样做，并抑制编译器
警告。

这些行按以下规则排序：左侧带有名称的所有 require
排在最前，并按这些名称的字母顺序排列。然后是
解构形式的 require，同样按左侧的名称排序。
最后是独立的 require 调用（通常对应那些仅为
副作用而导入的模块）。

> 提示：无需记住这个顺序并手动强制执行。你可以
> 依赖 IDE 报告排序不正确的 require。

如果较长的别名或模块名会让某一行超过 80 列限制，
也**不得**换行：require 行是 80 列
限制的例外。

示例：

<div class='goodcode'></div>

```js
// Standard alias style.
const asserts = goog.require('goog.asserts');
// Namespace-based alias used to disambiguate.
const testingAsserts = goog.require('goog.testing.asserts');
// Standard destructuring into aliases.
const {MyClass} = goog.require('some.package');
const {MyType} = goog.requireType('other.package');
const {clear, clone} = goog.require('goog.array');
const {Rgb} = goog.require('goog.color');
// Namespace-based destructuring into aliases used to disambiguate.
const {MyClass: NsMyClass} = goog.require('other.ns');
const {SomeType: FooSomeType} = goog.requireType('foo.types');
const {clear: objectClear, clone: objectClone} = goog.require('goog.object');
// Namespace-based destructuring into aliases used to prevent masking native type.
const {Element: RendererElement} = goog.require('web.renderer');
// Out of sequence namespace-based aliases used to improve readability.
// Also, require lines longer than 80 columns must not be wrapped.
const {SomeDataStructure: SomeDataStructureModel} = goog.requireType('identical.package.identifiers.models');
const {SomeDataStructure: SomeDataStructureProto} = goog.require('proto.identical.package.identifiers');
// goog.require without an alias in order to trigger side effects.
/** @suppress {extraRequire} Initializes MyFramework. */
goog.require('my.framework.initialization');
```

不鼓励：

<div class='badcode'></div>

```js
// Some legacy code uses a "default export" style to export a single class, enum,
// record type, etc. Do not use this pattern in new JS.
// When using a "default export", prefer destructuring into aliases.
const MyClass = goog.require('some.package.MyClass');
const MyType = goog.requireType('some.package.MyType');
```

<div class='badcode'></div>

```js
// If necessary to disambiguate, prefer PackageClass over SomeClass as it is
// closer to the format of the module name.
const SomeClass = goog.require('some.package.Class');
```

不允许：

<div class='badcode'></div>

```js
// Extra terms must come from the namespace.
const MyClassForBizzing = goog.require('some.package.MyClass');
// Alias must include the entire final namespace component.
const MyClass = goog.require('some.package.MyClassForBizzing');
// Alias must not mask native type (should be `const JspbMap` here).
const Map = goog.require('jspb.Map');
// Don't break goog.require lines over 80 columns.
const SomeDataStructure =
    goog.require('proto.identical.package.identifiers.SomeDataStructure');
// Alias must be based on the namespace.
const randomName = goog.require('something.else');
// Missing a space after the colon.
const {Foo:FooProto} = goog.require('some.package.proto.Foo');
// goog.requireType without an alias.
goog.requireType('some.package.with.a.Type');


/**
 * @param {!some.unimported.Dependency} param All external types used in JSDoc
 *     annotations must be goog.require'd, unless declared in externs.
 */
function someFunction(param) {
  // goog.require lines must be at the top level before any other code.
  const alias = goog.require('my.long.name.alias');
  // ...
}
```

<a id="file-implementation"></a>

### 3.7 文件的实现

实际的实现位于所有依赖信息声明之后
（至少以一个空行分隔）。

它可以包含任意模块局部声明（常量、变量、
类、函数等），以及任意导出的符号。

<a id="formatting"></a>

## 4 格式

**术语说明**：*block-like construct*（块状结构）指类、
函数、方法或以花括号分隔的代码块的主体。请注意，根据
[5.2 数组字面量](#features-array-literals) 和
[5.3 对象字面量](#features-object-literals)，任何数组或对象字面量
都可以选择视为块状结构。

> 提示：使用 `clang-format`。JavaScript 社区投入了精力，
> 以确保 clang-format 在 JavaScript 文件上「做正确的事」。
> `clang-format` 已与多款流行的编辑器集成。

<a id="formatting-braces"></a>

### 4.1 花括号

<a id="formatting-braces-all"></a>

#### 4.1.1 所有控制结构都使用花括号

所有控制结构（即 `if`、`else`、`for`、`do`、
`while` 以及任何其他控制结构）都必须使用花括号，即使
主体只包含一条语句。非空块的第一条语句必须独占一行。

不允许：

<div class='badcode'></div>

```js
if (someVeryLongCondition())
  doSomething();

for (let i = 0; i < foo.length; i++) bar(foo[i]);
```

**例外**：能完整放在一行且不换行、也没有 else 的简单
if 语句，在能提升可读性时可以保持单行并省略
花括号。这是控制结构唯一可以省略花括号和换行
的情形。

<div class='goodcode'></div>

```js
if (shortCondition()) foo();
```

<a id="formatting-nonempty-blocks"></a>

#### 4.1.2 非空块：K&R 风格

花括号遵循 Kernighan 和 Ritchie 风格
（即“[Egyptian brackets](https://blog.codinghorror.com/new-programming-jargon/#3)”）
用于*非空*块和块状结构：

*   左花括号前不换行。
*   左花括号后换行。
*   右花括号前换行。
*   右花括号后换行，*如果*该花括号结束一条语句、
    函数或类语句的主体，或一个类方法。具体来说，
    若其后紧跟 `else`、
    `catch`、`while`，或逗号、分号、右圆括号，则*不*换行。

示例：

<div class='goodcode'></div>

```js
class InnerClass {
  constructor() {}

  /** @param {number} foo */
  method(foo) {
    if (condition(foo)) {
      try {
        // Note: this might fail.
        something();
      } catch (err) {
        recover();
      }
    }
  }
}
```

<a id="formatting-empty-blocks"></a>

#### 4.1.3 空块：可以简洁

空块或块状结构*可以*在打开后立即闭合，中间
不含任何字符、空格或换行（即 `{}`），
**除非**它是*多块语句*的一部分（即直接包含
多个块的语句：`if`/`else` 或 `try`/`catch`/`finally`）。

示例：

<div class='goodcode'></div>

```js
function doNothing() {}
```

不允许：

<div class='badcode'></div>

```js
if (condition) {
  // …
} else if (otherCondition) {} else {
  // …
}

try {
  // …
} catch (e) {}
```

<a id="formatting-block-indentation"></a>

### 4.2 块缩进：+2 空格

每打开一个新的块或块状结构，缩进增加
两个空格。块结束时，缩进回到上一层
缩进级别。缩进级别适用于整个块内的代码和注释。
（参见
[4.1.2 非空块：K&R 风格](#formatting-nonempty-blocks) 中的示例）。

<a id="formatting-array-literals"></a>

#### 4.2.1 数组字面量：可选地视为“块状”

任何数组字面量都可以选择按“块状
结构”的格式排版。例如，以下写法都有效（**并非**
完整列表）：

<div class='goodcode'></div>

```js
const a = [
  0,
  1,
  2,
];

const b =
    [0, 1, 2];
```

<div class='goodcode'></div>

```js
const c = [0, 1, 2];

someMethod(foo, [
  0, 1, 2,
], bar);
```

也允许其他组合，特别是在强调元素之间的语义分组时，
但不应仅仅为了缩减较大数组的纵向尺寸而
使用。

<a id="formatting-object-literals"></a>

#### 4.2.2 对象字面量：可选地视为“块状”

任何对象字面量都可以选择按“块状
结构”的格式排版。同样的示例也适用于
[4.2.1 数组字面量：可选地视为“块状”](#formatting-array-literals)。
例如，以下写法都有效（**并非**完整列表）：

<div class='goodcode'></div>

```js
const a = {
  a: 0,
  b: 1,
};

const b =
    {a: 0, b: 1};
```

<div class='goodcode'></div>

```js
const c = {a: 0, b: 1};

someMethod(foo, {
  a: 0, b: 1,
}, bar);
```

<a id="formatting-class-literals"></a>

#### 4.2.3 类字面量

类字面量（无论是声明还是表达式）都按块来缩进。
不要在方法之后，或在类*声明*的右花括号之后
添加分号（包含类*表达式*的语句——例如赋值——
仍以分号结尾）。对于继承，除非父类是模板化的，
否则 `extends` 关键字就足够了。模板化类型的子类
必须在 `@extends` JSDoc 注解中显式指定模板类型，
即使只是沿用同一个模板名称。

示例：

<div class='goodcode'></div>

```js
/** @template T */
class Foo {
  /** @param {T} x */
  constructor(x) {
    /** @type {T} */
    this.x = x;
  }
}

/** @extends {Foo<number>} */
class Bar extends Foo {
  constructor() {
    super(42);
  }
}

exports.Baz = class extends Bar {
  /** @return {number} */
  method() {
    return this.x;
  }
};
```

<div class='badcode'></div>

```js
/** @extends {Bar} */ // <-- unnecessary @extends
exports.Baz = class extends Bar {
  /** @return {number} */
  method() {
    return this.x;
  }
};
```

<a id="formatting-function-expressions"></a>

#### 4.2.4 函数表达式

在函数调用的实参列表中声明匿名函数时，
函数体要比上一层的缩进深度多缩进两个
空格。

示例：

<div class='goodcode'></div>

```js
prefix.something.reallyLongFunctionName('whatever', (a1, a2) => {
  // Indent the function body +2 relative to indentation depth
  // of the 'prefix' statement one line above.
  if (a1.equals(a2)) {
    someOtherLongFunctionName(a1);
  } else {
    andNowForSomethingCompletelyDifferent(a2.parrot);
  }
});

some.reallyLongFunctionCall(arg1, arg2, arg3)
    .thatsWrapped()
    .then((result) => {
      // Indent the function body +2 relative to the indentation depth
      // of the '.then()' call.
      if (result) {
        result.use();
      }
    });
```

<a id="formatting-switch-statements"></a>

#### 4.2.5 switch 语句

与任何其他块一样，switch 块的内容缩进 +2。

在 switch 标签之后换行，缩进级别增加
+2，就像打开了一个块一样。如果词法作用域需要，
可以使用显式的块。下一个 switch 标签回到上一层
缩进级别，就像关闭了一个块。

`break` 与紧随其后的 case 之间可以有一个空行。

示例：

<div class='goodcode'></div>

```js
switch (animal) {
  case Animal.BANDERSNATCH:
    handleBandersnatch();
    break;

  case Animal.JABBERWOCK:
    handleJabberwock();
    break;

  default:
    throw new Error('Unknown animal');
}
```

<a id="formatting-statements"></a>

### 4.3 语句

<a id="formatting-one-statement-perline"></a>

#### 4.3.1 每行一条语句

每条语句后面都要换行。

<a id="formatting-semicolons-are-required"></a>

#### 4.3.2 必须使用分号

每条语句都必须以分号结尾。禁止依赖自动
分号插入。

<a id="formatting-column-limit"></a>

### 4.4 列宽限制：80

JavaScript 代码的列宽限制为 80 个字符。除下文所述例外，
任何超过此限制的行都必须换行，具体参见
[4.5 换行](#formatting-line-wrapping)。

**例外：**

1.  `goog.module`、`goog.require` 和 `goog.requireType` 语句（参见
    [3.3 `goog.module` 语句](#file-goog-module) 以及
    [3.6 `goog.require` 与 `goog.requireType` 语句](#file-goog-require)）。
2.  ES 模块的 `import` 和 `export from` 语句（参见
    [3.4.1 导入](#es-module-imports) 以及
    [3.4.2.3 export from](#es-module-export-from)）。
3.  无法遵守列宽限制，或遵守后会妨碍
    可发现性的行。例如：
    *   在源代码中应可点击的长 URL。
    *   供复制粘贴的 shell 命令。
    *   可能需要整体复制或搜索的长字符串字面量
        （例如很长的文件路径）。

<a id="formatting-line-wrapping"></a>

### 4.5 换行

**术语说明**：*换行*指把一段代码拆成多行
以遵守列宽限制，而这段代码本来可以合法地
放在单行中。

没有一个全面、确定的公式能说明在每种情况下
*究竟*该如何换行。同一段代码往往有多种
有效的换行方式。

注意：虽然换行的常见原因是避免超出
列宽限制，但实际上即便代码能放下，作者也
可以自行决定是否换行。

> 提示：提取一个方法或局部变量也许就能解决问题，
> 而无需换行。

<a id="formatting-where-to-break"></a>

#### 4.5.1 在哪里断行

换行的首要原则是：优先在**更高的语法
层级**处断行。

推荐：

<div class='goodcode'></div>

```js
currentEstimate =
    calc(currentEstimate + x * currentEstimate) /
        2.0;
```

不鼓励：

<div class='badcode'></div>

```js
currentEstimate = calc(currentEstimate + x *
    currentEstimate) / 2.0;
```

在上例中，语法层级从高到低依次为：
赋值、除法、函数调用、参数、数值常量。

运算符的换行规则如下：

1.  在运算符处断行时，断行位置在符号之后。（注意，
    这与 Google 的 Java 风格中的做法不同。）
    1.  这不适用于“点号”（`.`），它实际上并不是
        运算符。
2.  方法名或构造函数名与其后的左圆括号（`(`）
    保持相连。
3.  逗号（`,`）与其前面的标记保持相连。
4.  绝不在 return 与返回值之间换行，因为这会
    改变代码的含义。
5.  带类型名的 JSDoc 注解在 “{” 后断行。这是必要的，
    因为带有可选类型的注解（@const、@private、@param 等）
    不会扫描下一行。

> 注意：换行的首要目标是让代码清晰，而不一定
> 是让代码占用最少的行数。

<a id="formatting-indent"></a>

#### 4.5.2 续行至少缩进 +4 空格

换行时，第一行之后的每一行（每个*续行*）
相对原行至少缩进 +4，除非它适用块缩进
的规则。

当有多个续行时，缩进可以根据情况在 +4 之上
变化。一般来说，语法层级更深的续行按更大的
4 的倍数缩进；两行使用相同的缩进级别，当且仅当
它们以语法上平行的元素开头。

[4.6.3 水平对齐：不鼓励](#formatting-horizontal-alignment)
讨论的是一种不鼓励的做法：用数量不一的空格
把某些标记与前几行对齐。

<a id="formatting-whitespace"></a>

### 4.6 空白

<a id="formatting-vertical-whitespace"></a>

#### 4.6.1 纵向空白

单个空行出现在以下位置：

1.  类或对象字面量中连续的方法之间
    1.  例外：对象字面量中两个连续的属性定义之间
        （中间没有其他代码）的空行是可选的。这类
        空行按需使用，用来形成字段的*逻辑分组*。
2.  方法体内，可用于形成语句的*逻辑分组*，但应节制。
    函数体开头或结尾不允许有空行。
3.  *可选地*出现在类或对象字面量中第一个方法之前
    或最后一个方法之后（既不鼓励也不反对）。
4.  按本文档其他章节的要求（例如
    [3.6 `goog.require` 与 `goog.requireType` 语句](#file-goog-require)）。

*多个*连续的空行是允许的，但从不要求（也
不鼓励）。

<a id="formatting-horizontal-whitespace"></a>

#### 4.6.2 横向空白

横向空白的使用取决于所在位置，分为三大类：
*行首*（位于一行开头）、*行尾*（位于一行末尾）
和*内部*。行首空白（即缩进）在别处讨论。
行尾空白是禁止的。

除语言或其他风格规则要求的位置之外，且除字面量、
注释和 JSDoc 之外，单个内部 ASCII 空格**仅**出现在
以下位置。

1.  将任意保留字（如 `if`、`for` 或 `catch`）与
    同一行中紧随其后的左圆括号（`(`）分隔开，
    但 `function` 和 `super` 除外。
2.  将任意保留字（如 `else` 或 `catch`）与同一行中
    位于其前的右花括号（`}`）分隔开。
3.  在任何左花括号（`{`）之前，但有两个例外：
    1.  作为函数第一个实参或数组字面量第一个元素的
        对象字面量之前（例如 `foo({a: [{c: d}]})`）。
    2.  在模板展开中，因为语言禁止这样做（例如合法：
        `` `ab${1 + 2}cd` ``，非法：`` `xy$ {3}z` ``）。
4.  任何二元或三元运算符的两侧。
5.  逗号（`,`）或分号（`;`）之后。注意这些字符
    之前*绝不*允许有空格。
6.  对象字面量中冒号（`:`）之后。
7.  行尾注释起始的双斜杠（`//`）两侧。
    这里允许多个空格，但并非必须。
8.  块注释起始字符之后，以及结束字符的两侧
    （例如简写形式类型声明、类型转换和参数名注释：
    `this.foo = /** @type {number} */ (bar)`；或 `function(/** string */ foo)
    {`；或 `baz(/* buzz= */ true)`）。

<a id="formatting-horizontal-alignment"></a>

#### 4.6.3 水平对齐：不鼓励

**术语说明**：*水平对齐*指在代码中添加
数量不一的额外空格，目的是让某些标记
正好位于前几行中另一些标记的正下方。

这种做法是允许的，但 Google 风格**通常不鼓励**这样做。
即便在已经使用了水平对齐的地方，也并不要求
*保持*水平对齐。

下面先给出一个未对齐的示例，再给出一个对齐的示例。
两者都允许，但后者不鼓励：

<div class='goodcode'></div>

```js
{
  tiny: 42, // this is great
  longer: 435, // this too
};

{
  tiny:   42,  // permitted, but future edits
  longer: 435, // may leave it unaligned
};
```

> 提示：对齐有助于可读性，但会给未来的
> 维护带来问题。设想将来有一次改动只需要改动一行。
> 这次改动可能让原本赏心悦目的格式变得凌乱，而这是
> 允许的。更常见的是，它会促使编码者（也许就是你）
> 顺带调整附近行的空白，可能触发一连串的重新排版。
> 这次单行改动于是有了“影响范围”。最坏的情况下，
> 这会导致毫无意义的杂务；即便在最好的情况下，也会
> 破坏版本历史信息、拖慢评审者并加剧合并冲突。

<a id="formatting-function-arguments"></a>

#### 4.6.4 函数实参

优先把所有函数实参放在与函数名同一行。如果
这样做会超过 80 列限制，则必须以可读的方式
对实参换行。为节省空间，可以尽量贴近 80 列换行，
也可以把每个实参单独放一行以提升可读性。缩进应为
四个空格。允许与圆括号对齐，但不鼓励。下面是
实参换行最常见的几种模式：

<div class='goodcode'></div>

```js
// Arguments start on a new line, indented four spaces. Preferred when the
// arguments don't fit on the same line with the function name (or the keyword
// "function") but fit entirely on the second line. Works with very long
// function names, survives renaming without reindenting, low on space.
doSomething(
    descriptiveArgumentOne, descriptiveArgumentTwo, descriptiveArgumentThree) {
  // …
}

// If the argument list is longer, wrap at 80. Uses less vertical space,
// but violates the rectangle rule and is thus not recommended.
doSomething(veryDescriptiveArgumentNumberOne, veryDescriptiveArgumentTwo,
    tableModelEventHandlerProxy, artichokeDescriptorAdapterIterator) {
  // …
}

// Four-space, one argument per line.  Works with long function names,
// survives renaming, and emphasizes each argument.
doSomething(
    veryDescriptiveArgumentNumberOne,
    veryDescriptiveArgumentTwo,
    tableModelEventHandlerProxy,
    artichokeDescriptorAdapterIterator) {
  // …
}
```

按照
[rectangle rule](https://github.com/google/google-java-format/wiki/The-Rectangle-Rule)
的要求，被换行表达式的每个部分都应放在各自的边界
矩形内，该矩形包含该部分的全部文本，而不含其他任何部分的文本。

<a id="formatting-grouping-parentheses"></a>

### 4.7 分组括号：推荐

只有当作者与评审者一致认为，没有它们代码
也不会被误解，而且它们也不会让代码更易读时，
才可以省略可选的分组括号。假定每位读者
都记住了完整的运算符优先级表，是*不*
合理的。

不要给 `delete`、`typeof`、`void`、`return`、
`throw`、`case`、`in`、`of` 或 `yield` 之后的整个表达式加不必要的括号。

类型转换必须使用括号：`/** @type {!Foo} */ (foo)`。

<a id="formatting-comments"></a>

### 4.8 注释

本节讨论*实现注释*。JSDoc 在 [7 JSDoc](#jsdoc)
中单独讨论。

<a id="formatting-block-comment-style"></a>

#### 4.8.1 块注释风格

块注释与周围代码保持同一缩进级别。可以采用
`/* … */` 或 `//` 风格。对于多行 `/* … */` 注释，
后续各行必须以 `*` 开头，并与上一行的 `*` 对齐，
以便无需额外上下文就能看出是注释。

<div class='goodcode'></div>

```js
/*
 * This is
 * okay.
 */

// And so
// is this.

/* This is fine, too. */
```

不要用星号或其他字符把注释框起来。

不要用 JSDoc（`/** … */`）来写实现注释。

<a id="formatting-param-name-comments"></a>

#### 4.8.2 参数名注释

当值和方法名不足以充分表达含义，且
无法通过重构方法使其更清晰时，应使用“参数名”注释。
其首选格式是放在值之前并带 “=”：

<div class='goodcode'></div>

```js
someFunction(obviousParam, /* shouldRender= */ true, /* name= */ 'hello');
```

为与周围代码保持一致，也可以把它们放在值之后，
不带 “=”：

<div class='goodcode'></div>

```js
someFunction(obviousParam, true /* shouldRender */, 'hello' /* name */);
```

<a id="language-features"></a>

## 5 语言特性

JavaScript 包含许多可疑（甚至危险）的特性。
本节界定哪些特性可以使用、哪些不可以使用，
以及使用这些特性时的任何额外约束。

本风格指南中未讨论的语言特性可以使用，
对其用法不作任何建议。

<a id="features-local-variable-declarations"></a>

### 5.1 局部变量声明

<a id="features-use-const-and-let"></a>

#### 5.1.1 使用 `const` 和 `let`

所有局部变量都用 `const` 或 `let` 声明。
默认使用 `const`，除非变量需要被重新赋值。
绝不能使用 `var` 关键字。

<a id="features-one-variable-per-declaration"></a>

#### 5.1.2 每条声明只声明一个变量

每条局部变量声明只声明一个变量：不使用形如
`let a = 1, b = 2;` 的声明。

<a id="features-declared-when-needed"></a>

#### 5.1.3 在需要时声明，尽快初始化

局部变量**不**习惯性地声明在其所在
块或类块结构的开头。相反，局部变量应声明在
首次使用处附近（在合理范围内），以最小化其作用域，
并尽快初始化。

<a id="features-declare-types-as-needed"></a>

#### 5.1.4 按需声明类型

JSDoc 类型注解可以加在声明的上一行，
或者在没有其他 JSDoc 时内联加在变量名之前。

示例：

<div class='goodcode'></div>

```js
const /** !Array<number> */ data = [];

/**
 * Some description.
 * @type {!Array<number>}
 */
const data = [];
```

不允许混用内联风格与 JSDoc 风格：编译器只会处理
第一个 JsDoc，内联注解将会丢失。

<div class='badcode'></div>

```js
/** Some description. */
const /** !Array<number> */ data = [];
```

在很多情况下，编译器能推断出模板化的类型，却无法
推断出其参数。尤其是当初始化字面量或构造函数调用
不包含任何模板参数类型的值时（例如空数组、对象、
`Map` 或 `Set`），或者变量在闭包中被修改时。
在这些情况下，局部变量类型注解特别有用，否则编译
器会把模板参数推断为 unknown。

<div class='goodcode'></div>

```js
/** @param {!Array<string>} ids */
function process(ids) {
  // Inferred as !Set<string> from the argument, so no annotation is needed.
  const uniqueIds = new Set(ids);
}

// Empty collections need an annotation.
const /** !Map<string, number> */ wordCounts = new Map();
const /** !Set<string> */ seenIds = new Set();
```

<div class='badcode'></div>

```js
// The key and value types of the Map are inferred as unknown.
const wordCounts = new Map();
```

<a id="features-array-literals"></a>

### 5.2 数组字面量

<a id="features-arrays-trailing-comma"></a>

#### 5.2.1 使用尾随逗号

当最后一个元素与右方括号之间存在换行时，
应加上尾随逗号。

示例：

<div class='goodcode'></div>

```js
const values = [
  'first value',
  'second value',
];
```

<a id="features-arrays-ctor"></a>

#### 5.2.2 不要使用可变参数的 `Array` 构造函数

在增加或删除参数时，该构造函数容易出错。
请改用字面量。

不允许：

<div class='badcode'></div>

```js
const a1 = new Array(x1, x2, x3);
const a2 = new Array(x1, x2);
const a3 = new Array(x1);
const a4 = new Array();
```

除第三种情况外，其余都符合预期：如果 `x1` 是整数，
那么 `a3` 是长度为 `x1` 的数组，其中所有元素都是
`undefined`。如果 `x1` 是其他数值，则会抛出异常；
如果是其他任何值，则是单元素数组。

应改写为

<div class='goodcode'></div>

```js
const a1 = [x1, x2, x3];
const a2 = [x1, x2];
const a3 = [x1];
const a4 = [];
```

在适当的情况下，允许使用 `new Array(length)`
显式分配指定长度的数组。

<a id="features-arrays-non-numeric-properties"></a>

#### 5.2.3 非数字属性

不要在数组上定义或使用非数字属性（`length` 除外）。
请改用 `Map`（或 `Object`）。

<a id="features-arrays-destructuring"></a>

#### 5.2.4 解构

数组字面量可以用在赋值语句的左侧来执行解构
（例如从单个数组或可迭代对象中解出多个值）。
可以包含一个末尾的“rest”元素（`...` 与变量名之间
不加空格）。未使用的元素应当省略。

<div class='goodcode'></div>

```js
const [a, b, c, ...rest] = generateResults();
let [, b,, d] = someArray;
```

解构也可以用于函数参数（注意参数名是必需的，
但会被忽略）。如果解构的数组参数是可选的，
务必将 `[]` 指定为默认值，并在左侧
提供默认值：

<div class='goodcode'></div>

```js
/** @param {!Array<number>=} param1 */
function optionalDestructuring([a = 4, b = 2] = []) { … };
```

不允许：

<div class='badcode'></div>

```js
function badDestructuring([a, b] = [4, 2]) { … };
```

在将多个值打包或解包到函数的参数或返回值时，
应尽可能优先使用对象解构而非数组解构，因为它允许
为各个元素命名，并为每个元素指定不同的类型。

<div class='goodcode'></div>

{% raw %}
```js
/** @return {{name: string, age: number}} */
function getUser() {
  return {name: 'Alice', age: 30};
}
const {name, age} = getUser();
```
{% endraw %}

<div class='badcode'></div>

```js
/** @return {!Array<string|number>} */
function getUser() {
  return ['Alice', 30];
}
const [name, age] = getUser();
```

<a id="features-arrays-spread-operator"></a>

#### 5.2.5 展开运算符

数组字面量可以包含展开运算符（`...`），用于把
一个或多个其他可迭代对象中的元素展开。应优先使用
展开运算符，而不是借助 `Array.prototype` 的
更笨拙的写法。`...` 后面不加空格。

示例：

<div class='goodcode'></div>

```js
[...foo]   // preferred over Array.prototype.slice.call(foo)
[...foo, ...bar]   // preferred over foo.concat(bar)
```

<a id="features-object-literals"></a>

### 5.3 对象字面量

<a id="features-objects-use-trailing-comma"></a>

#### 5.3.1 使用尾随逗号

当最后一个属性与右花括号之间存在换行时，
应加上尾随逗号。

<a id="features-objects-ctor"></a>

#### 5.3.2 不要使用 `Object` 构造函数

虽然 `Object` 没有 `Array` 那样的问题，
但为了保持一致，仍然不允许使用。请改用
对象字面量（`{}` 或 `{a: 0, b: 1, c: 2}`）。

<a id="features-objects-mixing-keys"></a>

#### 5.3.3 不要混用加引号与不加引号的键

对象字面量既可以表示 *structs*（不加引号的键和/或
符号），也可以表示 *dicts*（加引号和/或计算的键）。
不要在单个对象字面量中混用这些键类型。

不允许：

<div class='badcode'></div>

```js
{
  width: 42, // struct-style unquoted key
  'maxWidth': 43, // dict-style quoted key
}
```

这同样适用于把属性名传给函数的情况，例如
`hasOwnProperty`。特别是，这样做会在编译后的代码中
出错，因为编译器无法重命名/混淆字符串字面量。

不允许：

<div class='badcode'></div>

<!-- {% raw %} -->

```js
/** @type {{width: number, maxWidth: (number|undefined)}} */
const o = {width: 42};
if (o.hasOwnProperty('maxWidth')) {
  ...
}
```

<!-- {% endraw %} -->

最佳实现方式是：

<div class='goodcode'></div>

<!-- {% raw %} -->

```js
/** @type {{width: number, maxWidth: (number|undefined)}} */
const o = {width: 42};
if (o.maxWidth != null) {
  ...
}
```

<!-- {% endraw %} -->

<a id="features-objects-computed-property-names"></a>

#### 5.3.4 计算属性名

计算属性名（例如 `{['key' + foo()]: 42}`）是允许的，并被
视为 dict 风格的（加引号的）键（即不得与不加引号
的键混用），除非该计算属性是
[symbol](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol)
（例如 `[Symbol.iterator]`）。枚举值也可用于计算键，
但不得在同一个字面量中与非枚举键混用。

<a id="features-objects-method-shorthand"></a>

#### 5.3.5 方法简写

可以在对象字面量上定义方法，方法简写形如（`{method()
{… }}`），用来代替紧跟 `function` 或箭头
函数字面量的冒号。

示例：

<div class='goodcode'></div>

```js
return {
  stuff: 'candy',
  method() {
    return this.stuff;  // Returns 'candy'
  },
};
```

注意，方法简写或 `function` 中的 `this` 指向对象
字面量本身，而箭头函数中的 `this` 指向对象字面量
外部的作用域。

示例：

<div class='goodcode'></div>

```js
class {
  getObjectLiteral() {
    this.stuff = 'fruit';
    return {
      stuff: 'candy',
      method: () => this.stuff,  // Returns 'fruit'
    };
  }
}
```

<a id="features-objects-shorthand-properties"></a>

#### 5.3.6 简写属性

对象字面量允许使用简写属性。

示例：

<div class='goodcode'></div>

```js
const foo = 1;
const bar = 2;
const obj = {
  foo,
  bar,
  method() { return this.foo + this.bar; },
};
assertEquals(3, obj.method());
```

<a id="features-objects-destructuring"></a>

#### 5.3.7 解构

对象解构模式可以用在赋值语句的左侧，用来执行解构，
并从单个对象中解出多个值。

解构后的对象也可以用作函数参数，但应尽可能
保持简单：只使用一层不加引号的简写属性。
参数解构中不得使用更深层的嵌套和计算属性。
默认值应写在被解构参数的左侧
（`{str = 'some default'} = {}`，而不是 `{str} =
{str: 'some default'}`）；如果被解构的对象本身是
可选的，它必须默认为 `{}`。被解构参数的 JSDoc
可以使用任意名称（该名称不会被使用，但编译器要求提供）。

示例：

<div class='goodcode'></div>

<!-- {% raw %} -->

```js
/**
 * @param {string} ordinary
 * @param {{num: (number|undefined), str: (string|undefined)}=} param1
 *     num: The number of times to do something.
 *     str: A string to do stuff to.
 */
function destructured(ordinary, {num, str = 'some default'} = {}) {}
```

<!-- {% endraw %} -->

不允许：

<div class='badcode'></div>

<!-- {% raw %} -->

```js
/** @param {{x: {num: (number|undefined), str: (string|undefined)}}} param1 */
function nestedTooDeeply({x: {num, str}}) {};
/** @param {{num: (number|undefined), str: (string|undefined)}=} param1 */
function nonShorthandProperty({num: a, str: b} = {}) {};
/** @param {{a: number, b: number}} param1 */
function computedKey({a, b, [a + b]: c}) {};
/** @param {{a: number, b: string}=} param1 */
function nontrivialDefault({a, b} = {a: 2, b: 4}) {};
```

<!-- {% endraw %} -->

解构也可以用于 `goog.require` 语句，在这种情况下
不得换行：整条语句占一行，无论它有多长
（见
[3.6 `goog.require` 与 `goog.requireType` 语句](#file-goog-require)）。

<a id="features-objects-enums"></a>

#### 5.3.8 枚举

枚举通过在对象字面量上添加 `@enum` 注解来定义。
枚举必须是模块局部的，或者直接赋值到 `exports` 上，
不得嵌套在某个类型或对象之下。

枚举定义之后不得再添加额外的属性。枚举必须是
常量。所有枚举值都必须是字符串字面量或数字。

<div class='goodcode'></div>

```js
/**
 * Supported temperature scales.
 * @enum {string}
 */
const TemperatureScale = {
  CELSIUS: 'celsius',
  FAHRENHEIT: 'fahrenheit',
};

/**
 * An enum with two values.
 * @enum {number}
 */
const Value = {
  /** The value used shall have been the first. */
  FIRST_VALUE: 1,
  /** The second among two values. */
  SECOND_VALUE: 2,
};
```

对于字符串枚举，所有值都必须静态初始化，不得通过
算术运算符、模板字面量替换、函数调用甚至变量
引用来计算。

<div class='badcode'></div>

```js
const ABSOLUTE_ZERO = '-273°F';

/**
 * Not supported computed values in string enum.
 * @enum {string}
 */
const TemperatureInFahrenheit = {
  MIN_POSSIBLE: ABSOLUTE_ZERO,
  ZERO_FAHRENHEIT: 0 + '°F',
  ONE_FAHRENHEIT: `${Values.FIRST_VALUE}°F`,
  TWO_FAHRENHEIT: Values.SECOND_VALUE + '°F',
  SOME_FAHRENHEIT: getTemperatureInFahrenheit() + '°F',
};
```

注意：虽然 TypeScript 支持更多枚举值的写法（例如 `A:
'a'+'b'` 等），但只允许字符串字面量和数字作为
枚举值，是为了便于向 TypeScript 迁移。对于复杂的
值，可以考虑使用不带 `@enum` 的 const 对象。

<a id="features-classes"></a>

### 5.4 类

<a id="features-classes-constructors"></a>

#### 5.4.1 构造函数

构造函数是可选的。子类的构造函数必须先调用 `super()`，
然后才能设置任何字段或访问 `this`。接口应在构造函数中
声明非方法属性。

<a id="features-classes-fields"></a>

#### 5.4.2 字段

在构造函数中定义具体对象的所有字段（即除方法以外
的所有属性）。对于从不被重新赋值的字段，用 `@const`
标注（这些字段不必是深层不可变的）。对于非公开字段，
用相应的可见性注解标注（`@private`、`@protected`、
`@package`）。`@private` 字段的名称可以选择以下划线
结尾。字段不得定义在构造函数内的嵌套作用域中，
也不得定义在具体类的 `prototype` 上。

示例：

<div class='goodcode'></div>

```js
class Foo {
  constructor() {
    /** @private @const {!Bar} */
    this.bar_ = computeBar();

    /** @protected @const {!Baz} */
    this.baz = computeBaz();
  }
}
```

> 提示：构造函数执行完毕后，绝不应再向实例添加
> 或移除属性，因为这会严重妨碍 VM 的优化能力。
> 如有必要，稍后才初始化的字段应在构造函数中
> 显式设为 `undefined`，以防止之后发生形状变化。
> 给对象添加 `@struct` 会检查是否添加/访问了
> 未声明的属性。类默认已添加此项。

<a id="features-classes-computed-properties"></a>

#### 5.4.3 计算属性

计算属性只有在属性是 symbol 时才可在类中使用。
dict 风格的属性（即加引号的键或计算得到的非
symbol 键，定义见 [5.3.3 不要混用加引号与不加引号的键](#features-objects-mixing-keys)）
不允许使用。任何逻辑上可迭代的类都应定义
`[Symbol.iterator]` 方法。除此之外，应谨慎使用 `Symbol`。

> 提示：谨慎使用任何其他内置 symbol（例如
> `Symbol.isConcatSpreadable`），因为编译器不会为它们提供
> polyfill，因此在较旧的浏览器中将无法工作。

<a id="features-classes-static-methods"></a>

#### 5.4.4 静态方法

在不影响可读性的前提下，优先使用模块局部函数，
而不是私有静态方法。

代码不应依赖静态方法的动态分派，因为这会妨碍
Closure Compiler 的优化。静态方法只应在基类
自身上调用。不应在包含动态实例的变量上调用静态
方法，该实例可能是构造函数，也可能是子类构造函数
（如果这样做，必须用 `@nocollapse` 定义），并且不得
在未自行定义该方法的子类上直接调用。不要在静态
方法中访问 `this`。

不允许：

<div class='badcode'></div>

```js
// Context for the examples below; by itself this code is allowed.
class Base {
  /** @nocollapse */ static foo() {}
}
class Sub extends Base {}

// discouraged: don't call static methods dynamically
function callFoo(cls) { cls.foo(); }

// Disallowed: don't call static methods on subclasses that don't define it themselves
Sub.foo();

// Disallowed: don't access this in static methods.
class Clazz {
  static foo() {
    return this.staticField;
  }
}
Class.staticField = 1;
```

<a id="features-classes-old-style"></a>

#### 5.4.5 旧式类声明

虽然首选 ES6 类，但有些情况下 ES6 类可能并不可行。
例如：

1.  如果存在或将存在子类（包括会创建子类的框架），
    而这些子类无法立即改为使用 ES6 类语法。如果
    这样的类使用了 ES6 语法，那么所有未使用 ES6
    类语法的下游子类都需要修改。
2.  有些框架要求在调用超类构造函数之前就有一个
    已知的 `this` 值，因为带有 ES6 超类的构造函数
    在 `super` 调用返回之前无法访问实例的 `this` 值。

在所有其他方面，风格指南仍然适用于这类代码：
在适当的时候，都应使用 `let`、`const`、默认参数、
rest 和箭头函数。

`goog.defineClass` 支持一种类似 ES6 类语法的
类定义形式：

<div class='goodcode'></div>

```js
let C = goog.defineClass(S, {
  /**
   * @param {string} value
   */
  constructor(value) {
    S.call(this, 2);
    /** @const */
    this.prop = value;
  },

  /**
   * @param {string} param
   * @return {number}
   */
  method(param) {
    return 0;
  },
});
```

另外，虽然所有新代码都应优先使用 `goog.defineClass`，
但也允许使用更传统的语法。

<div class='goodcode'></div>

```js
/**
  * @constructor @extends {S}
  * @param {string} value
  */
function C(value) {
  S.call(this, 2);
  /** @const */
  this.prop = value;
}
goog.inherits(C, S);

/**
 * @param {string} param
 * @return {number}
 */
C.prototype.method = function(param) {
  return 0;
};
```

每个实例的属性都应在构造函数中、调用超类构造函数
之后定义（如果有超类的话）。方法应定义在
构造函数的 prototype 上。

正确定义构造函数的 prototype 继承层次比初看上去
要难！因此，最好使用
[Closure Library](http://code.google.com/closure/library/) 中的 `goog.inherits`。

<a id="features-classes-prototypes"></a>

#### 5.4.6 不要直接操作 `prototype`

与定义 `prototype` 属性相比，`class` 关键字能带来
更清晰、更易读的类定义。普通的实现代码不应操作
这些对象，不过它们在按
[5.4.5 旧式类声明](#features-classes-old-style) 定义类时仍然有用。
明确禁止使用 mixin 以及修改内置对象的 prototype。

**例外**：框架代码（例如 Polymer 或 Angular）可能需要
使用 `prototype`，不应为了避免使用它而采用更糟糕的变通办法。

<a id="features-classes-getters-and-setters"></a>

#### 5.4.7 Getter 与 Setter

不要使用
[JavaScript 的 getter 和 setter 属性](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/get)。
它们可能出人意料、难以推理，而且编译器对它们的
支持有限。请改用普通方法。

**例外**：在某些情况下，定义 getter 或 setter 不可避免
（例如 Angular 和 Polymer 这类数据绑定框架，或为了
与无法调整的外部 API 兼容）。仅在这些情况下，才可
*谨慎*使用 getter 和 setter，前提是用 `get` 和 `set`
简写方法关键字或 `Object.defineProperties` 定义（不要用
`Object.defineProperty`，它会妨碍属性重命名）。Getter
**绝不能**改变可观察状态。

不允许：

<div class='badcode'></div>

```js
class Foo {
  get next() { return this.nextId++; }
}
```

<a id="features-classes-overriding-tostring"></a>

#### 5.4.8 重写 toString

可以重写 `toString` 方法，但必须始终成功，
且绝不能产生可见的副作用。

> 提示：尤其要当心在 toString 中调用其他方法，
> 因为异常情况可能导致无限循环。

<a id="features-classes-interfaces"></a>

#### 5.4.9 接口

接口可以用 `@interface` 或 `@record` 声明。用 `@record`
声明的接口可以由类或对象字面量显式实现（即通过
`@implements`），也可以隐式实现。

接口上的所有方法都必须是非静态的，且方法体必须是
空块。字段必须在类构造函数中声明为未初始化的
成员。

示例：

<div class='goodcode'></div>

```js
/**
 * Something that can frobnicate.
 * @record
 */
class Frobnicator {
  constructor() {
    /** @type {number} The number of attempts before giving up. */
    this.attempts;
  }

  /**
   * Performs the frobnication according to the given strategy.
   * @param {!FrobnicationStrategy} strategy
   */
  frobnicate(strategy) {}
}
```

<a id="features-classes-abstract-classes"></a>

#### 5.4.10 抽象类

在适当的时候使用抽象类。抽象类和方法必须带有
`@abstract` 注解。不要使用 `goog.abstractMethod`。参见
[抽象类与方法](https://github.com/google/closure-compiler/wiki/@abstract-classes-and-methods)。

<a id="static-containers"></a>

#### 5.4.11 不要创建静态容器类

不要仅仅为了命名空间而使用只含静态方法或属性的
容器类。

<div class='badcode'></div>

```js
// container.js
// Bad: Container is an exported class that has only static methods and fields.
class Container {
  /** @return {number} */
  static bar() {
    return 1;
  }
}

/** @const {number} */
Container.FOO = 1;

exports = {Container};
```

应改为分别导出常量和函数：

<div class='goodcode'></div>

```js
/** @return {number} */
exports.bar = () => {
  return 1;
}

/** @const {number} */
exports.FOO = 1;
```

<a id="nested-namespaces"></a>

#### 5.4.12 不要定义嵌套命名空间

不要在另一个模块局部名称上定义嵌套类型
（例如 class、typedef、enum、interface）。

<div class='badcode'></div>

<!-- {% raw %} -->

```js
// foo.js
goog.module('my.namespace');

class Foo {...}

Foo.Bar = class {...};

/** @enum {number} */
Foo.Baz = {...};

/** @typedef {{value: number}} */
Foo.Qux;

/** @interface */
Foo.Quuz = class {...}

exports.Foo = Foo;
```

<!-- {% endraw %} -->

这些值应当是顶层的导出。为这些值选择清晰的名称
（例如，对本来可以嵌套在 Foo 下的 Converter，
取名为 FooConverter）。不过，当模块名与类名的
一部分重复时，可以考虑省略冗余：用 `foo.Foo` 和
`foo.Converter`，而不是 `foo.Foo` 和 `foo.FooConverter`。
为清晰起见，导入方可以在必要时加上前缀（例如
`import {Converter as FooConverter} from './foo';`），但在把整个模块作为命名空间导入时，却很难去掉冗余。

<div class='goodcode'></div>

<!-- {% raw %} -->

```js
// foo.js
goog.module('my.namespace');

class Foo {...}

class FooBar {...}

/** @enum {string} */
let FooBaz = {...};

/** @typedef {{value: number}} */
let FooQux;

/** @interface */
class FooQuuz {...};

export = {
  Foo,
  FooBar,
  FooBaz,
  FooQux,
  FooQuuz,
};
```

<!-- {% endraw %} -->

<a id="features-functions"></a>

### 5.5 函数

<a id="features-functions-top-level-functions"></a>

#### 5.5.1 顶层函数

顶层函数可以直接定义在 `exports` 对象上，也可以
在局部声明后选择性地导出。更多关于导出的内容，参见
[3.3.3 `goog.module` 导出](#file-goog-module-exports)。

示例：

<div class='goodcode'></div>

```js
/** @param {string} str */
exports.processString = (str) => {
  // Process the string.
};
```

<div class='goodcode'></div>

```js
/** @param {string} str */
const processString = (str) => {
  // Process the string.
};

exports = {processString};
```

<a id="features-functions-nested-functions"></a>

#### 5.5.2 嵌套函数与闭包

函数可以包含嵌套的函数定义。如果需要给函数命名，
应把它赋值给一个局部 `const`。

<a id="features-functions-arrow-functions"></a>

#### 5.5.3 箭头函数

箭头函数提供了简洁的函数语法，并简化了嵌套函数中
`this` 的作用域。对于嵌套函数，优先使用箭头函数
而非 `function` 关键字（但参见
[5.3.5 方法简写](#features-objects-method-shorthand)）。

相对于其他 `this` 作用域处理方式，如 `f.bind(this)`、
`goog.bind(f, this)` 和 `const self = this`，应优先使用
箭头函数。箭头函数在调用回调时尤其有用，因为它允许
显式指定要传给回调的参数，而绑定会不加区分地
把所有参数都传递过去。

箭头左侧包含零个或多个参数。如果只有一个非解构
参数，参数外的括号可以省略。使用括号时，可以指定
内联参数类型（参见
[7.8 方法与函数注释](#jsdoc-method-and-function-comments)）。

> 提示：即使对单参数箭头函数也始终使用括号，可以避免
> 因添加参数却忘记加括号而产生虽可解析、但行为已
> 不再符合预期的代码。

箭头右侧包含函数体。默认情况下，函数体是一个
块语句（由花括号包围的零条或多条语句）。在以下
任一情况下，函数体也可以是隐式返回的单个表达式：
程序逻辑要求返回一个值，或者 `void` 运算符位于
单个函数或方法调用之前（使用 `void` 可确保返回
`undefined`、防止值泄漏，并表明意图）。如果单个
表达式形式能提升可读性（例如表达式很短或很简单），
则优先使用这种形式。

示例：

<div class='goodcode'></div>

```js
/**
 * Arrow functions can be documented just like normal functions.
 * @param {number} numParam A number to add.
 * @param {string} strParam Another number to add that happens to be a string.
 * @return {number} The sum of the two parameters.
 */
const moduleLocalFunc = (numParam, strParam) => numParam + Number(strParam);

// Uses the single expression syntax with `void` because the program logic does
// not require returning a value.
getValue((result) => void alert(`Got ${result}`));

class CallbackExample {
  constructor() {
    /** @private {number} */
    this.cachedValue_ = 0;

    // For inline callbacks, you can use inline typing for parameters.
    // Uses a block statement because the value of the single expression should
    // not be returned and the expression is not a single function call.
    getNullableValue((/** ?number */ result) => {
      this.cachedValue_ = result == null ? 0 : result;
    });
  }
}
```

不允许：

<div class='badcode'></div>

```js
/**
 * A function with no params and no returned value.
 * This single expression body usage is illegal because the program logic does
 * not require returning a value and we're missing the `void` operator.
 */
const moduleLocalFunc = () => anotherFunction();
```

<a id="features-functions-generators"></a>

#### 5.5.4 生成器

生成器支持许多有用的抽象，可按需使用。

定义生成器函数时，把 `*` 贴在 `function` 关键字上
（如果存在的话），并与函数名之间用一个空格隔开。
使用委托 yield 时，把 `*` 贴在 `yield` 关键字上。

示例：

<div class='goodcode'></div>

```js
/** @return {!Iterator<number>} */
function* gen1() {
  yield 42;
}

/** @return {!Iterator<number>} */
const gen2 = function*() {
  yield* gen1();
}

class SomeClass {
  /** @return {!Iterator<number>} */
  * gen() {
    yield 42;
  }
}
```

<a id="features-functions-parameter-return-types"></a>

#### 5.5.5 参数与返回类型

函数参数和返回类型通常应使用 JSDoc 注解记录。
有关更多信息，
参见 [7.8 方法与函数注释](#jsdoc-method-and-function-comments)
一节。

<a id="features-functions-default-parameters"></a>

##### 5.5.5.1 默认参数

允许在参数列表中使用等号运算符来声明可选参数。
可选参数必须在等号运算符两侧各留一个空格，
其命名必须与必需参数完全一致（即不得加 `opt_`
前缀），在 JSDoc 类型中使用 `=` 后缀，位于必需
参数之后，并且不得使用会产生可观察副作用的
初始化器。具体函数的所有可选参数都必须有默认值，
即使该值是 `undefined`。与具体函数相反，抽象方法和
接口方法必须省略默认参数值。

示例：

<div class='goodcode'></div>

```js
/**
 * @param {string} required This parameter is always needed.
 * @param {string=} optional This parameter can be omitted.
 * @param {!Node=} node Another optional parameter.
 */
function maybeDoSomething(required, optional = '', node = undefined) {}

/** @interface */
class MyInterface {
  /**
   * Interface and abstract methods must omit default parameter values.
   * @param {string=} optional
   */
  someMethod(optional) {}
}
```

谨慎使用默认参数。当可选参数较多且没有自然的
顺序时，应优先使用解构（如
[5.3.7 解构](#features-objects-destructuring) 所述）来
创建可读的 API。

注意：与 Python 的默认参数不同，可以使用返回新的
可变对象的初始化器（例如 `{}` 或 `[]`），因为每次使用
默认值时都会重新求值初始化器，因此单个对象不会在
多次调用之间共享。

> 提示：虽然包括函数调用在内的任意表达式都可以用作
> 初始化器，但应尽可能保持简单。避免使用会暴露共享
> 可变状态的初始化器，因为这很容易在函数调用之间
> 引入意外的耦合。

<a id="features-functions-rest-parameters"></a>

##### 5.5.5.2 Rest 参数

使用 *rest* 参数，而不要访问 `arguments`。Rest 参数
在 JSDoc 中以 `...` 前缀标注类型。rest 参数必须是
参数列表中的最后一个参数。`...` 与参数名之间
不加空格。不要把 rest 参数命名为 `var_args`。绝不要
把局部变量或参数命名为 `arguments`，因为它会令人困惑地遮蔽内置名称。

示例：

<div class='goodcode'></div>

```js
/**
 * @param {!Array<string>} array This is an ordinary parameter.
 * @param {...number} numbers The remainder of arguments are all numbers.
 */
function variadic(array, ...numbers) {}
```

<a id="features-functions-generics"></a>

#### 5.5.6 泛型

必要时，在函数或方法定义上方的 JSDoc 中用
`@template TYPE` 声明泛型函数和方法。

<a id="features-functions-spread-operator"></a>

#### 5.5.7 展开运算符

函数调用可以使用展开运算符（`...`）。当把数组或
可迭代对象展开为可变参数函数的多个参数时，优先使用
展开运算符而非 `Function.prototype.apply`。`...` 后不加空格。

示例：

<div class='goodcode'></div>

```js
function myFunction(...elements) {}
myFunction(...array, ...iterable, ...generator());
```

<a id="features-string-literals"></a>

### 5.6 字符串字面量

<a id="features-strings-use-single-quotes"></a>

#### 5.6.1 使用单引号

普通字符串字面量用单引号（`'`）定界，
而不用双引号（`"`）。

> 提示：如果字符串中包含单引号字符，可以考虑使用模板
> 字符串，以免必须对引号进行转义。

普通字符串字面量不得跨越多行。

<a id="features-strings-template-strings"></a>

#### 5.6.2 模板字面量

使用模板字面量（以 `` ` `` 定界）而非复杂的字符串
拼接，尤其是涉及多个字符串字面量时。模板
字面量可以跨越多行。

如果模板字面量跨越多行，它不必遵循所在块的
缩进，不过如果多出的空白无关紧要，也可以
遵循缩进。

示例：

<div class='goodcode'></div>

```js
function arithmetic(a, b) {
  return `Here is a table of arithmetic operations:
${a} + ${b} = ${a + b}
${a} - ${b} = ${a - b}
${a} * ${b} = ${a * b}
${a} / ${b} = ${a / b}`;
}
```

<a id="features-strings-no-line-continuations"></a>

#### 5.6.3 不使用行延续符

不要在普通字符串字面量或模板字符串字面量中使用
*行延续符*（即在字符串字面量内用反斜杠结束一行）。
尽管 ES5 允许这样做，但如果反斜杠之后出现任何
尾随空白，就可能导致难以排查的错误，而且对读者来说也不够直观。

不允许：

<div class='badcode'></div>

```js
const longString = 'This is a very long string that far exceeds the 80 \
    column limit. It unfortunately contains long stretches of spaces due \
    to how the continued lines are indented.';
```

应改写为

<div class='goodcode'></div>

```js
const longString = 'This is a very long string that far exceeds the 80 ' +
    'column limit. It does not contain long stretches of spaces since ' +
    'the concatenated strings are cleaner.';
```

这同样适用于模板字面量：

<div class='goodcode'></div>

```js
const longString = `Hello ${name}, this is a very long string that far ` +
    `exceeds the 80 column limit, so it is split into concatenated ` +
    `template literals.`;
```

<a id="features-number-literals"></a>

### 5.7 数字字面量

数字可以用十进制、十六进制、八进制或二进制表示。
十六进制、八进制和二进制分别严格使用 `0x`、`0o`
和 `0b` 前缀，并使用小写字母。除非前导零后面
紧跟 `x`、`o` 或 `b`，否则绝不要包含前导零。

<a id="features-control-structures"></a>

### 5.8 控制结构

<a id="features-for-loops"></a>

#### 5.8.1 For 循环

有了 ES6，这门语言现在有三种不同的 `for` 循环。
三种都可以使用，不过应尽可能优先使用 `for`-`of` 循环。

`for`-`in` 循环只能用于 dict 风格对象（参见
[5.3.3 不要混用加引号与不加引号的键](#features-objects-mixing-keys)），
并且不应用于遍历数组。在 `for`-`in` 循环中应使用
`Object.prototype.hasOwnProperty` 来排除不需要的
prototype 属性。应尽可能优先使用 `for`-`of` 和 `Object.keys`，而不是 `for`-`in`。

<a id="features-exceptions"></a>

#### 5.8.2 异常

异常是该语言的重要组成部分，发生异常情况时
就应使用。始终抛出 `Error` 或 `Error` 的子类：绝不要
抛出字符串字面量或其他对象。构造 `Error` 时
始终使用 `new`。

这一处理也适用于 `Promise` 的拒绝值，因为在异步
函数中 `Promise.reject(obj)` 等价于 `throw obj;`。

自定义异常是从函数传递额外错误信息的好方法。
只要原生 `Error` 类型不够用，就应定义并使用
自定义异常。

相对于临时的错误处理方式（例如传递错误容器
引用类型，或返回带有错误属性的对象），应优先
抛出异常。

<a id="features-empty-catch-blocks"></a>

##### 5.8.2.1 空的 catch 块

捕获异常后什么都不做，极少是正确的做法。当
catch 块中确实完全不需要采取任何行动时，应在
注释中说明这样做的理由。

<div class='goodcode'></div>

```js
try {
  return handleNumericResponse(response);
} catch (ok) {
  // it's not numeric; that's fine, just continue
}
return handleTextResponse(response);
```

不允许：

<div class='badcode'></div>

```js
  try {
    shouldFail();
    fail('expected an error');
  } catch (expected) {
  }
```

> 提示：与某些其他语言不同，上面这样的写法根本行不通，
> 因为这会捕获 `fail` 抛出的错误。请改用
> `assertThrows()`。

<a id="features-switch-statements"></a>

#### 5.8.3 Switch 语句

术语说明：switch 块的花括号内是一个或多个语句组。
每个语句组由一个或多个 switch 标签（`case
FOO:` 或 `default:`）以及其后的一条或多条语句组成。

<a id="features-switch-fall-through"></a>

##### 5.8.3.1 贯穿：需加注释

在 switch 块内，每个语句组要么突然终止（用
`break`、`return` 或由 `throw` 抛出的异常），要么用
注释标明执行将会或可能会继续进入下一个
语句组。任何能表达贯穿含义的注释都足够
（通常是 `// fall through`）。switch 块的最后一个
语句组不需要这种特殊注释。

示例：

<div class='goodcode'></div>

```js
switch (input) {
  case 1:
  case 2:
    prepareOneOrTwo();
  // fall through
  case 3:
    handleOneTwoOrThree();
    break;
  default:
    handleLargeNumber(input);
}
```

<a id="features-switch-default-case"></a>

##### 5.8.3.2 必须有 `default` 分支

每个 switch 语句都包含一个 `default` 语句组，即使
其中没有任何代码。`default` 语句组必须放在最后。

<a id="features-this"></a>

### 5.9 this

只在类的构造函数和方法中、在类的构造函数和方法内
定义的箭头函数中，或者在紧邻外层函数的 JSDoc 中
显式声明了 `@this` 的函数里使用 `this`。

绝不要用 `this` 来指代全局对象、`eval` 的上下文、
事件的目标，或被无谓地 `call()` / `apply()` 调用的函数。

<a id="features-equality-checks"></a>

### 5.10 相等性检查

除下文所述情况外，一律使用恒等运算符（`===`/`!==`）。

<a id="features-equality-checks-exceptions"></a>

#### 5.10.1 需要强制类型转换的例外情况

同时捕获 `null` 和 `undefined` 值：

<div class='goodcode'></div>

```js
if (someObjectOrPrimitive == null) {
  // Checking for null catches both null and undefined for objects and
  // primitives, but does not catch other falsy values like 0 or the empty
  // string.
}
```

<a id="disallowed-features"></a>

### 5.11 禁止使用的特性

<a id="disallowed-features-with"></a>

#### 5.11.1 with

不要使用 `with` 关键字。它会使代码更难理解，并且自 ES5 起
就已在严格模式中被禁用。

<a id="disallowed-features-dynamic-code-evaluation"></a>

#### 5.11.2 动态代码求值

不要使用 `eval` 或 `Function(...string)` 构造函数（代码加载器除外）。
这些特性具有潜在危险，并且在采用
如下策略的环境中根本无法工作：
[内容安全策略（CSP）](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP)。

<a id="disallowed-features-automatic-semicolon-insertion"></a>

#### 5.11.3 自动分号插入

始终用分号结束语句（如上文所述，函数声明和
类声明除外）。

<a id="disallowed-features-non-standard-features"></a>

#### 5.11.4 非标准特性

不要使用非标准特性。这包括已经
被移除的旧特性（例如 `WeakMap.clear`）、尚未标准化的
新特性（例如当前的 TC39 工作草案、处于任何阶段的提案，
或已提出但尚未完成的 Web 标准），以及仅在部分浏览器中
实现的专有特性。只使用当前 ECMA-262
或 WHATWG 标准定义的特性。（注意，针对特定 API 编写的项目，
例如 Chrome 扩展或 Node.js，显然可以使用那些 API。）非标准
的语言“扩展”（例如某些外部转译器所提供的）
一律禁止。

<a id="disallowed-features-wrapper-objects"></a>

#### 5.11.5 原始类型的包装对象

切勿对原始类型的对象包装器（`Boolean`、`Number`、`String`、
`Symbol`）使用 `new`，也不要把它们写进类型注解。

不允许：

<div class='badcode'></div>

```js
const /** Boolean */ x = new Boolean(false);
if (x) alert(typeof x);  // alerts 'object' - WAT?
```

可以像函数一样调用这些包装器来进行强制类型转换（这比
使用 `+` 或拼接空字符串更可取），也可用于创建 symbol。

示例：

<div class='goodcode'></div>

```js
const /** boolean */ x = Boolean(0);
if (!x) alert(typeof x);  // alerts 'boolean', as expected
```

<a id="disallowed-features-modifying-builtin-objects"></a>

#### 5.11.6 修改内置对象

切勿修改内置类型，无论是给它们的构造函数还是给
它们的原型添加方法。避免依赖会这样做的库。请注意，
JSCompiler 的运行时库会尽可能提供符合标准的 polyfill；
除此之外，任何东西都不得修改内置对象。

除非绝对必要（例如第三方 API 有此要求），否则不要向
全局对象添加符号。

<a id="disallowed-features-omitting-parents-with-new"></a>

#### 5.11.7 调用构造函数时省略 `()`

切勿在 `new` 语句中不使用括号 `()` 就调用构造函数。

不允许：

<div class='badcode'></div>

```js
new Foo;
```

应改用：

<div class='goodcode'></div>

```js
new Foo();
```

省略括号可能导致难以察觉的错误。下面两行并不
等价：

<div class='goodcode'></div>

```js
new Foo().Bar();
new Foo.Bar();
```

<a id="naming"></a>

## 6 命名

<a id="naming-rules-common-to-all-identifiers"></a>

### 6.1 所有标识符通用的规则

标识符只使用 ASCII 字母和数字，在下文注明的少数情况下
可使用下划线，极少数情况下（当 Angular 之类的框架有要求时）
可使用美元符号。

在合理范围内，名称要尽可能具有描述性。不必担心节省
水平空间，因为让新读者立刻看懂代码要重要得多。
不要使用对项目之外的读者而言含糊或不熟悉的缩写，
也不要通过删掉单词内部的字母来进行
缩写。

<div class='goodcode'></div>

```js
errorCount          // No abbreviation.
dnsConnectionIndex  // Most people know what "DNS" stands for.
referrerUrl         // Ditto for "URL".
customerId          // "Id" is both ubiquitous and unlikely to be misunderstood.
```

不允许：

<div class='badcode'></div>

```js
n                   // Meaningless.
nErr                // Ambiguous abbreviation.
nCompConns          // Ambiguous abbreviation.
wgcConnections      // Only your group knows what this stands for.
pcReader            // Lots of things can be abbreviated "pc".
cstmrId             // Deletes internal letters.
kSecondsPerDay      // Do not use Hungarian notation.
```

**例外**：作用域不超过 10 行的变量，包括*不*属于导出 API 的
参数，*可以*使用简短的（例如单字母）
变量名。

<a id="naming-rules-by-identifier-type"></a>

### 6.2 按标识符类型划分的规则

<a id="naming-package-names"></a>

#### 6.2.1 包名

包名一律使用 `lowerCamelCase`。例如 `my.exampleCode.deepSpace`，
而不是 `my.examplecode.deepspace` 或 `my.example_code.deep_space`。

**例外**：包名可以遵循 TypeScript 的基于路径的模式。
通常为全小写，并在文件名中相应位置保留下划线。

<a id="naming-class-names"></a>

#### 6.2.2 类名

类、接口、record 和 typedef 的名称使用 `UpperCamelCase`。
未导出的类就是局部变量：不要给它们标注 `@private`。

类型名称通常是名词或名词短语。例如 `Request`、
`ImmutableView` 或 `VisibilityMode`。此外，接口名称有时
也可以是形容词或形容词短语（例如 `Readable`）。

<a id="naming-method-names"></a>

#### 6.2.3 方法名

方法名使用 `lowerCamelCase`。`@private` 方法的名称可以
选择性地以尾随下划线结尾。

方法名通常是动词或动词短语。例如 `sendMessage` 或
`stop_`。属性的 getter 和 setter 方法从来不是必需的，但如果
使用它们，应命名为 `getFoo`（对布尔值也可选用 `isFoo` 或 `hasFoo`），
setter 则命名为 `setFoo(value)`。

JsUnit 测试方法名中也可以使用下划线来分隔名称中
的各个逻辑组成部分。一种典型模式是
`test<MethodUnderTest>_<state>_<expectedOutcome>`，例如
`testPop_emptyStack_throws`。测试方法命名没有唯一正确的做法。

<a id="naming-enum-names"></a>

#### 6.2.4 枚举名

枚举名使用 `UpperCamelCase`，与类相似，通常应为
单数名词。枚举内部的各个项使用
`CONSTANT_CASE` 命名。

<a id="naming-constant-names"></a>

#### 6.2.5 常量名

常量名使用 `CONSTANT_CASE`：全部大写字母，单词之间
用下划线分隔。常量名没有理由以尾随下划线结尾，
因为私有静态属性可以用（隐式私有的）模块局部变量
来替代。

<a id="naming-definition-of-constant"></a>

##### 6.2.5.1 “常量”的定义

每个常量都是 `@const` 静态属性或模块局部的 `const`
声明，但并非所有 `@const` 静态属性和模块局部 `const` 都是
常量。在选用常量命名法之前，先考虑该字段是否真的
算得上*深度不可变*的常量。例如，如果该实例的任何
可观察状态会发生变化，那它几乎肯定不是常量。仅仅
打算永不修改该对象，通常是不够的。

示例：

<div class='goodcode'></div>

```js
// Constants
const NUMBER = 5;
/** @const */ exports.NAMES = goog.debug.freeze(['Ed', 'Ann']);
/** @enum */ exports.SomeEnum = { ENUM_CONSTANT: 'value' };

// Not constants
let letVariable = 'non-const';

class MyClass {
  constructor() { /** @const {string} */ this.nonStatic = 'non-static'; }
};
/** @type {string} */
MyClass.staticButMutable = 'not @const, can be reassigned';

const /** Set<string> */ mutableCollection = new Set();

const /** MyImmutableContainer<SomeMutableType> */ stillMutable =
    new MyImmutableContainer(mutableInner);

const {Foo} = goog.require('my.foo');  // mirrors imported name

const logger = log.getLogger('loggers.are.not.immutable');
```

常量的名称通常是名词或名词短语。

<a id="naming-local-aliases"></a>

##### 6.2.5.2 局部别名

只要相比全限定名能提升可读性，就应使用局部别名。
遵循与 `goog.require` 相同的规则
（[3.6 `goog.require` 与 `goog.requireType` 语句](#file-goog-require)），
并保留被别名名称的最后一部分。别名也可以在
函数内使用。别名必须是 `const`。

示例：

<div class='goodcode'></div>

```js
const staticHelper = importedNamespace.staticHelper;
const CONSTANT_NAME = ImportedClass.CONSTANT_NAME;
const {assert, assertInstanceof} = asserts;
```

<a id="naming-non-constant-field-names"></a>

#### 6.2.6 非常量字段名

非常量字段名（静态或其他）使用 `lowerCamelCase`，
私有字段可以选择性地带尾随下划线。

这些名称通常是名词或名词短语。例如 `computedValues`
或 `index_`。

<a id="naming-parameter-names"></a>

#### 6.2.7 参数名

参数名使用 `lowerCamelCase`。注意，即使参数期望接收一个
构造函数，这条规则同样适用。

公共方法中不应使用单字符参数名。

**例外**：当第三方框架有要求时，参数名可以
以 `$` 开头。此例外不适用于任何其他标识符（例如
局部变量或属性）。

<a id="naming-local-variable-names"></a>

#### 6.2.8 局部变量名

局部变量名使用 `lowerCamelCase`，但上文所述的模块局部
（顶层）常量除外。函数作用域内的常量仍使用
`lowerCamelCase` 命名。注意，即使变量保存的是构造函数，
也仍使用 `lowerCamelCase`。

<a id="naming-template-parameter-names"></a>

#### 6.2.9 模板参数名

模板参数名应为简洁的、由单个单词或单个字母构成的
标识符，并且必须全部大写，例如 `TYPE` 或 `THIS`。

<div class='goodcode'></div>

```js
/** @template T */
/** @template KEY, VALUE */
```

<div class='badcode'></div>

```js
/** @template ElementType */
/** @template KEY_TYPE */
```

<a id="naming-module-local-names"></a>

#### 6.2.10 模块局部名称

未被导出的模块局部名称隐式具有私有性。不要给它们
标注 `@private`。这适用于类、函数、变量、常量、
枚举以及其他模块局部标识符。

<a id="naming-camel-case-defined"></a>

### 6.3 驼峰命名法：定义

有时，把英文短语转换为驼峰形式不止一种合理方式，
例如当出现 "IPv6" 或 "iOS" 这类缩写词或不寻常的构词时。
为提高可预测性，Google Style 规定了以下（几乎）
确定性的方案。

从名称的散文形式开始：

1.  把短语转换为纯 ASCII 并去掉所有撇号。例如，
    "Müller's algorithm" 可能变为 "Muellers algorithm"。
2.  把得到的结果切分为单词，按空格和其余
    标点（通常是连字符）拆分。
    1.  建议：如果某个单词在日常用法中已经有约定俗成的
        驼峰式外观，就把它拆成各个组成部分（例如
        "AdWords" 变成 "ad words"）。注意，"iOS" 这样的词
        本身其实并不算驼峰形式；它不遵循任何惯例，因此
        这条建议并不适用。
3.  现在把全部内容转为小写（包括缩写词），然后只把以下
    各项的首字符大写：
    1.  … 每个单词，得到 `UpperCamelCase`，或者
    2.  … 除第一个单词外的每个单词，得到 `lowerCamelCase`
4.  最后，把所有单词拼接成单个标识符。

注意，原始单词的大小写形式几乎完全被忽略。

`lowerCamelCase` 的示例：

散文形式              | 正确             | 不正确
:---------------------: | :-----------------: | :-----------------:
"XML HTTP request"      | `xmlHttpRequest`    | `XMLHTTPRequest`
"new customer ID"       | `newCustomerId`     | `newCustomerID`
"inner stopwatch"       | `innerStopwatch`    | `innerStopWatch`
"supports IPv6 on iOS?" | `supportsIpv6OnIos` | `supportsIPv6OnIOS`
"YouTube importer"      | `youTubeImporter`   | `youtubeImporter`*

*可以接受，但不推荐。

至于 `UpperCamelCase` 的示例，把每个正确的
`lowerCamelCase` 示例的首字母大写即可。

注：英语中有些单词的连字符用法存在歧义：例如
"nonempty" 和 "non-empty" 都正确，因此方法名 `checkNonempty`
和 `checkNonEmpty` 也同样都正确。

<a id="jsdoc"></a>

## 7 JSDoc

[JSDoc](https://github.com/google/closure-compiler/wiki/Annotating-JavaScript-for-the-Closure-Compiler)
用于所有的类、字段和方法。

<a id="jsdoc-general-form"></a>

### 7.1 通用形式

JSDoc 块的基本格式如下例所示：

<div class='goodcode'></div>

```js
/**
 * Multiple lines of JSDoc text are written here,
 * wrapped normally.
 * @param {number} arg A number to do something to.
 */
function doSomething(arg) { … }
```

或如下面这个单行示例：

<div class='goodcode'></div>

```js
/** @const @private {!Foo} A short bit of JSDoc. */
this.foo_ = foo;
```

如果单行注释溢出为多行，就必须采用多行风格，
让 `/**` 和 `*/` 各自独占一行。

许多工具会从 JSDoc 注释中提取元数据，以执行代码校验和
优化。因此，这些注释**必须**格式正确。

<a id="jsdoc-markdown"></a>

### 7.2 Markdown

JSDoc 使用 Markdown 书写，必要时也可以包含 HTML。

注意，自动提取 JSDoc 的工具（例如
[JsDossier](https://github.com/jleyba/js-dossier)）通常会忽略纯文本
格式，因此如果你这样写：

<div class='badcode'></div>

```js
/**
 * Computes weight based on three factors:
 *   items sent
 *   items received
 *   last timestamp
 */
```

它就会变成这样：

```
Computes weight based on three factors: items sent items received last timestamp
```

应改写成 Markdown 列表：

<div class='goodcode'></div>

```js
/**
 * Computes weight based on three factors:
 *
 *  - items sent
 *  - items received
 *  - last timestamp
 */
```

<a id="jsdoc-tags"></a>

### 7.3 JSDoc 标签

Google Style 只允许使用 JSDoc 标签的一个子集。
完整列表参见 [9.1 JSDoc 标签参考](#appendices-jsdoc-tag-reference)。
大多数标签必须各自独占一行，且标签要放在
行首。

不允许：

<div class='badcode'></div>

```js
/**
 * The "param" tag must occupy its own line and may not be combined.
 * @param {number} left @param {number} right
 */
function add(left, right) { ... }
```

不需要任何附加数据的简单标签（例如 `@private`、
`@const`、`@final`、`@export`）可以合并到同一行，
并在适当时候附带可选的类型。

<div class='goodcode'></div>

```js
/**
 * Place more complex annotations (like "implements" and "template")
 * on their own lines. Multiple simple tags (like "export" and "final")
 * may be combined in one line.
 * @export @final
 * @implements {Iterable<TYPE>}
 * @template TYPE
 */
class MyClass {
  /**
   * @param {!ObjType} obj Some object.
   * @param {number=} num An optional number.
   */
  constructor(obj, num = 42) {
    /** @private @const {!Array<!ObjType|number>} */
    this.data_ = [obj, num];
  }
}
```

关于何时合并标签、以何种顺序合并，并没有硬性规定，但要
保持一致。

有关在 JavaScript 中标注类型的一般信息，参见
[Annotating JavaScript for the Closure Compiler](https://github.com/google/closure-compiler/wiki/Annotating-JavaScript-for-the-Closure-Compiler)
以及
[Types in the Closure Type System](https://github.com/google/closure-compiler/wiki/Types-in-the-Closure-Type-System)。

<a id="jsdoc-line-wrapping"></a>

### 7.4 换行

换行的块标签缩进四个空格。换行的描述文本可以与
前几行的描述对齐，但不鼓励这种水平
对齐方式。

<div class='goodcode'></div>

```js
/**
 * Illustrates line wrapping for long param/return descriptions.
 * @param {string} foo This is a param with a description too long to fit in
 *     one line.
 * @return {number} This returns something that has a description too long to
 *     fit in one line.
 */
exports.method = function(foo) {
  return 5;
};
```

换行 `@desc` 或 `@fileoverview` 描述时不要缩进。

<a id="jsdoc-top-file-level-comments"></a>

### 7.5 顶层／文件级注释

文件可以有一个顶层的文件概览。版权声明、作者
信息以及默认的[可见性级别](#jsdoc-visibility-annotations) 都是
可选的。通常只要文件包含的不止单个类定义，就建议
写文件概览。顶层注释旨在让不熟悉代码的读者
了解该文件中有什么。如果存在，它可以
描述文件的内容，以及任何依赖项或
兼容性信息。换行不缩进。

示例：

<div class='goodcode'></div>

```js
/**
 * @fileoverview Description of file, its uses and information
 * about its dependencies.
 * @package
 */
```

<a id="jsdoc-class-comments"></a>

### 7.6 类注释

类、接口和 record 都必须带有描述性文档，并按需
标注模板参数、所实现的接口、可见性或其他适当的
标签。类描述应为读者提供足够的信息，使其
知道如何以及何时使用该类，以及正确使用该类
所需的其他注意事项。构造函数上可以省略文字描述。
定义类时，`@constructor` 和 `@extends` 注解不与 `class` 关键字
一起使用，除非该类继承自泛型类。
定义 `@interface` 或 `@record` 时，`@extends` 注解用于
定义子类，而绝不使用 `extends` 关键字。

<div class='goodcode'></div>

```js
/**
 * A fancier event target that does cool things.
 * @implements {Iterable<string>}
 */
class MyFancyTarget extends EventTarget {
  /**
   * @param {string} arg1 An argument that makes this more interesting.
   * @param {!Array<number>} arg2 List of numbers to be processed.
   */
  constructor(arg1, arg2) {
    // ...
  }
};

/**
 * Records are also helpful.
 * @extends {Iterator<TYPE>}
 * @record
 * @template TYPE
 */
class Listable {
  /** @return {TYPE} The next item in line to be returned. */
  next() {}
}
```

<a id="jsdoc-enum-and-typedef-comments"></a>

### 7.7 枚举与 typedef 注释

所有枚举和 typedef 都必须在前一行用适当的 JSDoc 标签
（`@typedef` 或 `@enum`）加以说明。公开的枚举和 typedef 还
必须有描述。各个枚举项可以在前一行用 JSDoc
注释加以说明。

<div class='goodcode'></div>

```js
/**
 * A useful type union, which is reused often.
 * @typedef {!FruitType|!FruitTypeEnum}
 */
let CoolUnionType;

/**
 * Types of fruits.
 * @enum {string}
 */
const FruitTypeEnum = {
  /** This kind is very sour. */
  SOUR: 'sour',
  /** The less-sour kind. */
  SWEET: 'sweet',
};
```

typedef 适合用来定义简短的 record 类型，或者为联合类型、
复杂函数或泛型类型定义别名。对于字段很多的 record 类型，
应避免使用 typedef，因为它无法为各个字段分别写文档，
也不能使用模板或递归引用。对于大型 record 类型，
应优先使用 `@record`。

<a id="jsdoc-method-and-function-comments"></a>

### 7.8 方法与函数注释

在方法和具名函数中，必须记录参数和返回类型，
即便是签名相同的 `@override` 也不例外。必要时
应记录 `this` 的类型。如果函数没有非空的 `return` 语句，
可以省略返回类型。

方法、参数和返回值的描述（但不包括类型）如果从方法
其余的 JSDoc 或其签名中已经显而易见，则可以省略。

方法描述以一个描述该方法作用的动词短语开头。
这个短语不是祈使句，而是用第三人称书写，
就像前面隐含了 "This method ..." 一样。

如果方法覆盖了超类的方法，就必须包含 `@override`
注解。对于被覆盖的方法，所有 `@param` 和 `@return` 注解
都必须显式写出，即使没有细化超类方法中的任何类型。
这是为了与 TypeScript 保持一致。

<div class='goodcode'></div>

```js
/** A class that does something. */
class SomeClass extends SomeBaseClass {
  /**
   * Operates on an instance of MyClass and returns something.
   * @param {!MyClass} obj An object that for some reason needs detailed
   *     explanation that spans multiple lines.
   * @param {!OtherClass} obviousOtherClass
   * @return {boolean} Whether something occurred.
   */
  someMethod(obj, obviousOtherClass) { ... }

  /**
   * @param {string} param
   * @return {string}
   * @override
   */
  overriddenMethod(param) { ... }
}

/**
 * Demonstrates how top-level functions follow the same rules.  This one
 * makes an array.
 * @param {TYPE} arg
 * @return {!Array<TYPE>}
 * @template TYPE
 */
function makeArray(arg) { ... }
```

如果只需要记录函数的参数和返回类型，可以
选择在函数签名中使用内联 JSDoc。这些内联 JSDoc
无需标签即可指定返回类型和参数类型。

<div class='goodcode'></div>

```js
function /** string */ foo(/** number */ arg) {...}
```

如果需要描述或标签，就在方法上方使用单个 JSDoc 注释。
例如，返回值的方法需要 `@return` 标签。

<div class='goodcode'></div>

```js
class MyClass {
  /**
   * @param {number} arg
   * @return {string}
   */
  bar(arg) {...}
}
```

<div class='badcode'></div>

```js
// Illegal inline JSDocs.

class MyClass {
  /** @return {string} */ foo() {...}
}

/** No function description allowed inline here. */ function bar() {...}

function /** Function description is also illegal here. */ baz() {...}
```

在匿名函数中，注解通常是可选的。如果自动类型
推断不够用，或者显式注解能提升可读性，就
像下面这样标注参数和返回类型：

<div class='goodcode'></div>

```js
promise.then(
    /** @return {string} */
    (/** !Array<string> */ items) => {
      doSomethingWith(items);
      return items[0];
    });
```

关于函数类型表达式，参见
[7.10.4 函数类型表达式](#jsdoc-function-types)。

<a id="jsdoc-property-comments"></a>

### 7.9 属性注释

必须记录属性的类型。对于私有属性，如果名称和类型
已经足以让代码被理解，则可以省略
描述。

公开导出的常量与属性采用相同的注释方式。

<div class='goodcode'></div>

```js
/** My class. */
class MyClass {
  /** @param {string=} someString */
  constructor(someString = 'default string') {
    /** @private @const {string} */
    this.someString_ = someString;

    /** @private @const {!OtherType} */
    this.someOtherThing_ = functionThatReturnsAThing();

    /**
     * Maximum number of things per pane.
     * @type {number}
     */
    this.someProperty = 4;
  }
}

/**
 * The number of times we'll try before giving up.
 * @const {number}
 */
MyClass.RETRY_COUNT = 33;
```

<a id="jsdoc-type-annotations"></a>

### 7.10 类型注解

类型注解出现在 `@param`、`@return`、`@this` 和 `@type` 标签上，
也可选地出现在 `@const`、`@export` 以及任何可见性标签上。
附着在 JSDoc 标签上的类型注解必须始终用花括号括起来。

<a id="jsdoc-nullability"></a>

#### 7.10.1 可空性

类型系统定义了修饰符 `!` 和 `?`，分别表示非空和可空。
这些修饰符必须放在类型之前。

可空性修饰符对不同类型有不同要求，这些类型
大致分为两类：

{% raw %}
1.  原始类型（`string`、`number`、`boolean`、`symbol`、
    `undefined`、`null`）与字面量类型（`{function(...): ...}` 和 `{{foo:
    string...}}`）的类型注解默认始终不可空。用 `?` 修饰符
    使其可空，但省略多余的 `!`。
{% endraw %}
2.  引用类型（一般指任何 `UpperCamelCase` 形式的类型，包括
    `some.namespace.ReferenceType`）指向在别处定义的类、枚举、record
    或 typedef。由于这些类型可能可空也可能不可空，
    仅凭名称无法判断它是否可空。对于这类类型，务必
    显式使用 `?` 和 `!` 修饰符，以避免在使用处
    产生歧义。

错误：

<div class='badcode'></div>

```js
const /** MyObject */ myObject = null; // Non-primitive types must be annotated.
const /** !number */ someNum = 5; // Primitives are non-nullable by default.
const /** number? */ someNullableNum = null; // ? should precede the type.
const /** !{foo: string, bar: number} */ record = ...; // Already non-nullable.
const /** MyTypeDef */ def = ...; // Not sure if MyTypeDef is nullable.

// Not sure if object (nullable), enum (non-nullable, unless otherwise
// specified), or typedef (depends on definition).
const /** SomeCamelCaseName */ n = ...;
```

正确：

<div class='goodcode'></div>

```js
const /** ?MyObject */ myObject = null;
const /** number */ someNum = 5;
const /** ?number */ someNullableNum = null;
const /** {foo: string, bar: number} */ record = ...;
const /** !MyTypeDef */ def = ...;
const /** ?SomeCamelCaseName */ n = ...;
```

<a id="jsdoc-type-casts"></a>

#### 7.10.2 类型转换

当编译器无法准确推断某个表达式的类型，
并且
[goog.asserts](https://google.github.io/closure-library/api/goog.asserts.html)
中的断言函数也无法补救时，可以添加类型注解
注释、并用括号把表达式括起来，以收紧类型。注意，
括号是必需的。

<div class='goodcode'></div>

```js
/** @type {number} */ (x)
```

<a id="jsdoc-template-parameter-types"></a>

#### 7.10.3 模板参数类型

始终指定模板参数。这样编译器能做得更好，也
让读者更容易理解代码的用途。

错误：

<div class='badcode'></div>

```js
const /** !Object */ users = {};
const /** !Array */ books = [];
const /** !Promise */ response = ...;
```

正确：

<div class='goodcode'></div>

```js
const /** !Object<string, !User> */ users = {};
const /** !Array<string> */ books = [];
const /** !Promise<!Response> */ response = ...;

const /** !Promise<undefined> */ thisPromiseReturnsNothingButParameterIsStillUseful = ...;
const /** !Object<string, *> */ mapOfEverything = {};
```

不应使用模板参数的情形：

*   `Object` 用于类型层次结构，而非类 map 的结构。

<a id="jsdoc-function-types"></a>

#### 7.10.4 函数类型表达式

**术语说明**：*函数类型表达式* 指带有 `function` 关键字的、
用于函数类型的类型注解（参见
下面的示例）。

凡是给出了函数定义的地方，都不要使用函数类型表达式。
用 `@param` 和 `@return` 指定参数和返回类型，或用内联
注解指定（参见
[7.8 方法与函数注释](#jsdoc-method-and-function-comments)）。
这包括匿名函数，以及定义后赋值给 const 的函数
（此时函数的 JSDoc 出现在整个赋值表达式上方）。

例如，在 `@typedef`、`@param` 或 `@return` 内部需要
函数类型表达式。对于函数类型的变量或属性，如果没有
立即用函数定义初始化，也要使用它。

<div class='goodcode'></div>

```js
  /** @private {function(string): string} */
  this.idGenerator_ = googFunctions.identity;
```

使用函数类型表达式时，务必显式指定返回类型。
否则默认返回类型是 "unknown"（`?`），这会导致
奇怪且意想不到的行为，而且很少是真正想要的。

错误 —— 存在类型错误，但没有给出警告：

<div class='badcode'></div>

```js
/** @param {function()} generateNumber */
function foo(generateNumber) {
  const /** number */ x = generateNumber();  // No compile-time type error here.
}

foo(() => 'clearly not a number');
```

正确：

<div class='goodcode'></div>

```js
/**
 * @param {function(): *} inputFunction1 Can return any type.
 * @param {function(): undefined} inputFunction2 Definitely doesn't return
 *      anything.
 * NOTE: the return type of `foo` itself is safely implied to be {undefined}.
 */
function foo(inputFunction1, inputFunction2) {...}
```

<a id="jsdoc-whitespace"></a>

#### 7.10.5 空白

在类型注解内部，每个逗号或冒号之后都必须有一个空格
或换行。可以插入额外的换行以提升可读性，或
避免超出列宽限制。这些换行应遵循相关指南来选择
并缩进（例如
[4.5 换行](#formatting-line-wrapping) 以及
[4.2 块缩进：+2 空格](#formatting-block-indentation)）。类型注解中
不允许出现其他空白。

正确：

<div class='goodcode'></div>

<!-- {% raw %} -->

```js
/** @type {function(string): number} */

/** @type {{foo: number, bar: number}} */

/** @type {number|string} */

/** @type {!Object<string, string>} */

/** @type {function(this: Object<string, string>, number): string} */

/**
 * @type {function(
 *     !SuperDuperReallyReallyLongTypedefThatForcesTheLineBreak,
 *     !OtherVeryLongTypedef): string}
 */

/**
 * @type {!SuperDuperReallyReallyLongTypedefThatForcesTheLineBreak|
 *     !OtherVeryLongTypedef}
 */
```

<!-- {% endraw %} -->

错误：

<div class='badcode'></div>

<!-- {% raw %} -->

```js
// Only put a space after the colon
/** @type {function(string) : number} */

// Put spaces after colons and commas
/** @type {{foo:number,bar:number}} */

// No space in union types
/** @type {number | string} */
```

<!-- {% endraw %} -->

<a id="jsdoc-visibility-annotations"></a>

### 7.11 可见性注解

可见性注解（`@private`、`@package`、`@protected`）可以在
`@fileoverview` 块中指定，也可以标注在任何导出的符号或属性上。
不要为局部变量指定可见性，无论它位于函数内还是模块
顶层。`@private` 名称可以选择性地以下划线结尾。

<a id="policies"></a>

## 8 策略

<a id="policies-be-consistent"></a>

### 8.1 Google Style 未规定的问题：保持一致！

对于本规范未能明确定论的任何风格问题，
优先沿用同一文件中其他代码已有的做法。如果这样
仍无法解决问题，就考虑仿照同一包中的其他
文件。

<a id="policies-compiler-warnings"></a>

### 8.2 编译器警告

<a id="policies-use-a-standard-warning-set"></a>

#### 8.2.1 使用标准警告集

项目应尽可能使用 `--warning_level=VERBOSE`。

<a id="policies-how-to-handle-a-warning"></a>

#### 8.2.2 如何处理警告

在采取任何行动之前，先确保自己准确理解警告
想告诉你什么。如果不确定警告为何出现，就寻求帮助。

理解警告之后，依次尝试以下解决方案：

1.  **首先，修复它或绕过它。** 尽最大努力真正
    解决该警告，或者换一种方式完成任务，从而完全
    避开这种情况。
2.  **否则，判断它是否为误报。** 如果你确信
    该警告无效、代码实际上安全且正确，就添加注释
    向读者说明这一点，并加上 `@suppress`
    注解。
3.  **否则，留下一条 TODO 注释。** 这是**最后的手段**。如果
    这样做，**不要屏蔽该警告。** 在能够妥善处理之前，
    警告应当保持可见。

<a id="policies-suppress-a-warning-at-the-narrowest-reasonable-scope"></a>

#### 8.2.3 在尽可能窄的合理范围内屏蔽警告

警告应在尽可能窄的合理范围内屏蔽，通常是
单个局部变量或非常小的方法。常常仅仅为了
这个原因就把变量或方法提取出来。

示例

<div class='goodcode'></div>

```js
/** @suppress {uselessCode} Unrecognized 'use asm' declaration */
function fn() {
  'use asm';
  return 0;
}
```

即便一个类里有大量屏蔽声明，也好过让整个类
对这类警告视而不见。

<a id="policies-deprecation"></a>

### 8.3 弃用

用 `@deprecated` 注解标记已弃用的方法、类或接口。
弃用注释必须包含简单、清晰的指引，告诉人们如何修改
调用处。

<a id="policies-code-not-in-google-style"></a>

### 8.4 不符合 Google Style 的代码

你偶尔会在代码库中遇到不完全符合 Google Style 的
文件。它们可能来自收购，可能写于 Google Style
就某个问题给出立场之前，也可能出于其他原因而
采用非 Google Style 的写法。

<a id="policies-reformatting-existing-code"></a>

#### 8.4.1 重新格式化已有代码

更新已有代码风格时，请遵循以下指南。

1.  不要求把所有已有代码都改成符合当前的风格
    指南。重新格式化已有代码是在代码改动量与一致性
    之间做权衡。风格规则会随时间演进，这类为保持
    合规而做的微调会带来不必要的改动。不过，如果对
    某个文件进行了重大修改，就应让该文件符合
    Google Style。
2.  注意不要让顺手做的风格修正冲淡 CL 的重点。
    如果你发现自己对 CL 的核心目标并不关键的风格
    改动做了很多，就把这些改动提到单独的 CL 中。

<a id="policies-newly-added-code-use-google-style"></a>

#### 8.4.2 新增代码：使用 Google Style

全新的文件一律使用 Google Style，而不管同一包中
其他文件采用了怎样的风格。

向不符合 Google Style 的文件添加新代码时，建议先
重新格式化已有代码，具体请遵循
[8.4.1 重新格式化已有代码](#policies-reformatting-existing-code) 中的建议。

如果没有做这种重新格式化，新代码就应尽可能与
同一文件中的已有代码保持一致，但不得违反风格
指南。

<a id="policies-local-style-rules"></a>

### 8.5 局部风格规则

团队和项目可以在本文档之外采用额外的风格规则，
但必须接受清理性改动可能不遵守这些附加规则，
也不得因违反任何附加规则而阻止此类清理改动。
当心那些毫无作用的过多规则。风格指南并不试图
为每一种可能的情形都定义风格，你也不应如此。

<a id="policies-generated-code-mostly-exempt"></a>

### 8.6 生成的代码：基本豁免

构建过程生成的源代码不要求符合
Google Style。不过，凡是会被手写源代码引用的生成标识符，
都必须遵循命名要求。作为一项特殊例外，这类标识符
允许包含下划线，这有助于避免与手写标识符
发生冲突。

<a id="appendices"></a>

## 9 附录

<a id="appendices-jsdoc-tag-reference"></a>

### 9.1 JSDoc 标签参考

JSDoc 在 JavaScript 中承担多种用途。除了用于
生成文档，它还被用来控制工具链。最广为人知的
是 Closure Compiler 的类型注解。

<a id="appendices-type-annotations"></a>

#### 9.1.1 类型注解与其他 Closure Compiler 注解

Closure Compiler 所使用的 JSDoc 文档见
[Annotating JavaScript for the Closure Compiler](https://github.com/google/closure-compiler/wiki/Annotating-JavaScript-for-the-Closure-Compiler)
以及
[Types in the Closure Type System](https://github.com/google/closure-compiler/wiki/Types-in-the-Closure-Type-System)。

<a id="appendices-documentation-annotations"></a>

#### 9.1.2 文档注解

除了
[Annotating JavaScript for the Closure Compiler](https://github.com/google/closure-compiler/wiki/Annotating-JavaScript-for-the-Closure-Compiler)
中描述的 JSDoc 之外，下列标签也很常见，并且被各种
文档生成工具（例如 [JsDossier](https://github.com/jleyba/js-dossier)）
很好地支持，纯粹用于文档目的。

##### 9.1.2.1 `@author` 或 `@owner` - *不推荐。*

**不推荐。**

语法：`@author username@google.com (First Last)`

<div class='goodcode'></div>

```js
/**
 * @fileoverview Utilities for handling textareas.
 * @author kuth@google.com (Uthur Pendragon)
 */
```

记录文件的作者或测试的所有者，通常只用在
`@fileoverview` 注释中。单元测试仪表盘使用 `@owner` 标签
来确定测试结果的归属。

##### 9.1.2.2 `@bug`

语法：`@bug bugnumber`

<div class='goodcode'></div>

```js
/** @bug 1234567 */
function testSomething() {
  // …
}

/**
 * @bug 1234568
 * @bug 1234569
 */
function testTwoBugs() {
  // …
}
```

指明给定测试函数所回归测试的 bug。

多个 bug 应各自占用一条 `@bug` 行，以便尽可能
方便地检索回归测试。

##### 9.1.2.3 `@code` - *已弃用。请勿使用。*

**已弃用。请勿使用。请改用 Markdown 反引号。**

语法：`{@code ...}`

过去，`` `BatchItem` `` 曾写作 `{@code BatchItem}`。

<div class='goodcode'></div>

```js
/** Processes pending `BatchItem` instances. */
function processBatchItems() {}
```

表示 JSDoc 描述中的某个术语是代码，以便在生成的
文档中正确地格式化。

##### 9.1.2.4 `@desc`

语法：`@desc Message description`

<div class='goodcode'></div>

```js
/** @desc Notifying a user that their account has been created. */
exports.MSG_ACCOUNT_CREATED = goog.getMsg(
    'Your account has been successfully created.');
```

##### 9.1.2.5 `@link`

语法：`{@link ...}`

该标签用于在生成的文档中生成交叉引用
链接。

<div class='goodcode'></div>

```js
/** Processes pending {@link BatchItem} instances. */
function processBatchItems() {}
```

**历史注记：** @link 标签也曾被用来在生成的文档中
创建外部链接。对于外部链接，请始终改用 Markdown 的
链接语法：

<div class='goodcode'></div>

```js
/**
 * This class implements a useful subset of the
 * [native Event interface](https://dom.spec.whatwg.org/#event).
 */
class ApplicationEvent {}
```

##### 9.1.2.6 `@see`

语法：`@see Link`

<div class='goodcode'></div>

```js
/**
 * Adds a single item, recklessly.
 * @see #addSafely
 * @see goog.Collect
 * @see goog.RecklessAdder#add
 */
```

建立指向另一个类函数或方法的引用。

##### 9.1.2.7 `@supported`

语法：`@supported Description`

<div class='goodcode'></div>

```js
/**
 * @fileoverview Event Manager
 * Provides an abstracted interface to the browsers' event systems.
 * @supported IE10+, Chrome, Safari
 */
```

用在 fileoverview 中，指明该文件支持哪些浏览器。

你还可能在第三方代码中看到其他类型的 JSDoc 注解。
这些注解出现在
[JSDoc Toolkit Tag Reference](http://code.google.com/p/jsdoc-toolkit/wiki/TagReference)
中，但不属于有效的 Google style 的组成部分。

<a id="appendices-framework-specific-annotations"></a>

#### 9.1.3 框架专属注解

以下注解专属于某个特定框架。

##### 9.1.3.1 `@ngInject` 用于 Angular 1

##### 9.1.3.2 `@polymerBehavior` 用于 Polymer

[https://github.com/google/closure-compiler/wiki/Polymer-Pass](https://github.com/google/closure-compiler/wiki/Polymer-Pass)

<a id="appendices-notes-about-standard-closure-compiler-annotations"></a>

#### 9.1.4 关于标准 Closure Compiler 注解的说明

以下标签曾是标准标签，但现已弃用。

##### 9.1.4.1 `@expose` - *已弃用。请勿使用。*

**已弃用。请勿使用。请改用 `@export` 和／或 `@nocollapse`。**

##### 9.1.4.2 `@inheritDoc` - *已弃用。请勿使用。*

**已弃用。请勿使用。请改用 `@override`。**

<a id="appendices-commonly-misunderstood-style-rules"></a>

### 9.2 常被误解的风格规则

这里汇集了一些关于 JavaScript 版 Google Style 的
鲜为人知或常被误解的事实。（以下都是正确的陈述，
并不是一份“迷思”清单。）

*   源文件中既不要求版权声明，也不要求 `@author` 署名。
    （两者也都没有被明确推荐。）
*   对于类成员的排列顺序，并没有“一成不变”的硬性规则
    （[5.4 类](#features-classes)）。
*   空块通常可以简洁地写成 `{}`，详见
    （[4.1.3 空块：可以简洁表示](#formatting-empty-blocks)）。
*   换行的首要原则是：尽量在更高的语法层级断开
    （[4.5.1 在哪里断行](#formatting-where-to-break)）。
*   字符串字面量、注释和 JSDoc 中都允许使用非 ASCII
    字符；事实上，当它们比等价的 Unicode 转义更易于
    阅读时，还推荐使用
    （[2.3.3 非 ASCII 字符](#non-ascii-characters)）。

<a id="appendices-style-related-tools"></a>

### 9.3 与风格相关的工具

以下工具用于支持 Google Style 的各个方面。

<a id="appendices-tools-closure-compiler"></a>

#### 9.3.1 Closure Compiler

该程序执行类型检查及其他检查、优化，以及其他
转换（例如把代码降级为 ECMAScript 5）。

<a id="appendices-clang-format"></a>

#### 9.3.2 `clang-format`

该程序把 JavaScript 源代码重新格式化为 Google Style，
还遵循若干非强制但常常能提升可读性的格式惯例。
`clang-format` 产生的输出符合
风格指南。

`clang-format` 并非强制要求。作者可以改动它的输出，
评审者也可以要求做出这类改动；争议按通常方式解决。
不过，各个子树可以选择在本地启用这种强制约束。

<a id="appendices-closure-compiler-linter"></a>

#### 9.3.3 Closure compiler linter

该程序用于检查各种失误和反模式。

<a id="appendices-conformance-framework"></a>

#### 9.3.4 一致性框架

JS Conformance Framework 是 Closure Compiler 的一部分，
它为开发者提供一种简便方式，用来指定在标准检查之外
还要对其代码库运行的一组附加检查。一致性检查
例如可以禁止访问某个属性、禁止调用某个
函数，或禁止缺少类型信息（unknowns）。

这些规则常用于强制实施关键限制（例如定义全局变量，
这可能破坏代码库）和安全模式（例如使用 `eval` 或对
`innerHTML` 赋值），或者较宽松地用于提升代码质量。

更多信息参见
[JS Conformance Framework](https://github.com/google/closure-compiler/wiki/JS-Conformance-Framework) 的官方文档。

<a id="appendices-legacy-exceptions"></a>

### 9.4 旧平台的例外

<a id="appendices-legacy-exceptions-overview"></a>

#### 9.4.1 概述

本节描述当代码作者无法使用现代 ECMAScript 语法时
需要遵循的例外与附加规则。当现代 ECMAScript
语法不可用时，就需要对推荐风格作出例外，
现列出如下：

*   允许使用 `var` 声明
*   允许使用 `arguments`
*   允许不带默认值的可选参数

<a id="appendices-legacy-exceptions-var"></a>

#### 9.4.2 使用 `var`

<a id="appendices-legacy-exceptions-var-scope"></a>

##### 9.4.2.1 `var` 声明不是块级作用域的

`var` 声明的作用域始于最近的外层函数、脚本或模块的
开头，这可能导致意外行为，尤其是当函数闭包引用
循环内的 `var` 声明时。下面的代码给出了
一个例子：

<div class='badcode'></div>

```js
for (var i = 0; i < 3; ++i) {
  var iteration = i;
  setTimeout(function() { console.log(iteration); }, i*1000);
}

// logs 2, 2, 2 -- NOT 0, 1, 2
// because `iteration` is function-scoped, not local to the loop.
```

<a id="appendices-legacy-exceptions-var-declare"></a>

##### 9.4.2.2 在尽可能接近首次使用的位置声明变量

尽管 `var` 声明的作用域始于外层函数的开头，
出于可读性考虑，`var` 声明仍应尽可能靠近首次使用处。
不过，如果某个变量在块外被引用，就不要把它的
`var` 声明放在该块内。例如：

<div class='goodcode'></div>

```js
function sillyFunction() {
  var count = 0;
  for (var x in y) {
    // "count" could be declared here, but don't do that.
    count++;
  }
  console.log(count + ' items in y');
}
```

<a id="appendices-legacy-exceptions-var-const"></a>

##### 9.4.2.3 对常量变量使用 @const

对于本应使用 `const` 关键字的全局声明，若该关键字
可用，则改为用 `@const` 标注 `var` 声明（对局部变量
而言这是可选的）。

<div class='goodcode'></div>

```js
/** @const */
var MAX_RETRIES = 3;
```

<a id="appendices-legacy-exceptions-function"></a>

#### 9.4.3 不要使用块级作用域的函数声明

**不要**这样做：

<div class='badcode'></div>

```js
if (x) {
  function foo() {}
}
```

虽然 ECMAScript 6 之前实现的大多数 JavaScript 虚拟机都支持
块内的函数声明，但这并未标准化。各实现之间彼此不一致，
也与如今已成为标准的 ECMAScript 块级作用域函数声明行为
不一致。ECMAScript 5 及更早的标准只允许在脚本或
函数的根语句列表中进行函数声明，并明确禁止在严格模式下
的块作用域中使用。

为获得一致的行为，请改用以函数表达式初始化的 `var`
来在块内定义函数：

<div class='goodcode'></div>

```js
if (x) {
  var foo = function() {};
}
```

<a id="appendices-legacy-exceptions-goog-provide"></a>

#### 9.4.4 使用 `goog.provide`/`goog.require` 进行依赖管理

<a id="appendices-legacy-exceptions-goog-provide-summary"></a>

##### 9.4.4.1 概要

**警告：`goog.provide` 依赖管理已弃用。** 所有新文件，
即使在旧文件中使用 `goog.provide` 的项目里，也应使用
[`goog.module`](#source-file-structure)。以下规则仅适用于
已有的 `goog.provide` 文件。

*   将所有 `goog.provide` 放在最前，`goog.require` 其次。用空行
    分隔这两类语句。
*   按字母顺序排列条目（大写字母优先）。
*   不要折行 `goog.provide` 和 `goog.require` 语句。必要时可超过 80
    列的限制。
*   只提供顶层符号。

`goog.provide` 语句应集中放在一起并置于最前。所有
`goog.require` 语句应紧随其后。两个列表之间应以
空行分隔。

与其他语言中的 import 语句类似，`goog.provide` 与
`goog.require` 语句都应写在一行内，即使会
超过 80 列的行长限制。

各行应按字母顺序排序，大写字母优先：

<div class='goodcode'></div>

```js
goog.provide('namespace.MyClass');
goog.provide('namespace.helperFoo');

goog.require('an.extremelyLongNamespace.thatSomeoneThought.wouldBeNice.andNowItIsLonger.Than80Columns');
goog.require('goog.dom');
goog.require('goog.dom.TagName');
goog.require('goog.dom.classes');
goog.require('goog.dominoes');
```

一个类上定义的所有成员都应放在同一个文件中。对于
包含同一类的多个成员（如枚举、内部类等）的文件，
只应提供顶层类。

应这样做：

<div class='goodcode'></div>

```js
goog.provide('namespace.MyClass');
```

不应这样做：

<div class='badcode'></div>

```js
goog.provide('namespace.MyClass');
goog.provide('namespace.MyClass.CONSTANT');
goog.provide('namespace.MyClass.Enum');
goog.provide('namespace.MyClass.InnerClass');
goog.provide('namespace.MyClass.TypeDef');
goog.provide('namespace.MyClass.staticMethod');
```

命名空间上的成员也可以提供：

<div class='goodcode'></div>

```js
goog.provide('foo.bar');
goog.provide('foo.bar.CONSTANT');
goog.provide('foo.bar.method');
```

<a id="appendices-legacy-exceptions-goog-scope"></a>

##### 9.4.4.2 使用 `goog.scope` 起别名

**警告：`goog.scope` 已弃用。** 即使在已有 `goog.scope`
用法的项目中，新文件也不应使用 `goog.scope`。

在使用 `goog.provide`/`goog.require` 依赖管理的代码中，
可用 `goog.scope` 缩短对带命名空间符号的引用。

每个文件只能添加一次 `goog.scope` 调用。始终将其置于
全局作用域中。

起始的 `goog.scope(function() {` 调用前必须恰好有一个
空行，并位于所有 `goog.provide` 语句、`goog.require` 语句
或顶层注释之后。该调用必须在文件的最后一行闭合。
在作用域的闭合语句后追加 `// goog.scope`，并用
两个空格将该注释与分号隔开。

与 C++ 命名空间类似，不要在 `goog.scope` 声明下缩进，
而是从第 0 列继续。

只为不会被重新赋值为另一个对象的名称创建别名
（例如大多数构造函数、枚举和命名空间）。不要这样做（下文
说明如何为构造函数起别名）：

<div class='badcode'></div>

```js
goog.scope(function() {
var Button = goog.ui.Button;

Button = function() { ... };
...
```

名称必须与其所别名化的全局对象的最后一个属性
同名。

<div class='goodcode'></div>

```js
goog.provide('my.module.SomeType');

goog.require('goog.dom');
goog.require('goog.ui.Button');

goog.scope(function() {
var Button = goog.ui.Button;
var dom = goog.dom;

// Alias new types after the constructor declaration.
my.module.SomeType = function() { ... };
var SomeType = my.module.SomeType;

// Declare methods on the prototype as usual:
SomeType.prototype.findButton = function() {
  // Button as aliased above.
  this.button = new Button(dom.getElement('my-button'));
};
...
});  // goog.scope
```

<a id="appendices-legacy-exceptions-forward-declare"></a>

##### 9.4.4.3 `goog.forwardDeclare`

要打破同一库中文件之间的循环依赖，优先使用
`goog.requireType` 而非 `goog.forwardDeclare`。与 `goog.require` 不同，
`goog.requireType` 语句允许在命名空间定义之前
导入它。

`goog.forwardDeclare` 语句必须遵循与
`goog.require` 和 `goog.requireType` 相同的风格规则。
`goog.forwardDeclare`、`goog.require` 与 `goog.requireType` 语句
组成的整块按字母顺序排序。

旧代码中使用 `goog.forwardDeclare` 来打破*跨库边界*的
循环引用。但构建工具对这种模式支持很差，
不应再使用。应通过合理组织代码来避免跨库的
循环依赖（拆分或合并库）。

<a id="appendices-legacy-exceptions-module-get"></a>

##### 9.4.4.4 `goog.module.get(name)`

如果 `goog.provide` 文件依赖某个 `goog.module` 文件，该
`goog.provide` 文件通常无法通过全局名称引用模块的导出。
相反，除了对模块调用 `goog.require()` 之外，`goog.provide` 文件还必须
通过调用 `goog.module.get('module.name')` 获取模块的导出对象。

注意：仅调用 `goog.module.get('module.name')` 并不会建立
代码对该模块的构建时依赖。要形成构建依赖，
仍需要 `goog.require`。

<a id="appendices-legacy-exceptions-declareLegacyNamespace"></a>

##### 9.4.4.5 `goog.module.declareLegacyNamespace()`

**警告：`goog.module.declareLegacyNamespace` 仅用于过渡期。**

`goog.module.declareLegacyNamespace` 仅在把 JavaScript 文件
及其使用方从 `goog.provide` 迁移到 `goog.module` 期间使用。
请更新你的 [`goog.module`](#source-file-structure) 的使用方，让它们
自己也使用 `goog.module`。并尽可能移除对
`goog.module.declareLegacyNamespace` 的调用。

如果短期内无法把旧命名空间的使用方从 `goog.provide`
更新为 `goog.module`，请把文件内容包在 `goog.scope`
调用中，用 `goog.module.get` 导入该旧命名空间——然后
删除 `goog.module` 中对 `goog.module.declareLegacyNamespace` 的调用。

在 `goog.module(name)` 内调用 `goog.module.declareLegacyNamespace()`，
会像 `goog.provide()` 调用一样，把模块的命名空间声明为
全局名称。这样，非 `goog.module` 命名空间就无需调用
`goog.module.get(name)`，也能访问该模块的导出。
