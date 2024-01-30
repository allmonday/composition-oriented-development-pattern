## pydantic-resolve 和 GraphQL 框架比较

### GraphQL

graphql 优点

- client 可以根据查询动态获取数据
- introspection 可以看到所有字段
- 强类型
- 前后端分离的场景开发体验较好, 对前端友好

graphql 缺点

- 缺少层级之间进行数据二次处理的能力. 比如上层无法在下层数据获取后进行额外操作.
- 如果是全栈开发，后端和写 query 有重复劳动
- 前后端需要引入 graphql 相关框架
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


### 使用 GraphQL 正确的姿势

graphql 的使用思路有两种

一种是根据数据的ER，构建关系型查询
典型的比如github，jira 提供的graphql接口

用户熟悉这种固定的ER，查询到规范的数据之后自己再做二次加工。换言之你哪怕有定制化的需求，也只能自己想办法处理，不可能向他们提出这种要求。

另一种是面向业务，构建的是业务层的查询接口
这种场景并不适合graphql，他对查询的数据定制化要求高，意味着通过通用接口拿到的数据往往需要根据业务做再加工，而且也会和后端商量，定制一些面向专用页面的graphql 接口。这也会慢慢变成常态，因为很多数据并不适合暴露到前端做二次处理。
对于一整套业务，graphql 这样一个灵活的中间层反而对业务的整体清晰度造成了影响。

结论就是，graphql 适合稳定的，轻业务概念的数据的组合查询。而不适合面向具体业务，高度定制化的场景。