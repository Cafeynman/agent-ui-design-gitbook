---
description: >-
  把 pen.dev 设计转成代码，并用截图差异审计保持设计和实现一致。
icon: code-compare
layout:
  width: default
  tableOfContents:
    visible: true
  pagination:
    visible: true
---

# Design ↔ Code 工作流

## Design → Code

1. 在 pen.dev 确认结构、视觉与状态；
2. 将 `.pen` 保存进项目工作区；
3. 告诉 Agent 现有技术栈和复用约束；
4. 生成代码；
5. 运行真实页面；
6. 截图并对照设计；
7. 修复 P0/P1 差异。

## Code → Design

适合改造已有项目：

1. 让 Agent 读取现有组件；
2. 在 pen.dev 中重建可视版本；
3. 探索改进方向；
4. 再把修改同步回代码。

## 实现 Prompt

```text
请根据已经确认的 Pencil 设计实现当前功能。

约束：
1. 使用仓库现有技术栈和组件；
2. 不为了方便引入新的 UI 框架；
3. 优先复用已有 Tokens 和 Components；
4. 保持语义化结构与键盘可用性；
5. 实现 Default、Hover、Focus、Disabled、Loading、
   Empty、Error 和 Success 状态；
6. 实现 Desktop 和 Mobile 响应式行为；
7. 不擅自改变已确认的信息架构；
8. 完成后运行项目并提供实际截图；
9. 对照 Pencil 列出差异；
10. 修复高优先级差异后再结束。
```
