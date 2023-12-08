# 可组合的API开发模式

在构建关系型数据的API时, 怎么寻找一个兼顾灵活, 性能, 可维护的方案?  我希望它能够:
- 支持异步
- 支持定义多层的数据结构, 定义方式要简洁, 扩展要友好, 支持列表
- 可以传入参数
- 利用Dataloader 避免 N+1 查询
- 避免GraphQL一套接口提供所有服务的模式, 每个API 接口都有能力快速定义自己所需的类型.
- 提供 **每层对象** 在`resolve` 完子孙数据后, 做额外计算的能力
- 挑选需要的返回字段 (类似GraphQL 编辑 query)

这个repo 会通过一系列的例子, 结合 `pydantic2-resolve`, 来定义这样一套灵活的面向组合的开发模式.

## Roadmap:
- ~~简单列表~~
- ~~嵌套列表~~
- 多层嵌套列表
- Dataloader 的复用
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

在`src.router.sample_1` 中，我们依次创建 users, tasks 的API， 以`list[T]`的形式返回。

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

> 为了避免类型名字重复,使用router名字作为前缀
>
> 因此 Sample1 开头的 schema 都是属于 sample_1 路由的 (这点在生成前端sdk ts 类型的时候会很有用.)

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


在 `router.py` 中, 依然是通过 `tq.get_tasks(session)` 来获取初始数据, 接着转换成 `Sample1TaskDetail`.  之后交给 `Resolver` 就能 `resolve` 出所有 `user` 信息.

```python
@route.get('/tasks-with-detail', response_model=List[Sample1TaskDetail])
async def get_tasks_with_detail(session: AsyncSession = Depends(db.get_session)):
    """ 1.3 return list of tasks(user) """
    tasks = await tq.get_tasks(session)
    tasks = [Sample1TaskDetail.model_validate(t) for t in tasks]
    tasks = await Resolver().resolve(tasks)
    return tasks
```






