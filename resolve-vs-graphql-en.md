## Comparison of pydantic-resolve and GraphQL frameworks

### GraphQL

GraphQL advantages

- The client can dynamically obtain data based on the query
- introspection can see all fields
- Strongly typed
- The scenario development experience with separation of front and back ends is better and is friendly to the front end.

GraphQL Disadvantages

- Lack of ability to perform data aggregation between tiers
- If it is full-stack development, there is duplication of work in the backend and writing queries.
- The backend needs to introduce graphql related framework
- Cache, authority, rate limit are not easy to control
- Not very friendly to the backend

### Pydantic-resolve

pydantic-resolve advantage：

- Provides the ability to combine various data
- Strong typing (pydantic)
- Provides hooks to modify data
- Seamless connection with RESTful interface, smooth transition
- It is very suitable for full-stack development. After implementing the interface yourself, you can directly generate ts sdk.
- Functions such as cache, authority, rate are not affected
- Interface independent, easy to do performance debugging
- Friendly to both front and back ends

pydantic-resolve disadvantages：

- To view the combination type, you need to view the response information through OpenAPI
- When the front and back ends are separated, it is not convenient to have a universal interface on the back end.
- Friend -> Friend graph expression is not friendly to define
