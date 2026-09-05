# 点一下，懂 UI

面向零基础 Agent Coding 用户：**动一下 → 看变化 → 选一道题 → 给 Agent 一句话**。

12 节互动入门课，168 个可搜索词条，原有图文书稿和独立实验。

## 本地预览

```sh
python -m pip install -r requirements.txt
python scripts/prepare_book.py
python scripts/build.py
python scripts/check.py
python -m http.server 8000 --directory _site
```

## 可复验测试

```sh
python -m pip install playwright==1.55.0
python -m playwright install chromium
python scripts/browser_check.py
```

`reviews/browser-results.json` 由真实浏览器测试生成；它不是独立模型审查，也不代表完整 WCAG 认证。

## 发布

GitHub Actions 对同一提交先测试、再部署，最后验证 `/version.json` 中的提交号。仅提交源码或 HTTP 200 不算发布验证通过。

GitBook 读取 `.gitbook.yaml` 的 `book/`。首次导入请选 GitHub 内容作为来源；Git Sync 可能双向写入，不要误把首次同步方向当成永久只读保护。本仓库没有自动回滚他人提交的工作流。

## 内容维护

- `assets/lessons.js`：12 节短课。
- `book/glossary/`：词条来源，构建为 `assets/catalog.js`。
- `scripts/prepare_book.py`：入门章节的可编辑源文本，会生成对应 Markdown。
- `book/` 其他章节：可直接编辑的长篇内容。
- `scripts/build.py`：生成 `_site/`，不写入任何 Git 引用。

原始三篇历史长文保留在会话提供的原始 ZIP，不重复塞进入门阅读目录。
