## Loader instance 的使用

通常情况下 loader instance 是由 Resolver 内部实例化并且维护的。

如果你已经有一个 loader，并且这个 loader 已经通过 `prime` 方法添加过了数据的话， 那么可以使用 `loader_instance` 参数传入，让 Resolver内部跳过初始化过程， 直接使用传进来的 loader 实例。

以 UserLoader 为例子， 可以使用一个真实可用的 loader `src.service.user.loader:user_batch_loader`，也可以使用 `generate_single_empty_loader` 来生成一个 Loader 类。

两者的区别在于， 如果`loader.load(key)` 传入的数据如果不在 loader cache 中， 会触发 `batch_load_fn` 进行查询

`generate_single_empty_loader` 内置的 `batch_load_fn` 不会做任何事情，如果不存在就返回 `None`

> generate_list_empty_loader 默认返回 []


```python
UserLoader = generate_single_empty_loader('UserLoader')

class Sample7TaskDetail(ts.Task):
    user: Optional[us.User] = None
    def resolve_user(self, loader=LoaderDepend(UserLoader)):
        return loader.load(self.owner_id)
```

router 中使用 `add_single_to_loader` 来处理 `prime` 逻辑

模拟预先获取 users 信息， 然后加入 loader, 再提供给 `Sample7TaskDetail` 使用。


```python
def add_single_to_loader(loader, items, get_key):
    _map = {}
    for item in items:
        _map[get_key(item)] = item
    for k, v in _map.items():
        loader.prime(k, v)

@route.get('/tasks', response_model=list[Sample7TaskDetail])
async def get_tasks(session: AsyncSession = Depends(db.get_session)):
    # 初始化 loader, 提前加载所有数据 
    user_loader = UserLoader()
    users = await uq.get_users(session)
    add_single_to_loader(user_loader, users, lambda u: u.id)

    tasks = await tskq.get_tasks(session)
    tasks = [Sample7TaskDetail.model_validate(t) for t in tasks]
    # 使用预先创建好的 loader 实例
    tasks = await Resolver(loader_instances={UserLoader: user_loader}).resolve(tasks)
    return tasks
```
> 如果注释 `add_single_to_loader`方法， 会发现所有的 user 都是 None

第二个稍微复杂一些的例子， 从 user[1] 开始， 层层寻找 user 拥有的 story, story 归属的 sprint， sprint 归属的 team, 然后反向从 Teams 开始层层往下展示。

```python
@route.get('/user/stat', response_model=list[Sample7TeamDetail])
async def get_user_stat(session: AsyncSession = Depends(db.get_session)):
    sprint_to_story_loader = SprintToStoryLoader()
    team_to_sprint_loader = TeamToSprintLoader()

    users = await uq.get_user_by_ids([1], session)
    stories = await sq.get_stories_by_owner_ids([u.id for u in users], session)
    add_to_loader(sprint_to_story_loader, stories, lambda s: s.sprint_id)

    sprint_ids = list({s.sprint_id for s in stories})
    sprints = await spq.get_sprints_by_ids(sprint_ids, session)
    add_to_loader(team_to_sprint_loader, sprints, lambda s: s.team_id)

    team_ids = list({s.team_id for s in sprints})

    teams = await tq.get_team_by_ids(team_ids, session)
    teams = [Sample7TeamDetail.model_validate(t) for t in teams]
    teams = await Resolver(loader_instances={
        SprintToStoryLoader: sprint_to_story_loader,
        TeamToSprintLoader: team_to_sprint_loader
    }).resolve(teams)
    return teams
```
