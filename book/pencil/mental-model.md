---
description: >-
  理解 pen.dev 作为结构探索、视觉沟通、设计系统与 Design ↔ Code 中间层的价值。
icon: pen-ruler
layout:
  width: wide
  tableOfContents:
    visible: true
  pagination:
    visible: true
---

# pen.dev 的正确心智模型

pen.dev 不是“自动变漂亮按钮”。它在 Agent Coding 工作流中承担四个角色。

## 1. 结构探索工具

在写代码前快速比较：页面结构、Hero、导航、信息层级和用户流程。

## 2. 可视化沟通层

选中画布元素后，让 Agent 在明确上下文中修改；比反复用自然语言描述坐标更可靠。

## 3. 设计系统载体

通过 Variables、Components、Instances、Slots 和 Design Libraries 管理一致性。

## 4. 设计与代码的中间层

`.pen` 文件与代码位于同一工作区，Agent 可以读取两侧上下文并持续同步。

```text
需求
  ↓
灰度结构
  ↓
视觉方向
  ↓
组件与状态
  ↓
响应式和无障碍
  ↓
生成代码
  ↓
截图对比
```

{% hint style="info" %}
你的价值不在于比 Agent 更快地画按钮，而在于决定应该画什么、为什么这样画、是否满足用户任务，以及什么时候已经达到可交付标准。
{% endhint %}
