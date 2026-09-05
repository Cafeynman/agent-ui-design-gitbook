---
description: >-
  掌握 Frame、Layer、Component、Instance、Variable、Theme、Slot、Design Library、MCP 与 .pen 文件。
icon: shapes
layout:
  width: default
  tableOfContents:
    visible: true
  pagination:
    visible: true
---

# pen.dev 核心概念

| 概念 | 白话解释 | 学习要求 |
|---|---|---|
| Infinite Canvas | 可同时摆放多个页面和方向的无限画布 | 会移动、缩放与比较 |
| Frame | 页面、屏幕或区域的容器 | 会组织 Desktop/Mobile |
| Layer | 元素层级 | 能看懂结构和命名 |
| Component | 可复用源组件 | 理解“改一次，多处更新” |
| Instance | 组件的使用副本 | 能分辨来源和局部覆盖 |
| Variable | 统一的颜色、字体、间距等值 | 要求 Agent 避免散落硬编码 |
| Theme | 同一变量在不同模式的值 | 理解 Light / Dark |
| Slot | 组件中允许替换内容的区域 | 理解灵活但受约束的复用 |
| Design Library | 跨 `.pen` 文件复用组件 | 后期学习 |
| MCP | Agent 操作画布的工具接口 | 确认连接即可 |
| `.pen` | 与代码一起版本管理的设计文件 | 主动保存和提交 |

## 第一次结构审计 Prompt

```text
请读取当前设计，不要修改。

用非技术语言告诉我：
1. 有哪些主要 Frame；
2. 每个 Frame 中有哪些层级；
3. 哪些元素适合成为 Component；
4. 是否存在无意义嵌套；
5. 哪些 Layer 名称需要改善。
```
