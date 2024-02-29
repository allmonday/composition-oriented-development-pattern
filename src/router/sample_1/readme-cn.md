作为开始, 我们会一步步迭代, 从返回单层 task 列表逐渐过渡到返回多层 Teams 列表.

来满足我们构建视图数据时最核心的需求.

## 简单列表

路由:

- `sample_1.router:get_users`
- `sample_1.router:get_tasks`

在`src.router.sample_1` 中，我们依次创建 users, tasks 的 API， 以 list[T] 的形式返回。

```python
import src.services.task.query as tq

@route.get('/tasks', response_model=List[ts.Task])
async def get_step_1_tasks(session: AsyncSession = Depends(db.get_session)):
    """ 1.2 return list of tasks """
    return await tq.get_tasks(session)
```

通过引入 `src.services.user.query` 和 `src.services.task.query` 中的查询,返回了 `list[orm]` 对象, 然后 FastAPI 会自动将对象转成 response_model 中对应的类型.

访问 
- `http://localhost:8000/sample_1/users`
- `http://localhost:8000/sample_1/tasks`


## 构建嵌套列表

接下来我们把 user 信息添加到 task 中, 在 sample_1 目录下创建 `schema.py`.

定义一个扩展了 user 信息的 `Sample1TaskDetail` 类型.

```python
class Sample1TaskDetail(ts.Task):
    user: Optional[us.User] = None
    def resolve_user(self, loader=LoaderDepend(ul.user_batch_loader)):
        return loader.load(self.owner_id)
```

> 为了避免类型名字重复, 使用 router 名字作为前缀
>
> 因此 Sample1 开头的 schema 都是属于 sample_1 路由的 (这点在生成前端 sdk ts 类型的时候将会很有用.)

几个注意点:

1. 继承`ts.Task`后, `Sample1TaskDetail` 就可以用 `tq.get_tasks(session)` 返回的 orm 对象赋值.
2. 定义 user 需要添加默认值, 否则用 `Sample1TaskDetail.model_valiate` 会报缺少字段错误.
3. `ul.user_batch_loader` 会根据 `list[task.owner_id]` 来关联 task 和 user 对象. 具体看 `src.services.user.loader`
4. resolve 返回的数据需要是 pydantic 可以转化的类型.
5. 如果是 orm 对象需要配置 `ConfigDict(from_attribute=True)`

loader 的作用是收集完所有task需要查询的 `task.owner_id`, 一次性查询完之后赋值给各自的 task


在 `router.py` 中, 依然是通过 `tq.get_tasks(session)` 来获取初始数据, 将数据转换成 `Sample1TaskDetail`. 之后交给 `Resolver` 就能 resolve 出所有 user 信息.

```python
@route.get('/tasks-with-detail', response_model=List[Sample1TaskDetail])
async def get_tasks_with_detail(session: AsyncSession = Depends(db.get_session)):
    """ 1.3 return list of tasks(user) """
    tasks = await tq.get_tasks(session)
    tasks = [Sample1TaskDetail.model_validate(t) for t in tasks]  # 装载到目标schema
    tasks = await Resolver().resolve(tasks)
    return tasks
```

访问:
- `http://localhost:8000/sample_1/tasks-with-detail`

可以看到 user 信息被添加了进来.
```json
[
    {
        "id": 1,
        "name": "mvp tech design",
        "owner_id": 2,
        "story_id": 1,
        "user": {
            "id": 2,
            "name": "Eric",
            "level": "junior"
        }
    },
    {
        "id": 2,
        "name": "implementation",
        "owner_id": 2,
        "story_id": 1,
        "user": {
            "id": 2,
            "name": "Eric",
            "level": "junior"
        }
    }
]
```


## 多层嵌套列表

用相同的方式， 我们从 `tasks-with-details` 逐步构建到了 `teams-with-details`. 虽然是层层嵌套，但定义的方式非常简单。

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

访问: `http://localhost:8000/sample_1/teams-with-detail`


### 另一种数据加载情景

`get_teams_with_detail_2` 描述了另一种场景, 假如我们利用了一些 ORM 的关联查询, 或者从某个GraphQL 查询, 提前获取到了 team + sprints 级别的数据, 那我可以以这个数据为基础继续向下 resolve.

