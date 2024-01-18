## Post hooks

进入 `sample_4` 

这次我想让 team, sprint, story 上面添加 task_count 字段, 来统计每一个级别包含的 task 总数. 

使用 `post_method` 可以做到, `post_method` 会在class 的所有 `resolve_methods` 执行完之后, 以同步的方式执行.

> 是的, 作为post hook, 它不支持 async

```python
class Sample4StoryDetail(ss.Story):
    tasks: list[Sample4TaskDetail] = []
    def resolve_tasks(self, loader=LoaderDepend(tl.story_to_task_loader)):
        return loader.load(self.id)
    
    task_count: int = 0
    def post_task_count(self):
        return len(self.tasks)
    
class Sample4SprintDetail(sps.Sprint):
    stories: list[Sample4StoryDetail] = []
    def resolve_stories(self, loader=LoaderDepend(sl.sprint_to_story_loader)):
        return loader.load(self.id)

    task_count: int = 0
    def post_task_count(self):
        return sum([s.task_count for s in self.stories])

class Sample4TeamDetail(tms.Team):
    sprints: list[Sample4SprintDetail] = []
    def resolve_sprints(self, loader=LoaderDepend(spl.team_to_sprint_loader)):
        return loader.load(self.id)

    task_count: int = 0
    def post_task_count(self):
        return sum([s.task_count for s in self.sprints])
```

从 Story 开始, 每一层都定义了一个 `task_count` 字段, 然后 `post_task_count` 会在 `tasks` 数据获取到之后执行, 计算出 `self.task` 的长度

等所有 post 方法执行完后, 才代表 Sprint 中的 `resolve_stories` 执行完毕, 接着 Sprint 中的 `post_task_count` 开始执行, 把所有 story 的 task_count 相加.

在往上 Team 也是类似的逻辑.

最后就能计算出每一层中的 task_count.

顺带一提, 在 post 方法中, 有一个特殊的方法 `post_default_handler`, 它会在所有的 `post_method` 执行完后再执行. 用它我们可以做一些有趣的功能:

比如我们可以为 Team 添加一个 description, 来总结 team 有多少task. 因为 `default_post_handler` 会在 resolve 和 post 执行完之后才执行, 所以就能获得所有信息 (task_count) 来生成 description.

```python
class Sample4TeamDetail(tms.Team):
    sprints: list[Sample4SprintDetail] = []
    def resolve_sprints(self, loader=LoaderDepend(spl.team_to_sprint_loader)):
        return loader.load(self.id)

    task_count: int = 0
    def post_task_count(self):
        return sum([s.task_count for s in self.sprints])
    
    description: str = ''
    def post_default_handler(self):
        self.description = f'team: {self.name} has {self.task_count} tasks in total.' 
```