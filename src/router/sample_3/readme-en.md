### Expose

Enter sample_3 .

In the second case, I want task to have another full_name field, which directly contains the prefixes of all levels. For example, team_a -> sprint_a -> story_a -> task_a, then the full_name of task_a is `team_a/sprint_a/story_a/task_a`

Schema can use `__pydantic_resolve_expose__ = {'name': 'team_name'}` to alias one of its fields and then expose it to all its descendant nodes.

> The alias needs to be globally (entire Resolve scope) unique.

n turn, at any descendant node, the value of the direct ancestor's name field can be read through the ancestor_context parameter.

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
