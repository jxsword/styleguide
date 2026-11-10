# Google C# 风格指南

本风格指南适用于 Google 内部开发的 C# 代码，并且是
Google C# 代码的默认风格。它所做的风格选择与
Google 的其他语言保持一致，例如 Google C++ 风格和 Google Java 风格。

<!-- mdformat off -->
* TOC
{:toc}
<!-- mdformat on -->

## 格式准则

### 命名规则

命名规则遵循
[Microsoft 的 C# 命名准则](https://docs.microsoft.com/en-us/dotnet/standard/design-guidelines/naming-guidelines)。
若 Microsoft 的命名准则未作规定（例如私有变量和局部
变量），则规则取自
[CoreFX C# 编码准则](https://github.com/dotnet/runtime/blob/HEAD/docs/coding-guidelines/coding-style.md)

规则摘要：

#### 代码

*   类、方法、枚举、公有字段、公有属性、
    命名空间的名称：`PascalCase`。
*   局部变量、参数的名称：`camelCase`。
*   私有、受保护、内部及受保护内部字段与
    属性的名称：`_camelCase`。
*   命名约定不受 const、static、
    readonly 等修饰符影响。
*   就大小写而言，"word" 指任何内部不含空格的书写单位，包括
    首字母缩略词。例如用 `MyRpc` 而非 ~~`MyRPC`~~。
*   接口名称以 `I` 开头，例如 `IInterface`。

#### 文件

*   文件名和目录名采用 `PascalCase`，例如 `MyFile.cs`。
*   在可能的情况下，文件名应与文件中主类的
    名称相同，例如 `MyClass.cs`。
*   一般而言，每个文件最好只放一个核心类。

### 组织结构

*   修饰符按以下顺序出现：`public protected internal private
    new abstract virtual override sealed static readonly extern unsafe volatile
    async`。
*   命名空间 `using` 声明放在最前面，位于任何命名空间之前。`using`
    导入顺序按字母排列，但 `System` 导入始终
    排在最前。
*   类成员顺序：
    *   按以下顺序对类成员分组：
        *   嵌套类、枚举、委托和事件。
        *   静态、const 和 readonly 字段。
        *   字段和属性。
        *   构造函数和终结器。
        *   方法。
    *   在每一组内，成员应按以下顺序排列：
        *   公有。
        *   内部。
        *   受保护内部。
        *   受保护。
        *   私有。
    *   在可能的情况下，把接口实现放在一起。

### 空白规则

源自 Google Java 风格。

*   每行最多一条语句。
*   每条语句最多一次赋值。
*   缩进为 2 个空格，不使用制表符。
*   列宽限制：100。
*   左花括号前不换行。
*   右花括号与 `else` 之间不换行。
*   即使可选也使用花括号。
*   `if`/`for`/`while` 等之后、以及逗号之后加空格。
*   左圆括号之后、右圆括号之前不加空格。
*   一元运算符与其操作数之间不加空格。其他所有运算符的
    运算符与每个操作数之间各加一个空格。
*   换行规则源自 Google C++ 风格准则，并为兼容
    Microsoft 的 C# 格式化工具做了少量修改：
    *   一般而言，续行缩进 4 个空格。
    *   带花括号的换行（例如列表初始化器、lambda、对象
        初始化器等）不计为续行。
    *   对于函数定义和调用，若参数无法全部放在
        一行，应拆分为多行，并使每个
        后续行与第一个参数对齐。若没有足够的
        空间这样做，也可把参数放在后续行，并
        使用 4 空格缩进。下面的代码示例说明了这一点。

### 示例

```c#
using System;                                       // `using` goes at the top, outside the
                                                    // namespace.

namespace MyNamespace {                             // Namespaces are PascalCase.
                                                    // Indent after namespace.
  public interface IMyInterface {                   // Interfaces start with 'I'
    public int Calculate(float value, float exp);   // Methods are PascalCase
                                                    // ...and space after comma.
  }

  public enum MyEnum {                              // Enumerations are PascalCase.
    Yes,                                            // Enumerators are PascalCase.
    No,
  }

  public class MyClass {                            // Classes are PascalCase.
    public int Foo = 0;                             // Public member variables are
                                                    // PascalCase.
    public bool NoCounting = false;                 // Field initializers are encouraged.
    private class Results {
      public int NumNegativeResults = 0;
      public int NumPositiveResults = 0;
    }
    private Results _results;                       // Private member variables are
                                                    // _camelCase.
    public static int NumTimesCalled = 0;
    private const int _bar = 100;                   // const does not affect naming
                                                    // convention.
    private int[] _someTable = {                    // Container initializers use a 2
      2, 3, 4,                                      // space indent.
    }

    public MyClass() {
      _results = new Results {
        NumNegativeResults = 1,                     // Object initializers use a 2 space
        NumPositiveResults = 1,                     // indent.
      };
    }

    public int CalculateValue(int mulNumber) {      // No line break before opening brace.
      var resultValue = Foo * mulNumber;            // Local variables are camelCase.
      NumTimesCalled++;
      Foo += _bar;

      if (!NoCounting) {                            // No space after unary operator and
                                                    // space after 'if'.
        if (resultValue < 0) {                      // Braces used even when optional and
                                                    // spaces around comparison operator.
          _results.NumNegativeResults++;
        } else if (resultValue > 0) {               // No newline between brace and else.
          _results.NumPositiveResults++;
        }
      }

      return resultValue;
    }

    public void ExpressionBodies() {
      // For simple lambdas, fit on one line if possible, no brackets or braces required.
      Func<int, int> increment = x => x + 1;

      // Closing brace aligns with first character on line that includes the opening brace.
      Func<int, int, long> difference1 = (x, y) => {
        long diff = (long)x - y;
        return diff >= 0 ? diff : -diff;
      };

      // If defining after a continuation line break, indent the whole body.
      Func<int, int, long> difference2 =
          (x, y) => {
            long diff = (long)x - y;
            return diff >= 0 ? diff : -diff;
          };

      // Inline lambda arguments also follow these rules. Prefer a leading newline before
      // groups of arguments if they include lambdas.
      CallWithDelegate(
          (x, y) => {
            long diff = (long)x - y;
            return diff >= 0 ? diff : -diff;
          });
    }

    void DoNothing() {}                             // Empty blocks may be concise.

    // If possible, wrap arguments by aligning newlines with the first argument.
    void AVeryLongFunctionNameThatCausesLineWrappingProblems(int longArgumentName,
                                                             int p1, int p2) {}

    // If aligning argument lines with the first argument doesn't fit, or is difficult to
    // read, wrap all arguments on new lines with a 4 space indent.
    void AnotherLongFunctionNameThatCausesLineWrappingProblems(
        int longArgumentName, int longArgumentName2, int longArgumentName3) {}

    void CallingLongFunctionName() {
      int veryLongArgumentName = 1234;
      int shortArg = 1;
      // If possible, wrap arguments by aligning newlines with the first argument.
      AnotherLongFunctionNameThatCausesLineWrappingProblems(shortArg, shortArg,
                                                            veryLongArgumentName);
      // If aligning argument lines with the first argument doesn't fit, or is difficult to
      // read, wrap all arguments on new lines with a 4 space indent.
      AnotherLongFunctionNameThatCausesLineWrappingProblems(
          veryLongArgumentName, veryLongArgumentName, veryLongArgumentName);
    }
  }
}
```

## C# 编码准则

### 常量

*   可以声明为 `const` 的变量和字段应一律声明为 `const`。
*   若无法使用 `const`，`readonly` 可以是合适的替代。
*   优先使用具名常量，而非魔数。

### 容器：IEnumerable 与 IList 与 IReadOnlyList

*   声明（输入）参数时，使用赋予实现所需最少能力的
    类型（例如 `IReadOnlyCollection`）。
    *   仅当实现最多只需对集合迭代一次时才使用 `IEnumerable`。这表示
        调用方可以安全地
        提供生成器。
*   对于输出，若把返回容器的所有权交给调用方，
    请使用能向调用方传达最大能力、又不暴露具体类型的接口类型。
    优先使用 `IList` 而非 `List`。若不转移所有权，则与输入一样，
    优先使用限制最严格的类型。

### 生成器与容器

*   请运用你的最佳判断，并牢记以下几点：
    *   生成器代码往往不如直接填充容器可读。
    *   若结果将被惰性处理（例如并不需要全部结果），
        生成器代码可能性能更好。
    *   通过 `ToList()` 直接转成容器的生成器代码，
        性能会不如直接填充容器。
    *   被多次调用的生成器代码会明显慢于
        对容器多次迭代。

### 属性样式

*   对于单行只读属性，尽可能优先使用表达式体属性
    （`=>`）。
*   其余情况使用较旧的 `{ get; set; }` 语法。

### 表达式体语法

例如：

<div class='goodcode'></div>

```c#
int SomeProperty => _someProperty
```

<div class='goodcode'></div>

```c#
void SomeMethod() => throw new NotImplementedException();
```

*   在 lambda 和属性中审慎使用表达式体语法。
*   对于方法定义，仅在单语句方法中优先使用表达式体语法——
    例如转发给委托或抛出
    异常。
*   与方法及其他有作用域的代码块一样，让右花括号与
    包含左花括号那一行的首字符对齐。
    示例参见示例代码。

### 结构体与类：

*   结构体与类差别很大：

    *   结构体始终按值传递和返回。
    *   给返回的结构体的成员赋值并不会修改
        原对象——例如 `transform.position.x = 10` 并不会把 transform 的
        position.x 设为 10；这里的 `position` 是一个按值返回 `Vector3`
        的属性，因此这只是设置了原对象副本的 x 参数。

*   几乎总是使用类。

*   当某个类型可以像其他值类型那样对待时，考虑使用结构体——
    例如，若该类型的实例很小、通常生命周期很短，或
    通常嵌入在其他对象中。好的例子包括 Vector3、
    Quaternion 和 Bounds。

*   请注意，这条指导可能因团队而异，例如
    性能问题可能迫使使用结构体。

### Lambda 与具名方法

*   若某个 lambda 并不简单（例如超过两三条语句，不含
    声明），或在多处被复用，它大概应该是一个
    具名方法。

### 字段初始化器

*   通常鼓励使用字段初始化器。

### 扩展方法

*   仅在原类的源码不可获得、或修改源码不可行时，
    才使用扩展方法。
*   仅当所添加的功能是适合加入原类源码的
    “核心”通用特性时，
    才使用扩展方法。
    *   注意——若我们拥有被扩展类的源码，而
        原类的维护者不想添加该方法，则最好
        不使用扩展方法。
*   只把扩展方法放入随处可用的核心库中——
    仅在某些代码中可用的扩展会造成
    可读性问题。
*   请注意，使用扩展方法总会让代码变得晦涩，因此
    宁可不加。

### ref 与 out

*   对那些不同时作为输入的额外返回值使用 `out`。
*   在方法定义中把 `out` 参数放在所有其他参数之后。
*   `ref` 应少用，仅在必须修改输入时使用。
*   不要把 `ref` 用作传递结构体的优化手段。
*   不要用 `ref` 把可修改的容器传入方法。`ref` 仅在
    所提供的容器需要被替换为完全不同的
    容器实例时才是必需的。

### LINQ

*   一般而言，优先使用单行 LINQ 调用和命令式代码，而非
    长长的 LINQ 链。把命令式代码与大量链式调用的 LINQ 混用
    往往难以阅读。
*   优先使用成员扩展方法，而非 SQL 风格的 LINQ 关键字——例如优先
    使用 `myList.Where(x)` 而非 `myList where x`。
*   对任何超过单条语句的情形，避免使用 `Container.ForEach(...)`。

### 数组与 List

*   一般而言，对于公有变量、属性和返回类型，优先使用 `List<>` 而非数组
    （请牢记上文关于 `IList` / `IEnumerable` /
    `IReadOnlyList` 的指导）。
*   当容器大小可能变化时，优先使用 `List<>`。
*   当容器大小固定且在构造时
    即已知时，优先使用数组。
*   对于多维数组，优先使用数组。
*   注意：
    *   数组和 `List<>` 都表示线性的连续容器。
    *   与 C++ 数组对比 `std::vector` 类似，数组容量固定，
        而 `List<>` 可以添加元素。
    *   在某些情况下数组性能更好，但一般而言 `List<>` 更为
        灵活。

### 文件夹与文件位置

*   与项目保持一致。
*   尽可能采用扁平结构。

### 使用 tuple 作为返回类型

*   一般而言，优先使用具名类类型而非 `Tuple<>`，尤其是在
    返回复杂类型时。

### 字符串插值与 `String.Format()` 与 `String.Concat` 与 `operator+`

*   一般而言，使用最易读的方式，尤其是对于日志和
    断言消息。
*   请注意，链式 `operator+` 拼接会更慢，并造成
    显著的内存抖动。
*   若关注性能，`StringBuilder` 在多次
    字符串拼接时会更快。

### `using`

*   一般而言，不要用 `using` 为长类型名设置别名。这往往表明
    某个 `Tuple<>` 需要改成类。
    *   例如 `using RecordList = List<Tuple<int, float>>` 大概应该
        改为具名类。
*   请注意，`using` 语句仅在文件范围内有效，因而用途有限。
    类型别名对外部用户不可用。

### 对象初始化器语法

例如：

<div class='goodcode'></div>

```c#
var x = new SomeClass {
  Property1 = value1,
  Property2 = value2,
};
```

*   对象初始化器语法适用于“纯旧数据”类型。
*   对带有构造函数的类或结构体避免使用此语法。
*   若拆分为多行，请缩进一个代码块层级。

### 命名空间命名

*   一般而言，命名空间不应超过 2 层。
*   不要强行让文件／文件夹布局与命名空间一致。
*   对于共享库／模块代码，请使用命名空间。对于叶子“应用”代码，
    例如 `unity_app`，则不需要命名空间。
*   新的顶层命名空间名称必须全局唯一且易于辨认。

### 结构体的默认值／返回 null

*   优先返回一个表示“成功”的布尔值和一个结构体 `out` 值。
*   在性能不成问题、且由此得到的代码明显
    更易读时（例如链式 null 条件运算符对比深层嵌套的 if
    语句），可空结构体是可以接受的。
*   说明：

    *   可空结构体很方便，但会强化 Google 倾向于避免的
        一般“null 即失败”模式。若需求足够多，我们将来会研究
        `StatusOr` 的对应方案。

### 迭代时从容器中移除元素

C#（与许多其他语言一样）没有提供在迭代时
从容器中移除元素的明显机制。有以下几种选择：

*   若只需移除满足某条件的元素，
    推荐使用 `someList.RemoveAll(somePredicate)`。
*   若迭代中还需完成其他工作，`RemoveAll` 可能不够。
    一种常见的替代做法是在循环外创建一个新容器，
    把要保留的元素放入新容器，并在迭代结束时
    用新容器替换原容器。

### 调用委托

*   调用委托时，请使用 `Invoke()` 并使用 null 条件
    运算符——例如 `SomeDelegate?.Invoke()`。这能在调用处清楚地标明
    这是“一个正在被调用的委托”。null 检查简洁，
    且能稳健地应对线程竞态条件。

### `var` 关键字

*   若使用 `var` 能通过避开冗杂、显而易见或无关紧要的类型名
    来提升可读性，则鼓励使用。
*   鼓励使用的情形：

    *   当类型显而易见时——例如 `var apple = new Apple();`，或
        `var request = Factory.Create<HttpRequest>();`
    *   对于仅直接传递给其他方法的临时变量——
        例如 `var item = GetItem(); ProcessItem(item);`

*   不鼓励使用的情形：

    *   处理基础类型时——例如 `var success = true;`
    *   处理由编译器解析的内置数值类型时——例如
        `var number = 12 * ReturnsFloat();`
    *   当用户显然能从知道类型中受益时——例如
        `var listOfItems = GetList();`

### 特性

*   特性应出现在其所关联的字段、属性或方法的
    上一行，并用空行与该成员分隔。
*   多个特性之间应以空行分隔。这样更便于
    增删特性，也确保每个特性都易于
    搜索。

### 参数命名

源自
[Google C++ style guide](https://google.github.io/styleguide/cppguide.html#Function_Argument_Comments)。

当方法参数的含义不明显时，请考虑以下
补救办法之一：

*   若参数是字面常量，且同一常量在
    多次方法调用中以默认它们相同的方式被使用，请使用
    具名常量把该约束显式化，并保证它
    成立。
*   考虑修改方法签名，把 `bool` 参数替换为
    `enum` 参数。这会让参数值自我描述。
*   用具名变量替换庞大或复杂的嵌套表达式。
*   考虑使用
    [具名参数](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/named-and-optional-arguments)
    在调用处阐明参数的含义。
*   对于有多个配置选项的方法，考虑定义一个
    单独的类或结构体来容纳所有选项，并传入其实例。
    这种做法有若干优点。选项在调用处按名称引用，
    从而阐明其含义。它还能减少方法参数的
    数量，使方法调用更易读写。额外的
    好处是，新增选项时无需改动调用处。

请看以下示例：

<div class='badcode'></div>

```c#
// What are these arguments?
DecimalNumber product = CalculateProduct(values, 7, false, null);
```

与之对比：

<div class='goodcode'></div>

```c#
var options = new ProductOptions();
options.PrecisionDecimals = 7;
options.UseCache = CacheUsage.DontUseCache;
DecimalNumber product = CalculateProduct(values, options, completionDelegate: null);
```

### 注释

（源自 [Google C++ style guide]。）

注释对于保持代码可读性绝对至关重要。以下规则
说明应该注释什么、在哪里注释。但请记住：虽然注释
非常重要，最好的代码是自文档化的。为
类型和变量起合理的名字，远胜于使用晦涩的名字然后再
通过注释去解释。

编写注释时，要为你的读者而写：下一个需要
理解你代码的人。请大方一些——下一个人可能就是你自己！

#### 类注释

每个不显而易见的类都应附有注释，说明
它的用途以及应当如何使用。

类注释应为读者提供足够的信息，使其知道如何
以及何时使用该类，以及正确使用该类所需的
任何额外注意事项。

#### 方法注释

几乎每个方法都应在紧邻其前的位置有注释，说明
该方法做什么以及如何使用。仅当
方法简单而显而易见时（例如简单的访问器）才可省略这些注释。方法注释
应以隐含主语*本方法*来写，并应以
动词短语开头；例如 "Opens the file"，而非 "Open the file"。

注释中应提及的事项类型：

*   输入和输出是什么。若方法参数名以
    `backticks` 给出，则代码索引工具或许能更好地呈现
    文档。

*   对象是否会在方法调用
    结束后仍记住参数。

*   是否有任何参数可以为 null。

*   方法的使用方式是否有任何性能影响。

不过，不要不必要地啰嗦，也不要陈述完全显而易见的内容。

为方法重写编写文档时，请聚焦于该重写
本身的细节，而不是重复被重写方法的注释。在许多
这类情形下，重写不需要额外的文档，因而
无需注释。

为构造函数写注释时，请记住读你代码的人知道
构造函数是做什么的，因此只说诸如 "creates
this object" 之类的注释并无用处。

#### 类成员

每个类数据成员的用途都必须清晰。若存在任何
未由类型和名称清楚表达的不变式
（特殊值、成员之间的关系、生命周期要求），就必须加以注释。
不过，若类型和名称已足够，则无需注释。

#### 变量注释

一般而言，变量的实际名称应足够具有描述性，能让人
清楚了解该变量的用途。在某些情况下，需要
更多注释。

#### 解释性注释

棘手或复杂的代码块前应附有注释。

[Google C++ style guide]: https://google.github.io/styleguide/cppguide.html#Comments
