# 页面不只有“正常”

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

[W3C：反馈与错误说明](https://www.w3.org/WAI/tutorials/forms/notifications/)。
