### Filter

Enter sample_2 .

Consider a scenario where you need to list the members of the team whose level is senior (or other value), then the loader needs to provide a means to add filter conditions.

We can do this by adding UserByLevelLoader in `src.services.user.loader`, which has a class attribute level . After initializing the loader, set `self.level`. The function can be realized. Now the question is how to assign a value to `self.level`.

> The filter field value of a loader instance is immutable. Different filter combinations need to correspond to their respective loader instances.

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

This parameter can be passed in from the Resolver. `loader_filters` specifies the DataLoader subclass and specific parameters to be set, and the values ​​will be assigned during internal execution.

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

By the way, if you need to use the loader multiple times, such as querying two sets of members, level senior and junior, at the same time, you can make a copy of the Loader and then use it as a new Loader.

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
