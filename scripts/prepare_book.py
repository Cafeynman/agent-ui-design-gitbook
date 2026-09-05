"""Author compact replacement chapters; preserve recovered long-form chapters."""
from pathlib import Path
import re,shutil
ROOT=Path(__file__).resolve().parents[1];BOOK=ROOT/'book'
BASE='https://cafeynman.github.io/agent-ui-design-gitbook'
pages={
'README.md':'''# 点一下，懂 UI

不用先学代码。打开互动课，先改一个按钮。

[开始互动课](https://cafeynman.github.io/agent-ui-design-gitbook/#lesson=hero)

![设计学习循环](.gitbook/assets/agent-design-loop.svg)

每课都是：**动一下 → 看变化 → 选一道题 → 复制一条 Agent 指令**。

查词用[术语词典](glossary/page-structure.md)。需要完整路线，再读[八周计划](learning-plan/overview.md)。

这是学习资料，不是产品能力保证。旧资料中的经验法则不等于所有项目的硬性规则。''',
'start/quick-start.md':'''# 先花两分钟

[打开第一课](https://cafeynman.github.io/agent-ui-design-gitbook/#lesson=hero)。切换“含糊的开场”和“说清用途”。

哪种更容易知道产品做什么？这就是今天要学的内容。

不用记 Hero 的英文。先记住：**开头要让人知道这里有什么。**

然后把页面下方的一句话复制给 Agent，让它修改你的首页。''',
'start/learning-map.md':'''# 怎么学

| 想做什么 | 去哪里 |
| --- | --- |
| 我什么都不懂 | [先做 12 节互动课](https://cafeynman.github.io/agent-ui-design-gitbook/) |
| Agent 说了一个陌生词 | [查词](https://cafeynman.github.io/agent-ui-design-gitbook/#dictionary) |
| 我要做完整产品 | [八周计划](../learning-plan/overview.md) |
| 我想检查结果 | [验收表](../practice/review-and-scoring.md) |

![八周学习路径](../.gitbook/assets/eight-week-roadmap.svg)

一次学会一个判断，比一次看完一百个术语更有用。''',
'start/tool-setup.md':'''# Pencil 从哪里开始

打开你现有开发环境中的 Pencil / pen.dev。先让 Agent 做一个按钮，不要直接生成整站。

> 在当前画布中画一个写着“生成笔记”的按钮，再给它一个键盘焦点状态。暂时不要写业务代码。

你要检查：字能读清吗？点击区域够用吗？键盘能找到它吗？

安装方式与支持环境以[官方安装文档](https://docs.pencil.dev/getting-started/installation)为准。[官方首页](https://docs.pencil.dev/)提供当前功能说明。''',
'foundations/hero.md':'''# Hero：网页的开场

像店门口的招牌。让新来的人知道这里有什么、下一步做什么。

[切换两个开场，亲自比较](https://cafeynman.github.io/agent-ui-design-gitbook/#lesson=hero)。

**Hero 是页面区域；首屏可见范围是当前屏幕能看到的部分。** 两者不一定一样高。

![页面区域示意](../.gitbook/assets/page-anatomy.svg)

给 Agent：

> 开头用一句具体的话介绍产品用途，只突出一个主要行动。不要用“赋能未来”替代信息。

“开场的论点”是本教材的比喻，不是对 Skill 的逐字引用。[查看 Anthropic 原文](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)。''',
'foundations/page-anatomy.md':'''# 页面像一家店

![页面解剖示意](../.gitbook/assets/page-anatomy.svg)

| 看到什么 | 常用名字 | 做什么 |
| --- | --- | --- |
| 顶部菜单 | 导航栏 Navbar | 告诉你能去哪 |
| 醒目的开场 | Hero | 介绍这里有什么 |
| 主要按钮 | CTA | 告诉你下一步做什么 |
| 分成几段的内容 | Section | 一段解释一件事 |
| 页面底部 | Footer | 放辅助信息 |

不是每种页面都要有这些区域。后台工具通常更需要直接进入任务。

[去第一课找一找](https://cafeynman.github.io/agent-ui-design-gitbook/#lesson=hero)。''',
'foundations/interaction-states.md':'''# 页面不只有“正常”

![状态示意](../.gitbook/assets/state-matrix.svg)

| 状态 | 用人话说 |
| --- | --- |
| 等待 Loading | 正在生成，稍等一下 |
| 空白 Empty | 还没有论文，先上传一份 |
| 失败 Error | 没成功，可以重试 |
| 成功 Success | 笔记已生成，在这里查看 |

[点一下，切换状态](https://cafeynman.github.io/agent-ui-design-gitbook/#lesson=states)。

给 Agent：

> 补齐等待、空白、失败、成功。失败时不要清空用户已输入的内容。

[W3C：反馈与错误说明](https://www.w3.org/WAI/tutorials/forms/notifications/)。''',
'foundations/responsive-accessibility.md':'''# 小屏能用，键盘也能用

[拖动宽度，看看怎么重新排](https://cafeynman.github.io/agent-ui-design-gitbook/#lesson=responsive)。

![响应式重排示意](../.gitbook/assets/responsive-reflow.svg)

响应式不是把整页缩小，而是重新安排内容。[MDN 官方解释](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design)。

再[体验键盘焦点](https://cafeynman.github.io/agent-ui-design-gitbook/#lesson=focus)：不碰鼠标，按 Tab，能知道现在在哪个按钮吗？

给 Agent：

> 检查手机无横向溢出；按 Tab 能完成主要操作；焦点清晰可见。

这只是起点，不代表已经通过完整无障碍审核。[W3C 焦点说明](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html)。''',
'foundations/typography-color-spacing.md':'''# 先让人读懂

文字大小告诉你轻重；间距告诉你谁和谁是一组；颜色用来强调。

[试文字层级](https://cafeynman.github.io/agent-ui-design-gitbook/#lesson=hierarchy) · [拖动间距](https://cafeynman.github.io/agent-ui-design-gitbook/#lesson=spacing) · [改变行距](https://cafeynman.github.io/agent-ui-design-gitbook/#lesson=type)

![层级示意](../.gitbook/assets/visual-hierarchy.svg)

给 Agent：

> 不增加装饰。让标题更突出、正文更好读，同组内容更靠近。

不是空白越多越好，也不是字号越大越好。[NN/g：视觉层级](https://www.nngroup.com/articles/visual-hierarchy-ux-definition/)。''',
'pencil/prompt-cookbook.md':'''# 给 Pencil 的三句话

先探索：

> 只画黑白草图。用相同内容，做三个结构不同的首页方案，不要写代码。

再改一处：

> 只调整选中区域的标题、正文和按钮轻重，不改变内容和其他区域。

最后验收：

> 给我桌面和手机的实际截图。指出文字、间距、交互状态与设计稿的差异，再逐项修复。

[官方设计与代码工作流](https://docs.pencil.dev/design-and-code/design-to-code)。不要把设计稿存在当成代码已正确实现。''',
'practice/brief-and-checklist.md':'''# 一页就够

给 Agent 的需求先填五项：

```text
给谁用：
帮他做什么：
页面最重要的一步：
必须出现的内容：
不要出现的内容：
```

验收先看三个问题：能看懂吗？能完成任务吗？失败后能恢复吗？

[打开需求生成器](https://cafeynman.github.io/agent-ui-design-gitbook/labs/brief-builder/) · [完整验收表](review-and-scoring.md)。''',
'resources/faq.md':'''# 常见问题

## 要先学代码吗？

不用。先能说清楚想做什么、判断结果对不对。

## 完成课程就算掌握了吗？

不算。完成只表示操作了示例并答对一次，还要在自己的项目里练。

## 记录存在哪里？

互动课记录只在当前浏览器。可导出 JSON，再到另一台浏览器导入。

## 什么都能自动发布吗？

不能这样假定。源码提交、部署成功、公开页面可访问，是三个不同的检查。''',
'resources/how-to-study-cases.md':'''# 看案例，只问三句

用户来做什么？第一眼看到什么？点错或失败后怎么办？

先画结构，再看颜色。不要把“像某个网站”当成全部需求。

[NN/g 视觉层级案例](https://www.nngroup.com/articles/visual-hierarchy-ux-definition/)展示大小、颜色和分组如何改变注意力。

交互规则可以直接试 [W3C 标签页示例](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/) 和 [弹窗示例](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)。''',
'resources/learning-resources.md':'''# 先看这三类资料

| 学什么 | 资料 | 看哪里 |
| --- | --- | --- |
| 重点怎么突出 | [NN/g 视觉层级](https://www.nngroup.com/articles/visual-hierarchy-ux-definition/) | 图片前后对比 |
| 组件应该怎么动 | [W3C 组件模式](https://www.w3.org/WAI/ARIA/apg/patterns/) | 演示与键盘行为 |
| Pencil 怎么用 | [Pencil 官方文档](https://docs.pencil.dev/) | 安装、变量、组件 |

不用按网页顺序读完。带着当前项目的问题查一小段，再回来试。''',
'resources/references.md':'''# 原始资料

- [Anthropic frontend-design Skill](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)
- [Pencil / pen.dev 官方文档](https://docs.pencil.dev/)
- [NN/g 视觉层级](https://www.nngroup.com/articles/visual-hierarchy-ux-definition/)
- [W3C 弹窗模式](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/)
- [W3C 标签页模式](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/)
- [W3C 表单通知](https://www.w3.org/WAI/tutorials/forms/notifications/)
- [MDN 响应式设计](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design)

本教材用原创示例解释概念。比喻、练习、评分框架属于教材编写，不应当作上述来源的原文或强制标准。'''
}
labs={'hero-hierarchy':('开场与层级','page-anatomy','hero'),'spacing-proximity':('间距与分组','visual-hierarchy','spacing'),'button-states':('按钮状态','state-matrix','cta'),'responsive-layout':('响应式重排','responsive-reflow','responsive'),'form-validation':('表单错误','state-matrix','form'),'ui-states':('界面状态','state-matrix','states'),'brief-builder':('需求生成器','agent-design-loop','hero')}
for slug,(title,image,lesson) in labs.items():
 pages[f'labs/{slug}.md']=f'# {title}\n\n先操作，再读文字。\n\n[打开独立实验]({BASE}/labs/{slug}/) · [先做零基础课]({BASE}/#lesson={lesson})\n\n![原理示意，非截图](../.gitbook/assets/{image}.svg)\n\n{{% embed url="{BASE}/labs/{slug}/" %}}\n\n如果阅读器不能内嵌，请直接打开实验。'
