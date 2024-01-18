作为开始, 我们会一步步开始, 返回单层 task 列表的 API 逐渐过渡到返回多层 Teams 列表 API.

To begin, we will start step by step, transitioning from an API that returns a single-layer task list to an API that returns a multi-layer Teams list.

## 简单列表 Simple list

对应的路由:

routers:

- `sample_1.router:get_users`
- `sample_1.router:get_tasks`

在`src.router.sample_1` 中，我们依次创建 users, tasks 的 API， 以 list[T] 的形式返回。

In `src.router.sample_1`, we will sequentially create APIs for users and tasks, returning them in the form of list[T].

```python
import src.services.task.query as tq

@route.get('/tasks', response_model=List[ts.Task])
async def get_step_1_tasks(session: AsyncSession = Depends(db.get_session)):
    """ 1.2 return list of tasks """
    return await tq.get_tasks(session)
```

通过引入 `src.services.user.query` 和 `src.services.task.query` 中的查询,返回了 `list[orm]` 对象, 然后 FastAPI 会自动将对象转成 response_model 中对应的类型.

by importing queries from `src.services.user.query` and `src.services.task.query`, we can get `list[orm]`, and then FastAPI will automatically convert the objects into the corresponding types defined in response_model

## 嵌套列表

接下来我们要将将 user 信息添加到 task 中, 在 sample_1 目录下创建 `schema.py`, 定义一个扩展了 user 信息的 `Sample1TaskDetail` 类型.

> 为了避免类型名字重复,使用 router 名字作为前缀
>
> 因此 Sample1 开头的 schema 都是属于 sample_1 路由的 (这点在生成前端 sdk ts 类型的时候会很有用.)

```python
class Sample1TaskDetail(ts.Task):
    user: Optional[us.User] = None
    def resolve_user(self, loader=LoaderDepend(ul.user_batch_loader)):
        return loader.load(self.owner_id)
```

几个注意点:

1. 继承`ts.Task`后, `Sample1TaskDetail` 就可以用 `tq.get_tasks(session)` 返回的 orm 对象赋值.
2. 定义 user 需要添加默认值, 否则用 `Sample1TaskDetail.model_valiate` 会报缺少字段错误.
3. `ul.user_batch_loader` 会根据 `list[task.owner_id]` 来关联 task 和 user 对象. 具体看 `src.services.user.loader`

> resolve 返回的数据需要是 pydantic 可以转化的类型.
>
> 如果是 orm 对象需要配置 `ConfigDict(from_attribute=True)`

在 `router.py` 中, 依然是通过 `tq.get_tasks(session)` 来获取初始数据, 接着转换成 `Sample1TaskDetail`. 之后交给 `Resolver` 就能 resolve 出所有 user 信息.

```python
@route.get('/tasks-with-detail', response_model=List[Sample1TaskDetail])
async def get_tasks_with_detail(session: AsyncSession = Depends(db.get_session)):
    """ 1.3 return list of tasks(user) """
    tasks = await tq.get_tasks(session)
    tasks = [Sample1TaskDetail.model_validate(t) for t in tasks]
    tasks = await Resolver().resolve(tasks)
    return tasks
```

## 多层嵌套列表

使用相同的方式， 我们从 `tasks-with-details` 逐步构建到了 `teams-with-details`. 虽然是层层嵌套，但定义的方式非常简单。

```python
# story
class Sample1StoryDetail(ss.Story):
    tasks: list[Sample1TaskDetail] = []
    def resolve_tasks(self, loader=LoaderDepend(tl.story_to_task_loader)):
        return loader.load(self.id)

# sprint
class Sample1SprintDetail(sps.Sprint):
    stories: list[Sample1StoryDetail] = []
    def resolve_stories(self, loader=LoaderDepend(sl.sprint_to_story_loader)):
        return loader.load(self.id)

# team
class Sample1TeamDetail(tms.Team):
    sprints: list[Sample1SprintDetail] = []
    def resolve_sprints(self, loader=LoaderDepend(spl.team_to_sprint_loader)):
        return loader.load(self.id)
```

## Dataloader 的使用

Dataloader 的作用收集完所有要查询的 parent_ids 之后，一次性查询到所有的 childrent 对象，接着根据 child 的 parent_id 聚合起来。

数据关系可能有 1:1, 1:N, M:N, 从 parent 角度看的话，就会只有 1:1 和 1:N 两种。 对应这两种情况，`pydantic2-resolve` 提供了两个辅助函数

```python
from pydantic2_resolve import build_list, build_object

# service.user.loader:  1 - 1
async def user_batch_loader(user_ids: list[int]):
    async with db.async_session() as session:
        users = await batch_get_users_by_ids(session, user_ids)
        return build_object(users, user_ids, lambda u: u.id)  # to object

# service.sprint.loader:  1 - N
async def team_to_sprint_loader(team_ids: list[int]):
    async with db.async_session() as session:
        sprints = await batch_get_sprint_by_ids(session, team_ids)
        return build_list(sprints, team_ids, lambda u: u.team_id)  # to list
```

可以看到 1:1 的关系查询 id 是目标的主键， 查询非常简单, 因此可复用性最高。

而 1:N 的查询需要有对应的关系表来确定，所以复用情况受限于 parent 类型。

### 1:1

用 story 举例， `story.owner_id` 指定了一个 story 的负责人， 如果需要把 user 信息添加到 story, 则只需直接复用 `user_batch_loader` 方法。

```python
class Sample1StoryDetail(ss.Story):
    tasks: list[Sample1TaskDetail] = []
    def resolve_tasks(self, loader=LoaderDepend(tl.story_to_task_loader)):
        return loader.load(self.id)

    owner: Optional[us.User] = None
    def resolve_owner(self, loader=LoaderDepend(ul.user_batch_loader)):
        return loader.load(self.owner_id)
```

可以在 swagger 中查看输出。

### 1:N

以 teams 举例， team_user 表维护了 team 和 user 之间的关系。
所以我们的 loader 需要 join team_user 来查询 user.

因此这种类型的 dataloader 的复用是跟着 parent 类型走的.

```python
# team -> user query
async def batch_get_user_by_team_ids(session: AsyncSession, team_ids: list[int]):
    stmt = (select(tm.TeamUser.team_id, User)
            .join(tm.TeamUser, tm.TeamUser.user_id == User.id)
            .where(tm.TeamUser.team_id.in_(team_ids)))
    rows = (await session.execute(stmt))
    return rows

# team -> user loader
async def team_to_user_loader(team_ids: list[int]):
    async with db.async_session() as session:
        pairs = await batch_get_user_by_team_ids(session, team_ids)
        dct = defaultdict(list)
        for pair in pairs:
            dct[pair.team_id].append(pair.User)
        return [dct.get(team_id, []) for team_id in team_ids]
```

然后去 `sample_1.schema:Sample1TeamDetail` 中添加 members(user) 以及刚刚创建的 loader 即可.

```python

class Sample1TeamDetail(tms.Team):
    sprints: list[Sample1SprintDetail] = []
    def resolve_sprints(self, loader=LoaderDepend(spl.team_to_sprint_loader)):
        return loader.load(self.id)

    members: list[us.User] = []
    def resolve_members(self, loader=LoaderDepend(ul.team_to_user_loader)):
        return loader.load(self.id)
```

> 顺便一提, `resolve_method` 并不需要从顶层 class 就开始定义. `Resolver` 会递归遍历然后找到`resolver_method` 进行解析.

至此， Dataloader 的复用性就介绍完了。
