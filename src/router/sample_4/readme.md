# 后处理钩子

```shell
router-viz -m src.main  --model_prefixs src.servicesls --tags sample_4 --show_fields
```

<img width="1623" height="913" alt="image" src="https://github.com/user-attachments/assets/75e67947-a0ee-40e2-961b-7c0bba6fad2e" />

进入 `sample_4`. 介绍如何在数据获取之后进行额外处理. 

这次我想在 team, sprint, story 上面添加 task_count 字段, 来统计每一层包含的 task 总数. 

使用 `post_method` 可以做到, `post_method` 会在class 的所有 `resolve_methods` 执行完之后, 以同步的方式执行.

> 是的, 作为post hook, 它不支持 async, 我们期望这里只进行可控的数据操作行为. (post hook 不会提供 loader)

```python
class Sample4StoryDetail(ss.Story):
    tasks: list[Sample4TaskDetail] = []
    def resolve_tasks(self, loader=LoaderDepend(tl.story_to_task_loader)):
        return loader.load(self.id)
    
    task_count: int = 0
    def post_task_count(self): # post hook
        return len(self.tasks)
    
class Sample4SprintDetail(sps.Sprint):
    stories: list[Sample4StoryDetail] = []
    def resolve_stories(self, loader=LoaderDepend(sl.sprint_to_story_loader)):
        return loader.load(self.id)

    task_count: int = 0
    def post_task_count(self):  # post hook
        return sum([s.task_count for s in self.stories])

class Sample4TeamDetail(tms.Team):
    sprints: list[Sample4SprintDetail] = []
    def resolve_sprints(self, loader=LoaderDepend(spl.team_to_sprint_loader)):
        return loader.load(self.id)

    task_count: int = 0
    def post_task_count(self): # post hook
        return sum([s.task_count for s in self.sprints])
```

从 Story 开始, 每一层都定义了一个 `task_count` 字段, 然后 `post_task_count` 会在 `tasks` 数据获取到之后执行, 计算出 `self.task` 的长度

等所有 post 方法执行完后, 才代表 Sprint 中的 `resolve_stories` 执行完毕, 接着 Sprint 中的 `post_task_count` 开始执行, 把所有 story 的 task_count 相加.

再往上 Team 也是类似的逻辑.

最后就能计算完每一层中的 task_count.

顺带一提, 在 post 方法中, 有一个特殊的方法 `post_default_handler`, 它等所有的 `post_method` 执行完后再执行. 

用它我们可以做一些有趣的功能:

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

利用这个功能, 我们在复用相同的数据时, 可以做很多定制化的修改.


## 隐藏/过滤字段

在上个案例中, 可能会有一种需求. 比如有一些层级的 task_count 我不想显示, 想将它在返回中屏蔽掉该怎么做?

对于这种对外隐藏字段的需求, 可以使用 model_config 装饰器搭配`Field(exclude=True)`来实现.

```python
@model_config()
class Sample4StoryDetail(ss.Story):
    tasks: list[Sample4TaskDetail] = []
    def resolve_tasks(self, loader=LoaderDepend(tl.story_to_task_loader)):
        return loader.load(self.id)
    
    task_count: int = Field(default=0, exclude=True)
    def post_task_count(self):
        return len(self.tasks)
```

两个改动, 一个是添加了 `model_config`装饰器, 另一个是用 `Field(exclude=True)` 来申明类型.

在pydantic 中,如果exclude=True, 则会在输出中屏蔽该字段, 但是 schema 中依然能看到这个字段. 

搭配了 `model_config` 就可以保证在 schema properties 中也屏蔽该字段.

可以将代码中的注释移除后测试.
