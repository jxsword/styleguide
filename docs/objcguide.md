# Google Objective-C 风格指南

> Objective-C 是 C 语言的动态、面向对象扩展。它的设计目标是
> 易于使用和阅读，同时支持精细的面向对象设计。它是
> Apple 平台上应用程序的主要
> 开发语言之一。
>
> Apple 已经编写了一份非常优秀且广受认可的、面向
> Objective-C 的 [Cocoa Coding Guidelines](https://developer.apple.com/library/content/documentation/Cocoa/Conceptual/CodingGuidelines/CodingGuidelines.html)。
> 除本风格指南之外，也请阅读该文档。
>
> 本文档旨在描述 Objective-C（以及
> Objective-C++）的编码指南与实践。这些指南是在其他
> 项目和团队中逐步演进并经过长期验证的。由 Google 开发的
> 开源项目均遵循本风格指南中的要求。
>
> 请注意，本风格指南并非 Objective-C 教程。我们假定读者
> 已熟悉该语言。如果您刚接触 Objective-C 或需要
> 温习，请阅读
> [Programming with Objective-C](https://developer.apple.com/library/mac/#documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/Introduction/Introduction.html)。

<!-- mdformat off -->
* TOC
{:toc}
<!-- mdformat on -->

## 原则

### 为读者优化，而非为编写者优化

代码库往往有很长的生命周期，阅读代码所花的时间
多于编写代码的时间。我们明确选择优化普通软件工程师
在代码库中阅读、维护和调试代码的体验，而不是
编写这些代码时的便利性。例如，当某段代码中发生
令人意外或不寻常的事情时，为读者留下文字提示
是很有价值的。

### 保持一致

当风格指南允许多个选项时，最好固定选择其中一种，
而不是混用多种选项。在整个代码库中始终使用一种
风格，能让工程师专注于其他（更重要的）问题。
一致性还有助于实现更好的自动化，因为一致的代码
能更高效地开发和运行用于格式化或重构代码的工具。
在许多情况下，那些归为「保持一致」的规则归结起来
无非是「选定一种，别再纠结」；在这些细枝末节上
允许灵活性的潜在价值，抵不过人们为此争论的成本。

### 与 Apple SDK 保持一致

与 Apple SDK 使用 Objective-C 的方式保持一致，
其价值与我们代码库内部保持一致性的理由相同。
如果某项 Objective-C 特性能解决某个问题，那便是
使用它的理由。不过，有时语言特性和惯用法本身
存在缺陷，或只是基于并不普适的假设而设计。
在这些情况下，对语言特性或惯用法加以限制或禁用是恰当的。

### 风格规则应当物有所值

一条风格规则的收益必须足够大，才值得要求工程师
去记住它。收益是相对于「没有这条规则时我们会得到
的代码库」来衡量的，因此，即便某条规则针对的是
一种危害极大的做法，如果人们本来就不太可能那样做，
它的收益也可能很小。这一原则主要解释的是我们
没有制定的规则，而非已有的规则：例如，goto 违背了
后面的许多原则，但因其极为罕见而不予讨论。

<a id="Example"></a>

## 示例

人们常说，一个示例胜过千言万语，所以我们先从
一个示例开始，让你感受一下风格、间距、命名等。

下面是一个头文件示例，展示了
`@interface` 声明正确的注释与间距。

<div class='goodcode'></div>

```objectivec
#import <Foundation/Foundation.h>

#import "path/to/Bar.h"

/**
 * A sample class demonstrating good Objective-C style. All interfaces,
 * categories, and protocols (read: all non-trivial top-level declarations
 * in a header) MUST be commented. Comments must also be adjacent to the
 * object they're documenting.
 */
@interface Foo : NSObject

/** The retained Bar. */
@property(nonatomic) Bar *bar;

/** The current drawing attributes. */
@property(nonatomic, copy) NSDictionary<NSString *, NSNumber *> *attributes;

/**
 * Convenience creation method.
 * See -initWithBar: for details about @c bar.
 *
 * @param bar The string for fooing.
 * @return An instance of Foo.
 */
+ (instancetype)fooWithBar:(Bar *)bar;

/**
 * Initializes and returns a Foo object using the provided Bar instance.
 *
 * @param bar A string that represents a thing that does a thing.
 */
- (instancetype)initWithBar:(Bar *)bar NS_DESIGNATED_INITIALIZER;

/**
 * Does some work with @c blah.
 *
 * @param blah
 * @return YES if the work was completed; NO otherwise.
 */
- (BOOL)doWorkWithBlah:(NSString *)blah;

@end
```

下面是一个源文件示例，展示了接口的
`@implementation` 部分正确的注释与间距。

<div class='goodcode'></div>

```objectivec
#import "Shared/Util/Foo.h"

@implementation Foo {
  /** The string used for displaying "hi". */
  NSString *_string;
}

+ (instancetype)fooWithBar:(Bar *)bar {
  return [[self alloc] initWithBar:bar];
}

- (instancetype)init {
  // Classes with a custom designated initializer should always override
  // the superclass's designated initializer.
  return [self initWithBar:nil];
}

- (instancetype)initWithBar:(Bar *)bar {
  self = [super init];
  if (self) {
    _bar = [bar copy];
    _string = [[NSString alloc] initWithFormat:@"hi %d", 3];
    _attributes = @{
      @"color" : UIColor.blueColor,
      @"hidden" : @NO
    };
  }
  return self;
}

- (BOOL)doWorkWithBlah:(NSString *)blah {
  // Work should be done here.
  return NO;
}

@end
```

<a id="Naming"></a>

## 命名

命名应在合理范围内尽可能具有描述性。请遵循标准的
[Objective-C 命名规则](https://developer.apple.com/library/content/documentation/Cocoa/Conceptual/CodingGuidelines/CodingGuidelines.html)。

避免使用非标准的缩写（包括非标准的首字母缩略词
（acronym）和首字母缩写（initialism））。不必担心
节省水平空间，让新读者能立即看懂代码要重要得多。
例如：

<div class='goodcode'></div>

```objectivec
// Good names.
int numberOfErrors = 0;
int completedConnectionsCount = 0;
tickets = [[NSMutableArray alloc] init];
userInfo = [someObject object];
port = [network port];
NSDate *gAppLaunchDate;
```

<div class='badcode'></div>

```objectivec
// Names to avoid.
int w;
int nerr;
int nCompConns;
tix = [[NSMutableArray alloc] init];
obj = [someObject object];
p = [network port];
```

任何类、类别、方法、函数或变量的名称中，其中的
缩写词与[首字母缩写](https://en.wikipedia.org/wiki/Initialism)（包括出现在名称
开头时）都应全部大写。这遵循了 Apple 的标准：
对 URL、ID、TIFF、EXIF 等缩写词在名称中一律全部大写。

C 函数和 typedef 的名称应大写，并根据周围代码的
情况采用驼峰命名法。

<a id="Inclusive_Language"></a>

### 包容性语言

在所有代码中（包括命名和注释），都应使用包容性语言，
避免使用其他程序员可能觉得不敬或冒犯的术语（如
"master"/"slave"、"blacklist"/"whitelist" 或
"redline"），即便它们表面上有中性含义。同样，
除非指代具体的人（并使用其代词），否则应使用
性别中立的语言。例如，对性别未指明的人（即使
是单数）用 "they"/"them"/"their"，对非人用 "it"/"its"。

<a id="File_Names"></a>

### 文件名

文件名应反映其中所包含的类实现的名称，
包括大小写。

遵循你所在项目使用的约定。

文件扩展名应如下所示：

扩展名 | 类型
--------- | ---------------------------------
.h        | C/C++/Objective-C 头文件
.m        | Objective-C 实现文件
.mm       | Objective-C++ 实现文件
.cc       | 纯 C++ 实现文件
.c        | C 实现文件

包含可能跨项目共享或在大型项目中使用的代码的
文件，应具有明显唯一的名字，通常要包含项目或
类的[前缀](#prefixes)。

类别的文件名应包含被扩展的类的名称，
例如 GTMNSString+Utils.h 或 NSTextView+GTMAutocomplete.h

### 前缀

在 Objective-C 中通常需要使用前缀，以避免
全局命名空间中的命名冲突。类、协议、全局函数和
全局常量一般应以一个大写字母开头、后跟一个
或多个大写字母或数字的前缀来命名。

警告：Apple 保留两字母前缀——参见
[Conventions in Programming with Objective-C](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/Conventions/Conventions.html)——因此
最少三个字符的前缀被视为最佳实践。

<div class='goodcode'></div>

```objectivec
/** An example error domain. */
GTM_EXTERN NSString *GTMExampleErrorDomain;

/** Gets the default time zone. */
GTM_EXTERN NSTimeZone *GTMGetDefaultTimeZone(void);

/** An example delegate. */
@protocol GTMExampleDelegate <NSObject>
@end

/** An example class. */
@interface GTMExample : NSObject
@end

```

<a id="Class_Names"></a>

### 类名

类名（以及类别名和协议名）应以大写字母开头，
并使用大小写混合来分隔单词。

在多个应用程序之间共享的代码中，类和协议必须带有
恰当的[前缀](#prefixes)（例如 GTMSendMessage）。对于其他
类和协议，建议使用前缀，但不作强制要求。

<a id="Category_Names"></a>

### 类别命名

类别名应以恰当的[前缀](#prefixes)开头，用于表明该
类别属于某个项目，或可供广泛使用。

类别的源文件名应以被扩展的类名开头，后跟
一个加号和类别名，例如 `NSString+GTMParsing.h`。
类别中的方法应以类别名所用前缀的小写形式，
后跟一个下划线作为前缀（例如
`gtm_myCategoryMethodOnAString:`），以防在
Objective-C 的全局命名空间中发生冲突。

类名与类别的左括号之间应留有
一个空格。

<div class='goodcode'></div>

```objectivec
// UIViewController+GTMCrashReporting.h

/** A category that adds metadata to include in crash reports to UIViewController. */
@interface UIViewController (GTMCrashReporting)

/** A unique identifier to represent the view controller in crash reports. */
@property(nonatomic, setter=gtm_setUniqueIdentifier:) int gtm_uniqueIdentifier;

/** Returns an encoded representation of the view controller's current state. */
- (nullable NSData *)gtm_encodedState;

@end
```

如果某个类不与其他项目共享，则扩展它的类别
可以省略名称前缀和方法名前缀。

<div class='goodcode'></div>

```objectivec
/** This category extends a class that is not shared with other projects. */
@interface XYZDataObject (Storage)
- (NSString *)storageIdentifier;
@end
```

<a id="Objective-C_Method_Names"></a>

### Objective-C 方法名

方法名和参数名通常以小写开头，随后使用大小写混合。

应遵守正确的大小写规则，包括名称的开头。

<div class='goodcode'></div>

```objectivec
+ (NSURL *)URLWithString:(NSString *)URLString;
```

方法名应尽可能读起来像一个句子，也就是说，
你应选择与方法名连贯搭配的参数名。Objective-C 的
方法名往往很长，但这样做的好处是代码块几乎
可以像散文一样阅读，从而免去许多实现注释。

仅在为阐明方法的含义或行为所必需时，才在第二个
及后续的参数名中使用介词和连词，如 "with"、
"from" 和 "to"。

<div class='goodcode'></div>

```objectivec
- (void)addTarget:(id)target action:(SEL)action;                          // GOOD; no conjunction needed
- (CGPoint)convertPoint:(CGPoint)point fromView:(UIView *)view;           // GOOD; conjunction clarifies parameter
- (void)replaceCharactersInRange:(NSRange)aRange
            withAttributedString:(NSAttributedString *)attributedString;  // GOOD.
```

如果方法返回接收者的某个属性，则以该属性
为方法命名。

<div class='goodcode'></div>

```objectivec
/** Returns this instance's sandwich. */
- (Sandwich *)sandwich;      // GOOD.

- (CGFloat)height;           // GOOD.

// GOOD; Returned value is not an attribute.
- (UIBackgroundTaskIdentifier)beginBackgroundTask;
```

<div class='badcode'></div>

```objectivec
- (CGFloat)calculateHeight;  // AVOID.
- (id)theDelegate;           // AVOID.
```

访问器方法应与其所获取的对象同名，但不
应以 `get` 一词作为前缀。例如：

<div class='goodcode'></div>

```objectivec
- (id)delegate;     // GOOD.
```

<div class='badcode'></div>

```objectivec
- (id)getDelegate;  // AVOID.
```

返回布尔形容词值的访问器，其方法名
以 `is` 开头，但对应这些方法的属性名则省略 `is`。

点语法只用于属性名，不用于方法名。

<div class='goodcode'></div>

```objectivec
@property(nonatomic, getter=isGlorious) BOOL glorious;
// The method for the getter of the property above is:
// - (BOOL)isGlorious;

BOOL isGood = object.glorious;      // GOOD.
BOOL isGood = [object isGlorious];  // GOOD.
```

<div class='badcode'></div>

```objectivec
BOOL isGood = object.isGlorious;    // AVOID.
```

<div class='goodcode'></div>

```objectivec
NSArray<Frog *> *frogs = [NSArray<Frog *> arrayWithObject:frog];
NSEnumerator *enumerator = [frogs reverseObjectEnumerator];  // GOOD.
```

<div class='badcode'></div>

```objectivec
NSEnumerator *enumerator = frogs.reverseObjectEnumerator;    // AVOID.
```

有关 Objective-C 命名的更多细节，
请参见
[Apple's Guide to Naming Methods](https://developer.apple.com/library/mac/documentation/Cocoa/Conceptual/CodingGuidelines/Articles/NamingMethods.html#//apple_ref/doc/uid/20001282-BCIGIJJF)。

这些指南仅适用于 Objective-C 方法。C++ 方法名
仍遵循 C++ 风格指南中设定的规则。

<a id="Function_Names"></a>

### 函数名

函数名应以大写字母开头，且每个新单词
都以大写字母开头（即「[驼峰命名法](https://en.wikipedia.org/wiki/Camel_case)」
或「帕斯卡命名法」）。

<div class='goodcode'></div>

```objectivec
static void AddTableEntry(NSString *tableEntry);
static BOOL DeleteFile(const char *filename);
```

由于 Objective-C 不提供命名空间，非静态函数
应带有[前缀](#prefixes)，以尽量降低名称冲突的可能。

<div class='goodcode'></div>

```objectivec
GTM_EXTERN NSTimeZone *GTMGetDefaultTimeZone(void);
GTM_EXTERN NSString *GTMGetURLScheme(NSURL *URL);
```

<a id="Variable_Names"></a>

### 变量名

变量名通常以小写字母开头，并使用大小写混合
来分隔单词。

实例变量带有前导下划线。文件作用域或全局变量
带有 `g` 前缀。例如：`myLocalVariable`、`_myInstanceVariable`、
`gMyGlobalVariable`。

<a id="Common_Variable_Names"></a>

#### 通用变量名

读者应能从名称推断出变量的类型，但不要对
语法属性使用匈牙利命名法，例如变量的静态类型
（int 或指针）。

在方法或函数作用域之外声明的文件作用域或全局
变量（与常量相对）应当少见，并应带有 `g` 前缀。

<div class='goodcode'></div>

```objectivec
static int gGlobalCounter;
```

<a id="Instance_Variables"></a>

#### 实例变量

实例变量名采用大小写混合，并应以下划线
作为前缀，例如 `_usernameTextField`。

注意：Google 此前对 Objective-C ivar 的约定是使用
后置下划线。现有项目可以选择在新代码中继续
使用后置下划线，以保持项目代码库内部的一致性。
每个类内部应保持前缀下划线或后缀下划线的
一致性。

<a id="Constants"></a>

#### 常量

常量符号（const 全局与静态变量，以及用 #define
创建的常量）应使用大小写混合来分隔单词。

全局和文件作用域的常量应带有恰当的[前缀](#prefixes)。

<div class='goodcode'></div>

```objectivec
/** The domain for GTL service errors. */
GTL_EXTERN NSString *const GTLServiceErrorDomain;

/** An enumeration of GTL service error codes. */
typedef NS_ENUM(int32_t, GTLServiceError) {
  /** An error code indicating that a query result was missing. */
  GTLServiceErrorQueryResultMissing = -3000,
  /** An error code indicating that the query timed out. */
  GTLServiceErrorQueryTimedOut      = -3001,
};
```

由于 Objective-C 不提供命名空间，具有外部链接的
常量应带有能尽量降低名称冲突概率的前缀，
通常形如 `ClassNameConstantName` 或 `ClassNameEnumName`。

为与 Swift 代码互操作，枚举值的名称应
扩展 typedef 的名称：

<div class='goodcode'></div>

```objectivec
/** An enumeration of supported display tinges. */
typedef NS_ENUM(int32_t, DisplayTinge) {
  DisplayTingeGreen = 1,
  DisplayTingeBlue = 2,
};
```

对于在实现文件中声明的、具有静态存储期的常量，
可以使用小写字母 k 作为独立前缀：

<div class='goodcode'></div>

```objectivec
static const int kFileCount = 12;
static NSString *const kUserKey = @"kUserKey";
```

注意：此前的约定是公开常量名以小写字母 k 开头，
后跟项目专属的[前缀](#prefixes)。现已不再推荐
这种做法。

<a id="Types_and_Declarations"></a>

## 类型与声明

<a id="Forward_Declarations"></a>

### 避免前向声明

避免使用类型的前向声明，除非为打破同一模块中
类型之间的循环依赖而确有必要。

前向声明：

*   会导致将头文件导入 Swift 时出现问题。
*   在类型被重命名时可能掩盖问题。

<div class='goodcode'></div>

```objectivec
#import "Path/To/Foo.h"

void CallWithAFoo(Foo *);  // GOOD.
...
```

<div class='goodcode'></div>

```objectivec
@class Foo;  // GOOD to break circular dependency

@protocol FooDelegate
- (void)handleACallFromAFoo:(Foo *)foo;
@end

@interface Foo : NSObject
@property(weak) FooDelegate *delegate;
@end
...
```

<div class='badcode'></div>

```objectivec
@class Foo;  // AVOID.

void CallWithAFoo(Foo *foo);
...
```

<a id="Method_Declarations"></a>

### 方法声明

如[示例](#Example)所示，在
`@interface` 声明中，声明的推荐顺序为：
属性、类方法、初始化方法，最后是实例方法。
类方法部分应以所有便捷构造器开头。

<a id="Local_Variables"></a>

### 局部变量

在尽可能窄且切实可行的作用域内、靠近使用处
声明变量，并在声明时初始化变量。

<div class='goodcode'></div>

```objectivec
CLLocation *location = [self lastKnownLocation];
for (int meters = 1; meters < 10; meters++) {
  reportFrogsWithinRadius(location, meters);
}
```

有时出于效率考虑，更合适的做法是在变量的
使用作用域之外声明它。下面的示例将 meters 的
声明与初始化分开，并且每次循环都多余地发送
lastKnownLocation 消息：

<div class='badcode'></div>

```objectivec
int meters;                                         // AVOID.
for (meters = 1; meters < 10; meters++) {
  CLLocation *location = [self lastKnownLocation];  // AVOID.
  reportFrogsWithinRadius(location, meters);
}
```

在自动引用计数（ARC）下，指向 Objective-C 对象的
强指针和弱指针会自动初始化为 `nil`，因此在这些
常见情况下无需显式初始化为 `nil`。不过，对于
许多 Objective-C 指针类型，自动初始化*并不*发生，
包括以 `__unsafe_unretained` 所有权限定符声明的
对象指针以及 CoreFoundation 对象指针类型。
如有疑问，最好初始化所有 Objective-C 局部变量。

### 静态变量

当实现文件中的文件作用域变量／常量声明不需要
在该文件之外被引用时，应将其声明为 static（在
Objective-C++ 中则置于匿名命名空间）。不要在 .h
文件中声明具有静态存储期的文件作用域变量或常量
（在 Objective-C++ 中也不置于匿名命名空间）。

<div class='goodcode'></div>

```objectivec
// file: Foo.m
static const int FOORequestLimit = 5;
```

<div class='badcode'></div>

```objectivec
// file: Foo.h
static const int FOORequestLimit = 5;  // AVOID.
```

<a id="Unsigned_Integers"></a>

### 无符号整数

除与系统接口所使用的类型相匹配外，应避免使用无符号整数。

使用无符号整数进行数学运算或倒数到零时，
容易滋生难以察觉的错误。除与系统接口中的
NSUInteger 匹配外，数学表达式中只使用有符号整数。

<div class='goodcode'></div>

```objectivec
NSUInteger numberOfObjects = array.count;
for (NSInteger counter = numberOfObjects - 1; counter >= 0; --counter)
```

<div class='badcode'></div>

```objectivec
for (NSUInteger counter = numberOfObjects - 1; counter >= 0; --counter)  // AVOID.
```

无符号整数可用于标志位和位掩码，不过通常
NS_OPTIONS 或 NS_ENUM 更为合适。

<a id="Types_with_Inconsistent_Sizes"></a>

### 大小不一致的类型

请注意，long、NSInteger、NSUInteger 和 CGFloat
这些类型在 32 位和 64 位构建中的大小不同。
在匹配系统接口时使用它们是合适的，但在处理
要求精确大小的 API（例如 proto API）时应避免使用。

<div class='goodcode'></div>

```objectivec
int32_t scalar1 = proto.intValue;

int64_t scalar2 = proto.longValue;

NSUInteger numberOfObjects = array.count;

CGFloat offset = view.bounds.origin.x;
```

<div class='badcode'></div>

```objectivec
NSInteger scalar2 = proto.longValue;  // AVOID.
```

文件和缓冲区的大小常常超过 32 位限制，因此
应使用 `int64_t` 声明，而不是 `long`、`NSInteger` 或 `NSUInteger`。

<a id="Floating_Point_Constants"></a>

#### 浮点常量

定义 `CGFloat` 常量时，请牢记以下几点。

以往对于面向 32 位平台的项目，使用 `float` 字面量
（带 `f` 后缀的数字）可能是必要的，以避免
类型转换警告。

由于所有 Google iOS 项目现在只面向 64 位运行时，`CGFloat`
常量可省略后缀（使用 `double` 值）。不过团队
可以选择继续使用 `float` 数值以保持遗留
代码一致，直到全面改用 `double` 值。避免在同一代码中混用 `float` 和
`double` 值。

<div class='goodcode'></div>

```objectivec
// Good since CGFloat is double
static const CGFloat kHorizontalMargin = 8.0;
static const CGFloat kVerticalMargin = 12.0;

// This is OK as long as all values for CGFloat constants in your project are float
static const CGFloat kHorizontalMargin = 8.0f;
static const CGFloat kVerticalMargin = 12.0f;
```

<div class='badcode'></div>

```objectivec
// Avoid a mixture of float and double constants
static const CGFloat kHorizontalMargin = 8.0f;
static const CGFloat kVerticalMargin = 12.0;
```

<a id="Comments"></a>

## 注释

注释对于保持代码的可读性至关重要。以下规则
描述了应在何处添加何种注释。但请记住：注释
固然重要，最好的代码却是自文档化的。为类型和
变量起一个合理的名字，远胜于使用晦涩的名称，
然后再试图通过注释去解释它们。

注意标点、拼写和语法；写得好的注释
比写得差的注释更易读。

注释应像叙述性文字一样易读，并使用正确的
大小写和标点。在许多情况下，完整的句子比
句子片段更易读。较短的注释（例如代码行末的
注释）有时可以不那么正式，但要保持风格一致。

编写注释时，要为读者着想：也就是下一位需要
理解你代码的贡献者。请多写一些——下一位可能就是你！

<a id="File_Comments"></a>

### 文件注释

文件可以选择以一段内容描述开头。

每个文件可以按顺序包含以下各项：

*   必要时加入许可证样板代码。为项目所使用的
    许可证选择合适的样板代码。
*   必要时加入文件内容的基本描述。

如果你对带有作者行的文件做了重大修改，请考虑
删除该作者行，因为版本历史已经提供了更详细、
更准确的作者记录。

<a id="Declaration_Comments"></a>

### 声明注释

每个非平凡的接口，无论公开还是私有，都应配有
注释，说明其用途以及它在整体中的作用。

应使用注释来记录类、属性、ivar、函数、
类别、协议声明和枚举。

<div class='goodcode'></div>

```objectivec
/**
 * A delegate for NSApplication to handle notifications about app
 * launch and shutdown. Owned by the main app controller.
 */
@interface MyAppDelegate : NSObject {
  /**
   * The background task in progress, if any. This is initialized
   * to the value UIBackgroundTaskInvalid.
   */
  UIBackgroundTaskIdentifier _backgroundTaskID;
}

/** The factory that creates and manages fetchers for the app. */
@property(nonatomic) GTMSessionFetcherService *fetcherService;

@end
```

鼓励为接口使用 [Doxygen](https://doxygen.nl) 风格的注释，
因为 Xcode 会解析它们以显示格式化的文档。
[Doxygen 命令](https://www.doxygen.nl/manual/commands.html)种类繁多；
在一个项目内应保持一致地使用。

如果你已在文件顶部的注释中详细描述过某个
接口，可以简单地写明「完整描述请参见文件顶部的
注释」，但务必保留某种形式的注释。

此外，每个方法都应有注释，说明其功能、
参数、返回值、线程或队列假设，以及任何副作用。
公开方法的文档注释应放在头文件中；非平凡的
私有方法，注释应紧邻方法之前。

方法和函数的注释应使用描述式（"Opens the file"），
而非祈使式（"Open the file"）。注释描述的是函数；
它并不命令函数去做什么。

记录类、属性或方法所作出的线程使用假设
（如果有的话）。如果类的实例可能被多个线程
访问，请格外用心地记录多线程使用的规则和不变式。

属性和 ivar 的任何哨兵值（例如 `nullptr` 或 `-1`）
都应在注释中加以说明。

声明注释解释方法或函数如何被使用。解释
方法或函数如何实现的注释，应放在实现处，
而不是声明处。

如果注释除了方法名之外无法传达更多信息，
测试用例类和测试方法可以省略声明注释。
测试中的工具方法或测试专用的类（例如辅助类）
应添加注释。

<a id="Implementation_Comments"></a>

### 实现注释

为棘手、微妙或复杂的代码段提供解释性注释。

<div class='goodcode'></div>

```objectivec
// Set the property to nil before invoking the completion handler to
// avoid the risk of reentrancy leading to the callback being
// invoked again.
CompletionHandler handler = self.completionHandler;
self.completionHandler = nil;
handler();
```

在有用时，也应为曾考虑过或已放弃的实现
方案提供注释。

行尾注释与代码之间应至少隔 2 个空格。
如果连续几行都有注释，将它们对齐
往往更易读。

<div class='goodcode'></div>

```objectivec
[self doSomethingWithALongName];  // Two spaces before the comment.
[self doSomethingShort];          // More spacing to align the comment.
```

<a id="Disambiguating_Symbols"></a>

### 消除符号歧义

为避免歧义而确有需要时，在注释中使用反引号
或竖线来引用变量名和符号，而不要使用引号，
也不要把符号直接写在行文中。

在 Doxygen 风格的注释中，最好使用等宽文本命令
来界定符号，例如 [`@c`](https://www.doxygen.nl/manual/commands.html#cmdc)。

当某个符号是常见词、可能使句子读起来像是
组织得不好时，加以界定有助于使表达清晰。
一个常见的例子是符号 `count`：

<div class='goodcode'></div>

```objectivec
// Sometimes `count` will be less than zero.
```

或者当引用本身已包含引号的内容时

<div class='goodcode'></div>

```objectivec
// Remember to call `StringWithoutSpaces("foo bar baz")`
```

当符号本身一目了然时，不需要使用反引号或竖线。

<div class='goodcode'></div>

```objectivec
// This class serves as a delegate to GTMDepthCharge.
```

Doxygen 格式也适用于标识符号。

<div class='goodcode'></div>

```objectivec
/** @param maximum The highest value for @c count. */
```

<a id="Object_Ownership"></a>

### 对象所有权

对于不受 ARC 管理的对象，当指针所有权模型
超出最常见的 Objective-C 使用惯用法时，应使其尽量明确。

<a id="Manual_Reference_Counting"></a>

#### 手动引用计数

NSObject 派生对象的实例变量被假定为已持有；
如果未被持有，则应注释为 weak，或使用
`__weak` 生命周期限定符来声明。

一个例外是 Mac 软件中标注为 `@IBOutlets` 的
实例变量，它们被假定为未被持有。

当实例变量是指向 Core Foundation、C++ 及其他
非 Objective-C 对象的指针时，应始终附带 strong 和
weak 注释，以指明哪些指针被持有、哪些没有。
Core Foundation 及其他非 Objective-C 对象指针
需要显式内存管理，即使为自动引用计数构建亦然。

strong 与 weak 声明的示例：

<div class='goodcode'></div>

```objectivec
@interface MyDelegate : NSObject

@property(nonatomic) NSString *doohickey;
@property(nonatomic, weak) NSString *parent;

@end


@implementation MyDelegate {
  IBOutlet NSButton *_okButton;  // Normal NSControl; implicitly weak on Mac only

  AnObjcObject *_doohickey;  // My doohickey
  __weak MyObjcParent *_parent;  // To send messages back (owns this instance)

  // non-NSObject pointers...
  CWackyCPPClass *_wacky;  // Strong, some cross-platform object
  CFDictionaryRef *_dict;  // Strong
}
@end
```

<a id="Automatic_Reference_Counting"></a>

#### 自动引用计数

使用 ARC 时，对象所有权和生命周期都是
显式的，因此对自动持有的对象无需附加注释。

<a id="C_Language_Features"></a>

## C 语言特性

<a id="Macros"></a>

### 宏

避免使用宏，尤其是在可以使用 `const` 变量、枚举、
Xcode 代码片段或 C 函数来替代的场合。

宏会让你看到的代码与编译器看到的代码不同。
现代 C 使得用宏来定义常量和工具函数的传统
用法变得没有必要。只有在没有其他可用方案时
才应使用宏。

在确实需要宏时，应使用唯一的名称，以避免
在编译单元内发生符号冲突。如果可行，应在使用后
通过 `#undefining` 宏来限制其作用域。

宏名应使用 `SHOUTY_SNAKE_CASE`——全部采用
大写字母，单词间以下划线分隔。函数式宏可采用
C 函数命名惯例。不要定义看似 C 或 Objective-C 关键字的宏。

<div class='goodcode'></div>

```objectivec
#define GTM_EXPERIMENTAL_BUILD ...      // GOOD

// Assert unless X > Y
#define GTM_ASSERT_GT(X, Y) ...         // GOOD, macro style.

// Assert unless X > Y
#define GTMAssertGreaterThan(X, Y) ...  // GOOD, function style.
```

<div class='badcode'></div>

```objectivec
#define kIsExperimentalBuild ...        // AVOID

#define unless(X) if(!(X))              // AVOID
```

避免展开为不平衡的 C 或 Objective-C 结构的宏。
避免引入作用域、或可能掩盖 block 中值捕获的宏。

避免在头文件中用宏生成类、属性或方法的定义
以充当公开 API。这只会让代码难以理解，而语言
本身已有更好的方式来实现这一点。

避免用宏生成方法实现，或生成在宏之外
被使用的变量声明。宏不应通过隐藏变量的
声明位置和方式来使代码难以理解。

<div class='badcode'></div>

```objectivec
#define ARRAY_ADDER(CLASS) \
  -(void)add ## CLASS ## :(CLASS *)obj toArray:(NSMutableArray *)array

ARRAY_ADDER(NSString) {
  if (array.count > 5) {              // AVOID -- where is 'array' defined?
    ...
  }
}
```

可接受的宏用法示例包括断言宏和调试日志宏，
它们会依据构建设置有条件地编译——通常
不会被编译进发布构建。

### `nullptr` 与 `NULL`

可能时，优先使用 [`nullptr`](https://en.cppreference.com/c/language/nullptr)
而非 `NULL`。

`nullptr` 通常是任意指针类型首选的空指针常量，
但 Objective-C 对象指针和 Objective-C 类指针除外。
当不支持 C23 时，应使用 `NULL` 代替 `nullptr`。

<a id="Nonstandard_Extensions"></a>

### 非标准扩展

除非另有规定，否则不得使用 C/Objective-C 的
非标准扩展。

编译器支持各种不属于标准 C 的扩展。例如
复合语句表达式（如 `foo = ({ int x; Bar(&x); x })`）。

#### `__typeof__` 关键字

当显式写出类型对读者无益时，允许使用 `__typeof__`
关键字；但更鼓励使用 `__typeof__`，而非其他
类似关键字（例如 `typeof` 关键字），因为
它在所有语言变体中都受支持。

<div class='goodcode'></div>

```objectivec
  __weak __typeof__(self) weakSelf = self;
```

<div class='badcode'></div>

```objectivec
  __typeof__(data) copiedData = [data copy];  // AVOID.
  __weak typeof(self) weakSelf = self;        // AVOID.
```

#### `__auto_type` 关键字与类型推导

使用 `__auto_type` 关键字进行类型推导，仅
允许用于 block 类型和函数指针类型的局部变量。
若该 block 或指针类型已有 typedef，则应避免类型推导。

<div class='goodcode'></div>

```objectivec
__auto_type block = ^(NSString *arg1, int arg2) { ... };
__auto_type functionPointer = &MyFunction;

typedef void(^SignInCallback)(Identity *, NSError *);
SignInCallback signInCallback = ^(Identity *identity, NSError *error) { ... };
```

<div class='badcode'></div>

```objectivec
__auto_type button = [self createButtonForInfo:info];
__auto_type viewController = [[MyCustomViewControllerClass alloc] initWith...];

typedef void(^SignInCallback)(Identity *, NSError *);
__auto_type signInCallback = ^(Identity *identity, NSError *error) { ... };
```

#### 获准使用的非标准扩展

*   `__attribute__` 关键字获准使用，因为它用于
    Apple API 声明中。
*   条件运算符的二元形式 `A ?: B` 获准使用。

<a id="Cocoa_and_Objective-C_Features"></a>

## Cocoa 与 Objective-C 特性

<a id="Identify_Designated_Initializer"></a>

### 标明指定初始化方法

清楚地标明你的指定初始化方法。

对于子类化而言，类清楚地标明其指定初始化
方法十分重要。这使子类能够重写一部分初始化
方法，以初始化子类状态或调用由子类提供的
新指定初始化方法。清楚地标明指定初始化方法
还能让追踪和调试初始化代码更为容易。

最好通过为指定初始化方法添加指定初始化
属性注解来标明它们，例如 `NS_DESIGNATED_INITIALIZER`。
当指定初始化属性不可用时，请在注释中声明
指定初始化方法。除非有令人信服的理由或要求
需要多个指定初始化方法，否则应优先只设一个。

支持从父类继承的初始化方法，可通过
[重写父类的指定初始化方法](#Override_Designated_Initializer)
来实现，以确保所有继承来的初始化方法都
经由子类的指定初始化方法。当有令人信服的
理由或要求不应支持某个继承来的初始化方法时，
可为该初始化方法添加可用性属性注解（如 `NS_UNAVAILABLE`）
以阻止使用；但请注意，仅靠可用性属性并不能完全
防止无效初始化。

<a id="Override_Designated_Initializer"></a>

### 重写指定初始化方法

编写需要新指定初始化方法的子类时，
务必重写父类的所有指定初始化方法。

在一个类上声明指定初始化方法时，请记住：
凡是在父类中被视作指定初始化方法的初始化
方法，都将成为子类的便捷初始化方法，除非
另行声明。若未重写父类的指定初始化方法，
可能因使用父类初始化方法造成无效初始化而
产生缺陷。为避免无效初始化，请确保便捷
初始化方法会调用某个指定初始化方法。

<a id="Overridden_NSObject_Method_Placement"></a>

### 被重写的 NSObject 方法的位置

将 NSObject 被重写的方法放在 `@implementation` 的顶部。

这通常适用于（但不限于）`init...`、`copyWithZone:`
和 `dealloc` 方法。`init...` 方法应归为一组，
包括那些 `init...` 方法（非 `NSObject` 重写），
其后是 `NSObject` 的 `description`、`isEqual:`、`hash` 等方法。

用于创建实例的便捷类工厂方法可以放在
`NSObject` 方法之前。

<a id="Initialization"></a>

### 初始化

不要将实例变量初始化为 `0` 或 `nil`：在 `init` 方法中
这样做是多余的。

新分配对象的所有实例变量都会
[被初始化为](https://developer.apple.com/library/mac/documentation/General/Conceptual/CocoaEncyclopedia/ObjectAllocation/ObjectAllocation.html)
`0`（isa 除外），因此不要把 init 方法弄得杂乱，
去将变量重新初始化为 `0` 或 `nil`。

<a id="Instance_Variables_In_Headers_Should_Be_@protected_or_@private"></a>

### 头文件中的实例变量应为 @protected 或 @private

实例变量通常应在实现文件中声明，或由属性
自动合成。当 ivar 在头文件中声明时，应
标记为 `@protected` 或 `@private`。

<div class='goodcode'></div>

```objectivec
@interface MyClass : NSObject {
 @protected
  id _myInstanceVariable;
}
@end
```

<a id="Avoid_+new"></a>

### 不要使用 +new

不要调用 `NSObject` 的类方法 `new`，也不要在子类中重写。
`+new` 很少使用，且与初始化方法的用法大相径庭。
应改用 `+alloc` 和 `-init` 方法来实例化持有的对象。

<a id="Keep_the_Public_API_Simple"></a>

### 保持公开 API 简洁

保持类的简洁；避免「大杂烩」式的 API。
如果某个方法不需要公开，就不要放入公开接口。

与 C++ 不同，Objective-C 不区分公开方法和
私有方法；任何消息都可以发送给对象。因此，
除非确实预期会被类的使用者调用，否则不要把
方法放进公开 API。这有助于降低它们在你
意料之外被调用的可能性。这也包括那些
从父类重写而来的方法。

由于内部方法并非真正私有，很容易在无意中
重写父类的「私有」方法，从而产生极难排查的
缺陷。一般而言，私有方法应使用相当独特的
名称，以防子类无意中重写它们。

<a id="#import_and_#include"></a>

### #import 与 #include

对 Objective-C 和 Objective-C++ 头文件使用 `#import`，对 C/C++ 头文件使用 `#include`。

C/C++ 头文件用 `#include` 包含其他头文件；用 `#import`
包含 C/C++ 头文件会阻碍日后以 `#include` 方式
再包含，并可能导致意外的编译行为。

C/C++ 头文件应提供自己的 `#define` 头文件保护。

<a id="Order_of_Includes"></a>

### 包含顺序

头文件的标准包含顺序为：相关头文件、操作系统
头文件、语言库头文件，最后是其他依赖项的
头文件组。

相关头文件置于最前，以确保它没有隐藏的
依赖。对实现文件而言，相关头文件就是其头文件；
对测试文件而言，则是包含被测接口的头文件。

每个非空的包含组之间用一个空行分隔。
同一组内的包含应按字母顺序排列。

使用相对于项目源码目录的路径来导入头文件。

<div class='goodcode'></div>

```objectivec
// The related header.
#import "ProjectX/BazViewController.h"

// Operating system headers.
#import <Foundation/Foundation.h>

// Language library headers.
#include <unistd.h>
#include <vector>

// Groups of headers for other dependencies.
#include "base/basictypes.h"
#include "base/integral_types.h"
#import "base/mac/FOOComplexNumberSupport.h"
#include "util/math/mathutil.h"

#import "ProjectX/BazModel.h"
#import "Shared/Util/Foo.h"
```

<a id="Use_Umbrella_Headers_for_System_Frameworks"></a>

### 对系统框架使用伞形头文件

对系统框架和系统库，应导入伞形头文件，
而不是包含单个文件。

虽然从 Cocoa 或 Foundation 之类的框架中
包含单个系统头文件看起来很诱人，但实际上
包含顶层根框架能让编译器的工作量更小。
根框架通常是预编译的，加载速度也快得多。
此外，对 Objective-C 框架请记得使用 `@import` 或 `#import`，而非 `#include`。

<div class='goodcode'></div>

```objectivec
@import UIKit;     // GOOD.
#import <Foundation/Foundation.h>     // GOOD.
```

<div class='badcode'></div>

```objectivec
#import <Foundation/NSArray.h>        // AVOID.
#import <Foundation/NSString.h>
...
```

### 避免在初始化方法和 `-dealloc` 中向当前对象发送消息

初始化方法和 `-dealloc` 中的代码应尽可能
避免调用实例方法。

父类的初始化先于子类的初始化完成。在所有
类都有机会初始化其实例状态之前，对 self 的
任何方法调用，都可能导致子类在未初始化的
实例状态上进行操作。

`-dealloc` 存在类似问题：方法调用可能使类
在已被释放的状态上进行操作。

一种不太明显的情况是属性访问器。它们和
任何其他选择器一样都能被重写。只要可行，
在初始化方法和 `-dealloc` 中应直接赋值和释放 ivar，而不要依赖访问器。

<div class='goodcode'></div>

```objectivec
- (instancetype)init {
  self = [super init];
  if (self) {
    _bar = 23;  // GOOD.
  }
  return self;
}
```

当心把通用的初始化代码抽取到辅助方法中：

-   方法可能在子类中被重写，可能是有意的，
    也可能因命名冲突而无意发生。
-   编辑辅助方法时，可能不易看出该代码
    是从初始化方法中运行的。

<div class='badcode'></div>

```objectivec
- (instancetype)init {
  self = [super init];
  if (self) {
    self.bar = 23;  // AVOID.
    [self sharedMethod];  // AVOID. Fragile to subclassing or future extension.
  }
  return self;
}
```

<div class='goodcode'></div>

```objectivec
- (void)dealloc {
  [_notifier removeObserver:self];  // GOOD.
}
```

<div class='badcode'></div>

```objectivec
- (void)dealloc {
  [self removeNotifications];  // AVOID.
}
```

在一些常见情形下，类在初始化期间可能需要
使用父类提供的属性和方法。这通常出现在
派生自 UIKit 和 AppKit 基类（以及其他基类）
的类。在决定是否对此规则作出例外时，
请运用你的判断力以及对通行实践的了解。

### 避免冗余的属性访问

代码应避免冗余的属性访问。当某个属性值
预期不会变化且需要被多次使用时，最好将其
赋给一个局部变量。

<div class='goodcode'></div>

```objc
UIView *view = self.view;
UIScrollView *scrollView = self.scrollView;
[scrollView.leadingAnchor constraintEqualToAnchor:view.leadingAnchor].active = YES;
[scrollView.trailingAnchor constraintEqualToAnchor:view.trailingAnchor].active = YES;
```

<div class='badcode'></div>

```objc
[self.scrollView.leadingAnchor constraintEqualToAnchor:self.view.leadingAnchor].active = YES;
[self.scrollView.trailingAnchor constraintEqualToAnchor:self.view.trailingAnchor].active = YES;
```

当需要反复引用链式属性调用时，最好将
重复的表达式捕获到局部变量中：

<div class='badcode'></div>

```objc
foo.bar.baz.field1 = 10;
foo.bar.baz.field2 = @"Hello";
foo.bar.baz.field3 = 2.71828183;
```

<div class='goodcode'></div>

```objc
Baz *baz = foo.bar.baz;
baz.field1 = 10;
baz.field2 = @"Hello";
baz.field3 = 2.71828183;
```

冗余地访问相同的属性会导致多次消息派发
去获取同一个值，并且在 ARC 下需要对所有
返回对象执行持有和释放；编译器无法优化掉
这些额外操作，从而导致执行变慢、二进制体积显著增大。

<a id="Mutables_Copies_Ownership"></a>

### 可变性、拷贝与所有权

对于
[Foundation 及其他同时包含不可变与可变子类的层级结构](https://developer.apple.com/library/archive/documentation/General/Conceptual/CocoaEncyclopedia/ObjectMutability/ObjectMutability.html)
可变子类可以在遵守不可变类契约的前提下，
替换不可变子类。

这类替换最常见的例子是所有权转移，
尤其是返回值。在这些情况下，额外的
拷贝是不必要的，返回可变子类效率更高。
[调用方应将被调用方声明的类型来对待返回值](https://developer.apple.com/library/archive/documentation/General/Conceptual/CocoaEncyclopedia/ObjectMutability/ObjectMutability.html#//apple_ref/doc/uid/TP40010810-CH5-SW67)，
因此返回值此后将被视为不可变的。

<div class='goodcode'></div>

```objectivec
- (NSArray *)listOfThings {
  NSMutableArray *generatedList = [NSMutableArray array];
  for (NSInteger i = 0; i < _someLimit; i++) {
    [generatedList addObject:[self thingForIndex:i]];
  }
  // Copy not necessary, ownership of generatedList is transferred.
  return generatedList;
}
```

只要所有权转移明确，这条规则同样适用于
仅存在可变变体的类。Protos 便是一个常见的例子。

<div class='goodcode'></div>

```objectivec
- (SomeProtoMessage *)someMessageForValue:(BOOL)value {
  SomeProtoMessage *message = [SomeProtoMessage message];
  message.someValue = value;
  return message;
}
```

只要可变参数在方法调用期间不会发生变化，
就无需为了匹配被调用方法的签名而创建
可变类型的本地不可变拷贝。被调用的方法应
将参数视为声明类型，并应当采取
[防御性拷贝](#Defensive_Copies)
（[Apple 称之为「快照」](https://developer.apple.com/library/archive/documentation/General/Conceptual/CocoaEncyclopedia/ObjectMutability/ObjectMutability.html#//apple_ref/doc/uid/TP40010810-CH5-SW68)），
如果打算在调用结束后继续持有这些参数。

<div class='badcode'></div>

```objectivec
NSMutableArray *updatedThings = [NSMutableArray array];
[updatedThings addObject:newThing];
[_otherManager updateWithCurrentThings:[updatedThings copy]];  // AVOID
```

<a id="Defensive_Copies"></a>
<a id="Setters_copy_NSStrings"></a>

### 拷贝可能可变的对象

接收并持有集合或其他带有 [可变变体](https://developer.apple.com/library/archive/documentation/General/Conceptual/CocoaEncyclopedia/ObjectMutability/ObjectMutability.html)
的类型的代码，应当考虑到传入的对象
可能是可变的，因此应当持有不可变或
可变拷贝，而不是原始对象。特别是，
初始化方法和设置器
[应当拷贝而不是持有那些类型带有可变变体的对象](https://developer.apple.com/library/archive/documentation/General/Conceptual/CocoaEncyclopedia/ObjectMutability/ObjectMutability.html#//apple_ref/doc/uid/TP40010810-CH5-SW68)。

合成访问器应当使用 `copy` 关键字，以确保生成的代码
符合这些预期。

NOTE:
[`copy` 属性关键字仅影响合成的 setter，对 getter 没有影响](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ObjectiveC/Chapters/ocProperties.html#//apple_ref/doc/uid/TP30001163-CH17-SW27)。
由于属性关键字对直接访问实例变量没有影响，
自定义访问器必须实现相同的拷贝语义。

<div class='goodcode'></div>

```objectivec
@property(nonatomic, copy) NSString *name;
@property(nonatomic, copy) NSSet<FilterThing *> *filters;

- (instancetype)initWithName:(NSString *)name
                     filters:(NSSet<FilterThing *> *)filters {
  self = [super init];
  if (self) {
    _name = [name copy];
    _filters = [filters copy];
  }
  return self;
}

- (void)setFilters:(NSSet<FilterThing *> *)filters {
  // Ensure that we retain an immutable collection.
  _filters = [filters copy];
}
```

类似地，getter 必须返回与所返回不可变类型的
契约预期相匹配的类型。

<div class='goodcode'></div>

```objectivec

@implementation Foo {
  NSMutableArray<ContentThing *> *_currentContent;
}

- (NSArray<ContentThing *> *)currentContent {
  return [_currentContent copy];
}

```

所有 Objective-C 的 proto 都是可变的，通常应当
拷贝而不是持有，
[除非在明确的所有权转移情况下](#Mutables_Copies_Ownership)。

<div class='goodcode'></div>

```objectivec
- (void)setFooMessage:(FooMessage *)fooMessage {
  // Copy proto to ensure no other retainer can mutate our value.
  _fooMessage = [fooMessage copy];
}

- (FooMessage *)fooMessage {
  // Copy proto to return so that caller cannot mutate our value.
  return [_fooMessage copy];
}
```

异步代码应当在派发之前拷贝可能可变的对象。
被 block 捕获的对象会被持有但不会被拷贝。

<div class='goodcode'></div>

```objectivec
- (void)doSomethingWithThings:(NSArray<Thing *> *)things {
  NSArray<Thing *> *thingsToWorkOn = [things copy];
  dispatch_async(_workQueue, ^{
    for (id<Thing> thing in thingsToWorkOn) {
      ...
    }
  });
}
```

NOTE: 没有必要拷贝那些没有可变变体的对象，例如
`NSURL`、`NSNumber`、`NSDate`、`UIColor` 等。

<a id="Use_Lightweight_Generics_to_Document_Contained_Types"></a>

### 使用轻量级泛型来标注所包含的类型

所有在 Xcode 7 或更新版本上编译的项目都应当使用
Objective-C 轻量级泛型记法来标注所包含对象的类型。

每个 `NSArray`、`NSDictionary` 或 `NSSet` 引用都应当使用轻量级泛型来
声明，以提高类型安全性并显式地记录用法。

<div class='goodcode'></div>

```objectivec
@property(nonatomic, copy) NSArray<Location *> *locations;
@property(nonatomic, copy, readonly) NSSet<NSString *> *identifiers;

NSMutableArray<MyLocation *> *mutableLocations = [otherObject.locations mutableCopy];
```

如果完整标注的类型变得复杂，考虑使用 typedef 来
保持可读性。

<div class='goodcode'></div>

```objectivec
typedef NSSet<NSDictionary<NSString *, NSDate *> *> TimeZoneMappingSet;
TimeZoneMappingSet *timeZoneMappings = [TimeZoneMappingSet setWithObjects:...];
```

使用可用的、最具描述性的公共父类或协议。在
最通用的情况下，当没有其他已知信息时，
使用 id 将集合显式地声明为异构的。

<div class='goodcode'></div>

```objectivec
@property(nonatomic, copy) NSArray<id> *unknowns;
```

<a id="Avoid_Throwing_Exceptions"></a>

### 避免抛出异常

不要 `@throw` Objective-C 异常，但你应该准备好从第三方或
系统调用中捕获它们。

这遵循了在 [Apple 的 Cocoa 异常编程主题简介](https://developer.apple.com/library/mac/documentation/Cocoa/Conceptual/Exceptions/Exceptions.html) 中使用
错误对象来传递错误的建议。

我们确实会使用 `-fobjc-exceptions` 编译（主要为了获得 `@synchronized`），但
我们不会 `@throw`。在需要正确使用第三方代码或库时，
允许使用 `@try`、`@catch` 和 `@finally`。如果你确实使用了它们，
请准确记录你预期哪些方法会抛出异常。

<a id="nil_Checks"></a>

### `nil` 检查

避免仅为了防止向 `nil` 发送消息而存在的 `nil` 指针检查。
向 `nil` 发送消息
[可靠地返回](http://www.sealiesoftware.com/blog/archive/2012/2/29/objc_explain_return_value_of_message_to_nil.html)
指针类型的 `nil`、整数或浮点类型的 `0`、初始化为 `0` 的结构体，以及
等于 `{0, 0}` 的 `_Complex` 值。

<div class='badcode'></div>

```objectivec
if (dataSource) {  // AVOID.
  [dataSource moveItemAtIndex:1 toIndex:0];
}
```

<div class='goodcode'></div>

```objectivec
[dataSource moveItemAtIndex:1 toIndex:0];  // GOOD.
```

注意，这适用于作为消息目标的 `nil`，而不是作为参数值的 `nil`。
个别方法可能会也可能不会安全地处理 `nil` 参数值。

还要注意，这与将 C/C++ 指针和 block 指针对照 `nullptr`
进行检查不同，运行时不会处理这种情况，并会
导致你的应用崩溃。你仍然需要确保不对其
解引用 `nullptr`。

### 可空性

接口可以用可空性注解来修饰，以描述接口应当如何
使用以及它的行为。使用可空性区域（例如
`NS_ASSUME_NONNULL_BEGIN` 和 `NS_ASSUME_NONNULL_END`）和显式的可空性
注解都是被接受的。优先使用 `_Nullable` 和 `_Nonnull`
关键字，而不是 `__nullable` 和 `__nonnull` 关键字。对于 Objective-C 方法和属性，
优先使用上下文敏感、不带下划线的关键字，
例如 `nonnull` 和 `nullable`。

<div class='goodcode'></div>

```objectivec
/** A class representing an owned book. */
@interface GTMBook : NSObject

/** The title of the book. */
@property(nonatomic, readonly, copy, nonnull) NSString *title;

/** The author of the book, if one exists. */
@property(nonatomic, readonly, copy, nullable) NSString *author;

/** The owner of the book. Setting nil resets to the default owner. */
@property(nonatomic, copy, null_resettable) NSString *owner;

/** Initializes a book with a title and an optional author. */
- (nonnull instancetype)initWithTitle:(nonnull NSString *)title
                               author:(nullable NSString *)author
    NS_DESIGNATED_INITIALIZER;

/** Returns nil because a book is expected to have a title. */
- (nullable instancetype)init;

@end

/** Loads books from the file specified by the given path. */
NSArray<GTMBook *> *_Nullable GTMLoadBooksFromFile(NSString *_Nonnull path);
```

<div class='badcode'></div>

```objectivec
NSArray<GTMBook *> *__nullable GTMLoadBooksFromTitle(NSString *__nonnull path);
```

不要因为某个 nonnull 限定符就假定指针不为空，因为
编译器只检查这类情况的一个子集，并不能
保证指针不为空。避免故意违反函数、方法
和属性声明的可空性语义。

<a id="BOOL_Pitfalls"></a>

### BOOL 陷阱

<a id="BOOL_Expressions_Conversions"></a>

#### BOOL 表达式与转换

将一般的整数值转换为 `BOOL` 时要小心。避免直接
与 `YES` 比较，或用比较运算符比较
多个 `BOOL` 值。

`BOOL` 在某些 Apple 平台（尤其是 Intel macOS、watchOS 和 32 位 iOS）上
被定义为有符号的 `char`，因此它可能具有 `YES`（`1`）和
`NO`（`0`）之外的值。不要将一般的整数值直接强制转换或转换为 `BOOL`。

常见的错误包括将数组的大小、指针值或位逻辑运算的
结果强制转换或转换为 `BOOL`。这些操作可能
依赖于整数值最后一个字节的值，从而导致
意外的 `NO` 值。对 NS_OPTIONS 值进行运算和
标志位掩码操作是特别常见的错误。

将一般整数值转换为 `BOOL` 时，使用条件运算符
返回 `YES` 或 `NO` 值。

你可以安全地互换和转换 `BOOL`、`_Bool` 和 `bool`（参见 C++ 标准
4.7.4、4.12 和 C99 标准 6.3.1.2）。在 Objective-C 方法签名中使用 `BOOL`。

对 `BOOL` 使用逻辑运算符（`&&`、`||` 和 `!`）同样是有效的，并且
会返回可以安全转换为 `BOOL` 的值，而无需
使用条件运算符。

<div class='badcode'></div>

```objectivec
- (BOOL)isBold {
  return [self fontTraits] & NSFontBoldTrait;  // AVOID.
}
- (BOOL)isValid {
  return [self stringValue];  // AVOID.
}
- (BOOL)isLongEnough {
  return (BOOL)([self stringValue].count);  // AVOID.
}
```

<div class='goodcode'></div>

```objectivec
- (BOOL)isBold {
  return ([self fontTraits] & NSFontBoldTrait) ? YES : NO;
}
- (BOOL)isValid {
  return [self stringValue] != nil;
}
- (BOOL)isLongEnough {
  return [self stringValue].count > 0;
}
- (BOOL)isEnabled {
  return [self isValid] && [self isBold];
}
```

不要将 `BOOL` 变量直接与 `YES` 比较。这不仅对精通 C 语言的
人更难阅读，而且上面第一点也说明返回值
可能并不总是你预期的那样。

<div class='badcode'></div>

```objectivec
BOOL great = [foo isGreat];
if (great == YES) {  // AVOID.
  // ...be great!
}
```

<div class='goodcode'></div>

```objectivec
BOOL great = [foo isGreat];
if (great) {         // GOOD.
  // ...be great!
}
```

不要使用比较运算符直接比较 `BOOL` 值。为 true 的
`BOOL` 值可能并不相等。使用逻辑运算符代替
`BOOL` 值的按位比较。

<div class='badcode'></div>

```objectivec
if (oldBoolValue != newBoolValue) {  // AVOID.
  // ... code that should only run when the value changes.
}
```

<div class='goodcode'></div>

```objectivec
if ((!oldBoolValue && newBoolValue) || (oldBoolValue && !newBoolValue)) {  // GOOD.
  // ... code that should only run when the value changes.
}

// GOOD, the results of logical operators on BOOLs are safe to compare.
if (!oldBoolValue != !newBoolValue) {
  // ... code that should only run when the value changes.
}
```

#### BOOL 字面量

此处 [BOOL NSNumber 字面量](https://clang.llvm.org/docs/ObjectiveCLiterals.html#nsnumber-literals) 是
`@YES` 和 `@NO`，它们等价于
`[NSNumber numberWithBool:...]`。

避免使用
[装箱表达式](https://clang.llvm.org/docs/ObjectiveCLiterals.html#boxed-expressions)
来创建 BOOL 值，包括像 `@(YES)` 这样的简单表达式。装箱表达式存在
[与其他 BOOL 表达式相同的陷阱](#BOOL_Expressions_Conversions)，因为对一般整数值
装箱可能产生 true 或 false 的
`NSNumbers`，它们
不等于 `@YES` 和 `@NO`。

将一般整数值转换为 BOOL 字面量时，使用条件运算符
转换为 `@YES` 或 `@NO`。不要在装箱表达式内部
嵌入条件运算符，因为即便运算结果是 BOOL，
这也等同于对一般整数值进行装箱。

<div class='badcode'></div>

```objectivec
[_boolArray addValue:@(YES)];  // AVOID boxing even in simple cases.
NSNumber *isBold = @(self.fontTraits & NSFontBoldTrait);  // AVOID.
NSNumber *hasContent = @([self stringValue].length);  // AVOID.
NSNumber *isValid = @([self stringValue]);  // AVOID.
NSNumber *isStringNotNil = @([self stringValue] ? YES : NO);  // AVOID.
```

<div class='goodcode'></div>

```objectivec
[_boolArray addValue:@YES];  // GOOD.
NSNumber *isBold = self.fontTraits & NSFontBoldTrait ? @YES : @NO;  // GOOD.
NSNumber *hasContent = [self stringValue].length ? @YES : @NO;  // GOOD.
NSNumber *isValid = [self stringValue] ? @YES : @NO;  // GOOD.
NSNumber *isStringNotNil = [self stringValue] ? @YES : @NO;  // GOOD.
```

<a id="Interfaces_Without_Instance_Variables"></a>
<a id="interfaces-without-instance-variables"></a>

### 不包含实例变量的容器

对于没有任何实例变量声明的接口、类扩展和实现，
省略空的括号对。

<div class='goodcode'></div>

```objectivec
@interface MyClass : NSObject
// Does a lot of stuff.
- (void)fooBarBam;
@end

@interface MyClass ()
- (void)classExtensionMethod;
@end

@implementation MyClass
// Actual implementation.
@end
```

<div class='badcode'></div>

```objectivec
@interface MyClass : NSObject {
}
// Does a lot of stuff.
- (void)fooBarBam;
@end

@interface MyClass () {
}
- (void)classExtensionMethod;
@end

@implementation MyClass {
}
// Actual implementation.
@end
```

<a id="Cocoa_Patterns"></a>

## Cocoa 模式

<a id="Delegate_Pattern"></a>

### 委托模式

当保留委托、目标对象和 block 指针会导致保留循环时，
不应保留它们。

为了避免造成保留循环，一旦明确不再需要向该对象
发送消息，就应当释放委托或目标指针。

如果没有明确的时间点表明不再需要委托或目标指针，
则该指针只应以弱引用的方式保留。

block 指针无法以弱引用方式保留。为了避免在客户端代码中
造成保留循环，block 指针只应在能够被显式释放的场景中
用于回调——即在被调用后或不再需要时释放。否则，
回调应当通过弱引用的委托或
目标指针来完成。

<a id="Objective-C++"></a>

## Objective-C++

<a id="Style_Matches_the_Language"></a>

### 风格与语言相匹配

在 Objective-C++ 源文件中，遵循你正在实现的函数或方法
所属语言的风格。为了尽量减少混合 Cocoa/Objective-C
与 C++ 时不同命名风格之间的冲突，请
遵循所实现方法的风格。

对于 `@implementation` 块中的代码，使用 Objective-C 命名规则。
对于 C++ 类方法中的代码，使用 C++ 命名规则。

对于 Objective-C++ 文件中位于类实现之外的代码，
应在文件内保持一致。

<div class='goodcode'></div>

```objectivec++
// file: cross_platform_header.h

class CrossPlatformAPI {
 public:
  ...
  int DoSomethingPlatformSpecific();  // impl on each platform
 private:
  int an_instance_var_;
};

// file: mac_implementation.mm
#include "cross_platform_header.h"

/** A typical Objective-C class, using Objective-C naming. */
@interface MyDelegate : NSObject {
 @private
  int _instanceVar;
  CrossPlatformAPI* _backEndObject;
}

- (void)respondToSomething:(id)something;

@end

@implementation MyDelegate

- (void)respondToSomething:(id)something {
  // bridge from Cocoa through our C++ backend
  _instanceVar = _backEndObject->DoSomethingPlatformSpecific();
  NSString* tempString = [NSString stringWithFormat:@"%d", _instanceVar];
  NSLog(@"%@", tempString);
}

@end

/** The platform-specific implementation of the C++ class, using C++ naming. */
int CrossPlatformAPI::DoSomethingPlatformSpecific() {
  NSString* temp_string = [NSString stringWithFormat:@"%d", an_instance_var_];
  NSLog(@"%@", temp_string);
  return [temp_string intValue];
}
```

项目可以选择使用 80 列的行长度限制，以与
Google 的 C++ 风格指南保持一致。

<a id="Spacing_and_Formatting"></a>

## 空格与格式化

<a id="Spaces_vs._Tabs"></a>

### 空格与制表符

只使用空格，每次缩进 2 个空格。我们使用空格进行缩进。
不要在代码中使用制表符。

你应该将编辑器设置为在按下 tab 键时输出空格，
并去除行尾的空格。

<a id="Line_Length"></a>

### 行长度

Objective-C 文件的最大行长度为 100 列。

<a id="Method_Declarations_and_Definitions"></a>

### 方法声明与定义

在 `-` 或 `+` 与返回类型之间应当使用一个空格。一般来说，
参数列表中除参数之间外不应有空格。

方法应当如下所示：

<div class='goodcode'></div>

```objectivec
- (void)doSomethingWithString:(NSString *)theString {
  ...
}
```

星号前的空格是可选的。添加新代码时，
应与周围文件的风格保持一致。

如果方法声明无法放在单行内，则将每个参数放在单独的一行。
除第一行外的所有行应当至少缩进四个空格。
参数前的冒号在所有行上应当对齐。如果方法声明
第一行中参数前的冒号位置使得冒号对齐会导致
后续行的缩进小于四个空格，那么冒号对齐只对
所有行（除第一行外）有要求。如果在方法声明
或定义中 `:` 后声明的参数会导致超出行长度限制，
则将该内容换行到下一行，并
至少缩进四个空格。

<div class='goodcode'></div>

```objectivec
- (void)doSomethingWithFoo:(GTMFoo *)theFoo
                      rect:(NSRect)theRect
                  interval:(float)theInterval {
  ...
}

- (void)shortKeyword:(GTMFoo *)theFoo
            longerKeyword:(NSRect)theRect
    someEvenLongerKeyword:(float)theInterval
                    error:(NSError **)theError {
  ...
}

- (id<UIAdaptivePresentationControllerDelegate>)
    adaptivePresentationControllerDelegateForViewController:(UIViewController *)viewController;

- (void)presentWithAdaptivePresentationControllerDelegate:
    (id<UIAdaptivePresentationControllerDelegate>)delegate;

- (void)updateContentHeaderViewForExpansionToContentOffset:(CGPoint)contentOffset
                                            withController:
                                                (GTMCollectionExpansionController *)controller;

```

### 函数声明与定义

优先将返回类型与函数名放在同一行，如果所有参数能放下，则
将它们追加在同一行。对于无法放在单行的参数列表，
按照在 [函数调用](#Function_Calls) 中换行参数的方式
进行处理。

<div class='goodcode'></div>

```objectivec
NSString *GTMVersionString(int majorVersion, int minorVersion) {
  ...
}

void GTMSerializeDictionaryToFileOnDispatchQueue(
    NSDictionary<NSString *, NSString *> *dictionary,
    NSString *filename,
    dispatch_queue_t queue) {
  ...
}
```

函数声明与定义还应当满足以下
条件：

*   左圆括号必须始终与函数名在
    同一行。
*   如果无法将返回类型和函数名放在同一行，
    则在它们之间换行，并且不要缩进函数名。
*   左圆括号前永远不应有空格。
*   函数圆括号与参数之间永远不应有空格。
*   左花括号始终位于函数声明最后一行的末尾，
    而不是下一行的开头。
*   右花括号要么单独位于最后一行，
    要么与左花括号在同一行。
*   右圆括号与左花括号之间应当有
    一个空格。
*   尽可能将所有参数对齐。
*   函数作用域应当缩进 2 个空格。
*   换行的参数应当缩进 4 个空格。

<a id="Conditionals"></a>

### 条件语句

在 `if`、`while`、`for` 和 `switch` 之后，以及比较
运算符两侧都包含空格。

<div class='goodcode'></div>

```objectivec
for (int i = 0; i < 5; ++i) {
}

while (test) {}
```

当循环体或条件语句能放在单行内时，
可以省略花括号。

<div class='goodcode'></div>

```objectivec
if (hasSillyName) LaughOutLoud();

for (int i = 0; i < 10; i++) {
  BlowTheHorn();
}
```

<div class='badcode'></div>

```objectivec
if (hasSillyName)
  LaughOutLoud();               // AVOID.

for (int i = 0; i < 10; i++)
  BlowTheHorn();                // AVOID.
```

如果 `if` 子句带有 `else` 子句，则两个子句都应当使用花括号。

<div class='goodcode'></div>

```objectivec
if (hasBaz) {
  foo();
} else {  // The else goes on the same line as the closing brace.
  bar();
}
```

<div class='badcode'></div>

```objectivec
if (hasBaz) foo();
else bar();        // AVOID.

if (hasBaz) {
  foo();
} else bar();      // AVOID.
```

故意 fall-through 到下一个 case 应当用注释加以说明，
除非该 case 在下一个 case 之前没有介入的代码。

<div class='goodcode'></div>

```objectivec
switch (i) {
  case 1:
    ...
    break;
  case 2:
    j++;
    // Falls through.
  case 3: {
    int k;
    ...
    break;
  }
  case 4:
  case 5:
  case 6: break;
}
```

<a id="Expressions"></a>

### 表达式

在二元运算符和赋值运算符两侧使用空格。一元
运算符省略空格。不要在圆括号内部添加空格。

<div class='goodcode'></div>

```objectivec
x = 0;
v = w * x + y / z;
v = -y * (x + z);
```

表达式中的因子可以省略空格。

<div class='goodcode'></div>

```objectivec
v = w*x + y/z;
```

<a id="Method_Invocations"></a>

### 方法调用

方法调用的格式应当与方法声明非常相似。

在存在多种格式化风格选择时，遵循给定源文件中已有的约定。
调用应当将所有参数放在一行：

<div class='goodcode'></div>

```objectivec
[myObject doFooWith:arg1 name:arg2 error:arg3];
```

或者每行一个参数，冒号对齐：

<div class='goodcode'></div>

```objectivec
[myObject doFooWith:arg1
               name:arg2
              error:arg3];
```

不要使用以下任何一种风格：

<div class='badcode'></div>

```objectivec
[myObject doFooWith:arg1 name:arg2  // some lines with >1 arg
              error:arg3];

[myObject doFooWith:arg1
               name:arg2 error:arg3];

[myObject doFooWith:arg1
          name:arg2  // aligning keywords instead of colons
          error:arg3];
```

与声明和定义一样，当第一个关键字比其他的短时，
将后续行至少缩进四个空格，并保持
冒号对齐：

<div class='goodcode'></div>

```objectivec
[myObj short:arg1
          longKeyword:arg2
    evenLongerKeyword:arg3
                error:arg4];
```

包含多个内联 block 的调用，其参数名可以在
四空格缩进处左对齐。

<a id="Function_Calls"></a>

### 函数调用

函数调用应当尽可能在每个行内包含能放下的多个参数，
除非为了参数的清晰性或文档说明需要更短的行。

函数参数的续行可以缩进到与左圆括号对齐，
也可以采用四空格缩进。

<div class='goodcode'></div>

```objectivec
CFArrayRef array = CFArrayCreate(kCFAllocatorDefault, objects, numberOfObjects,
                                 &kCFTypeArrayCallBacks);

NSString *string = NSLocalizedStringWithDefaultValue(@"FEET", @"DistanceTable",
    resourceBundle, @"%@ feet", @"Distance for multiple feet");

UpdateTally(scores[x] * y + bases[x],  // Score heuristic.
            x, y, z);

TransformImage(image,
               x1, x2, x3,
               y1, y2, y3,
               z1, z2, z3);
```

使用具有描述性名称的局部变量来缩短函数调用并
减少调用的嵌套。

<div class='goodcode'></div>

```objectivec
double scoreHeuristic = scores[x] * y + bases[x];
UpdateTally(scoreHeuristic, x, y, z);
```

<a id="Exceptions"></a>

### 异常

将 `@catch` 和 `@finally` 标签与前面的 `}` 放在同一行来
格式化异常。在 `@` 标签与左花括号（`{`）之间，以及
`@catch` 与被捕获对象声明之间，各添加一个空格。
如果你必须使用 Objective-C 异常，请按如下方式
格式化。不过，关于你不应使用异常的原因，请参见
[避免抛出异常](#Avoid_Throwing_Exceptions)。

<div class='goodcode'></div>

```objectivec
@try {
  foo();
} @catch (NSException *ex) {
  bar(ex);
} @finally {
  baz();
}
```

<a id="Function_Length"></a>

### 函数长度

优先使用小而专注的函数。

长的函数和方法偶尔也是合适的，因此不对函数长度设置硬性限制。
如果函数超过约 40 行，请考虑是否可以在不损害
程序结构的情况下将其拆分。

即使你的长函数现在运行得很好，几个月后修改它的
人可能会添加新行为。这可能导致难以发现的
bug。保持函数短小简洁，可以让其他人更容易
阅读和修改你的代码。

在更新遗留代码时，也请考虑将长函数拆分成
更小、更易管理的片段。

<a id="Vertical_Whitespace"></a>

### 垂直空白

谨慎使用垂直空白。

为了让更多代码能方便地在屏幕上查看，避免在
函数花括号内部直接放置空行。

在函数之间以及代码的逻辑分组之间，
将空行限制在一到两行。

<a id="Objective-C_Style_Exceptions"></a>

## Objective-C 风格例外

<a id="Indicating_style_exceptions"></a>

### 标明风格例外

不打算遵守这些风格建议的代码行，需要在行末加上
`// NOLINT` 或在上一行行末加上 `// NOLINTNEXTLINE`。有时，
Objective-C 代码的某些部分必须忽略这些风格建议
（例如代码可能是机器生成的，或者代码结构使得
无法正确地进行风格化）。

该行上的 `// NOLINT` 注释或上一行上的 `// NOLINTNEXTLINE` 可以用来向读者
表明，代码是有意忽略风格指南的。此外，
这些注解也可以被 linters 等自动化工具识别，
并正确处理代码。注意，`//` 与 `NOLINT*` 之间
只有一个空格。
