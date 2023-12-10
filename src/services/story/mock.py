from .model import Story

stories = [
    Story(id=1, name="deliver a MVP", owner_id=1, sprint_id=1),
    Story(id=2, name="some tests", owner_id=1, sprint_id=1),
    Story(id=3, name="deliver a beeter MVP", owner_id=2, sprint_id=2),
    Story(id=4, name="more tests", owner_id=2, sprint_id=2),
    Story(id=5, name="next phase design", owner_id=2, sprint_id=3),
    Story(id=6, name="non function requirements", owner_id=2, sprint_id=3),

    Story(id=7, name="requirement colelction", owner_id=5, sprint_id=4),
    Story(id=8, name="UI/UX design", owner_id=5, sprint_id=5),
    Story(id=9, name="prod design", owner_id=6, sprint_id=6),
]