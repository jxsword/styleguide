<!--
AUTHORS:
Prefer only GitHub-flavored Markdown in external text.
See README.md for details.
-->

# Google Python 风格指南

<!-- mdformat off -->
* TOC
{:toc}
<!-- mdformat on -->

<a id="s1-background"></a>
<a id="1-background"></a>

<a id="background"></a>

## 1 背景

Python 是 Google 主要使用的动态语言。本风格指南列出了编写 Python
程序时*该做与不该做*的事项。

为了帮助你正确地格式化代码，我们创建了
[Vim 的设置文件](google_python_style.vim)。对于 Emacs，默认
设置就应该没问题。

许多团队使用 [Black](https://github.com/psf/black) 或
[Pyink](https://github.com/google/pyink) 自动格式化工具，以避免就格式问题
争论不休。

<a id="s2-python-language-rules"></a>
<a id="2-python-language-rules"></a>

<a id="python-language-rules"></a>

## 2 Python 语言规则

<a id="s2.1-lint"></a>
<a id="21-lint"></a>

<a id="lint"></a>

### 2.1 静态检查

使用此 [pylintrc](https://google.github.io/styleguide/pylintrc) 对你的代码
运行 `pylint`。

<a id="s2.1.1-definition"></a>
<a id="211-definition"></a>

<a id="lint-definition"></a>

#### 2.1.1 定义

`pylint` 是一款用于在 Python 源代码中查找缺陷与风格问题的工具。
它能发现那些在动态性较弱的语言（如 C 和 C++）中通常由编译器
捕获的问题。由于 Python 的动态特性，某些警告可能并不准确；不过，
误报应当相当少见。

<a id="s2.1.2-pros"></a>
<a id="212-pros"></a>

<a id="lint-pros"></a>

#### 2.1.2 优点

能捕获容易忽略的错误，如拼写错误、赋值前使用变量等。

<a id="s2.1.3-cons"></a>
<a id="213-cons"></a>

<a id="lint-cons"></a>

#### 2.1.3 缺点

`pylint` 并不完美。为了充分利用它，有时我们需要绕开它、
屏蔽它的警告，或者修正它。

<a id="s2.1.4-decision"></a>
<a id="214-decision"></a>

<a id="lint-decision"></a>

#### 2.1.4 结论

务必对你的代码运行 `pylint`。

如果警告不恰当，请将其屏蔽，以免掩盖其他问题。
要屏蔽警告，你可以设置一条行级注释：

<div class='goodcode'></div>

```python
def do_PUT(self):  # WSGI name, so pylint: disable=invalid-name
  ...
```

`pylint` 警告各自以符号名称标识（`empty-docstring`）。
Google 特有的警告以 `g-` 开头。

如果从符号名称看不出屏蔽的原因，请补充
说明。

以这种方式屏蔽的好处是，我们可以轻松地搜索这些屏蔽
并重新审视它们。

你可以这样获取 `pylint` 警告的列表：

```shell
pylint --list-msgs
```

要获取某条特定消息的更多信息，请使用：

```shell
pylint --help-msg=invalid-name
```

请优先使用 `pylint: disable`，而非已弃用的旧形式 `pylint: disable-msg`。

未使用参数的警告可以通过在函数开头删除变量来屏蔽。
请始终附上注释说明删除的原因。写 "Unused." 就足够了。
例如：

<div class='goodcode'></div>

```python
def viking_cafe_order(spam: str, beans: str, eggs: str | None = None) -> str:
    del beans, eggs  # Unused by vikings.
    return spam + spam + spam
```

屏蔽此警告的其他常见形式还有：把 '`_`' 用作未使用参数的标识符，
或是给参数名加上 '`unused_`' 前缀，或是把它们赋值给 '`_`'。
这些形式仍然允许使用，但已不再推荐，因为它们会破坏那些
按名称传递参数的调用方，而且无法强制保证这些参数
确实未被使用。

<a id="s2.2-imports"></a>
<a id="22-imports"></a>

<a id="imports"></a>

### 2.2 导入

仅对包和模块使用 `import` 语句，而不要用于单个类型、
类或函数。

<a id="s2.2.1-definition"></a>
<a id="221-definition"></a>

<a id="imports-definition"></a>

#### 2.2.1 定义

一种在模块之间共享代码的可复用机制。

<a id="s2.2.2-pros"></a>
<a id="222-pros"></a>

<a id="imports-pros"></a>

#### 2.2.2 优点

命名空间管理约定很简单。每个标识符的来源
都以一致的方式标明；`x.Obj` 表示对象 `Obj`
定义在模块 `x` 中。

<a id="s2.2.3-cons"></a>
<a id="223-cons"></a>

<a id="imports-cons"></a>

#### 2.2.3 缺点

模块名仍可能冲突。有些模块名冗长不便。

<a id="s2.2.4-decision"></a>
<a id="224-decision"></a>

<a id="imports-decision"></a>

#### 2.2.4 结论

*   使用 `import x` 导入包和模块。
*   使用 `from x import y`，其中 `x` 是包前缀，`y` 是不带前缀的模块
    名。
*   在以下任一情形下使用 `from x import y as z`：
    -   需要导入两个同名为 `y` 的模块。
    -   `y` 与当前模块中定义的顶层名称冲突。
    -   `y` 与公共 API 中某个常用参数名冲突
        （例如 `features`）。
    -   `y` 的名字冗长不便。
    -   `y` 在你的代码上下文中过于笼统（例如
        `from storage.file_system import options as fs_options`）。
*   仅当 `z` 是标准缩写时才使用 `import y as z`（例如
    `import numpy as np`）。

例如，模块 `sound.effects.echo` 可以按如下方式导入：

<div class='goodcode'></div>

```python
from sound.effects import echo
...
echo.EchoFilter(input, output, delay=0.7, atten=4)
```

导入时不要使用相对名称。即使模块位于同一个包中，
也要使用完整的包名。这有助于避免无意中把同一个包
导入两次。

<a id="imports-exemptions"></a>

##### 2.2.4.1 例外

以下模块中用于支持静态分析和类型检查的符号
不受此规则约束：

*   [`typing` 模块](#typing-imports)
*   [`collections.abc` 模块](#typing-imports)
*   [`typing_extensions` 模块](https://github.com/python/typing_extensions/blob/main/README.md)

<a id="s2.3-packages"></a>
<a id="23-packages"></a>

<a id="packages"></a>

### 2.3 包

使用模块的完整路径位置来导入每个模块。

<a id="s2.3.1-pros"></a>
<a id="231-pros"></a>

<a id="packages-pros"></a>

#### 2.3.1 优点

可避免模块名冲突，以及因模块搜索路径与作者预期不符而造成的
错误导入，同时也更容易定位模块。

<a id="s2.3.2-cons"></a>
<a id="232-cons"></a>

<a id="packages-cons"></a>

#### 2.3.2 缺点

由于必须复制包层次结构，代码的部署会更困难。对于现代部署机制而言，
这其实算不上问题。

<a id="s2.3.3-decision"></a>
<a id="233-decision"></a>

<a id="packages-decision"></a>

#### 2.3.3 结论

所有新代码都应按完整包名导入每个模块。

导入应如下所示：

<div class='goodcode'></div>

```python
Yes:
  # Reference absl.flags in code with the complete name (verbose).
  import absl.flags
  from doctor.who import jodie

  _FOO = absl.flags.DEFINE_string(...)
```

<div class='goodcode'></div>

```python
Yes:
  # Reference flags in code with just the module name (common).
  from absl import flags
  from doctor.who import jodie

  _FOO = flags.DEFINE_string(...)
```

*（假设此文件位于 `doctor/who/`，且同级也存在 `jodie.py`）*

<div class='badcode'></div>

```python
No:
  # Unclear what module the author wanted and what will be imported.  The actual
  # import behavior depends on external factors controlling sys.path.
  # Which possible jodie module did the author intend to import?
  import jodie
```

不应假定主二进制文件所在的目录位于 `sys.path` 中，尽管在某些环境中
确实如此。有鉴于此，代码应假定 `import jodie` 引用的是名为 `jodie`
的第三方包或顶层包，
而非本地的 `jodie.py`。

<a id="s2.4-exceptions"></a>
<a id="24-exceptions"></a>

<a id="exceptions"></a>

### 2.4 异常

允许使用异常，但必须谨慎使用。

<a id="s2.4.1-definition"></a>
<a id="241-definition"></a>

<a id="exceptions-definition"></a>

#### 2.4.1 定义

异常是一种跳出正常控制流、用以处理错误或其他
异常状况的手段。

<a id="s2.4.2-pros"></a>
<a id="242-pros"></a>

<a id="exceptions-pros"></a>

#### 2.4.2 优点

正常运行代码的控制流不会被错误处理代码弄得杂乱无章。
当某个条件出现时，它还允许控制流一次跳过多个栈帧，例如
一步就从 N 层嵌套函数中返回，而不必
层层传递错误码。

<a id="s2.4.3-cons"></a>
<a id="243-cons"></a>

<a id="exceptions-cons"></a>

#### 2.4.3 缺点

可能使控制流变得难以理解。调用库时容易漏掉
错误情形。

<a id="s2.4.4-decision"></a>
<a id="244-decision"></a>

<a id="exceptions-decision"></a>

#### 2.4.4 结论

异常必须遵循以下条件：

-   在合理时使用内置的异常类。例如，抛出 `ValueError` 来表示
    类似违反前置条件这样的编程错误，比如在校验函数参数时
    就可能出现这种情况。

-   不要用 `assert` 语句来替代条件判断或校验前置条件。
    它们绝不能成为应用逻辑的关键所在。一个检验标准是：
    即便把 `assert` 删掉也不会破坏代码。`assert`
    条件语句[并不保证](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement)
    一定会被求值。对于基于 [pytest](https://pytest.org) 的测试，
    使用 `assert` 是可以的，而且理应用来验证预期。
    例如：

    <div class='goodcode'></div>

    ```python
    Yes:
      def connect_to_next_port(self, minimum: int) -> int:
        """Connects to the next available port.

        Args:
          minimum: A port value greater or equal to 1024.

        Returns:
          The new minimum port.

        Raises:
          ConnectionError: If no available port is found.
        """
        if minimum < 1024:
          # Note that this raising of ValueError is not mentioned in the doc
          # string's "Raises:" section because it is not appropriate to
          # guarantee this specific behavioral reaction to API misuse.
          raise ValueError(f'Min. port must be at least 1024, not {minimum}.')
        port = self._find_next_open_port(minimum)
        if port is None:
          raise ConnectionError(
              f'Could not connect to service on port {minimum} or higher.')
        # The code does not depend on the result of this assert.
        assert port >= minimum, (
            f'Unexpected port {port} when minimum was {minimum}.')
        return port
    ```

    <div class='badcode'></div>

    ```python
    No:
      def connect_to_next_port(self, minimum: int) -> int:
        """Connects to the next available port.

        Args:
          minimum: A port value greater or equal to 1024.

        Returns:
          The new minimum port.
        """
        assert minimum >= 1024, 'Minimum port must be at least 1024.'
        # The following code depends on the previous assert.
        port = self._find_next_open_port(minimum)
        assert port is not None
        # The type checking of the return statement relies on the assert.
        return port
    ```

-   库或包可以定义自己的异常。这样做时，它们必须继承自某个已有的
    异常类。异常名称应以 `Error` 结尾，且不应引入重复
    （如 `foo.FooError`）。

-   绝不要使用捕获一切的 `except:` 语句，也不要捕获 `Exception`
    或 `StandardError`，除非你是在

    -   重新抛出该异常，或
    -   在程序中建立隔离点，让异常不再传播，而是被记录并屏蔽，
        例如通过守护线程最外层的代码块，防止线程
        因异常而崩溃。

    Python 在这方面非常宽容，`except:` 真的会捕获一切，包括
    拼错的名称、sys.exit() 调用、Ctrl+C 中断、
    unittest 失败，以及各类你根本
    不想捕获的异常。

-   尽量减少 `try`/`except` 块中的代码量。`try` 的主体越大，
    就越可能由某行你并未预料会抛出异常的代码抛出异常。在这种情况
    下，`try`/`except` 块会掩盖真正的
    错误。

-   使用 `finally` 子句来执行代码，无论 `try` 块中是否抛出异常。
    这对清理工作往往很有用，例如关闭
    文件。

<a id="s2.5-global-variables"></a>
<a id="25-global-variables"></a>
<a id="s2.5-global-state"></a>
<a id="25-global-state"></a>

<a id="global-variables"></a>

### 2.5 可变全局状态

避免可变全局状态。

<a id="s2.5.1-definition"></a>
<a id="251-definition"></a>

<a id="global-variables-definition"></a>

#### 2.5.1 定义

在程序执行期间可能被改变的模块级值
或类属性。

<a id="s2.5.2-pros"></a>
<a id="252-pros"></a>

<a id="global-variables-pros"></a>

#### 2.5.2 优点

偶尔有用。

<a id="s2.5.3-cons"></a>
<a id="253-cons"></a>

<a id="global-variables-cons"></a>

#### 2.5.3 缺点

*   破坏封装：这样的设计会让合理的目标难以实现。例如，
    若用全局状态来管理数据库连接，那么同时连接两个不同的
    数据库（比如在迁移期间计算差异）就会变得困难。
    全局注册表同样容易
    出现类似问题。

*   有可能在导入期间改变模块行为，因为对全局变量的赋值
    是在模块首次被导入时完成的。

<a id="s2.5.4-decision"></a>
<a id="254-decision"></a>

<a id="global-variables-decision"></a>

#### 2.5.4 结论

避免可变全局状态。

在少数确有正当理由使用全局状态的情形下，可变全局实体应声明
在模块级或作为类属性，并通过在名称前加 `_` 使其成为内部使用。
如有必要，对可变全局状态的外部访问必须通过公开函数或类方法
来完成。参见下文的[命名](#s3.16-naming)。请在注释或由注释链接到的
文档中，说明使用可变全局状态的
设计理由。

允许并鼓励使用模块级常量。例如，内部使用的常量可写作
`_MAX_HOLY_HANDGRENADE_COUNT = 3`，公共 API 常量可写作
`SIR_LANCELOTS_FAVORITE_COLOR = "blue"`。常量必须使用全大写
字母加下划线来命名。参见下文
的[命名](#s3.16-naming)。

<a id="s2.6-nested"></a>
<a id="26-nested"></a>

<a id="nested-classes-functions"></a>

### 2.6 嵌套/局部/内部类与函数

用于闭包捕获局部变量时，嵌套的局部函数或类是可以的。
内部类也是可以的。

<a id="s2.6.1-definition"></a>
<a id="261-definition"></a>

<a id="nested-classes-functions-definition"></a>

#### 2.6.1 定义

类可以定义在方法、函数或类的内部。函数可以定义在
方法或函数内部。嵌套函数对外围作用域中定义的变量
只有只读访问权限。

<a id="s2.6.2-pros"></a>
<a id="262-pros"></a>

<a id="nested-classes-functions-pros"></a>

#### 2.6.2 优点

允许定义仅在非常有限的作用域内使用的工具类与函数。
很有
[ADT](https://en.wikipedia.org/wiki/Abstract_data_type) 的味道。常用于
实现装饰器。

<a id="s2.6.3-cons"></a>
<a id="263-cons"></a>

<a id="nested-classes-functions-cons"></a>

#### 2.6.3 缺点

嵌套的函数和类无法直接测试。嵌套会让外层函数变得更长、
可读性更差。

<a id="s2.6.4-decision"></a>
<a id="264-decision"></a>

<a id="nested-classes-functions-decision"></a>

#### 2.6.4 结论

它们可以使用，但有几点注意事项。除非是为了闭包捕获 `self` 或 `cls`
之外的局部值，否则应避免使用嵌套函数或类。不要仅仅为了向模块的
使用者隐藏某个函数而将其嵌套；而应在模块级给名称加上 \_ 前缀，
以便测试仍可访问它。

<a id="s2.7-comprehensions"></a>
<a id="s2.7-list_comprehensions"></a>
<a id="27-list_comprehensions"></a>
<a id="list_comprehensions"></a>
<a id="list-comprehensions"></a>

<a id="comprehensions"></a>

### 2.7 推导式与生成器表达式

简单情形下可以使用。

<a id="s2.7.1-definition"></a>
<a id="271-definition"></a>

<a id="comprehensions-definition"></a>

#### 2.7.1 定义

列表、字典与集合推导式以及生成器表达式，提供了一种简洁高效的
方式来创建容器类型和迭代器，而不必借助传统的循环、`map()`、
`filter()` 或 `lambda`。

<a id="s2.7.2-pros"></a>
<a id="272-pros"></a>

<a id="comprehensions-pros"></a>

#### 2.7.2 优点

简单的推导式比其他创建 dict、list 或 set 的方式更清晰、
更简洁。生成器表达式可能非常高效，因为它完全避免了
创建列表。

<a id="s2.7.3-cons"></a>
<a id="273-cons"></a>

<a id="comprehensions-cons"></a>

#### 2.7.3 缺点

复杂的推导式或生成器表达式可能难以阅读。

<a id="s2.7.4-decision"></a>
<a id="274-decision"></a>

<a id="comprehensions-decision"></a>

#### 2.7.4 结论

允许使用推导式，但不允许多个 `for` 子句或多个过滤表达式。
应优化可读性，而非简洁性。

<div class='goodcode'></div>

```python
Yes:
  result = [mapping_expr for value in iterable if filter_expr]

  result = [
      is_valid(metric={'key': value})
      for value in interesting_iterable
      if a_longer_filter_expression(value)
  ]

  descriptive_name = [
      transform({'key': key, 'value': value}, color='black')
      for key, value in generate_iterable(some_input)
      if complicated_condition_is_met(key, value)
  ]

  result = []
  for x in range(10):
    for y in range(5):
      if x * y > 10:
        result.append((x, y))

  return {
      x: complicated_transform(x)
      for x in long_generator_function(parameter)
      if x is not None
  }

  return (x**2 for x in range(10))

  unique_names = {user.name for user in users if user is not None}
```

<div class='badcode'></div>

```python
No:
  result = [(x, y) for x in range(10) for y in range(5) if x * y > 10]

  return (
      (x, y, z)
      for x in range(5)
      for y in range(5)
      if x != y
      for z in range(5)
      if y != z
  )
```

<a id="s2.8-default-iterators-and-operators"></a>

<a id="default-iterators-operators"></a>

### 2.8 默认迭代器与运算符

对支持默认迭代器和运算符的类型（如列表、字典和文件），
请使用它们。

<a id="s2.8.1-definition"></a>
<a id="281-definition"></a>

<a id="default-iterators-operators-definition"></a>

#### 2.8.1 定义

容器类型（如字典和列表）定义了默认迭代器以及
成员检测运算符（"in" 和 "not in"）。

<a id="s2.8.2-pros"></a>
<a id="282-pros"></a>

<a id="default-iterators-operators-pros"></a>

#### 2.8.2 优点

默认迭代器和运算符简单而高效。它们直接表达操作，
无需额外的方法调用。使用默认运算符的函数是泛型的，
可用于任何支持该操作的类型。

<a id="s2.8.3-cons"></a>
<a id="283-cons"></a>

<a id="default-iterators-operators-cons"></a>

#### 2.8.3 缺点

仅看方法名无法判断对象的类型（除非变量带有
类型注解）。这同时也是一项优点。

<a id="s2.8.4-decision"></a>
<a id="284-decision"></a>

<a id="default-iterators-operators-decision"></a>

#### 2.8.4 结论

对支持默认迭代器和运算符的类型（如列表、字典和文件），请使用它们。
内置类型也定义了迭代器方法。应优先使用这些方法，而非返回列表的
方法，但不要在迭代容器的过程中
修改该容器。

<div class='goodcode'></div>

```python
Yes:  for key in adict: ...
      if obj in alist: ...
      for line in afile: ...
      for k, v in adict.items(): ...
```

<div class='badcode'></div>

```python
No:   for key in adict.keys(): ...
      for line in afile.readlines(): ...
```

<a id="s2.9-generators"></a>
<a id="29-generators"></a>

<a id="generators"></a>

### 2.9 生成器

按需使用生成器。

<a id="s2.9.1-definition"></a>
<a id="291-definition"></a>

<a id="generators-definition"></a>

#### 2.9.1 定义

生成器函数返回一个迭代器，每次执行 yield 语句时产出一个值。
产出值之后，生成器函数的运行时状态会挂起，
直到需要下一个值为止。

<a id="s2.9.2-pros"></a>
<a id="292-pros"></a>

<a id="generators-pros"></a>

#### 2.9.2 优点

代码更简单，因为每次调用都会保留局部变量和控制流的状态。
与一次性创建整个值列表的函数相比，生成器
占用的内存更少。

<a id="s2.9.3-cons"></a>
<a id="293-cons"></a>

<a id="generators-cons"></a>

#### 2.9.3 缺点

生成器中的局部变量不会被垃圾回收，直到生成器被消耗殆尽，
或其自身被垃圾回收为止。

<a id="s2.9.4-decision"></a>
<a id="294-decision"></a>

<a id="generators-decision"></a>

#### 2.9.4 结论

可以使用。在生成器函数的文档字符串中，使用 "Yields:" 而非
"Returns:"。

如果生成器管理着昂贵的资源，务必强制进行清理。

进行清理的一个好办法是用上下文管理器
[PEP-0533](https://peps.python.org/pep-0533/) 来包装生成器。

<a id="s2.10-lambda-functions"></a>
<a id="210-lambda-functions"></a>

<a id="lambdas"></a>

### 2.10 Lambda 函数

单行表达式可以使用。对于 `map()` 或 `filter()` 搭配 `lambda` 的情形，
应优先使用生成器表达式。

<a id="s2.10.1-definition"></a>
<a id="2101-definition"></a>

<a id="lambdas-definition"></a>

#### 2.10.1 定义

Lambda 在表达式中定义匿名函数，而非通过语句定义。

<a id="s2.10.2-pros"></a>
<a id="2102-pros"></a>

<a id="lambdas-pros"></a>

#### 2.10.2 优点

方便。

<a id="s2.10.3-cons"></a>
<a id="2103-cons"></a>

<a id="lambdas-cons"></a>

#### 2.10.3 缺点

比局部函数更难阅读和调试。缺少名称意味着栈追踪
更难理解。表达能力有限，因为函数体
只能包含一个表达式。

<a id="s2.10.4-decision"></a>
<a id="2104-decision"></a>

<a id="lambdas-decision"></a>

#### 2.10.4 结论

允许使用 Lambda。如果 lambda 函数内的代码跨越多行，
或长度超过 60-80 个字符，最好将其定义为常规的
[嵌套函数](#lexical-scoping)。

对于乘法之类的常见操作，请使用 `operator` 模块中的函数，
而非 lambda 函数。例如，优先使用 `operator.mul`，而不是
`lambda x, y: x * y`。

<a id="s2.11-conditional-expressions"></a>
<a id="211-conditional-expressions"></a>

<a id="conditional-expressions"></a>

### 2.11 条件表达式

简单情形下可以使用。

<a id="s2.11.1-definition"></a>
<a id="2111-definition"></a>

<a id="conditional-expressions-definition"></a>

#### 2.11.1 定义

条件表达式（有时称为“三元运算符”）是一种为 if 语句提供
更简短语法的机制。例如：
`x = 1 if cond else 2`。

<a id="s2.11.2-pros"></a>
<a id="2112-pros"></a>

<a id="conditional-expressions-pros"></a>

#### 2.11.2 优点

比 if 语句更简短、更方便。

<a id="s2.11.3-cons"></a>
<a id="2113-cons"></a>

<a id="conditional-expressions-cons"></a>

#### 2.11.3 缺点

可能比 if 语句更难阅读。当表达式很长时，条件
可能难以定位。

<a id="s2.11.4-decision"></a>
<a id="2114-decision"></a>

<a id="conditional-expressions-decision"></a>

#### 2.11.4 结论

简单情形下可以使用。每个部分都必须放在一行内：
true-expression、if-expression、else-expression。情况更复杂时，
请使用完整的 if 语句。

<div class='goodcode'></div>

```python
Yes:
    one_line = 'yes' if predicate(value) else 'no'
    slightly_split = ('yes' if predicate(value)
                      else 'no, nein, nyet')
    the_longest_ternary_style_that_can_be_done = (
        'yes, true, affirmative, confirmed, correct'
        if predicate(value)
        else 'no, false, negative, nay')
```

<div class='badcode'></div>

```python
No:
    bad_line_breaking = ('yes' if predicate(value) else
                         'no')
    portion_too_long = ('yes'
                        if some_long_module.some_long_predicate_function(
                            really_long_variable_name)
                        else 'no, false, negative, nay')
```

<a id="s2.12-default-argument-values"></a>
<a id="212-default-argument-values"></a>

<a id="default-arguments"></a>

### 2.12 默认参数值

多数情况下可以使用。

<a id="s2.12.1-definition"></a>
<a id="2121-definition"></a>

<a id="default-arguments-definition"></a>

#### 2.12.1 定义

可以在函数参数列表的末尾为变量指定值，例如
`def foo(a, b=0):`。如果只用一个参数调用 `foo`，`b` 被设为
0；如果用两个参数调用，`b` 取第二个
参数的值。

<a id="s2.12.2-pros"></a>
<a id="2122-pros"></a>

<a id="default-arguments-pros"></a>

#### 2.12.2 优点

常常会有这样的函数：它使用大量默认值，但偶尔你又想覆盖这些
默认值。默认参数值提供了一种简便的做法，无需为少数例外情况
定义大量函数。由于 Python 不支持方法/函数的重载，
默认参数便成了“模拟”重载行为的
一种简便方式。

<a id="s2.12.3-cons"></a>
<a id="2123-cons"></a>

<a id="default-arguments-cons"></a>

#### 2.12.3 缺点

默认参数在模块加载时只求值一次。如果参数是列表或字典这样的
可变对象，就可能引发问题。若函数修改了该对象（例如向列表
追加一项），默认值也随之
被修改。

<a id="s2.12.4-decision"></a>
<a id="2124-decision"></a>

<a id="default-arguments-decision"></a>

#### 2.12.4 结论

可以使用，但需注意以下事项：

不要在函数或方法的定义中使用可变对象作为
默认值。

<div class='goodcode'></div>

```python
Yes: def foo(a, b=None):
         if b is None:
             b = []
Yes: def foo(a, b: Sequence | None = None):
         if b is None:
             b = []
Yes: def foo(a, b: Sequence = ()):  # Empty tuple OK since tuples are immutable.
         ...
```

<div class='badcode'></div>

```python
from absl import flags
_FOO = flags.DEFINE_string(...)

No:  def foo(a, b=[]):
         ...
No:  def foo(a, b=time.time()):  # Is `b` supposed to represent when this module was loaded?
         ...
No:  def foo(a, b=_FOO.value):  # sys.argv has not yet been parsed...
         ...
No:  def foo(a, b: Mapping = {}):  # Could still get passed to unchecked code.
         ...
```

<a id="s2.13-properties"></a>
<a id="213-properties"></a>

<a id="properties"></a>

### 2.13 属性

对于只需简单计算或逻辑的属性，可用属性来控制其读取或设置。
属性的实现必须符合常规属性访问的一般预期：开销小、
直截了当、不会让人
感到意外。

<a id="s2.13.1-definition"></a>
<a id="2131-definition"></a>

<a id="properties-definition"></a>

#### 2.13.1 定义

一种把属性的读取与设置方法调用包装成标准
属性访问的方式。

<a id="s2.13.2-pros"></a>
<a id="2132-pros"></a>

<a id="properties-pros"></a>

#### 2.13.2 优点

*   允许使用属性访问与赋值 API，而非
    [getter 与 setter](#getters-and-setters) 方法调用。
*   可用于将属性设为只读。
*   允许延迟计算。
*   当内部实现独立于类的使用者演进时，提供一种保持类的
    公共接口的方式。

<a id="s2.13.3-cons"></a>
<a id="2133-cons"></a>

<a id="properties-cons"></a>

#### 2.13.3 缺点

*   可能像运算符重载那样隐藏副作用。
*   可能让子类感到困惑。

<a id="s2.13.4-decision"></a>
<a id="2134-decision"></a>

<a id="properties-decision"></a>

#### 2.13.4 结论

允许使用属性，但与运算符重载一样，只应在确有必要时使用，
且要符合典型属性访问的预期；否则请遵循
[getter 与 setter](#getters-and-setters) 规则。

例如，不允许仅仅为了读取和设置某个内部属性而使用属性：
这里并没有发生任何计算，因此属性是多余的
（[改为将该属性设为公开](#getters-and-setters)）。相比之下，
用属性来控制属性访问，或计算 *简单* 派生值是允许的：
其逻辑简单且不会让人意外。

属性应使用 `@property`
[装饰器](#s2.17-function-and-method-decorators) 来创建。手动实现
属性描述符被视为一种[高级特性](#power-features)。

属性与继承结合时可能并不直观。不要用属性来实现子类可能想要
覆盖并扩展的计算。

<a id="s2.14-truefalse-evaluations"></a>
<a id="214-truefalse-evaluations"></a>

<a id="truefalse-evaluations"></a>

### 2.14 真/假求值

尽可能使用“隐式”假值（但有几点注意事项）。

<a id="s2.14.1-definition"></a>
<a id="2141-definition"></a>

<a id="truefalse-evaluations-definition"></a>

#### 2.14.1 定义

在布尔上下文中，Python 会把某些值求值为 `False`。
一条简便的“经验法则”是：所有“空”值都被视为假，因此
`0, None, [], {}, ''` 在布尔上下文中都求值为假。

<a id="s2.14.2-pros"></a>
<a id="2142-pros"></a>

<a id="truefalse-evaluations-pros"></a>

#### 2.14.2 优点

使用 Python 布尔值的条件更易阅读，也更不容易出错。在多数情况下，
它们还更快。

<a id="s2.14.3-cons"></a>
<a id="2143-cons"></a>

<a id="truefalse-evaluations-cons"></a>

#### 2.14.3 缺点

对 C/C++ 开发者而言可能看起来有些奇怪。

<a id="s2.14.4-decision"></a>
<a id="2144-decision"></a>

<a id="truefalse-evaluations-decision"></a>

#### 2.14.4 结论

尽可能使用“隐式”假值，例如 `if foo:` 而非
`if foo != []:`。不过有几点注意事项需要牢记：

-   检查 `None` 值时，始终使用 `if foo is None:`（或 `is not None`）。
    例如，判断某个默认为 `None` 的变量或参数是否被设为其他值，
    而那个其他值有可能恰好在布尔上下文中
    为假！

-   绝不要用 `==` 把布尔变量与 `False` 比较，而应使用 `if not x:`。
    如果需要区分 `False` 与 `None`，请把表达式串起来，
    例如 `if not x and x is not None:`。

-   对于序列（字符串、列表、元组），可利用空序列为假这一事实，
    因此 `if seq:` 和 `if not seq:` 分别优于 `if len(seq):`
    和 `if not len(seq):`。

-   处理整数时，隐式假值可能弊大于利（例如不小心把 `None`
    当成 0 处理）。对于已知为整数（且不是 `len()` 的结果）的值，
    可以将其与整数
    0 比较。

    <div class='goodcode'></div>

    ```python
    Yes: if not users:
             print('no users')

         if i % 10 == 0:
             self.handle_multiple_of_ten()

         def f(x=None):
             if x is None:
                 x = []
    ```

    <div class='badcode'></div>

    ```python
    No:  if len(users) == 0:
             print('no users')

         if not i % 10:
             self.handle_multiple_of_ten()

         def f(x=None):
             x = x or []
    ```

-   注意，`'0'`（即字符串形式的 `0`）求值为真。

-   注意，Numpy 数组在隐式布尔上下文中可能抛出异常。检测
    `np.array` 是否为空时，优先使用 `.size` 属性
    （例如 `if not users.size`）。

<a id="s2.16-lexical-scoping"></a>
<a id="216-lexical-scoping"></a>

<a id="lexical-scoping"></a>

### 2.16 词法作用域

可以使用。

<a id="s2.16.1-definition"></a>
<a id="2161-definition"></a>

<a id="lexical-scoping-definition"></a>

#### 2.16.1 定义

嵌套的 Python 函数可以引用外围函数中定义的变量，但
不能对它们赋值。变量绑定通过词法作用域来解析，
也就是说，基于静态的程序文本。代码块中对某个名称的任何赋值，
都会让 Python 把对该名称的所有引用视为局部变量，
即使使用出现在赋值之前也是如此。若出现了 global 声明，该名称
会被视为全局变量。

使用此特性的一个例子如下：

<div class='goodcode'></div>

```python
def get_adder(summand1: float) -> Callable[[float], float]:
    """Returns a function that adds numbers to a given number."""
    def adder(summand2: float) -> float:
        return summand1 + summand2

    return adder
```

<a id="s2.16.2-pros"></a>
<a id="2162-pros"></a>

<a id="lexical-scoping-pros"></a>

#### 2.16.2 优点

往往能带来更清晰、更优雅的代码。对于有经验的 Lisp 和 Scheme
（以及 Haskell、ML 等）程序员来说尤其令人安心。

<a id="s2.16.3-cons"></a>
<a id="2163-cons"></a>

<a id="lexical-scoping-cons"></a>

#### 2.16.3 缺点

可能导致令人困惑的缺陷，例如这个基于
[PEP-0227](https://peps.python.org/pep-0227/) 的例子：

<div class='badcode'></div>

```python
i = 4
def foo(x: Iterable[int]):
    def bar():
        print(i, end='')
    # ...
    # A bunch of code here
    # ...
    for i in x:  # Ah, i *is* local to foo, so this is what bar sees
        print(i, end='')
    bar()
```

因此 `foo([1, 2, 3])` 会打印 `1 2 3 3`，而不是 `1 2 3 4`。

<a id="s2.16.4-decision"></a>
<a id="2164-decision"></a>

<a id="lexical-scoping-decision"></a>

#### 2.16.4 结论

可以使用。

<a id="s2.17-function-and-method-decorators"></a>
<a id="217-function-and-method-decorators"></a>
<a id="function-and-method-decorators"></a>

<a id="decorators"></a>

### 2.17 函数与方法装饰器

当有明显好处时，审慎地使用装饰器。避免使用 `staticmethod`，
并限制 `classmethod` 的使用。

<a id="s2.17.1-definition"></a>
<a id="2171-definition"></a>

<a id="decorators-definition"></a>

#### 2.17.1 定义

[函数与方法装饰器](https://docs.python.org/3/glossary.html#term-decorator)
（亦称“`@` 记法”）。一种常见的装饰器是 `@property`，用来把
普通方法转换为动态计算的属性。不过，装饰器语法同样允许
用户自定义装饰器。具体而言，对于某个函数
`my_decorator`，以下这段代码：

<div class='goodcode'></div>

```python
class C:
    @my_decorator
    def method(self):
        # method body ...
```

等价于：

<div class='goodcode'></div>

```python
class C:
    def method(self):
        # method body ...
    method = my_decorator(method)
```

<a id="s2.17.2-pros"></a>
<a id="2172-pros"></a>

<a id="decorators-pros"></a>

#### 2.17.2 优点

优雅地指定对方法的某种变换；这种变换可以消除重复代码、
强制保证不变量等。

<a id="s2.17.3-cons"></a>
<a id="2173-cons"></a>

<a id="decorators-cons"></a>

#### 2.17.3 缺点

装饰器可以对函数的参数或返回值执行任意操作，从而产生令人意外的
隐式行为。此外，装饰器在对象定义时执行。对于模块级对象
（类、模块函数等），这发生在导入时。装饰器代码中的失败
几乎不可能
恢复。

<a id="s2.17.4-decision"></a>
<a id="2174-decision"></a>

<a id="decorators-decision"></a>

#### 2.17.4 结论

当有明显好处时，审慎地使用装饰器。装饰器应遵循与函数相同的
导入和命名准则。装饰器的文档字符串应明确说明该函数是一个
装饰器。为装饰器编写
单元测试。

装饰器自身应避免外部依赖（例如不要依赖文件、套接字、数据库连接等），
因为装饰器运行时（导入时，可能由 `pydoc` 或其他工具触发）它们
可能并不可用。以合法参数调用的装饰器，应（尽可能）
保证在
所有情况下都成功。

装饰器是“顶层代码”的一种特例——更多讨论参见
[main](#s3.17-main)。

除非为了与既有库中定义的 API 集成而不得不使用，否则绝不要使用
`staticmethod`。应改为编写模块级函数。

仅在编写具名构造函数，或修改必要全局状态（如进程级缓存）的
类专属例程时，才使用 `classmethod`。

<a id="s2.18-threading"></a>
<a id="218-threading"></a>

<a id="threading"></a>

### 2.18 线程

不要依赖内置类型的原子性。

尽管 Python 的内置数据类型（如字典）看起来具有原子操作，但仍存在
一些并非原子的边界情况（例如当 `__hash__` 或 `__eq__` 被实现为
Python 方法时），因此不应依赖其原子性。同样也不应依赖
原子性的变量赋值（因为这又
依赖于字典）。

优先使用 `queue` 模块的 `Queue` 数据类型在线程之间传递数据。
否则，请使用 `threading` 模块及其锁原语。优先使用条件变量和
`threading.Condition`，而不是
较低层的锁。

<a id="s2.19-power-features"></a>
<a id="219-power-features"></a>

<a id="power-features"></a>

### 2.19 高级特性

避免使用这些特性。

<a id="s2.19.1-definition"></a>
<a id="2191-definition"></a>

<a id="power-features-definition"></a>

#### 2.19.1 定义

Python 是一门极其灵活的语言，提供了许多花哨的特性，
例如自定义元类、访问字节码、即时编译、动态继承、
改变对象的父级、import 技巧、反射（例如 `getattr()` 的
某些用法）、修改系统内部、实现自定义清理的
`__del__` 方法等。

<a id="s2.19.2-pros"></a>
<a id="2192-pros"></a>

<a id="power-features-pros"></a>

#### 2.19.2 优点

这些是强大的语言特性，可以让代码更紧凑。

<a id="s2.19.3-cons"></a>
<a id="2193-cons"></a>

<a id="power-features-cons"></a>

#### 2.19.3 缺点

在并非绝对必要时，人们很容易忍不住使用这些“炫酷”特性。
底层使用了不寻常特性的代码更难阅读、理解和调试。起初
（对原作者而言）似乎并非如此，但重新审视代码时，它往往
比那些虽然更长却直截了当的代码
更难对付。

<a id="s2.19.4-decision"></a>
<a id="2194-decision"></a>

<a id="power-features-decision"></a>

#### 2.19.4 结论

在代码中避免使用这些特性。

内部使用了这些特性的标准库模块和类是可以
使用的（例如 `abc.ABCMeta`、`dataclasses` 和 `enum`）。

<a id="s2.20-modern-python"></a>
<a id="220-modern-python"></a>

<a id="modern-python"></a>

### 2.20 现代 Python：from \_\_future\_\_ imports

新语言版本的语义变更可能需要通过特殊的 future import 来启用，从而
在较早的运行时中按文件逐一开启这些特性。

<a id="s2.20.1-definition"></a>
<a id="2201-definition"></a>

<a id="modern-python-definition"></a>

#### 2.20.1 定义

通过 `from __future__ import` 语句
启用一些较现代的特性，可以提前用上预期
未来 Python 版本中的特性。

<a id="s2.20.2-pros"></a>
<a id="2202-pros"></a>

<a id="modern-python-pros"></a>

#### 2.20.2 优点

实践证明，这能让运行时版本升级更为平顺，因为变更可以按文件逐一进行，
同时声明兼容性并防止这些文件内部出现回归。现代代码更易于维护，因为它
不太可能积累技术债，
而这类技术债在未来的
运行时升级中会引发问题。

<a id="s2.20.3-cons"></a>
<a id="2203-cons"></a>

<a id="modern-python-cons"></a>

#### 2.20.3 缺点

此类代码可能无法在所需的 future 语句
引入之前的极旧解释器版本上运行。在支持极其广泛的
各类环境的项目中，这种需求更为常见。

<a id="s2.20.4-decision"></a>
<a id="2204-decision"></a>

<a id="modern-python-decision"></a>

#### 2.20.4 结论

##### from \_\_future\_\_ imports

鼓励使用 `from __future__ import` 语句。它使某个源文件
能够立即开始使用更现代的 Python 语法特性。一旦不再需要
在特性被 `__future__` import 所隐藏的
版本上运行，便可随意删除这些行。

对于可能运行在低至 3.5 而非 >= 3.7 的版本上的代码，请导入：

<div class='goodcode'></div>

```python
from __future__ import generator_stop
```

更多信息请参阅
[Python future 语句定义](https://docs.python.org/3/library/__future__.html)
文档。

在确信代码只会在足够现代的环境中使用之前，请不要移除这些 import。
即便你目前没有在代码中使用某个特定 future import 所启用的特性，
把它保留在文件中，也能防止日后
对代码的修改无意间
依赖于旧的行为。

可按需自行使用其他 `from __future__` import 语句。

<a id="s2.21-type-annotated-code"></a>
<a id="s2.21-typed-code"></a>
<a id="221-type-annotated-code"></a>
<a id="typed-code"></a>

<a id="typed-code"></a>

### 2.21 带类型注解的代码

你可以用
[类型提示](https://docs.python.org/3/library/typing.html) 为 Python 代码添加注解。在构建时
使用诸如 [pyrefly](https://pyrefly.org/) 之类的类型检查工具对代码做类型检查。
在大多数可行的情况下，类型注解放在源文件中。对于
第三方模块或扩展模块，注解可以放在
[存根 `.pyi` 文件](https://peps.python.org/pep-0484/#stub-files) 中。

<a id="s2.21.1-definition"></a>
<a id="2211-definition"></a>

<a id="typed-code-definition"></a>

#### 2.21.1 定义

类型注解（或称“类型提示”）用于函数或方法的参数
以及返回值：

<div class='goodcode'></div>

```python
def func(a: int) -> list[int]:
```

你也可以用类似的语法声明变量的类型：

<div class='goodcode'></div>

```python
a: SomeType = some_func()
```

<a id="s2.21.2-pros"></a>
<a id="2212-pros"></a>

<a id="typed-code-pros"></a>

#### 2.21.2 优点

类型注解能提升代码的可读性与可维护性。
类型检查器会把许多运行时错误转化为构建时错误，并降低
你使用 [高级特性](#power-features) 的能力。

<a id="s2.21.3-cons"></a>
<a id="2213-cons"></a>

<a id="typed-code-cons"></a>

#### 2.21.3 缺点

你必须持续更新类型声明。你可能会看到一些
自认为是合法代码的类型错误。使用类型检查器
可能会降低你使用 [高级特性](#power-features) 的能力。

<a id="s2.21.4-decision"></a>
<a id="2214-decision"></a>

<a id="typed-code-decision"></a>

#### 2.21.4 结论

强烈建议在更新代码时启用 Python 类型分析。
在新增或修改公共 API 时，请加入类型注解，并在构建系统中
启用类型检查。由于静态分析对于 Python 来说
还相对较新，我们承认某些非预期的副作用（例如
被错误推断的类型）可能会阻碍部分项目采用它。在这种情况下，
建议作者在 BUILD 文件或代码本身中（视情况而定）
添加一条带 TODO 的注释，或附上指向描述
当前阻碍采用类型注解的问题的 bug 链接。

<a id="s3-python-style-rules"></a>
<a id="3-python-style-rules"></a>

<a id="python-style-rules"></a>

## 3 Python 风格规则

<a id="s3.1-semicolons"></a>
<a id="31-semicolons"></a>

<a id="semicolons"></a>

### 3.1 分号

不要用分号结束一行，也不要用分号把
两条语句放在同一行。

<a id="s3.2-line-length"></a>
<a id="32-line-length"></a>

<a id="line-length"></a>

### 3.2 行长度

最大行长度为 *80 个字符*。

对 80 字符限制的明确例外：

-   长的 import 语句。
-   注释中的 URL、路径名或长标志。
-   不含空白、不便跨行拆分的长字符串模块级常量，
    例如 URL 或路径名。
-   Pylint 禁用注释。（例如：`# pylint: disable=invalid-name`）

不要用反斜杠来实现
[显式行连接](https://docs.python.org/3/reference/lexical_analysis.html#explicit-line-joining)。

应改用 Python 的
[圆括号、方括号和花括号内的隐式行连接](http://docs.python.org/reference/lexical_analysis.html#implicit-line-joining)。
如有必要，可以在表达式外再添一对圆括号。

注意，本规则并不禁止字符串内用反斜杠转义的换行
（参见[下文](#strings)）。

<div class='goodcode'></div>

```python
Yes: foo_bar(self, width, height, color='black', design=None, x='foo',
             emphasis=None, highlight=0)
```

<div class='goodcode'></div>

```python

Yes: if (width == 0 and height == 0 and
         color == 'red' and emphasis == 'strong'):

     (bridge_questions.clarification_on
      .average_airspeed_of.unladen_swallow) = 'African or European?'

     with (
         very_long_first_expression_function() as spam,
         very_long_second_expression_function() as beans,
         third_thing() as eggs,
     ):
       place_order(eggs, beans, spam, beans)
```

<div class='badcode'></div>

```python

No:  if width == 0 and height == 0 and \
         color == 'red' and emphasis == 'strong':

     bridge_questions.clarification_on \
         .average_airspeed_of.unladen_swallow = 'African or European?'

     with very_long_first_expression_function() as spam, \
           very_long_second_expression_function() as beans, \
           third_thing() as eggs:
       place_order(eggs, beans, spam, beans)
```

当字面字符串无法放在单行内时，请使用圆括号实现
隐式行连接。

<div class='goodcode'></div>

```python
x = ('This will build a very long long '
     'long long long long long long string')
```

尽量在尽可能高的语法层级换行。如果必须
把一行断两次，两次都应断在相同的语法层级。

<div class='goodcode'></div>

```python
Yes: bridgekeeper.answer(
         name="Arthur", quest=questlib.find(owner="Arthur", perilous=True))

     answer = (a_long_line().of_chained_methods()
               .that_eventually_provides().an_answer())

     if (
         config is None
         or 'editor.language' not in config
         or config['editor.language'].use_spaces is False
     ):
       use_tabs()
```

<div class='badcode'></div>

```python
No: bridgekeeper.answer(name="Arthur", quest=questlib.find(
        owner="Arthur", perilous=True))

    answer = a_long_line().of_chained_methods().that_eventually_provides(
        ).an_answer()

    if (config is None or 'editor.language' not in config or config[
        'editor.language'].use_spaces is False):
      use_tabs()

```

在注释中，如有必要，请把长 URL 单独放在一行。

<div class='goodcode'></div>

```python
Yes:  # See details at
      # http://www.example.com/us/developer/documentation/api/content/v2.0/csv_file_name_extension_full_specification.html
```

<div class='badcode'></div>

```python
No:  # See details at
     # http://www.example.com/us/developer/documentation/api/content/\
     # v2.0/csv_file_name_extension_full_specification.html
```

请留意上述续行示例中各元素的缩进；相关说明
参见[缩进](#s3.4-indentation)一节。

[文档字符串](#docstrings) 的摘要行必须保持在
80 字符限制之内。

在所有其他行超过 80 个字符、且
[Black](https://github.com/psf/black) 或
[Pyink](https://github.com/google/pyink) 自动格式化工具无法
将该行压回限制之内的情形下，允许该行超过此上限。
在合适的情况下，建议作者依据上述说明
手动拆分该行。

<a id="s3.3-parentheses"></a>
<a id="33-parentheses"></a>

<a id="parentheses"></a>

### 3.3 圆括号

尽量少用圆括号。

在元组外使用圆括号是可以的，但并非必需。不要在
return 语句或条件语句中使用圆括号，除非是为了
隐式续行或表示元组。

<div class='goodcode'></div>

```python
Yes: if foo:
         bar()
     while x:
         x = bar()
     if x and y:
         bar()
     if not x:
         bar()
     # For a 1 item tuple the ()s are more visually obvious than the comma.
     onesie = (foo,)
     return foo
     return spam, beans
     return (spam, beans)
     for (x, y) in dict.items(): ...
```

<div class='badcode'></div>

```python
No:  if (x):
         bar()
     if not(x):
         bar()
     return (foo)
```

<a id="s3.4-indentation"></a>
<a id="34-indentation"></a>

<a id="indentation"></a>

### 3.4 缩进

用 *4 个空格* 缩进代码块。

绝不使用制表符。隐式续行应让被折行的元素
垂直对齐（参见[行长度示例](#s3.2-line-length)），或使用
4 空格悬挂缩进。右（圆、方或花）括号可以
放在表达式末尾，或单独成行；若单独成行，则
应与对应的左括号所在行保持相同缩进。

<div class='goodcode'></div>

```python
Yes:   # Aligned with opening delimiter.
       foo = long_function_name(var_one, var_two,
                                var_three, var_four)
       meal = (spam,
               beans)

       # Aligned with opening delimiter in a dictionary.
       foo = {
           'long_dictionary_key': value1 +
                                  value2,
           ...
       }

       # 4-space hanging indent; nothing on first line.
       foo = long_function_name(
           var_one, var_two, var_three,
           var_four)
       meal = (
           spam,
           beans)

       # 4-space hanging indent; nothing on first line,
       # closing parenthesis on a new line.
       foo = long_function_name(
           var_one, var_two, var_three,
           var_four
       )
       meal = (
           spam,
           beans,
       )

       # 4-space hanging indent in a dictionary.
       foo = {
           'long_dictionary_key':
               long_dictionary_value,
           ...
       }
```

<div class='badcode'></div>

```python
No:    # Stuff on first line forbidden.
       foo = long_function_name(var_one, var_two,
           var_three, var_four)
       meal = (spam,
           beans)

       # 2-space hanging indent forbidden.
       foo = long_function_name(
         var_one, var_two, var_three,
         var_four)

       # No hanging indent in a dictionary.
       foo = {
           'long_dictionary_key':
           long_dictionary_value,
           ...
       }
```

<a id="s3.4.1-trailing-comma"></a>
<a id="s3.4.1-trailing-commas"></a>
<a id="s3.4.1-trailing_comma"></a>
<a id="s3.4.1-trailing_commas"></a>
<a id="341-trailing_comma"></a>
<a id="341-trailing_commas"></a>
<a id="trailing_comma"></a>
<a id="trailing_commas"></a>

<a id="trailing-comma"></a>

#### 3.4.1 元素序列中的尾随逗号？

仅当表示容器结束的 `]`、`)` 或 `}` 与最后一个元素
不在同一行时，才建议在元素序列中使用尾随逗号；
单元素元组也同样建议。尾随逗号的存在还
可作为提示，指引我们的 Python 代码自动格式化工具
[Black](https://github.com/psf/black) 或
[Pyink](https://github.com/google/pyink) 在最后一个元素后
出现 `,` 时，把装有元素的容器
自动格式化为每行一个元素。

<div class='goodcode'></div>

```python
Yes:   golomb3 = [0, 1, 3]
       golomb4 = [
           0,
           1,
           4,
           6,
       ]
```

<div class='badcode'></div>

```python
No:    golomb4 = [
           0,
           1,
           4,
           6,]
```

<a id="s3.5-blank-lines"></a>
<a id="35-blank-lines"></a>

<a id="blank-lines"></a>

### 3.5 空行

顶层定义（无论是函数定义还是类定义）之间留两个空行。
方法定义之间、以及 `class` 的文档字符串与第一个方法之间，
留一个空行。`def` 行之后不留空行。
在函数或方法内部，按你的判断酌情使用单个空行。

空行不必紧贴定义。例如，紧靠在函数、类和方法
定义之前的相关注释可能是合理的。不妨考虑一下，
你的注释作为文档字符串的一部分是否更有用。

<a id="s3.6-whitespace"></a>
<a id="36-whitespace"></a>

<a id="whitespace"></a>

### 3.6 空白

遵循标准的排版规则，在标点符号周围使用空格。

圆括号、方括号或花括号内部不留空白。

<div class='goodcode'></div>

```python
Yes: spam(ham[1], {'eggs': 2}, [])
```

<div class='badcode'></div>

```python
No:  spam( ham[ 1 ], { 'eggs': 2 }, [ ] )
```

逗号、分号或冒号前不留空白。逗号、分号或冒号后
要留空白，但行末除外。

<div class='goodcode'></div>

```python
Yes: if x == 4:
         print(x, y)
     x, y = y, x
```

<div class='badcode'></div>

```python
No:  if x == 4 :
         print(x , y)
     x , y = y , x
```

用于开始参数列表、索引或切片的左圆括号/左方括号
之前不留空白。

<div class='goodcode'></div>

```python
Yes: spam(1)
```

<div class='badcode'></div>

```python
No:  spam (1)
```

<div class='goodcode'></div>

```python
Yes: dict['key'] = list[index]
```

<div class='badcode'></div>

```python
No:  dict ['key'] = list [index]
```

不留行尾空白。

对于赋值（`=`）、比较
（`==, <, >, !=, <>, <=, >=, in, not in, is, is not`）以及
布尔运算（`and, or, not`）等二元运算符，两侧各留一个空格。
算术运算符（`+`、`-`、`*`、`/`、`//`、`%`、`**`、`@`）周围是否加空格，请自行判断。

<div class='goodcode'></div>

```python
Yes: x == 1
```

<div class='badcode'></div>

```python
No:  x<1
```

在传入关键字参数或定义默认参数值时，绝不要在 `=` 周围
使用空格，但有一个例外：
[当存在类型注解时](#typing-default-values)，*务必* 在
默认参数值的 `=` 周围使用空格。

<div class='goodcode'></div>

```python
Yes: def complex(real, imag=0.0): return Magic(r=real, i=imag)
Yes: def complex(real, imag: float = 0.0): return Magic(r=real, i=imag)
```

<div class='badcode'></div>

```python
No:  def complex(real, imag = 0.0): return Magic(r = real, i = imag)
No:  def complex(real, imag: float=0.0): return Magic(r = real, i = imag)
```

不要用空格在连续多行间垂直对齐标记，因为这会
成为维护负担（适用于 `:`、`#`、`=` 等）：

<div class='goodcode'></div>

```python
Yes:
  foo = 1000  # comment
  long_name = 2  # comment that should not be aligned

  dictionary = {
      'foo': 1,
      'long_name': 2,
  }
```

<div class='badcode'></div>

```python
No:
  foo       = 1000  # comment
  long_name = 2     # comment that should not be aligned

  dictionary = {
      'foo'      : 1,
      'long_name': 2,
  }
```

<a id="Python_Interpreter"></a>
<a id="s3.7-shebang-line"></a>
<a id="37-shebang-line"></a>

<a id="shebang-line"></a>

### 3.7 Shebang 行

大多数 `.py` 文件不需要以 `#!` 行开头。程序的
主文件应以 `#!/usr/bin/env python3`（以支持 virtualenvs）或
`#!/usr/bin/python3` 开头，遵循 [PEP-394](https://peps.python.org/pep-0394/)。

内核用这一行来查找 Python 解释器，但 Python 在
导入模块时会忽略它。只有打算直接执行的
文件才需要这一行。

<a id="s3.8-comments-and-docstrings"></a>
<a id="s3.8-comments"></a>
<a id="38-comments-and-docstrings"></a>

<a id="documentation"></a>

### 3.8 注释与文档字符串

务必为模块、函数、方法的文档字符串以及
行内注释使用恰当的风格。

<a id="s3.8.1-comments-in-doc-strings"></a>
<a id="381-docstrings"></a>
<a id="comments-in-doc-strings"></a>

<a id="docstrings"></a>

#### 3.8.1 文档字符串

Python 使用 *文档字符串* 来为代码编写文档。文档字符串是
包、模块、类或函数中的第一条语句所对应的字符串。这些
字符串可以通过对象的 `__doc__` 成员自动提取，并供
`pydoc` 使用。（试着对你的模块运行 `pydoc` 看看效果。）请始终
为文档字符串使用三双引号 `"""` 格式（遵循
[PEP 257](https://peps.python.org/pep-0257/)）。文档字符串应组织为
一行摘要（不超过 80 个字符的一个物理行），以
句号、问号或感叹号结尾。若要写更多内容（鼓励这样做），
则摘要之后必须接一个空行，随后是文档字符串的其余部分，
其起始位置与第一行首个引号所在的游标位置相同。下文
还有更多关于文档字符串的格式指南。

<a id="s3.8.2-comments-in-modules"></a>
<a id="382-modules"></a>
<a id="comments-in-modules"></a>

<a id="module-docs"></a>

#### 3.8.2 模块

每个文件都应包含许可证样板代码。请根据项目
所使用的许可证选择合适的样板代码（例如 Apache 2.0、BSD、
LGPL、GPL）。

文件应以描述模块内容
与用法的文档字符串开头。

<div class='goodcode'></div>

```python
"""A one-line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

Typical usage example:

  foo = ClassFoo()
  bar = foo.function_bar()
"""
```

<a id="s3.8.2.1-test-modules"></a>

<a id="test-docs"></a>

##### 3.8.2.1 测试模块

测试模块不要求模块级文档字符串。`unittest.TestCase` 的
子类不要求类文档字符串，`unittest.TestCase` 子类中的
`test_` 方法也不要求方法文档字符串。仅仅重复
类或方法名称的文档字符串应当省略。

当文档字符串能提供额外信息时，就应当写，
例如说明测试应如何运行的具体细节，或解释
某种不常见的设置模式或外部依赖。

<div class='goodcode'></div>

```python
"""This blaze test uses golden files.

You can update those files by running
`blaze run //foo/bar:foo_test -- --update_golden_files` from the `google3`
directory.
"""
```

不应使用不提供任何新信息的文档字符串。

<div class='badcode'></div>

```python
"""Tests for foo.bar."""
```

或

<div class='badcode'></div>

```python
  def test_foo_is_barred(self):
    """Tests that bar is applied to foo."""
```

<a id="s3.8.3-functions-and-methods"></a>
<a id="383-functions-and-methods"></a>
<a id="functions-and-methods"></a>

<a id="function-docs"></a>

#### 3.8.3 函数与方法

在本节中，“函数”指方法、函数、生成器或属性。

凡是具备以下一项或多项特征的
函数，都必须有文档字符串：

-   属于公共 API 的一部分
-   规模不小
-   逻辑不明显

文档字符串应提供足够的信息，使人无需阅读函数的代码
就能写出对该函数的调用。文档字符串应描述
函数的调用语法及其语义，但一般不涉及
实现细节，除非这些细节与函数的使用方式相关。
例如，某个函数若会作为副作用修改
它的某个参数，就应在文档字符串中注明。除此之外，
与调用方无关、却又微妙而重要的
函数实现细节，与其写在函数的文档字符串里，
不如用代码旁的注释来表达。

文档字符串可以是描述式（`"""Fetches rows from a Bigtable."""`）
或命令式（`"""Fetch rows from a Bigtable."""`），但同一文件内的
风格应保持一致。`@property` 数据描述符的
文档字符串，应使用与属性或
<a href="#doc-function-args">函数参数</a> 的文档字符串相同的风格（`"""The Bigtable path."""`，
而不是 `"""Returns the Bigtable path."""`）。

函数的某些方面应在下面列出的专门章节中
加以说明。每个章节以一行标题开头，标题以冒号结尾。
除标题外的所有内容应保持两空格或四空格的
悬挂缩进（在同一文件内保持一致）。当函数的
名称与签名已足够说明问题、用一行文档字符串
即可恰当描述时，可以省略这些章节。

<a id="doc-function-args"></a>
[*Args:*](#doc-function-args)
:   按名称逐一列出每个参数。名称后应跟一段描述，
    并以冒号分隔，冒号后接一个空格或换行。如果
    描述过长、无法放进单行 80 字符之内，则使用比参数名
    多 2 或 4 个空格的悬挂缩进（与文件中其余
    文档字符串保持一致）。若代码中没有对应的类型注解，
    描述中应包含所需的类型。若某个函数
    接受 `*foo`（可变长度参数列表）和/或 `**bar`
    （任意关键字参数），应将它们列为 `*foo` 和 `**bar`。

<a id="doc-function-returns"></a>
[*Returns:*（或用于生成器的 *Yields:*）](#doc-function-returns)
:   描述返回值的语义，包括类型注解
    未提供的类型信息。若函数只返回
    None，则不需要这一节。若文档字符串
    以“Return”、“Returns”、“Yield”或“Yields”开头（例如
    `"""Returns row from Bigtable as a tuple of strings."""`）*并且* 开头
    那句话已足以描述返回值，也可以省略这一节。不要模仿旧式的
    ‘NumPy 风格’
    （[示例](https://numpy.org/doc/1.24/reference/generated/numpy.linalg.qr.html)），
    它常把元组返回值记录成好像是
    多个带各自名称的返回值（从不提及元组）。相反，
    应把这样的返回值描述为：“Returns: A tuple (mat_a, mat_b), where
    mat_a is ..., and ...”。文档字符串中的辅助名称
    不必一定与函数体中使用的任何内部名称对应（因为
    那些名称不属于 API）。若函数使用了 `yield`（是
    生成器），则 `Yields:` 一节应记录 `next()` 返回的对象，
    而不是调用所求值得到的生成器对象本身。

<a id="doc-function-raises"></a>
[*Raises:*](#doc-function-raises)
:   列出与接口相关的所有异常，并在后面附上
    描述。使用与 *Args:* 中所述类似的
    “异常名称 + 冒号 + 空格或换行”以及
    悬挂缩进风格。不应记录那些
    因违反文档字符串所规定的 API 而引发的异常
    （因为这会自相矛盾地把违反 API 时的行为也变成 API 的一部分）。

<div class='goodcode'></div>

```python
def fetch_smalltable_rows(
    table_handle: smalltable.Table,
    keys: Sequence[bytes | str],
    require_all_keys: bool = False,
) -> Mapping[bytes, tuple[str, ...]]:
    """Fetches rows from a Smalltable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by table_handle.  String keys will be UTF-8 encoded.

    Args:
        table_handle: An open smalltable.Table instance.
        keys: A sequence of strings representing the key of each table
          row to fetch.  String keys will be UTF-8 encoded.
        require_all_keys: If True only rows with values set for all keys will be
          returned.

    Returns:
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings. For
        example:

        {b'Serak': ('Rigel VII', 'Preparer'),
         b'Zim': ('Irk', 'Invader'),
         b'Lrrr': ('Omicron Persei 8', 'Emperor')}

        Returned keys are always bytes.  If a key from the keys argument is
        missing from the dictionary, then that row was not found in the
        table (and require_all_keys must have been False).

    Raises:
        IOError: An error occurred accessing the smalltable.
    """
```

同样，`Args:` 的这种带换行的变体也是允许的：

<div class='goodcode'></div>

```python
def fetch_smalltable_rows(
    table_handle: smalltable.Table,
    keys: Sequence[bytes | str],
    require_all_keys: bool = False,
) -> Mapping[bytes, tuple[str, ...]]:
    """Fetches rows from a Smalltable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by table_handle.  String keys will be UTF-8 encoded.

    Args:
      table_handle:
        An open smalltable.Table instance.
      keys:
        A sequence of strings representing the key of each table row to
        fetch.  String keys will be UTF-8 encoded.
      require_all_keys:
        If True only rows with values set for all keys will be returned.

    Returns:
      A dict mapping keys to the corresponding table row data
      fetched. Each row is represented as a tuple of strings. For
      example:

      {b'Serak': ('Rigel VII', 'Preparer'),
       b'Zim': ('Irk', 'Invader'),
       b'Lrrr': ('Omicron Persei 8', 'Emperor')}

      Returned keys are always bytes.  If a key from the keys argument is
      missing from the dictionary, then that row was not found in the
      table (and require_all_keys must have been False).

    Raises:
      IOError: An error occurred accessing the smalltable.
    """
```

被装饰函数的文档字符串必须说明
装饰器应用之后该函数的行为，因为
那才是调用方会观察到的行为。

<div class='goodcode'></div>

```python
@contextlib.contextmanager
def read_from_remote_filesystem(url: str) -> Iterator[RemoteFile]:
    """Open a file for reading from a remote filesystem.

    Args:
      url: The address of the remote file.

    Returns:
      A context manager providing a reference to a remote file.
    """
    reader = remote_file_reader(url)
    try:
        yield reader
    finally:
        reader.close()
```

<a id="s3.8.3.1-overridden-methods"></a>

<a id="overridden-method-docs"></a>

##### 3.8.3.1 被重写的方法

重写基类方法的方法，如果
显式地用
[`@override`](https://typing.python.org/en/latest/spec/class-compat.html#override) 装饰，
则不需要文档字符串；除非该重写方法的行为
实质性地细化了基类方法的契约，或需要
提供额外细节（例如记录附加的副作用），此时
重写方法必须带有至少说明这些差异的文档字符串。

<div class='goodcode'></div>

```python
from typing import override

class Parent:
  def do_something(self):
    """Parent method, includes docstring."""

# Child class, method annotated with override.
class Child(Parent):
  @override
  def do_something(self):
    pass
```

<div class='badcode'></div>

```python
# Child class, but without @override decorator, a docstring is required.
class Child(Parent):
  def do_something(self):
    pass

# Docstring is trivial, @override is sufficient to indicate that docs can be
# found in the base class.
class Child(Parent):
  @override
  def do_something(self):
    """See base class."""
```

<a id="s3.8.4-comments-in-classes"></a>
<a id="384-classes"></a>
<a id="comments-in-classes"></a>

<a id="class-docs"></a>

#### 3.8.4 类

类应在类定义下方有一个描述该类的文档字符串。
公开属性（不包括 [特性](#properties)）应在
此处的 `Attributes` 章节中加以说明，并遵循与
[函数的 `Args`](#doc-function-args) 章节相同的格式。

<div class='goodcode'></div>

```python
class SampleClass:
    """Summary of class here.

    Longer class information...
    Longer class information...

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self, likes_spam: bool = False):
        """Initializes the instance based on spam preference.

        Args:
          likes_spam: Defines if instance exhibits this preference.
        """
        self.likes_spam = likes_spam
        self.eggs = 0

    @property
    def butter_sticks(self) -> int:
        """The number of butter sticks we have."""
```

所有类的文档字符串都应以一行摘要开头，说明
该类的实例表示什么。这意味着 `Exception` 的
子类也应描述该异常表示什么，而不是
它可能发生的上下文。类的文档字符串不应
重复多余的信息，例如说明该类是一个类。

<div class='goodcode'></div>

```python
# Yes:
class CheeseShopAddress:
  """The address of a cheese shop.

  ...
  """

class OutOfCheeseError(Exception):
  """No more cheese is available."""
```

<div class='badcode'></div>

```python
# No:
class CheeseShopAddress:
  """Class that describes the address of a cheese shop.

  ...
  """

class OutOfCheeseError(Exception):
  """Raised when no more cheese is available."""
```

如果类被装饰，其文档字符串必须说明
装饰器应用之后该类的行为。

<a id="s3.8.5-block-and-inline-comments"></a>
<a id="comments-in-block-and-inline"></a>
<a id="s3.8.5-comments-in-block-and-inline"></a>
<a id="385-block-and-inline-comments"></a>

<a id="comments"></a>

#### 3.8.5 块注释与行内注释

最后一类该写注释的地方是代码中棘手的部分。
如果你不得不在下一次
[代码评审](http://en.wikipedia.org/wiki/Code_review) 中解释它，
现在就该加注释。复杂的操作应在操作开始前
配上几行注释。不明显的操作则在行尾加注释。

<div class='goodcode'></div>

```python
# We use a weighted dictionary search to find out where i is in
# the array.  We extrapolate position based on the largest num
# in the array and the array size and then do binary search to
# get the exact number.

if i & (i-1) == 0:  # True if i is 0 or a power of 2.
```

为提高可读性，这些注释应与代码至少相隔 2 个空格，
以注释字符 `#` 开头，其后在注释文字
之前至少留一个空格。

另一方面，绝不要描述代码本身。假定读代码的人
比你更懂 Python（只是不知道你想做什么）。

<div class='badcode'></div>

```python
# BAD COMMENT: Now go through the b array and make sure whenever i occurs
# the next element is i+1
```

<!-- The next section is copied from the C++ style guide. -->

<a id="s3.8.6-punctuation-spelling-and-grammar"></a>
<a id="386-punctuation-spelling-and-grammar"></a>
<a id="spelling"></a>
<a id="punctuation"></a>
<a id="grammar"></a>

<a id="punctuation-spelling-grammar"></a>

#### 3.8.6 标点、拼写与语法

注意标点、拼写和语法；写得好的
注释比写得差的更容易阅读。

注释应像叙述文字一样易读，使用正确的大小写
和标点。多数情况下，完整句子比
句子片段更易读。较短的注释（例如代码行尾的注释）
有时可以不太正式，但应保持风格一致。

尽管被代码评审者指出该用分号的地方却用了
逗号可能令人懊恼，但源码保持
高度的清晰与可读性非常重要。正确的
标点、拼写和语法有助于实现这一目标。

<a id="s3.10-strings"></a>
<a id="310-strings"></a>

<a id="strings"></a>

### 3.10 字符串

使用
[f-string](https://docs.python.org/3/reference/lexical_analysis.html#f-strings)、
`%` 运算符或 `format` 方法来格式化字符串，即使
参数全都是字符串也是如此。在各种字符串格式化方案之间，
请运用你的最佳判断来取舍。用 `+` 做一次拼接可以，但不要用 `+` 来格式化。

<div class='goodcode'></div>

```python
Yes: x = f'name: {name}; score: {n}'
     x = '%s, %s!' % (imperative, expletive)
     x = '{}, {}'.format(first, second)
     x = 'name: %s; score: %d' % (name, n)
     x = 'name: %(name)s; score: %(score)d' % {'name':name, 'score':n}
     x = 'name: {}; score: {}'.format(name, n)
     x = a + b
```

<div class='badcode'></div>

```python
No: x = first + ', ' + second
    x = 'name: ' + name + '; score: ' + str(n)
```

避免在循环中用 `+` 和 `+=` 运算符
来累加字符串。在某些情况下，用加法累加
字符串可能导致平方级而非线性级的运行时间。
尽管这类常见累加在 CPython 上可能
被优化，但那属于实现细节。优化
适用的条件不易预测，也可能变化。应当改为
把每个子字符串加入列表，并在循环结束后
对列表做 `''.join`，或把每个子字符串写入 `io.StringIO` 缓冲区。这些手法始终具有摊还线性级的时间复杂度。

<div class='goodcode'></div>

```python
Yes: items = ['<table>']
     for last_name, first_name in employee_list:
         items.append('<tr><td>%s, %s</td></tr>' % (last_name, first_name))
     items.append('</table>')
     employee_table = ''.join(items)
```

<div class='badcode'></div>

```python
No: employee_table = '<table>'
    for last_name, first_name in employee_list:
        employee_table += '<tr><td>%s, %s</td></tr>' % (last_name, first_name)
    employee_table += '</table>'
```

在同一文件内，字符串引号字符的选择应保持一致。
选定 `'` 或 `"` 并坚持使用。为避免对字符串内的
引号字符做反斜杠转义，可以在该字符串上使用另一种引号字符。

<div class='goodcode'></div>

```python
Yes:
  Python('Why are you hiding your eyes?')
  Gollum("I'm scared of lint errors.")
  Narrator('"Good!" thought a happy Python reviewer.')
```

<div class='badcode'></div>

```python
No:
  Python("Why are you hiding your eyes?")
  Gollum('The lint. It burns. It burns us.')
  Gollum("Always the great lint. Watching. Watching.")
```

多行字符串优先使用 `"""` 而非 `'''`。当且仅当项目
对普通字符串也使用 `'` 时，才可以选择对所有
非文档字符串的多行字符串使用 `'''`。无论如何，文档字符串都必须使用 `"""`。

多行字符串不会随程序其余部分的缩进一起排版。
如果需要在字符串中避免嵌入多余的空格，
可以使用拼接起来的单行字符串，或使用带
[`textwrap.dedent()`](https://docs.python.org/3/library/textwrap.html#textwrap.dedent) 的多行字符串，
以去掉每行开头的空格：

<div class='badcode'></div>

```python
  No:
  long_string = """This is pretty ugly.
Don't do this.
"""
```

<div class='goodcode'></div>

```python
  Yes:
  long_string = """This is fine if your use case can accept
      extraneous leading spaces."""
```

<div class='goodcode'></div>

```python
  Yes:
  long_string = ("And this is fine if you cannot accept\n" +
                 "extraneous leading spaces.")
```

<div class='goodcode'></div>

```python
  Yes:
  long_string = ("And this too is fine if you cannot accept\n"
                 "extraneous leading spaces.")
```

<div class='goodcode'></div>

```python
  Yes:
  import textwrap

  long_string = textwrap.dedent("""\
      This is also fine, because textwrap.dedent()
      will collapse common leading spaces in each line.""")
```

注意，此处使用反斜杠并不违反针对
[显式行连接](#line-length) 的禁令；在本例中，反斜杠
[转义换行符](https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals)，
发生在字符串字面量内部。

<a id="s3.10.1-logging"></a>
<a id="3101-logging"></a>
<a id="logging"></a>

<a id="logging"></a>

#### 3.10.1 日志

对于那些第一个参数是模式字符串（含 % 占位符）的
日志函数：务必始终以字符串字面量（而不是 f-string！）
作为第一个参数来调用它们，并把模式参数
作为后续参数传入。某些日志实现会把
未展开的模式字符串收集为可查询字段。
这也能避免把时间花在渲染没有 logger 配置输出的消息上。

<div class='goodcode'></div>

```python
  Yes:
  import tensorflow as tf
  logger = tf.get_logger()
  logger.info('TensorFlow Version is: %s', tf.__version__)
```

<div class='goodcode'></div>

```python
  Yes:
  import os
  from absl import logging

  logging.info('Current $PAGER is: %s', os.getenv('PAGER', default=''))

  homedir = os.getenv('HOME')
  if homedir is None or not os.access(homedir, os.W_OK):
    logging.error('Cannot write to home directory, $HOME=%r', homedir)
```

<div class='badcode'></div>

```python
  No:
  import os
  from absl import logging

  logging.info('Current $PAGER is:')
  logging.info(os.getenv('PAGER', default=''))

  homedir = os.getenv('HOME')
  if homedir is None or not os.access(homedir, os.W_OK):
    logging.error(f'Cannot write to home directory, $HOME={homedir!r}')
```

<a id="s3.10.2-error-messages"></a>
<a id="3102-error-messages"></a>
<a id="error-messages"></a>

<a id="error-messages"></a>

#### 3.10.2 错误消息

错误消息（例如：`ValueError` 等异常上的消息字符串，
或展示给用户的消息）应遵循三条准则：

1.  消息需要与实际错误状况精确吻合。

2.  插入的部分必须始终能被清楚地识别出来。

3.  它们应便于简单的自动化处理（例如 grep）。

<div class='goodcode'></div>

```python
  Yes:
  if not 0 <= p <= 1:
    raise ValueError(f'Not a probability: {p=}')

  try:
    os.rmdir(workdir)
  except OSError as error:
    logging.warning('Could not remove directory (reason: %r): %r',
                    error, workdir)
```

<div class='badcode'></div>

```python
  No:
  if p < 0 or p > 1:  # PROBLEM: also false for float('nan')!
    raise ValueError(f'Not a probability: {p=}')

  try:
    os.rmdir(workdir)
  except OSError:
    # PROBLEM: Message makes an assumption that might not be true:
    # Deletion might have failed for some other reason, misleading
    # whoever has to debug this.
    logging.warning('Directory already was deleted: %s', workdir)

  try:
    os.rmdir(workdir)
  except OSError:
    # PROBLEM: The message is harder to grep for than necessary, and
    # not universally non-confusing for all possible values of `workdir`.
    # Imagine someone calling a library function with such code
    # using a name such as workdir = 'deleted'. The warning would read:
    # "The deleted directory could not be deleted."
    logging.warning('The %s directory could not be deleted.', workdir)
```

<a id="s3.11-files-sockets-closeables"></a>
<a id="s3.11-files-and-sockets"></a>
<a id="311-files-and-sockets"></a>
<a id="files-and-sockets"></a>

<a id="files"></a>

### 3.11 文件、套接字及类似的有状态资源

用完文件和套接字后要显式关闭。这条规则
自然也延伸到内部使用套接字的可关闭资源，
例如数据库连接，以及同样需要
以类似方式关闭的其他资源。仅举几例，
这还包括 [mmap](https://docs.python.org/3/library/mmap.html) 映射、
[h5py File 对象](https://docs.h5py.org/en/stable/high/file.html)，以及
[matplotlib.pyplot figure 窗口](https://matplotlib.org/2.1.0/api/_as_gen/matplotlib.pyplot.close.html)。

让文件、套接字或其他这类有状态对象
不必要地保持打开，有许多弊端：

-   它们可能消耗有限的系统资源，例如文件描述符。
    处理大量此类对象的代码若在用完后没有
    及时把这些资源归还给系统，可能不必要地耗尽它们。
-   保持文件打开可能妨碍其他操作，例如移动或
    删除它们，或者卸载文件系统。
-   在程序中共享的文件和套接字，在逻辑上
    被关闭之后，可能仍被无意地读取或写入。
    如果确实关闭了，再尝试读取或写入
    就会引发异常，从而更早暴露问题。

此外，虽然文件和套接字（以及一些行为类似的资源）
在对象被销毁时会自动关闭，但把对象的生命周期
与资源的状态绑定在一起是糟糕的做法：

-   无法保证运行时何时真正调用
    `__del__` 方法。不同的 Python 实现采用不同的
    内存管理技术，例如延迟垃圾回收，这可能
    任意且无限期地延长对象的生命周期。
-   对文件的意外引用（例如在 globals 或异常回溯中）
    可能使它比预期存活得更久。

依赖终结器执行带有可观察副作用的自动清理，
在几十年间、跨多种语言被一次次
重新发现会引发重大问题（例如参见针对 Java 的
[这篇文章](https://wiki.sei.cmu.edu/confluence/display/java/MET12-J.+Do+not+use+finalizers)
）。

管理文件和类似资源的首选方式是使用
[`with` 语句](http://docs.python.org/reference/compound_stmts.html#the-with-statement)：

<div class='goodcode'></div>

```python
with open("hello.txt") as hello_file:
    for line in hello_file:
        print(line)
```

对于不支持 `with` 语句的文件类对象，请使用
`contextlib.closing()`：

<div class='goodcode'></div>

```python
import contextlib

with contextlib.closing(urllib.urlopen("http://www.python.org/")) as front_page:
    for line in front_page:
        print(line)
```

在极少数基于上下文的资源管理不可行的情况下，
代码文档必须清楚地说明资源生命周期是如何管理的。

<a id="s3.12-todo-comments"></a>
<a id="312-todo-comments"></a>

<a id="todo"></a>

### 3.12 TODO 注释

对临时代码、短期解决方案，或够用但
并不完美的代码，使用 `TODO` 注释。

`TODO` 注释以全大写的 `TODO` 一词开头，后接一个
括号内的链接，指向包含相关背景的资源，最好是 bug 引用。
bug 引用更为可取，因为 bug 会被跟踪并有后续注释。
在这段背景信息之后跟一个冒号和一段解释性文字。

目的在于形成一致的 `TODO` 格式，便于通过搜索
找到更多细节。

<div class='goodcode'></div>

```python
# TODO(example.com/12345): Investigate cpufreq optimizations.
```

旧式写法，过去曾推荐，但不建议在新代码中使用：

```python
# TODO: example.com/12345 - Investigate cpufreq optimizations.
```

避免添加以个人或团队作为背景信息的 TODO：

<div class='badcode'></div>

```python
# TODO(username): File an issue and use a '*' for repetition.
```

如果你的 `TODO` 属于“将来某天做某事”这种形式，
务必包含一个非常具体的日期（“在 2009 年 11 月前修复”）
或一个非常具体的事件（“当所有客户端都能处理 XML 响应时移除此代码。”），
以便未来的代码维护者能够理解。issue 非常适合用来跟踪这类事项。

<a id="s3.13-imports-formatting"></a>
<a id="313-imports-formatting"></a>

<a id="imports-formatting"></a>

### 3.13 导入格式

导入应各占一行；但
[`typing` 和 `collections.abc` 的导入](#typing-imports)有例外。

例如：

<div class='goodcode'></div>

```python
Yes: from collections.abc import Mapping, Sequence
     import os
     import sys
     from typing import Any, NewType
```

<div class='badcode'></div>

```python
No:  import os, sys
```

导入总是放在文件顶部，紧接在任何模块注释和
文档字符串之后，并在模块全局变量和常量之前。导入应按
从最通用到最不通用的顺序分组：

1.  Python future 导入语句。例如：

    <div class='goodcode'></div>

    ```python
    from __future__ import annotations
    ```

    关于这些内容的更多信息，请参见[上文](#from-future-imports)。

2.  Python 标准库导入。例如：

    <div class='goodcode'></div>

    ```python
    import sys
    ```

3.  [第三方](https://pypi.org/)模块或包的导入。例如：

    <div class='goodcode'></div>

    ```python
    import tensorflow as tf
    ```

4.  代码仓库子包的导入。例如：

    <div class='goodcode'></div>

    ```python
    from otherproject.ai import mind
    ```

5.  **已弃用：**与该文件同属同一顶层子包的、特定于
    应用的导入。例如：

    <div class='goodcode'></div>

    ```python
    from myproject.backend.hgwells import time_machine
    ```

    你可能会看到较旧的 Google Python Style 代码这样做，但如今已不再
    要求如此。**建议新代码不必为此费心。**只需将特定于应用的
    子包导入与其他子包导入
    同等对待即可。

在每个分组内，导入应按各模块的完整包路径（即
`from path import ...` 中的 `path`）按字典序排序，忽略大小写。
代码可以选择在各个导入
区段之间留一个空行。

<div class='goodcode'></div>

```python
import collections
import queue
import sys

from absl import app
from absl import flags
import bs4
import cryptography
import tensorflow as tf

from book.genres import scifi
from myproject.backend import huxley
from myproject.backend.hgwells import time_machine
from myproject.backend.state_machine import main_loop
from otherproject.ai import body
from otherproject.ai import mind
from otherproject.ai import soul

# Older style code may have these imports down here instead:
#from myproject.backend.hgwells import time_machine
#from myproject.backend.state_machine import main_loop
```

<a id="s3.14-statements"></a>
<a id="314-statements"></a>

<a id="statements"></a>

### 3.14 语句

通常每行只写一条语句。

不过，仅当整条语句能放在一行时，才可以把测试的结果与测试
放在同一行。特别地，绝不能对 `try`/`except` 这样做，因为 `try` 和 `except`
无法同时放在同一行；对 `if` 则只有在没有 `else` 时
才能这样做。

<div class='goodcode'></div>

```python
Yes:

  if foo: bar(foo)
```

<div class='badcode'></div>

```python
No:

  if foo: bar(foo)
  else:   baz(foo)

  try:               bar(foo)
  except ValueError: baz(foo)

  try:
      bar(foo)
  except ValueError: baz(foo)
```

<a id="s3.15-accessors"></a>
<a id="s3.15-access-control"></a>
<a id="315-access-control"></a>
<a id="access-control"></a>
<a id="accessors"></a>

<a id="getters-and-setters"></a>

### 3.15 取值器和设值器

当取值器和设值器函数（也称为访问器和修改器）能为获取或设置变量的
值提供有意义的角色或行为时，就应
使用它们。

特别是，当获取或设置变量的过程较为复杂，或无论在当下还是可预见的
将来代价都很显著时，就应使用它们。

例如，如果一对取值器/设值器只是读写某个内部属性，
则应把该内部属性改为公开。相比之下，如果设置某个变量
意味着某些状态会失效或被重建，那就应使用设值器函数。
函数调用暗示正在发生一项可能并不简单的操作。另一种做法是，
当需要简单逻辑时，[properties](#properties) 可能是一个选择，
或者重构代码，使其不再需要取值器
和设值器。

取值器和设值器应遵循[命名](#s3.16-naming)指南，例如
`get_foo()` 和 `set_foo()`。

如果过去的行为允许通过 property 访问，不要把新的取值器/设值器
函数绑定到该 property 上。任何仍试图用旧方式访问该变量的代码都应
明显地出错，以便让相关人员意识到
复杂度发生了变化。

<a id="s3.16-naming"></a>
<a id="316-naming"></a>

<a id="naming"></a>

### 3.16 命名

`module_name`, `package_name`, `ClassName`, `method_name`, `ExceptionName`,
`function_name`, `GLOBAL_CONSTANT_NAME`, `global_var_name`, `instance_var_name`,
`function_parameter_name`, `local_var_name`, `query_proper_noun_for_thing`,
`send_acronym_via_https`.

名称应具有描述性。这包括函数、类、变量、
属性、文件以及任何其他类型的命名实体。

避免缩写。尤其不要使用对项目之外的读者而言含义模糊或不熟悉的
缩写，也不要通过删掉单词内部的字母
来进行缩写。

始终使用 `.py` 作为文件扩展名。切勿使用连字符。

<a id="s3.16.1-names-to-avoid"></a>
<a id="3161-names-to-avoid"></a>

<a id="names-to-avoid"></a>

#### 3.16.1 应避免的名称

-   单字符名称，但明确允许的情况除外：

    -   计数器或迭代器（例如 `i`、`j`、`k`、`v` 等）
    -   在 `try/except` 语句中用作异常标识符的 `e`。
    -   在 `with` 语句中用作文件句柄的 `f`
    -   无约束的私有[类型变量](#typing-type-var)（例如
        `_T = TypeVar("_T")`、`_P = ParamSpec("_P")`）
    -   与参考论文或算法中既有记法一致的名称
        （参见[数学记法](#math-notation)）

    请注意不要滥用单字符命名。一般来说，名称的描述性应与名称的
    可见作用域成正比。例如，对于 5 行的代码块，`i` 也许是个好名字，
    但在多层嵌套的作用域中，它
    很可能过于含糊。

-   任何包/模块名称中的连字符（`-`）

-   `__double_leading_and_trailing_underscore__` 名称（由 Python 保留）

-   冒犯性词语

-   无必要地包含变量类型的名称（例如：
    `id_to_name_dict`）

<a id="s3.16.2-naming-conventions"></a>
<a id="3162-naming-convention"></a>

<a id="naming-conventions"></a>

#### 3.16.2 命名约定

-   通常遵循 [PEP 8 命名约定][PEP-8-naming-conventions]。

-   「Internal」表示某个模块的内部，或者类中受保护或
    私有的成员。

-   前置单个下划线（`_`）在保护模块变量和函数方面有一定的支持
    （静态检查工具会对受保护成员的访问发出警告）。请注意，单元测试
    访问被测模块中的受保护常量
    是允许的。

-   在实例变量或方法前加双下划线（`__`，又称「dunder」）实际上会
    通过名称改写使该变量或方法成为类的私有成员；我们不鼓励这样
    做，因为它影响可读性和可测试性，而且并非*真正*私有。
    请优先使用单个下划线。

-   把相关的类和顶层函数放在同一个模块中。与 Java 不同，没有必要
    把每个模块限制为只有一个类。

-   类名使用 CapWords，而模块名使用 lower\_with\_under.py。
    尽管仍有一些旧模块命名为 CapWords.py，但现在已不鼓励这样
    做，因为当模块恰好以某个类命名时会造成混淆。
    （「等等——我写的是 `import StringIO` 还是
    `from StringIO import StringIO`？」）

    -   请注意 [PEP 8 指出][PEP-8-acronyms]：「在 CapWords 中使用首字母缩写时，
        要把该缩写的每个字母都大写。因此
        HTTPServerError 优于 HttpServerError。」

-   新建的*单元测试*文件遵循符合 PEP 8 的 lower\_with\_under 方法名，
    例如 `test_<method_under_test>_<state>`。为了与采用 CapWords
    函数名的遗留模块保持一致（\*），以 `test` 开头的方法名中可以出现
    下划线，用于分隔名称中的逻辑组成部分。一种可能的模式是
    `test<MethodUnderTest>_<state>`。

[PEP-8-naming-conventions]: https://peps.python.org/pep-0008/#naming-conventions
[PEP-8-acronyms]: https://peps.python.org/pep-0008/#descriptive-naming-styles

<a id="naming-exemptions"></a>

##### 3.16.2.1 例外

以下例外适用于上述通用命名约定：

-   当 Python 代码与外部或非 Python 代码库紧密耦合时（例如与 C++ 的
    外部函数接口（FFI）），为与另一个代码库保持一致，可能有必要
    遵循不同的约定
    （[一致性](#consistency)）。

<a id="s3.16.3-file-naming"></a>
<a id="3163-file-naming"></a>

<a id="file-naming"></a>

#### 3.16.3 文件命名

Python 文件名必须带有 `.py` 扩展名，且不得包含连字符（`-`）。
这样才能导入它们并进行单元测试。如果希望某个可执行文件不带扩展名
也能访问，可以使用符号链接，或一个简单的 bash 包装器，其中
包含 `exec "$0.py" "$@"`。

<a id="s3.16.4-guidelines-derived-from-guidos-recommendations"></a>
<a id="3164-guidelines-derived-from-guidos-recommendations"></a>

<a id="guidelines-derived-from-guidos-recommendations"></a>

#### 3.16.4 源自 [Guido](https://en.wikipedia.org/wiki/Guido_van_Rossum) 建议的指南

<table rules="all" border="1" summary="Guidelines from Guido's Recommendations"
       cellspacing="2" cellpadding="2">

  <tr>
    <th>类型</th>
    <th>公开</th>
    <th>内部</th>
  </tr>

  <tr>
    <td>包</td>
    <td><code>lower_with_under</code></td>
    <td></td>
  </tr>

  <tr>
    <td>模块</td>
    <td><code>lower_with_under</code></td>
    <td><code>_lower_with_under</code></td>
  </tr>

  <tr>
    <td>类</td>
    <td><code>CapWords</code></td>
    <td><code>_CapWords</code></td>
  </tr>

  <tr>
    <td>异常</td>
    <td><code>CapWords</code></td>
    <td></td>
  </tr>

  <tr>
    <td>函数</td>
    <td><code>lower_with_under()</code></td>
    <td><code>_lower_with_under()</code></td>
  </tr>

  <tr>
    <td>全局/类常量</td>
    <td><code>CAPS_WITH_UNDER</code></td>
    <td><code>_CAPS_WITH_UNDER</code></td>
  </tr>

  <tr>
    <td>全局/类变量</td>
    <td><code>lower_with_under</code></td>
    <td><code>_lower_with_under</code></td>
  </tr>

  <tr>
    <td>实例变量</td>
    <td><code>lower_with_under</code></td>
    <td><code>_lower_with_under</code>（受保护的）</td>
  </tr>

  <tr>
    <td>方法名</td>
    <td><code>lower_with_under()</code></td>
    <td><code>_lower_with_under()</code>（受保护的）</td>
  </tr>

  <tr>
    <td>函数/方法参数</td>
    <td><code>lower_with_under</code></td>
    <td></td>
  </tr>

  <tr>
    <td>局部变量</td>
    <td><code>lower_with_under</code></td>
    <td></td>
  </tr>

</table>

<a id="s3.17-main"></a>
<a id="317-main"></a>

<a id="math-notation"></a>

#### 3.16.5 数学记法

对于数学运算密集的代码，如果短变量名与参考论文或算法中的既有
记法一致，则优先使用它们，即使这些名称本来会违反
风格指南。

使用基于既有记法的名称时：

1.  在注释或文档字符串中注明所有命名约定的出处，最好附上指向
    该学术资源本身的超链接。如果无法访问该来源，请清楚地
    记录命名约定。
2.  对公开 API 优先使用符合 PEP 8 的 `descriptive_names`，因为它们
    更有可能在脱离上下文时被读到。
3.  使用作用域很窄的 `pylint: disable=invalid-name` 指令来消除
    警告。若只涉及少数几个变量，则把该指令作为每个变量的行尾
    注释；若涉及更多变量，则在该代码块的开头应用该指令。

<a id="main"></a>

### 3.17 主函数

在 Python 中，`pydoc` 以及单元测试都要求模块是可导入的。如果某个
文件要作为可执行文件使用，其主体功能应放在 `main()` 函数中，且
代码在执行主程序前始终应检查 `if __name__ == '__main__'`，
以免在模块被导入时
执行主程序。

使用 [absl](https://github.com/abseil/abseil-py) 时，请使用 `app.run`：

<div class='goodcode'></div>

```python
from absl import app
...

def main(argv: Sequence[str]):
    # process non-flag arguments
    ...

if __name__ == '__main__':
    app.run(main)
```

否则，使用：

<div class='goodcode'></div>

```python
def main():
    ...

if __name__ == '__main__':
    main()
```

模块被导入时，顶层的所有代码都会被执行。注意不要调用函数、创建
对象，或执行其他在该文件被 `pydoc` 处理时
不应执行的操作。

<a id="s3.18-function-length"></a>
<a id="318-function-length"></a>

<a id="function-length"></a>

### 3.18 函数长度

优先使用短小且专注的函数。

我们认识到长函数有时是合适的，因此对函数长度不设硬性
限制。如果某个函数超过约 40 行，请考虑能否在不损害程序结构
的前提下将其拆分。

即使你的长函数现在运行得完美无缺，几个月后修改它的人也可能
加入新的行为。这可能导致难以发现的缺陷。保持函数短小简单，
能让其他人更容易阅读
和修改你的代码。

处理某些代码时，你可能会遇到又长又复杂的函数。不要畏惧修改
既有代码：如果发现使用这样的函数很困难、错误难以调试，或者
你希望在多个不同的上下文中复用它的某一部分，就应考虑
把该函数拆分成更小、
更易于管理的片段。

<a id="s3.19-type-annotations"></a>
<a id="319-type-annotations"></a>

<a id="type-annotations"></a>

### 3.19 类型注解

<a id="s3.19.1-general-rules"></a>
<a id="s3.19.1-general"></a>
<a id="3191-general-rules"></a>

<a id="typing-general"></a>

#### 3.19.1 通用规则

*   请熟悉
    [类型提示](https://docs.python.org/3/library/typing.html)。

*   通常没有必要为 `self` 或 `cls` 添加注解。
    [`Self`](https://docs.python.org/3/library/typing.html#typing.Self) 可在
    为获得正确类型信息而确有需要时使用，例如

    <div class='goodcode'></div>

    ```python
    from typing import Self

    class BaseClass:
      @classmethod
      def create(cls) -> Self:
        ...

      def difference(self, other: Self) -> float:
        ...
    ```

*   同样，不必强求为 `__init__` 的返回值添加注解
    （`None` 是唯一有效的选项）。

*   如果其他变量或返回类型不宜明确写出，请使用 `Any`。

*   不要求为模块中的所有函数都添加注解。

    -   至少要为公开 API 添加注解。
    -   运用判断力，在安全性与清晰性，以及灵活性之间取得
        良好的平衡。
    -   为容易出现类型相关错误的代码（曾出现过缺陷或较为复杂）
        添加注解。
    -   为难以理解的代码添加注解。
    -   当代码从类型角度看趋于稳定时，为其添加注解。在很多
        情况下，你可以为成熟代码中的所有函数添加注解，
        而不会损失太多灵活性。

<a id="s3.19.2-line-breaking"></a>
<a id="3192-line-breaking"></a>

<a id="typing-line-breaking"></a>

#### 3.19.2 换行

尽量遵循既有的[缩进](#indentation)规则。

添加注解后，许多函数签名会变成「每行一个参数」。
为确保返回类型也独占一行，可以在最后一个参数
之后加上逗号。

<div class='goodcode'></div>

```python
def my_method(
    self,
    first_var: int,
    second_var: Foo,
    third_var: Bar | None,
) -> int:
  ...
```

始终优先在变量之间换行，而不要在变量名与类型注解之间
换行。不过，如果所有内容都能放在同一行，就
照做即可。

<div class='goodcode'></div>

```python
def my_method(self, first_var: int) -> int:
  ...
```

如果函数名、最后一个参数和返回类型组合起来过长，请另起一行
缩进 4 个空格。使用换行时，优先把每个参数和返回类型各自放在
独立的一行，并让右括号
与 `def` 对齐：

<div class='goodcode'></div>

```python
Yes:
def my_method(
    self,
    other_arg: MyLongType | None,
) -> tuple[MyLongType1, MyLongType1]:
  ...
```

也可以选择把返回类型放在与最后一个参数相同的行上：

<div class='goodcode'></div>

```python
Okay:
def my_method(
    self,
    first_var: int,
    second_var: int) -> dict[OtherLongType, MyLongType]:
  ...
```

`pylint` 允许把右括号移到新的一行并与左括号对齐，
但这样可读性较差。

<div class='badcode'></div>

```python
No:
def my_method(self,
              other_arg: MyLongType | None,
             ) -> dict[OtherLongType, MyLongType]:
  ...
```

如上面的示例所示，尽量不要拆开类型。不过，有时类型过长，
无法放在一行内（请尽量保持子类型不被拆开）。

<div class='goodcode'></div>

```python
def my_method(
    self,
    first_var: tuple[list[MyLongType1],
                     list[MyLongType2]],
    second_var: list[dict[
        MyLongType3, MyLongType4]],
) -> None:
  ...
```

如果单个名称加类型过长，可考虑为该类型使用
[别名](#typing-aliases)。最后的手段是在冒号后换行，
并缩进 4 个空格。

<div class='goodcode'></div>

```python
Yes:
def my_function(
    long_variable_name:
        long_module_name.LongTypeName,
) -> None:
  ...
```

<div class='badcode'></div>

```python
No:
def my_function(
    long_variable_name: long_module_name.
        LongTypeName,
) -> None:
  ...
```

<a id="s3.19.3-forward-declarations"></a>
<a id="3193-forward-declarations"></a>

<a id="forward-declarations"></a>

#### 3.19.3 前向声明

如果需要使用同一模块中尚未定义的类名——例如在该类的声明
内部需要用到类名，或者使用了在代码后面才定义的类——
要么使用 `from __future__ import annotations`，要么
用字符串表示类名。

<div class='goodcode'></div>

```python
Yes:
from __future__ import annotations

class MyClass:
  def __init__(self, stack: Sequence[MyClass], item: OtherClass) -> None:

class OtherClass:
  ...
```

<div class='goodcode'></div>

```python
Yes:
class MyClass:
  def __init__(self, stack: Sequence['MyClass'], item: 'OtherClass') -> None:

class OtherClass:
  ...
```

<a id="s3.19.4-default-values"></a>
<a id="3194-default-values"></a>

<a id="typing-default-values"></a>

#### 3.19.4 默认值

按照 [PEP-008](https://peps.python.org/pep-0008/#other-recommendations)，*仅*对
同时带有类型注解和默认值的参数，才在 `=` 两侧
加空格。

<div class='goodcode'></div>

```python
Yes:
def func(a: int = 0) -> int:
  ...
```

<div class='badcode'></div>

```python
No:
def func(a:int=0) -> int:
  ...
```

<a id="s3.19.5-nonetype"></a>
<a id="s3.19.5-none-type"></a>
<a id="3195-nonetype"></a>

<a id="none-type"></a>

#### 3.19.5 NoneType

在 Python 类型系统中，`NoneType` 是「一等」类型，就类型标注
而言，`None` 是 `NoneType` 的别名。如果某个参数可以为 `None`，
就必须声明！可以使用 `|` 联合类型表达式（在新的 Python 3.10+
代码中推荐），或较旧的 `Optional` 和 `Union` 语法。

使用显式的 `X | None`，而不要隐式表达。早期版本的类型检查器
允许把 `a: str = None` 解读为 `a: str | None = None`，但这已
不再是首选行为。

<div class='goodcode'></div>

```python
Yes:
def modern_or_union(a: str | int | None, b: str | None = None) -> str:
  ...
def union_optional(a: Union[str, int, None], b: Optional[str] = None) -> str:
  ...
```

<div class='badcode'></div>

```python
No:
def nullable_union(a: Union[None, str]) -> str:
  ...
def implicit_optional(a: str = None) -> str:
  ...
```

<a id="s3.19.6-type-aliases"></a>
<a id="s3.19.6-aliases"></a>
<a id="3196-type-aliases"></a>
<a id="typing-aliases"></a>

<a id="type-aliases"></a>

#### 3.19.6 类型别名

可以为复杂类型声明别名。

*   别名的名称应使用 CapWords 风格。如果别名只在本模块中使用，
    则应使用 \_Private 形式。
*   应为别名添加 `typing.TypeAlias` 类型注解，以便把它与
    非类型的全局变量区分开来。
*   不要用类型别名来替代 `from module import symbol` 惯用法，
    后者是[不允许的](#imports)。

<div class='goodcode'></div>

```python
Yes:
from typing import TypeAlias

_LossAndGradient: TypeAlias = tuple[tf.Tensor, tf.Tensor]
ComplexTFMap: TypeAlias = Mapping[str, _LossAndGradient]
```

<div class='badcode'></div>

```python
No:
import immutabledict

immutabledict = immutabledict.immutabledict
```

```python
# Acceptable for convenience (provided the alias is not used in a public API,
# such as a public function's signature, of this module).
_ShortName: TypeAlias = other_module.SignificantlyInconvenientlyLongName
```

<a id="s3.19.7-ignoring-types"></a>
<a id="s3.19.7-ignore"></a>
<a id="3197-ignoring-types"></a>

<a id="typing-ignore"></a>

#### 3.19.7 忽略类型

可以用特殊注释 `# type: ignore` 在某一行上
禁用类型检查。

`pyrefly` 针对特定错误提供了禁用选项（类似于静态检查）：

<div class='goodcode'></div>

```python
# pyrefly: ignore[attribute-error]
```

<a id="s3.19.8-typing-variables"></a>
<a id="s3.19.8-comments"></a>
<a id="3198-typing-internal-variables"></a>

<a id="typing-variables"></a>

#### 3.19.8 变量类型标注

<a id="annotated-assignments"></a>
[*带注解的赋值*](#annotated-assignments)
:   如果某个内部变量的类型难以或无法推断，请用带注解的赋值
    语句指定其类型——在变量名和值之间使用冒号与类型
    （与带默认值的函数参数的
    做法相同）：

    <div class='goodcode'></div>

    ```python
    a: Foo = SomeUndecoratedFunction()
    ```

<a id="type-comments"></a>
[*类型注释*](#type-comments)
:   尽管你可能会在代码库中看到它们残留（在 Python 3.6 之前
    它们是必需的），但不要再新增在行尾使用
    `# type: <type name>` 注释的做法：

    <div class='badcode'></div>

    ```python
    a = SomeUndecoratedFunction()  # type: Foo
    ```

<a id="s3.19.9-tuples-vs-lists"></a>
<a id="s3.19.9-tuples"></a>
<a id="3199-tuples-vs-lists"></a>

<a id="typing-tuples"></a>

#### 3.19.9 元组与列表

带类型的列表只能包含单一类型的对象。带类型的元组既可以
是单一重复类型，也可以是固定数量、类型各异的元素。
后者常用作函数的返回类型。

<div class='goodcode'></div>

```python
a: list[int] = [1, 2, 3]
b: tuple[int, ...] = (1, 2, 3)
c: tuple[int, str, float] = (1, "2", 3.5)
```

<a id="s3.19.10-typevars"></a>
<a id="s3.19.10-type-var"></a>
<a id="31910-typevar"></a>
<a id="typing-type-var"></a>

<a id="typevars"></a>

#### 3.19.10 类型变量

Python 类型系统支持
[泛型](https://docs.python.org/3/library/typing.html#generics)。类型变量
（如 `TypeVar` 和 `ParamSpec`）是使用泛型的一种常见方式。

示例：

<div class='goodcode'></div>

```python
from collections.abc import Callable
from typing import ParamSpec, TypeVar
_P = ParamSpec("_P")
_T = TypeVar("_T")
...
def next(l: list[_T]) -> _T:
  return l.pop()

def print_when_called(f: Callable[_P, _T]) -> Callable[_P, _T]:
  def inner(*args: _P.args, **kwargs: _P.kwargs) -> _T:
    print("Function was called")
    return f(*args, **kwargs)
  return inner
```

可以对 `TypeVar` 施加约束：

<div class='goodcode'></div>

```python
AddableType = TypeVar("AddableType", int, float, str)
def add(a: AddableType, b: AddableType) -> AddableType:
  return a + b
```

`typing` 模块中一个常见的预定义类型变量是 `AnyStr`。当多个注解
可以为 `bytes` 或 `str` 且必须都是同一类型时，请使用它。

<div class='goodcode'></div>

```python
from typing import AnyStr
def check_length(x: AnyStr) -> AnyStr:
  if len(x) <= 42:
    return x
  raise ValueError()
```

类型变量必须具有描述性的名称，除非它同时满足以下
所有条件：

*   不对外部可见
*   未施加约束

<div class='goodcode'></div>

```python
Yes:
  _T = TypeVar("_T")
  _P = ParamSpec("_P")
  AddableType = TypeVar("AddableType", int, float, str)
  AnyFunction = TypeVar("AnyFunction", bound=Callable)
```

<div class='badcode'></div>

```python
No:
  T = TypeVar("T")
  P = ParamSpec("P")
  _T = TypeVar("_T", int, float, str)
  _F = TypeVar("_F", bound=Callable)
```

<a id="s3.19.11-string-types"></a>
<a id="s3.19.11-strings"></a>
<a id="31911-string-types"></a>

<a id="typing-strings"></a>

#### 3.19.11 字符串类型

> 不要在新代码中使用 `typing.Text`。它只用于 Python 2/3 兼容。

对字符串/文本数据使用 `str`。对处理二进制数据的代码，
使用 `bytes`。

<div class='goodcode'></div>

```python
def deals_with_text_data(x: str) -> str:
  ...
def deals_with_binary_data(x: bytes) -> bytes:
  ...
```

如果某个函数的所有字符串类型始终相同，例如上面代码中返回
类型与参数类型相同，请使用
[AnyStr](#typing-type-var)。

<a id="s3.19.12-imports-for-typing"></a>
<a id="s3.19.12-imports"></a>
<a id="31912-imports-for-typing"></a>

<a id="typing-imports"></a>

#### 3.19.12 用于类型标注的导入

对于 `typing` 或 `collections.abc` 模块中用于支持静态分析和类型
检查的符号（包括类型、函数和常量），应始终导入符号本身。
这能让常见注解更简洁，也符合世界各地的类型标注实践。
明确允许在一行内从 `typing` 和 `collections.abc` 模块
导入多个特定的符号。
例如：

<div class='goodcode'></div>

```python
from collections.abc import Mapping, Sequence
from typing import Any, Generic, cast, TYPE_CHECKING
```

由于这种导入方式会向局部命名空间添加条目，`typing` 或
`collections.abc` 中的名称应视同关键字，不要在 Python 代码中定义
它们（无论是否带类型标注）。如果某个类型与模块中已有的名称
发生冲突，请使用 `import x as y` 导入它。

<div class='goodcode'></div>

```python
from typing import Any as AnyType
```

为函数签名添加注解时，优先使用 `collections.abc.Sequence` 之类的
抽象容器类型，而非 `list` 之类的具体类型。如果需要使用具体
类型（例如由带类型元素组成的 `tuple`），应优先使用 `tuple` 等
内置类型，而不是 `typing` 模块中的参数化类型别名（例如
`typing.Tuple`）。

<div class='badcode'></div>

```python
from typing import List, Tuple

def transform_coordinates(original: List[Tuple[float, float]]) ->
    List[Tuple[float, float]]:
  ...
```

<div class='goodcode'></div>

```python
from collections.abc import Sequence

def transform_coordinates(original: Sequence[tuple[float, float]]) ->
    Sequence[tuple[float, float]]:
  ...
```

<a id="s3.19.13-conditional-imports"></a>
<a id="31913-conditional-imports"></a>

<a id="typing-conditional-imports"></a>

#### 3.19.13 条件导入

仅在特殊情况下使用条件导入：即类型检查所需的额外导入
必须在运行时避免。不鼓励采用这种模式；应优先选择
其他方案，例如重构代码
以允许顶层导入。

仅类型注解所需的导入可以放在
`if TYPE_CHECKING:` 块内。

-   条件导入的类型需要以字符串形式引用，以便向前兼容
    Python 3.6——在该版本中注解表达式会被
    实际求值。
-   此处只应定义纯粹用于类型标注的实体；
    这也包括别名。否则会引发运行时错误，因为该模块
    在运行时不会被导入。
-   该块应紧跟在所有常规导入之后。
-   类型标注导入列表中不应出现空行。
-   像对待常规导入列表一样对该列表排序。

<div class='goodcode'></div>

```python
import typing
if typing.TYPE_CHECKING:
  import sketch
def f(x: "sketch.Sketch"): ...
```

<a id="s3.19.14-circular-dependencies"></a>
<a id="s3.19.14-circular-deps"></a>
<a id="31914-circular-dependencies"></a>

<a id="typing-circular-deps"></a>

#### 3.19.14 循环依赖

由类型标注引起的循环依赖是代码异味。这类代码很适合
进行重构。尽管技术上可以保留循环依赖，但各种构建
系统并不允许这样做，因为每个模块都必须
相互依赖。

把造成循环依赖导入的模块替换成 `Any`。设置一个名称
有意义的[别名](#typing-aliases)，并使用本模块中真实的
类型名（`Any` 的任何属性都是 `Any`）。别名定义
应与最后一个导入之间隔一行。

<div class='goodcode'></div>

```python
from typing import Any

some_mod = Any  # some_mod.py imports this module.
...

def my_method(self, var: "some_mod.SomeType") -> None:
  ...
```

<a id="typing-generics"></a>
<a id="s3.19.15-generics"></a>
<a id="31915-generics"></a>

<a id="generics"></a>

#### 3.19.15 泛型

添加注解时，优先在参数列表中为
[泛型](https://docs.python.org/3/library/typing.html#generics)类型指定
类型参数；否则，泛型的参数将被假定为
[`Any`](https://docs.python.org/3/library/typing.html#the-any-type)。

<div class='goodcode'></div>

```python
# Yes:
def get_names(employee_ids: Sequence[int]) -> Mapping[int, str]:
  ...
```

<div class='badcode'></div>

```python
# No:
# This is interpreted as get_names(employee_ids: Sequence[Any]) -> Mapping[Any, Any]
def get_names(employee_ids: Sequence) -> Mapping:
  ...
```

如果某个泛型最合适的类型参数是 `Any`，请显式写出，
但要记住，在很多情况下 [`TypeVar`](#typing-type-var)
可能更合适：

<div class='badcode'></div>

```python
# No:
def get_names(employee_ids: Sequence[Any]) -> Mapping[Any, str]:
  """Returns a mapping from employee ID to employee name for given IDs."""
```

<div class='goodcode'></div>

```python
# Yes:
_T = TypeVar('_T')
def get_names(employee_ids: Sequence[_T]) -> Mapping[_T, str]:
  """Returns a mapping from employee ID to employee name for given IDs."""
```

<a id="4-parting-words"></a>

<a id="consistency"></a>

## 4 结语

*保持一致性*。

如果你在编辑代码，花几分钟看看周围的代码，判断它的风格。
如果他们在索引变量名中使用 `_idx` 后缀，你也应照做。
如果他们的注释周围有用井号围成的小方框，
让你的注释也带上井号围成的小方框。

制定风格指南的意义在于形成一套通用的编码词汇，使人们
能专注于你在说什么，而不是你如何表达。我们在这里给出
全局风格规则，好让大家了解这套词汇，但局部风格同样
重要。如果你添加到文件中的代码与周围既有代码
看起来截然不同，读者在阅读时
就会被打乱节奏。

不过，一致性也有其限度。它在局部范围内、以及在全局风格
未作规定的选择上更为适用。一般不应把一致性当作
借口，用来在不考虑新风格好处的情况下沿用旧风格，
也不应忽视代码库随时间
向更新风格趋同的趋势。