输入数据, 已经是嵌套的结构:

```python
teams = [{
    "id": 1,
    "name": "team-A",
    "sprints": [
        {
            "id": 1,
            "name": "Sprint A W1",
            "status": "close",
            "team_id": 1
        },
        {
            "id": 2,
            "name": "Sprint A W3",
            "status": "active",
            "team_id": 1
        },
        {
            "id": 3,
            "name": "Sprint A W5",
            "status": "plan",
            "team_id": 1
        }
    ]
}]
```

转换类型, 可以看到此处没有 `resolve_sprints`(由根数据提供).  sprints 数据转换成 `Simple1SprintDetail` 类型之后, 会自动继续扩展获取定义的关联类型.

```python
class Sample1TeamDetail2(tms.Team):
    sprints: list[Sample1SprintDetail]  # no resolver, no default
    
    members: list[us.User] = []
    def resolve_members(self, loader=LoaderDepend(ul.team_to_user_loader)):
        return loader.load(self.id)
```

> `resolve_method` 并不需要从顶层 class 就开始定义. `Resolver` 会递归遍历然后找到`resolver_method` 进行解析.
>
> 因此你可以根据输入的数据做定制, 找到最简洁的扩展方式
>
> pydantic-resolve 不会去考虑 ORM model 和 schema 直接是否统需要一声明的问题, 因为 ORM 层面向的持久层和pydantic schema 面向的业务层并不能保证一致.


## Dataloader 的使用

Dataloader 的作用收集完所有要查询的 parent_ids 之后，一次性查询到所有的 childrent 对象，接着根据 child 的 parent_id 聚合起来。

数据关系从 parent 角度看的话，有 1:1 和 1:N 两种。 对应这两种情况，`pydantic2-resolve` 提供了两个辅助函数

```python
from pydantic_resolve import build_list, build_object

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

可以看到 1:1 的关系查询 id 是目标的主键， 查询非常简单, 复用最方便。

而 1:N 的查询需要有对应的关系表 (parent_id -> id) 来确定，所以复用情况取决于 parent_id。

### 1:1

用 story 举例， `story.owner_id` 指定了一个 story 的负责人， 如果需要把 user 信息添加到 story, 则只需直接使用 `user_batch_loader` 方法。

```python
class Sample1StoryDetail(ss.Story):
    owner: Optional[us.User] = None
    def resolve_owner(self, loader=LoaderDepend(ul.user_batch_loader)):
        return loader.load(self.owner_id)
```

### 1:N

以 teams 举例， team_user 表维护了 team 和 user 之间的关系。
所以我们的 loader 需要 join team_user 来查询 user.

因此这种类型的 dataloader 的复用是跟着 parent 走的.

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
    members: list[us.User] = []
    def resolve_members(self, loader=LoaderDepend(ul.team_to_user_loader)):
        return loader.load(self.id)
```

至此， Dataloader 的使用介绍完毕.


## 聊聊DataLoader

对于使用过 `graphene` 或者 `strawberry` 之类 graphql 框架的开发, dataloader 是一个很熟悉的东西.

在GraphQL 的模式下, 添加loader 需要将所有要使用的 loader 放到一个公共 context 里面, 这个问题受制于 GraphQL 单一入口, 所以没有好的解决方法.
 
- https://github.com/syrusakbary/aiodataloader?tab=readme-ov-file#creating-a-new-dataloader-per-request
- https://strawberry.rocks/docs/guides/dataloaders#usage-with-context
- https://www.apollographql.com/docs/apollo-server/data/fetching-data/#adding-data-sources-to-your-context-function


这间接导致, 如果一个 loader 在多处被使用了, 那么对这个loader 的修改就会很困难. ( 因为 Query 太全能, 一个系统被全局关联了, 反而导致修改很困难 )

因此 `pydantic-resolve` 利用 Resolver 提供的单独入口, 实现了通过 `LoaderDepend` 就近申明 loader 的功能

这样一来 Resolver 就能按需来生成各个 loader 实例. loader 之间的替换修改就非常容易. 而且也不用把所有 loader 往一个 context 里面放了. 

在 `pydantic-resolve` 中, loader 们彻底自由了, 开发可以随心所欲定制各种loader 而不用担心任何全局管理问题.