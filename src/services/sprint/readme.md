## Test of service

You can see that there are two test files in this directory

- `test_loader.py`
- `test_query.py`

These two files form the basis of the service integration test.

As long as all queries and loaders are tested correctly, the router layer will be stable and reliable based on the schema objects they splice together.

Therefore, API testing at the router layer is not that necessary.

> Unless you write additional error-prone code in the router layer
>
> If present, perform separate test coverage on it.
