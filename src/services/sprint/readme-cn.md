## service 的测试

可以看到该目录下有两个测试文件

- `test_loader.py`
- `test_query.py`

这两个文件构成了 service integration test 的基础。

只要保证所有的 query 和 loader 的测试正确，那么 router 层基于他们拼接的 schema 对象就是稳定可靠的。

于是，router 层的 API 测试就没有必要了。

> 除非你在 router 层又写了容易出错的额外代码
>
> 如果存在， 请对其单独进行测试覆盖。
