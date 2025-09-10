To begin, we will start step by step, transitioning from an API that returns a single-layer task list to an API that returns a multi-layer Teams list.

## Simple list

routers:

- `sample_1.router:get_users`
- `sample_1.router:get_tasks`

In `src.router.sample_1`, we will sequentially create APIs for users and tasks, returning them in the form of list[T].

```python
import src.services.task.query as tq

@route.get('/tasks', response_model=List[ts.Task])
async def get_step_1_tasks(session: AsyncSession = Depends(db.get_session)):
    """ 1.2 return list of tasks """
    return await tq.get_tasks(session)
```

by importing queries from `src.services.user.query` and `src.services.task.query`, we can get `list[orm]`, and then FastAPI will automatically convert the objects into the corresponding types defined in response_model

## Nested lists

Next, we need to add user information to the task, create schema.py in the sample_1 directory, and define a Sample1TaskDetail type that extends user information.

> To avoid duplication of type names, use the router name as a prefix
>
> The schema at the beginning of Sample1 all belongs to the sample_1 route (this will be very useful when generating the front-end sdk ts type.)

```python
class Sample1TaskDetail(ts.Task):
    user: Optional[us.User] = None
    def resolve_user(self, loader=LoaderDepend(ul.user_batch_loader)):
        return loader.load(self.owner_id)
```

A few points to note::

1. After inheriting ts.Task , Sample1TaskDetail can be assigned with the orm object returned by `tq.get_tasks(session)`.
2. Defining `user` needs to add a default value, otherwise using Sample1TaskDetail.model_valiate will report a missing field error.
3. `ul.user_batch_loader` will associate task and user objects based on `list[task.owner_id]` . See src.services.user.loader for details.

> The data returned by resolve needs to be a type that pydantic can convert.
>
> If it is an orm object, it needs to be configured `ConfigDict(from_attribute=True)`

In router.py , the initial data is still obtained through `tq.get_tasks(session)` , and then converted into Sample1TaskDetail . Then it can be resolved by handing it to Resolver to get all `user` information.

```python
@route.get('/tasks-with-detail', response_model=List[Sample1TaskDetail])
async def get_tasks_with_detail(session: AsyncSession = Depends(db.get_session)):
    """ 1.3 return list of tasks(user) """
    tasks = await tq.get_tasks(session)
    tasks = [Sample1TaskDetail.model_validate(t) for t in tasks]
    tasks = await Resolver().resolve(tasks)
    return tasks
```

## Multi-level nested lists

Using the same method, we gradually built from `tasks-with-details` to `teams-with-details` . Although it is nested layer by layer, the definition method is very simple.

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

## Use of Dataloader

The function of Dataloader is to collect all parent_ids to be queried, query all childrent objects at once, and then aggregate them according to the parent_id of the child.

Data relationships may be 1:1, 1:N, M:N. From the parent's perspective, there are only two types: 1:1 and 1:N. Corresponding to these two situations, pydantic2-resolve provides two auxiliary functions

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

You can see that the 1:1 relational query id is the primary key of the target. The query is very simple, so it has the highest reusability.

The 1:N query requires a corresponding relationship table to determine, so the reuse is limited to the parent type.

### 1:1

Using story as an example, story.owner_id specifies the person in charge of a story. If you need to add user information to the story, you only need to directly reuse the user_batch_loader method.

```python
class Sample1StoryDetail(ss.Story):
    tasks: list[Sample1TaskDetail] = []
    def resolve_tasks(self, loader=LoaderDepend(tl.story_to_task_loader)):
        return loader.load(self.id)

    owner: Optional[us.User] = None
    def resolve_owner(self, loader=LoaderDepend(ul.user_batch_loader)):
        return loader.load(self.owner_id)
```

The output can be viewed in swagger.

### 1:N

Taking teams as an example, the team_user table maintains the relationship between team and user. So our loader needs to join team_user to query user.

Therefore, the reuse of this type of dataloader follows the parent type.

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

Then go to `sample_1.schema:Sample1TeamDetail` and add members(user) and the loader you just created.

```python

class Sample1TeamDetail(tms.Team):
    sprints: list[Sample1SprintDetail] = []
    def resolve_sprints(self, loader=LoaderDepend(spl.team_to_sprint_loader)):
        return loader.load(self.id)

    members: list[us.User] = []
    def resolve_members(self, loader=LoaderDepend(ul.team_to_user_loader)):
        return loader.load(self.id)
```

> By the way, resolve_method does not need to be defined from the top class. Resolver will be traversed recursively and find resolver_method for parsing.

At this point, the reusability of Dataloader has been introduced.
