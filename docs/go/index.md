# Go 风格

https://google.github.io/styleguide/go

[概览](index) | [指南](guide) | [决策](decisions) |
[最佳实践](best-practices)

<!--

-->

{% raw %}

<a id="about"></a>

## 关于

Go 风格指南及其配套文档，把当前编写可读、惯用的 Go 代码的
最佳方法整理成文。对风格指南的遵循并非意在成为绝对准则，
这些文档也永远不会穷尽一切。我们的目标是尽量减少编写可读
Go 代码时的猜测，让刚接触这门语言的新手能够避开常见错误。
风格指南还用于统一在 Google 评审 Go 代码时，任何人所给出的
风格指导，使各方口径一致。

文档                | 链接                                                  | 主要读者            | [Normative] | [Canonical]
------------------- | ----------------------------------------------------- | ------------------- | ----------- | -----------
**风格指南**     | https://google.github.io/styleguide/go/guide          | 所有人              | 是         | 是
**风格决策** | https://google.github.io/styleguide/go/decisions      | 可读性导师          | 是         | 否
**最佳实践**  | https://google.github.io/styleguide/go/best-practices | 任何感兴趣的人      | 否          | 否

[Normative]: #normative
[Canonical]: #canonical

<a id="docs"></a>

### 文档

1.  **[风格指南](https://google.github.io/styleguide/go/guide)** 概述了
    Google 内部 Go 风格的基础。本文档是权威依据，同时充当
    风格决策与最佳实践两份文档里各项建议的基础，
    后两者的建议都由此衍生。

1.  **[风格决策](https://google.github.io/styleguide/go/decisions)** 是一份
    更为详尽的文档，汇总了针对具体风格要点的决策，并在适当之处
    讨论了这些决策背后的理由。

    这些决策可能随新数据、新的语言特性、新的库或新出现的
    模式而调整，但并不要求 Google 的每位 Go 程序员都与
    本文档保持同步；也就是说，无需时时跟进本文档的
    最新修订。

1.  **[最佳实践](https://google.github.io/styleguide/go/best-practices)**
    记录了一些历经时间演进而形成的模式：它们能解决常见问题、
    读起来顺畅，并且足以应对代码维护的需要。

    这些最佳实践并不具有权威性，但仍鼓励 Google 的 Go 程序员
    在可能的情况下加以采用，以使代码库保持统一、
    前后一致。

这些文档旨在：

*   就权衡不同风格时所依据的一组原则达成共识
*   把 Go 风格中已有定论的事项整理成文
*   记录 Go 惯用写法，并给出权威的示例
*   记录各种风格决策的利与弊
*   帮助减少 Go 可读性评审中的意外情况
*   帮助可读性导师使用一致的术语与指导口径

这些文档**不**旨在：

*   穷举可读性评审中可能给出的所有意见
*   列出要求每个人时刻牢记、随时遵守的全部规则，
    无一遗漏
*   取代在运用语言特性与风格时的良好判断力
*   为消除风格差异而进行大规模改动提供理由

不同 Go 程序员之间、不同团队的代码库之间，差异
总会存在。不过，让代码库尽可能保持一致，才最
符合 Google 与 Alphabet 的利益。（关于一致性的
更多说明，参见[指南](guide#consistency)。）为此，
尽可按自己的判断去做风格改进，但也不必对发现的
每一处违反风格指南之处都吹毛求疵。尤其是，这些
文档会随时间演进，而这并不构成在既有代码库里
额外折腾的理由；只需用最新的最佳实践编写新代码，
再随时间顺手处理邻近的问题，便已足够。

重要的是要认识到，风格问题本质上是个人化的，也始终
存在固有的权衡。这些文档里的许多指导带有主观性，但
正如 `gofmt` 一样，它们所带来的一致性有很大价值。
因此，未经充分讨论不会改动风格建议；也鼓励 Google 的
Go 程序员遵循风格指南，即便在某些地方他们可能并
不认同。

<a id="definitions"></a>

## 定义

风格文档中通篇使用的下列词语，其含义
界定如下：

*   **Canonical**：确立具规定性且长期有效的规则
    <a id="canonical"></a>

    在这些文档中，“canonical” 用来描述这样一种事物：它
    被视为所有代码（无论新旧）都应当遵循的标准，而且
    预计不会随时间发生大幅变化。权威文档里的原则，
    作者与评审者双方都应理解，所以凡收进权威文档的
    内容，都必须达到很高的门槛。也正因为如此，
    权威文档通常更短，所规定的风格要素也比
    非权威文档更少。

    https://google.github.io/styleguide/go#canonical

*   **Normative**：旨在建立一致性 <a id="normative"></a>

    在这些文档中，“normative” 用来描述一种经各方约定
    一致的风格要素，供 Go 代码评审者使用，目的是让
    建议、术语以及理由说明保持一致。这些要素可能
    随时间变化，文档也会反映此类改动，以便评审者
    始终保持口径一致、跟上最新情况。并不要求 Go
    代码的作者熟悉规范性文档，但评审者在可读性
    评审中会频繁把它们用作参考。

    https://google.github.io/styleguide/go#normative

*   **Idiomatic**：常见且为人熟知 <a id="idiomatic"></a>

    在这些文档中，“idiomatic” 用来指在 Go 代码中普遍
    存在、并已成为易于辨认的熟悉模式的写法。一般
    来说，若惯用模式与不惯用的写法在语境中服务于
    相同目的，应优先选用惯用模式，因为这正是读者
    最为熟悉的写法。

    https://google.github.io/styleguide/go#idiomatic

<a id="references"></a>

## 补充参考资料

本指南假定读者已熟悉 [Effective Go]，因为它为整个 Go 社区的
Go 代码提供了共同基线。

以下列出一些补充资料，供想自学 Go 风格的人，
以及想在评审里补充可链接背景资料的评审者参考。
参与 Go 可读性流程的人不必熟悉这些资料，
不过它们仍可能作为背景资料，出现在可读性
评审当中。

[Effective Go]: https://go.dev/doc/effective_go

**外部参考资料**

*   [Go 语言规范](https://go.dev/ref/spec)
*   [Go FAQ](https://go.dev/doc/faq)
*   [Go 内存模型](https://go.dev/ref/mem)
*   [Go 数据结构](https://research.swtch.com/godata)
*   [Go 接口](https://research.swtch.com/interfaces)
*   [Go 谚语](https://go-proverbs.github.io/)

*   <a id="gotip"></a> Go Tip 系列节目 - 敬请期待。

*   <a id="unit-testing-practices"></a> 单元测试实践 - 敬请期待。

**相关的 Testing-on-the-Toilet 文章**

*   [TotT：标识符命名][tott-431]
*   [TotT：测试状态与测试交互][tott-281]
*   [TotT：有效测试][tott-324]
*   [TotT：风险驱动测试][tott-329]
*   [TotT：变更探测器测试之害][tott-350]

[tott-431]: https://testing.googleblog.com/2017/10/code-health-identifiernamingpostforworl.html
[tott-281]: https://testing.googleblog.com/2013/03/testing-on-toilet-testing-state-vs.html
[tott-324]: https://testing.googleblog.com/2014/05/testing-on-toilet-effective-testing.html
[tott-329]: https://testing.googleblog.com/2014/05/testing-on-toilet-risk-driven-testing.html
[tott-350]: https://testing.googleblog.com/2015/01/testing-on-toilet-change-detector-tests.html

**其他外部文章**

*   [Go 与教条](https://research.swtch.com/dogma)
*   [少即是指数级的多](https://commandcenter.blogspot.com/2012/06/less-is-exponentially-more.html)
*   [Esmerelda 的想象力](https://commandcenter.blogspot.com/2011/12/esmereldas-imagination.html)
*   [用于解析的正则表达式](https://commandcenter.blogspot.com/2011/08/regular-expressions-in-lexing-and.html)
*   [Gofmt 的风格不是谁的最爱，却是所有人的最爱](https://www.youtube.com/watch?v=PAAkCSZUG1c&t=8m43s)
    (YouTube)

<!--

-->

{% endraw %}