for path,text in pages.items():
 p=BOOK/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text+'\n',encoding='utf-8')
# Original long appendices stay in the separately supplied archival ZIP; no broken online appendix links.
if (BOOK/'appendix').exists():shutil.rmtree(BOOK/'appendix')
for p in BOOK.rglob('*.md'):
 text=p.read_text(encoding='utf-8')
 text=text.replace('## Hero is a thesis','## Hero：开场集中讲清用途（教材概括）')
 p.write_text(text,encoding='utf-8')
summary=['# 目录','', '## 先动手','',f'* [开始](README.md)']
folders={'start':'快速开始','foundations':'设计基础','anthropic':'Skill 解读','pencil':'Pencil 工作流','learning-plan':'八周计划','labs':'交互实验','practice':'实际项目','glossary':'术语查询','resources':'参考资料'}
for folder,title in folders.items():
 summary+=['',f'## {title}','']
 for p in sorted((BOOK/folder).glob('*.md')):
  text=p.read_text(encoding='utf-8');m=re.search(r'^# (.+)',text,re.M)
  summary.append(f'* [{m[1] if m else p.stem}]({p.relative_to(BOOK).as_posix()})')
(BOOK/'SUMMARY.md').write_text('\n'.join(summary)+'\n',encoding='utf-8')
# Keep the old Hero URL useful; the lesson is now the canonical interactive view.
p=ROOT/'labs/hero-hierarchy/index.html';p.parent.mkdir(parents=True,exist_ok=True)
p.write_text('''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>开场与层级</title><link rel="stylesheet" href="../../assets/style.css"><main><h1>Hero：开头说清楚</h1><p>去互动课切换两个开场，看哪种更容易懂。</p><a href="../../index.html#lesson=hero">打开互动课</a><p><a href="../index.html">其他实验</a></p></main></html>''',encoding='utf-8')
