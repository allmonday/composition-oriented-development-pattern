## 挑选所需的字段

进入 `sample_6`

既然提到了 GraphQL, 在查询体中可以选择需要的字段, 那么在 Resolver里面怎么做呢? 以 Sprint为例, 我不想让 status 字段显示出来.

需要分两步, 第一步是去拷贝一下 Sprint 里面要的字段, 第二步是添加 `@ensure_subset` 装饰器, 它会检查字段是否和 Sprint 中的名字,类型一致 (避免修改了 Sprint 之后, 其他复制的字段出现不一致, 这样就会给出错误提醒. )

> 当前的实现要手动复制字段还是有点啰嗦的, 下个阶段计划只需要在装饰器中提供字段名字列表.

```python
@ensure_subset(sps.Sprint)
class Sample6SprintDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    # status: str
    team_id: int

    stories: list[Sample6StoryDetail] = []
    def resolve_stories(self, loader=LoaderDepend(sl.sprint_to_story_loader)):
        return loader.load(self.id)
```