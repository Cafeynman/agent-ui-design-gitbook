---
description: >-
  区分 UX、UI、Web Design、Frontend Engineering 与 Product Design，避免在给 Agent 下指令时混淆。
icon: diagram-project
layout:
  width: default
  tableOfContents:
    visible: true
  pagination:
    visible: true
---

# UX、UI、Web Design 与 Frontend 的区别

| 领域 | 关注点 | 典型问题 |
|---|---|---|
| UX（用户体验） | 用户能否顺利完成目标 | 流程是否清楚？错误能否恢复？ |
| UI（用户界面） | 界面的视觉与交互表现 | 层级、控件、状态是否明确？ |
| Web Design | 网页的信息、视觉与交互组织 | 页面如何表达品牌与内容？ |
| Product Design | 从问题、流程到界面的一体化设计 | 做什么、为谁做、如何验证？ |
| Frontend Engineering | 把界面可靠实现为软件 | 组件、状态、性能、可维护性 |

{% hint style="info" %}
在 Agent Coding 场景中，你不必承担 Frontend Engineering 的所有细节，但必须能定义 Product/UX/UI 约束，并检查实现是否满足这些约束。
{% endhint %}

## 为什么“功能实现了”不等于“体验完成了”

一个注册表单即使能提交，也可能存在：

- Label 不清楚；
- 错误只用红框表达；
- 键盘无法看见 Focus；
- 提交中没有 Loading；
- 失败后清空用户输入；
- 手机端按钮难以点击。

这些并非“美化”，而是产品是否可用的一部分。
