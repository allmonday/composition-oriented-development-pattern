from .model import Task

tasks = [
    Task(id=1, name="mvp tech design", owner_id=2, story_id=1),
    Task(id=2, name="implementation", owner_id=2, story_id=1),
    Task(id=3, name="tests", owner_id=2, story_id=1),
    Task(id=4, name="code review", owner_id=2, story_id=1),
    Task(id=5, name="xxx-1", owner_id=3, story_id=2),
    Task(id=6, name="xxx-2", owner_id=4, story_id=3),
    Task(id=7, name="xxx-3", owner_id=2, story_id=4),
    Task(id=8, name="xxx-4", owner_id=5, story_id=5),
    Task(id=9, name="xxx-5", owner_id=2, story_id=6),

    Task(id=10, name="xxx-6", owner_id=5, story_id=7),
    Task(id=11, name="xxx-7", owner_id=5, story_id=8),
    Task(id=12, name="xxx-6", owner_id=7, story_id=9),
    Task(id=13, name="xxx-7", owner_id=6, story_id=9),
]