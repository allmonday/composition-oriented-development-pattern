## Loader reuses

Enter sample_5

In the previous example, what we returned was always an array. If we think about it one level higher, what would happen if I defined a schema that contains all the data needed for a page?

Let’s try it out, assuming the page wants to display summary and teams information:

```python
class Sample5Root(BaseModel):
    summary: str

    teams: list[Sample5TeamDetail] = []
    async def resolve_teams(self):
        async with db.async_session() as session:
            teams = await tmq.get_teams(session)
            return teams
```

As you can see, just move the query in the original router to the schema. So easy. Even the steps of manual data conversion are omitted, because Resolver will do the conversion by itself.

```python
@route.get('/page-info', response_model=Sample5Root)
async def get_page_info(session: AsyncSession = Depends(db.get_session)):
    page = Sample5Root(summary="hello world")
    page = await Resolver().resolve(page)
    return page
```

The router only needs to be initialized and the Resolver will do the rest.

> At this point, you may find that the process of defining a schema is very similar to the experience of using a GraphQL handwritten query. The difference is that the schema processed by the Resolver requires you to choose the loader and schema yourself. There is a little more configuration, but there is more freedom and functionality. A lot.
>
> A small best practice: Do not write your own business query logic in resolve_method, but call the query method encapsulated in servcie. This can keep the schema concise and the assembly clear. In the schema, either call query or loader, use the configured Think about the way you define a schema.

Let's go one step further and allow the router to receive a team_id parameter, and then teams becomes team. At this time, parameters can be passed through context. context is a reserved parameter that is used in all resolve and post methods. This can be used to obtain parameters defined in the Resolver.

```python
# router
@route.get('/page-info/{team_id}', response_model=Sample5Root)
async def get_page_info(team_id: int, session: AsyncSession = Depends(db.get_session)):
    page = Sample5Root(summary="hello world")
    page = await Resolver(context={'team_id': team_id}).resolve(page)
    return page

# schema
class Sample5Root(BaseModel):
    summary: str

    team: Optional[Sample5TeamDetail] = None
    async def resolve_team(self, context):
        async with db.async_session() as session:
            team = await tmq.get_team_by_id(session, context['team_id'])
            return team
```
