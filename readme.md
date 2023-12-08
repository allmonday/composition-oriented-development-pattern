# 可组合的API开发模式

Roadmap:
- 创建简单列表
- 创建两层的嵌套列表
- 创建三层的嵌套列表
- 可复用的dataloader
- 支持参数设置
- 额外的过滤逻辑
- 后处理功能
- 可组合的service规范

## 简单列表
让我们从一个 mini-jira 系统开始.

`mini-jira` 有这么些概念实体，分配到了各个 `service·中。
- team
- sprint
- story
- task
- user

在`src.main` 中，我们依次创建 users, tasks, stories 的API， 以list[T] 的形式返回。

## 嵌套列表

接着根据 task.owner_id 的信息，为task 添加 user 信息。





