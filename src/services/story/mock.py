from .model import Story

stories = [
    Story(id=1, name="deliver a MVP", owner_id=1, sprint_id=1),
    Story(id=2, name="Doing some tests", owner_id=1, sprint_id=1),

    Story(id=3, name="deliver a beeter MVP", owner_id=2, sprint_id=2),
    Story(id=4, name="Doing more tests", owner_id=2, sprint_id=2),

    # Story(id=5, name="deliver a beeter MVP", owner_id=2, sprint_id=2),
    # Story(id=6, name="Doing more tests", owner_id=2, sprint_id=2),
]