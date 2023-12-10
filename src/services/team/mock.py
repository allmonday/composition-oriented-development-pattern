from .model import Team, TeamUser

teams = [
    Team(id=1, name="team-A"),
    Team(id=2, name="team-B")
]

team_users = [
    TeamUser(id=1, user_id=1, team_id=1),
    TeamUser(id=2, user_id=2, team_id=1),
    TeamUser(id=3, user_id=3, team_id=1),
    TeamUser(id=4, user_id=4, team_id=1),

    TeamUser(id=5, user_id=5, team_id=2),
    TeamUser(id=6, user_id=6, team_id=2),
    TeamUser(id=7, user_id=7, team_id=2),
]