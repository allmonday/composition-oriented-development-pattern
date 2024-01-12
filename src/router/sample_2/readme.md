
### Filter
进入 `sample_2`.

考虑这么一种场景, 需要列出 team 中 level 为 senior (或者其他值) 的 members, 那么 loader 需要提供添加过滤条件的手段.

我们可以这么做, 在 `src.services.user.loader` 中添加 `UserByLevelLoader`, 它有一个类属性 `level`. 在初始化 loader 之后, 通过设置 `self.level` 就能实现功能, 现在问题是怎么为 `self.level` 赋值.

> 一个 loader 实例的 filter 字段值是不可改变的. 不同的 filter 组合需要对应到各自的 loader 实例

```python

# team -> user (level filter)
class UserByLevelLoader(DataLoader):
    level: str = ''

    async def batch_load_fn(self, team_ids: list[int]):
        async with db.async_session() as session:
            stmt = (select(tm.TeamUser.team_id, User)
                    .join(tm.TeamUser, tm.TeamUser.user_id == User.id)
                    .where(tm.TeamUser.team_id.in_(team_ids))
                    .where(User.level == self.level))  # <--- filter
            pairs = (await session.execute(stmt))
            dct = defaultdict(list)
            for pair in pairs:
                dct[pair.team_id].append(pair.User)
            return [dct.get(team_id, []) for team_id in team_ids]
```

这个参数可以从 Resolver 中传入, `loader_filters` 中指定要设置参数的 DataLoader 子类和具体参数, 在内部执行时就会赋值过去.

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

顺带说一下, 如果需要使用 loader 多次, 比如同时查询 level senior 和 junior 的两组members, 可以对Loader 做一次拷贝之后变成新的Loader 来使用.

```python
# schema.py
def copy_class(name, Kls):
    return type(name, Kls.__bases__, dict(Kls.__dict__))

SeniorMemberLoader = copy_class('SeniorMemberLoader', ul.UserByLevelLoader)
JuniorMemberLoader = copy_class('JuniorMemberLoader', ul.UserByLevelLoader)


class Sample2TeamDetailMultipleLevel(tms.Team):
    senior_members: list[us.User] = []
    def resolve_senior_members(self, loader=LoaderDepend(SeniorMemberLoader)):
        return loader.load(self.id)

    junior_members: list[us.User] = []
    def resolve_junior_members(self, loader=LoaderDepend(JuniorMemberLoader)):
        return loader.load(self.id)

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