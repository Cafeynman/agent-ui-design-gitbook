---
description: >-
  两个完整案例：SaaS 落地页与 AI 工作台 Dashboard，展示结构、状态和 Review 思路。
icon: display
layout:
  width: default
  tableOfContents:
    visible: true
  pagination:
    visible: true
---

# 完整案例

## 案例 A：SaaS Landing Page

### 产品

面向企业研究团队的 AI 证据工作台。

### 页面任务

让合格访客申请 Demo。

### 推荐结构

```text
Navbar
Hero：核心价值 + Demo 入口
Evidence：客户、数据或安全资质
Workflow：从资料到证据链
Capabilities：三个核心能力
Use cases：不同角色如何使用
Security / Trust
Final CTA
Footer
```

### 必须 Review

- Hero 是否在五秒内说明服务谁和解决什么；
- 证据是否在用户需要时出现；
- 功能是否翻译成用户收益；
- CTA 是否始终使用同一名称；
- 手机端是否保留主要行动。

## 案例 B：AI 工作台 Dashboard

### 主要任务

查看文档处理状态、打开结果、处理失败任务。

### 关键状态

- 首次使用 Empty；
- 上传中与解析中；
- 部分成功；
- 文件格式错误；
- 网络中断；
- 无权限；
- 删除确认与 Undo。

### 页面层级

```text
全局导航
  ↓
页面标题 + 主要行动
  ↓
状态摘要
  ↓
任务列表 / 文档列表
  ↓
筛选、批量操作、分页
```

### 常见错误

- 把 Dashboard 做成营销首页；
- 每个数字都使用大卡片；
- Loading 时整个页面闪烁；
- Error 只显示“Something went wrong”；
- 筛选条件在手机端不可见。
