## Use of Loader instance

Normally loader instance is instantiated and maintained internally by Resolver.

If you already have a loader, and the loader has added data through the `prime` method, you can use the loader_instance parameter to pass in the Resolver internally to skip the initialization process and use it directly. The loader instance passed in.

Taking UserLoader as an example, you can use a real and available `loader src.service.user.loader:user_batch_loader`, or you can use `generate_single_empty_loader` to generate a Loader class.

The difference between the two is that if the data passed in by `loader.load`(key) is not in the loader cache, batch_load_fn will be triggered to query, while `generate_single_empty_loader` will do nothing, if it does not exist, return None

> generate_list_empty_loader returns [] by default

schema

```python
UserLoader = generate_single_empty_loader('UserLoader')

class Sample7TaskDetail(ts.Task):
    user: Optional[us.User] = None
    def resolve_user(self, loader=LoaderDepend(UserLoader)):
        return loader.load(self.owner_id)
```

In the router, `add_single_to_loader` is used to handle the prime logic. It simulates pre-fetching user information, adds it to the loader, and then provides it to Sample7TaskDetail.

If you comment the `add_single_to_loader` method, you will find that all users are None

```python
def add_single_to_loader(loader, items, get_key):
    _map = {}
    for item in items:
        _map[get_key(item)] = item
    for k, v in _map.items():
        loader.prime(k, v)

@route.get('/tasks', response_model=list[Sample7TaskDetail])
async def get_tasks(session: AsyncSession = Depends(db.get_session)):
    users = await uq.get_users(session)
    user_loader = UserLoader()
    add_single_to_loader(user_loader, users, lambda u: u.id)

    tasks = await tskq.get_tasks(session)
    tasks = [Sample7TaskDetail.model_validate(t) for t in tasks]
    tasks = await Resolver(loader_instances={UserLoader: user_loader}).resolve(tasks)
    return tasks
```

In the slightly more complex second example, we start from user[1] and traverse through each layer to find the stories owned by the user, the sprints to which each story belongs, and the teams to which each sprint belongs. The display starts from the Teams level and continues to unfold layer by layer.

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
