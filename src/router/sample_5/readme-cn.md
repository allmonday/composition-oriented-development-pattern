## 利用 Context 和 Schema 实现复用.

进入 `sample_5`

在前面的例子中,我们返回的始终是一个数组, 如果往上想一层, 我定义一个 schema, 这个 schema 包含了一个页面所需要的所有数据, 那会是怎么样?

动手来试一下, 假设页面要展示 summary 和 teams 信息:

```python
class Sample5Root(BaseModel):
    summary: str

    teams: list[Sample5TeamDetail] = []
    async def resolve_teams(self):
        async with db.async_session() as session:
            teams = await tmq.get_teams(session)
            return teams
```

可以看到, 只要把原先 router 中的 query 搬到 schema 里面就好了. so easy. 甚至手动做数据转换的步骤都省略了, 因为 Resolver 会自己做转换.

```python
@route.get('/page-info', response_model=Sample5Root)
async def get_page_info(session: AsyncSession = Depends(db.get_session)):
    page = Sample5Root(summary="hello world")
    page = await Resolver().resolve(page)
    return page
```

router 里面只要初始化一下, 剩下的交给 Resolver 就好了.

> 到这里, 你也许会发现, 定义 schema 的过程和使用 GraphQL 手写查询体的体验是很相似的, 区别是 Resolver 处理的 schema 还需要自己选择 loader 和 schema. 配置多了点, 但是自由度和功能多了许多.
>
> 一个小的最佳实践: resolve_method 中不要自己写业务查询逻辑, 要调用 servcie 中封装好的 query 方法. 这样可以保持 schema 的简洁和拼装的清晰. schema 中要么调用 query, 要么调用 loader, 用配置+组合的思考方式来定义 schema.

让我们更进一步, 让 router 可以接收一个 `team_id` 参数, 然后 teams 变成 team, 这时就可以通过 context 来传递参数了.
context 是一个保留参数, 在所有 resolve 和 post 方法中都可以使用它来获取 Resolver 中定义的参数.

```python
# schema
class Sample5Root(BaseModel):
    summary: str

    team: Optional[Sample5TeamDetail] = None
    async def resolve_team(self, context):
        async with db.async_session() as session:
            team = await tmq.get_team_by_id(session, context['team_id'])
            return team

# router
@route.get('/page-info/{team_id}', response_model=Sample5Root)
async def get_page_info(team_id: int, session: AsyncSession = Depends(db.get_session)):
    page = Sample5Root(summary="hello world")
    page = await Resolver(context={'team_id': team_id}).resolve(page)
    return page
```

使用这种方式, 我们可以拼装出一个可以复用的 schema 组合.