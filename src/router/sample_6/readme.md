# 挑选所需的字段

```shell
router-viz -m src.main  --model_prefixs src.servicesls --tags sample_6 --show_fields
```

<img width="1628" height="921" alt="image" src="https://github.com/user-attachments/assets/74c46e13-342f-4cc8-aebf-e027ca2a41e6" />

进入 `sample_6`

既然提到了 GraphQL, 在查询体中可以选择需要的字段, 那么在 Resolver 里面怎么做呢? 以 Sprint 为例, 我不想让 status 字段显示出来.

需要分两步, 第一步是去拷贝一下 Sprint 里面要的字段, 第二步是添加 `@ensure_subset` 装饰器, 它会检查字段是否和 Sprint 中的名字,类型一致 

> 避免修改了 Sprint 之后, 其他复制的字段出现不一致, 否则会给出错误提醒. 

```python
@ensure_subset(sps.Sprint)
class Sample6SprintDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    team_id: int

    stories: list[Sample6StoryDetail] = []
    def resolve_stories(self, loader=LoaderDepend(sl.sprint_to_story_loader)):
        return loader.load(self.id)
```

我们可以通过添加 Field(exclude=True) 来完全隐藏掉字段.
