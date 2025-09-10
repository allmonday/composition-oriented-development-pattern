### 向子孙节点提供字段信息.

进入 `sample_3`.

我想让 task 有一个 full_name 字段, 里面包含所有上层的name作为前缀.

比如 team_a -> sprint_a -> story_a -> task_a, 那么 task_a 的 full_name就是 `team_a/sprint_a/story_a/task_a`

我们可以通过给 schema 设置 `__pydantic_resolve_expose__ = {'name': 'team_name'}` 这样的方式, 为自己的某个字段取别名, 然后让自己所有的子孙节点可以读取到.

> 别名需要保证全局 (整个Resolve 接收的 schema) 唯一. 否则 pydantic-reslove 会抛出错误.

反过来在任意子孙节点, 都能够通过 ancestor_context 参数, 来读取到直接祖先的 `name` 字段的值.

```python
class Sample3TeamDetail(tms.Team):
    __pydantic_resolve_expose__ = {'name': 'team_name'}  # expose name

    sprints: list[Sample3SprintDetail] = []
    def resolve_sprints(self, loader=LoaderDepend(spl.team_to_sprint_loader)):
        return loader.load(self.id)

class Sample3TaskDetail(ts.Task):
    ...

    full_name: str = ''
    def resolve_full_name(self, ancestor_context: Dict):
        team = ancestor_context['team_name']
        sprint = ancestor_context['sprint_name']
        story = ancestor_context['story_name']
        return f"{team}/{sprint}/{story}/{self.name}"
```

通过这种方式, 我们可以访问任意层级的祖先数据, 这给数据处理带来了巨大的便利. 可以满足各种视图构建的需求.