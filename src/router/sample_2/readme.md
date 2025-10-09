# 为 Loader 提供过滤

```shell
router-viz -m src.main  --model_prefixs src.servicesls --tags sample_2 --show_fields
```

<img width="1627" height="864" alt="image" src="https://github.com/user-attachments/assets/584c35cd-de0e-4607-a990-1ec58a46bfa2" />

进入 `sample_2`. 为 1:N 的 loader 提供额外的过滤功能.

考虑这么一种场景, 需要列出 Team 中 level 为 senior (或者其他值) 的 members, 那么 loader 需要提供添加过滤条件的手段.

我们可以这么做, 在 `src.services.user.loader` 中添加 `UserByLevelLoader`, 它有一个类属性 `level`. 

在初始化 loader 之后, 通过设置 `self.level` 就能实现功能


```python
loader = UserByLevelLoader()
loader.level = 'senior'
```

于是问题是如何在Resolver中为 `self.level` 赋值.


```python

# team -> user (level filter)
class UserByLevelLoader(DataLoader):
    level: str = ''  # filter

    async def batch_load_fn(self, team_ids: list[int]):
        async with db.async_session() as session:
            stmt = (select(tm.TeamUser.team_id, User)
                    .join(tm.TeamUser, tm.TeamUser.user_id == User.id)
                    .where(tm.TeamUser.team_id.in_(team_ids))
                    .where(User.level == self.level))  # <---------------- filter
            pairs = (await session.execute(stmt))
            dct = defaultdict(list)
            for pair in pairs:
                dct[pair.team_id].append(pair.User)
            return [dct.get(team_id, []) for team_id in team_ids]
```

> 一个 loader 实例的 filter 字段值是不可改变的.

这个参数可以从 Resolver 中传入, `loader_filters` 中指定要设置参数的 DataLoader 子类和具体参数, 在内部执行时就会进行赋值.

```python
teams = await tmq.get_teams(session)
teams = [Sample2TeamDetail.model_validate(t) for t in teams]
teams = await Resolver(loader_filters={
    ul.UserByLevelLoader: {
        "level": 'senior'
    }
}).resolve(teams)
return teams
```

## 相同的Loader 使用不同的filter

顺带说一下, 如果需要使用 loader 多次, 比如同时查询 level senior 和 junior 的两组 members, 因为 `pydantic-resolve` 中是对每一个 DataLoader类生成实例的, 所以无法对同一个 DataLoader 传递不同参数.

解决方法是对 DataLoader 做一次拷贝之后变成新的 DataLoader 来使用.

```python
# schema.py
def copy_class(name, Kls):
    return type(name, Kls.__bases__, dict(Kls.__dict__))  # provide in pydantic_resolve

SeniorMemberLoader = copy_class('SeniorMemberLoader', ul.UserByLevelLoader)
JuniorMemberLoader = copy_class('JuniorMemberLoader', ul.UserByLevelLoader)


class Sample2TeamDetailMultipleLevel(tms.Team):
    senior_members: list[us.User] = []
    def resolve_senior_members(self, loader=LoaderDepend(SeniorMemberLoader)):
        return loader.load(self.id)

    junior_members: list[us.User] = []
    def resolve_junior_members(self, loader=LoaderDepend(JuniorMemberLoader)):
        return loader.load(self.id)

    senior_junior: List[us.User] = []
    async def resolve_senior_junior(self,
                                    loader_j=LoaderDepend(JuniorMemberLoader),
                                    loader_s=LoaderDepend(SeniorMemberLoader)
                                    ):
        return await loader_j.load(self.id) + await loader_s.load(self.id)

```

> 请注意 `senior_junior`, 你会发现， loader 支持同时加载多个来组合使用.
>
> 这种情况下， loader_j 和 loader_s 的 batch 会分两批执行。


```python
# router.py
@route.get('/teams-with-detail-of-multiple-level', response_model=List[Sample2TeamDetail])
async def get_teams_with_detail_of_multiple_level(session: AsyncSession = Depends(db.get_session)):
    """1.2 teams with senior and junior members"""
    teams = await tmq.get_teams(session)
    teams = [Sample2TeamDetailMultipleLevel.model_validate(t) for t in teams]
    teams = await Resolver(loader_filters={
        SeniorMemberLoader: {
            "level": 'senior'
        },
        JuniorMemberLoader: {
            "level": 'junior'
        }
    }).resolve(teams)
    return teams
```

## 简便方式

如果使用了多个loader 并且参数都相同的话, 可以使用 `global_loader_filter` 参数来统一提供参数.

```python
await Resolver(loader_filters={
    LoaderA: {'level': 'senior'},
    LoaderB: {'level': 'senior'},
    LoaderC: {'level': 'senior'},
    LoaderD: {'level': 'senior'},
    LoaderE: {'level': 'senior', 'other': 'value'}}).resolve(data)
```

可以简化成
```python
await Resolver(
    global_loader_filter={'level': 'senior'},
    loader_filters={LoaderE: {'other': 'value'}}).resolve(data)
```
