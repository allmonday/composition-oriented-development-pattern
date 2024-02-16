## service 的测试

在组合模式中, 借助query 和 loader, 我们可以大幅简化测试内容.

本例中 `src/services/conftest.py` 和 `src/services/sprint/tests/conftest` 两个文件一起定义了pytest所需的fixtures.

可以看到该目录下有两个测试文件

- `test_loader.py`
- `test_query.py`

这两个文件构成了 service 测试的基石, 

对于没有session传入的 loader 案例, 通过简单的 mock 也能搞掂.

只要保证所有的 query 和 loader 的测试正确，那么 router 层拼接的 schema 对象就是稳定可靠的。

> pydantic-resolve 通过充分的测试保证组合过程是可靠的.

于是，router 层的 API 测试就没有必要去写了。

> 除非你在 router 层又写了容易出错的额外代码, 如果存在，请对其单独进行测试覆盖。
