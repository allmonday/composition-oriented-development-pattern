## Pick the required fields

Enter `sample_6`

Now that GraphQL is mentioned, you can select the required fields in the query body, so how do you do it in Resolver? Taking Sprint as an example, I don't want the status field to be displayed.

It needs to be divided into two steps. The first step is to copy the fields required in Sprint. The second step is to add the `@ensure_subset` decorator. It will check whether the field is consistent with the name and type in Sprint (to avoid modification After Sprint, if other copied fields are inconsistent, an error reminder will be given.)

> The current implementation is a bit cumbersome to manually copy fields. In the next stage, we plan to only provide a list of field names in the decorator.

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
