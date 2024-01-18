## Post hooks

Enter sample_4

This time I want to add the task_count field to team, sprint, and story to count the total number of tasks included in each level.

This can be done using post_method . post_method will be executed synchronously after all resolve_methods of the class are executed.

> Yes, as a post hook, it does not support async

```python
class Sample4StoryDetail(ss.Story):
    tasks: list[Sample4TaskDetail] = []
    def resolve_tasks(self, loader=LoaderDepend(tl.story_to_task_loader)):
        return loader.load(self.id)

    task_count: int = 0
    def post_task_count(self):
        return len(self.tasks)

class Sample4SprintDetail(sps.Sprint):
    stories: list[Sample4StoryDetail] = []
    def resolve_stories(self, loader=LoaderDepend(sl.sprint_to_story_loader)):
        return loader.load(self.id)

    task_count: int = 0
    def post_task_count(self):
        return sum([s.task_count for s in self.stories])

class Sample4TeamDetail(tms.Team):
    sprints: list[Sample4SprintDetail] = []
    def resolve_sprints(self, loader=LoaderDepend(spl.team_to_sprint_loader)):
        return loader.load(self.id)

    task_count: int = 0
    def post_task_count(self):
        return sum([s.task_count for s in self.sprints])
```

Starting from Story, each layer defines a task_count field, and then post_task_count will be executed after the tasks data is obtained to calculate `self.task`

After all post methods are executed, it means that resolve_stories in Sprint has been executed. Then post_task_count in Sprint starts to execute, and the task_count of all stories is added up.

The same logic applies to Team above.

Finally, the task_count in each layer can be calculated.

By the way, in the post method, there is a special method `post_default_handler`, which will be executed after all post_method have been executed. We can do some interesting functions with it:

For example, we can add a description to Team to summarize how many tasks the team has. Because `default_post_handler` will be executed after resolve and post are executed, all the information (task_count) can be obtained to generate the description.

```python
class Sample4TeamDetail(tms.Team):
    sprints: list[Sample4SprintDetail] = []
    def resolve_sprints(self, loader=LoaderDepend(spl.team_to_sprint_loader)):
        return loader.load(self.id)

    task_count: int = 0
    def post_task_count(self):
        return sum([s.task_count for s in self.sprints])

    description: str = ''
    def post_default_handler(self):
        self.description = f'team: {self.name} has {self.task_count} tasks in total.'
```
