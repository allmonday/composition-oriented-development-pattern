from pydantic_resolve import ErDiagram, Entity, Relationship
from src.services.team.schema import Team
from src.services.sprint.schema import Sprint
from src.services.story.schema import Story
from src.services.task.schema import Task
from src.services.user.schema import User
import src.services.sprint.loader as sprint_loader
import src.services.user.loader as user_loader
import src.services.story.loader as story_loader
import src.services.task.loader as task_loader

diagram = ErDiagram(
    configs=[
        Entity(
            kls=Team,
            relationships=[
                Relationship( field='id', target_kls=list[Sprint], loader=sprint_loader.team_to_sprint_loader),
                Relationship( field='id', target_kls=list[User], loader=user_loader.team_to_user_loader)
            ]
        ),
        Entity(
            kls=Sprint,
            relationships=[
                Relationship( field='id', target_kls=list[Story], loader=story_loader.sprint_to_story_loader)
            ]
        ),
        Entity(
            kls=Story,
            relationships=[
                Relationship( field='id', target_kls=list[Task], loader=task_loader.story_to_task_loader),
                Relationship( field='owner_id', target_kls=User, loader=user_loader.user_batch_loader)
            ]
        ),
        Entity(
            kls=Task,
            relationships=[
                Relationship( field='owner_id', target_kls=User, loader=user_loader.user_batch_loader)
            ]
        )
    ]
)