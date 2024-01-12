### Expose

进入 `sample_3`.

第二种情况, 我想让 task 又一个 full_name 字段, 直接包含所有层级的前缀. 比如 team_a -> sprint_a -> story_a -> task_a, 那么 task_a 的 full_name就是 `team_a/sprint_a/story_a/task_a`

schema 可以通过 `__pydantic_resolve_expose__ = {'name': 'team_name'}` 这样的方式, 给自己的某个字段取别名, 然后暴露给自己所有的子孙节点.

> 别名需要保证全局 (整个Resolve scope) 唯一.

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