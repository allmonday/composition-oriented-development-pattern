# 可组合的 API 开发模式

在构建关系型数据的 API 时, 怎么寻找一个兼顾灵活, 性能, 可维护的方案? 我希望它能够:

- 支持异步
- 支持定义多层的数据结构, 定义方式要简洁, 扩展要友好, 支持列表
- 可以传入参数
- 利用 Dataloader 避免 N+1 查询
- 避免 GraphQL 一套接口提供所有服务的模式, 每个 API 接口都有能力快速定义自己所需的类型.
- 提供 **每层对象** 在`resolve` 完子孙数据后, 做额外计算的能力
- 挑选需要的返回字段 (类似 GraphQL 编辑 query)

这个 repo 会通过一系列的例子, 结合 `pydantic2-resolve`, 来定义这样一套灵活的面向组合的开发模式.

## Roadmap:

- ~~简单列表~~
- ~~嵌套列表~~
- ~~多层嵌套列表~~
- ~~Dataloader 的复用~~
  - ~~`1 - 1`~~
  - ~~`1 - N`~~
- Resolver 参数
- 后处理
- 面向可组合模式的一些约定

## Mini-JIRA

让我们从一个 mini-jira 系统开始.

`mini-jira` 有这么些实体概念，分配到了各个 `service·中。

- team
- sprint
- story
- task
- user

team -> sprint -> story -> task 层层往下都是一对多的关系

task 和 user 是一对一.

## 执行代码

```shell
python -m venv venv
source venv/bin/activate
pip install -r requirement.txt
uvicorn src.main:app --port=8000 --reload
# http://localhost:8000/docs
```

## 简单列表

对应的路由:

- `sample_1.router:get_users`
- `sample_1.router:get_tasks`

在`src.router.sample_1` 中，我们依次创建 users, tasks 的 API， 以`list[T]`的形式返回。

```python
import src.services.task.query as tq

@route.get('/tasks', response_model=List[ts.Task])
async def get_step_1_tasks(session: AsyncSession = Depends(db.get_session)):
    """ 1.2 return list of tasks """
    return await tq.get_tasks(session)
```

通过引入 `src.services.user.query` 和 `src.services.task.query` 中的查询,返回了 `list[orm]` 对象, 然后 FastAPI 会自动将对象转成 `response_model` 中对应的类型.

## 嵌套列表

接下来我们要将将 `user` 信息添加到 `task` 中, 在`sample_1` 目录下创建 `schema.py`, 定义一个扩展了 `user` 信息的 `Sample1TaskDetail` 类型.

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

在 `router.py` 中, 依然是通过 `tq.get_tasks(session)` 来获取初始数据, 接着转换成 `Sample1TaskDetail`. 之后交给 `Resolver` 就能 `resolve` 出所有 `user` 信息.

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

使用相同的方式， 我们从 `tasks-with-details` 构建到了 `teams-with-details`. 虽然是层层嵌套，但定义的方式非常简单。

```python
class Sample1StoryDetail(ss.Story):
    tasks: list[Sample1TaskDetail] = []
    def resolve_tasks(self, loader=LoaderDepend(tl.story_to_task_loader)):
        return loader.load(self.id)

class Sample1SprintDetail(sps.Sprint):
    stories: list[Sample1StoryDetail] = []
    def resolve_stories(self, loader=LoaderDepend(sl.sprint_to_story_loader)):
        return loader.load(self.id)

class Sample1TeamDetail(tms.Team):
    sprints: list[Sample1SprintDetail] = []
    def resolve_sprints(self, loader=LoaderDepend(spl.team_to_sprint_loader)):
        return loader.load(self.id)
```

## Dataloader 的复用

Dataloader 的作用收集完所有要查询的 parent_ids 之后，一次性查询到所有的 childrent 对象，接着根据 child 的 parent_id 聚合起来。

数据关系可能有 `1 - 1`, `1 - N`, `M - N`, 从 parent 角度看的话，就会只有 `1 - 1` 和 `1 - N` 两种。 对应这两种情况，`pydantic2-resolve` 提供了两个辅助函数

```python
from pydantic2_resolve import build_list, build_object

# service.user.loader:  1 - 1
async def user_batch_loader(user_ids: list[int]):
    async with db.async_session() as session:
        users = await batch_get_users_by_ids(session, user_ids)
        return build_object(users, user_ids, lambda u: u.id)

# service.sprint.loader:  1 - N
async def team_to_sprint_loader(team_ids: list[int]):
    async with db.async_session() as session:
        sprints = await batch_get_sprint_by_ids(session, team_ids)
        return build_list(sprints, team_ids, lambda u: u.team_id)
```

可以看到 `1 -1` 的关系查询 id 是目标的主键， 查询非常简单, 因此可复用性最高。

而 `1-N` 的查询需要有对应的关系表来确定，所以复用情况受限于 parent 类型。

### 1 - 1

用 `story` 举例， `story.owner_id` 指定了一个 story 的负责人， 如果需要把 `user` 信息添加到 `story`, 只需直接复用 `user_batch_loader` 方法。

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

### 1 - N

以 `teams` 距离， 有 `team_user` 表维护了 `team`和 `user`之间的关系。
所以我们的 `loader` 需要 join `team_user` 来查询 `user`.

因此这种类型的 `dataloader` 的复用是跟着 parent 类型来的。

```python
# team -> user
async def batch_get_user_by_team_ids(session: AsyncSession, team_ids: list[int]):
    stmt = (select(tm.TeamUser.team_id, User)
            .join(tm.TeamUser, tm.TeamUser.user_id == User.id)
            .where(tm.TeamUser.team_id.in_(team_ids)))
    rows = (await session.execute(stmt))
    return rows

async def team_to_user_loader(team_ids: list[int]):
    async with db.async_session() as session:
        pairs = await batch_get_user_by_team_ids(session, team_ids)
        dct = defaultdict(list)  # 因为是 1 - N 所以default 是 list
        for pair in pairs:
            dct[pair.team_id].append(pair.User)
        return [dct.get(team_id, []) for team_id in team_ids]
```

然后去 `sample_1.schema:Sample1TeamDetail` 中添加 `members` 以及刚刚创建的 loader 即可.

```python

class Sample1TeamDetail(tms.Team):
    sprints: list[Sample1SprintDetail] = []
    def resolve_sprints(self, loader=LoaderDepend(spl.team_to_sprint_loader)):
        return loader.load(self.id)

    members: list[us.User] = []
    def resolve_members(self, loader=LoaderDepend(ul.team_to_user_loader)):
        return loader.load(self.id)
```

至此， Dataloader 的复用性就介绍完了。

之后的案例会进入 `sample_2` router 中描述。
