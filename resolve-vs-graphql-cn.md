## pydantic-resolve 和 GraphQL 框架比较

### GraphQL

graphql 优点

- client 可以根据查询动态获取数据
- introspection 可以看到所有字段
- 强类型
- 前后端分离的场景开发体验较好, 对前端友好

graphql 缺点

- 缺少层级之间进行数据聚合的能力
- 如果是全栈开发，后端和写 query 有重复劳动
- 后端需要引入 graphql 相关框架
- cache， authority, rate limit 控制起来不容易
- 对后端不太友好

### Pydantic-resolve

pydantic-resolve 优点：

- 提供了各种数据组合的能力
- 强类型（pydantic）
- 提供了 hook 来修改数据
- 和 restful 接口无缝衔接，平滑过度
- 非常适合全栈开发，自己实现好接口之后直接生成 ts sdk
- cache, authority, rate 之类的功能不受影响
- 接口独立，容易做性能调试
- 对前后端都很友好

pydantic-resolve 缺点：

- 查看组合类型需要通过 OpenAPI 查看 response 信息
- 前后端分离的情况，没有后端一个万能接口来得方便
- Friend -> Friend 的 graph 描述不方便
