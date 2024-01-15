from .model import Sprint

_sprints = [
    dict(id=1, name="Sprint A W1", status="close", team_id=1),
    dict(id=2, name="Sprint A W3", status="active", team_id=1),
    dict(id=3, name="Sprint A W5", status="plan", team_id=1),

    dict(id=4, name="Sprint B W1", status="close", team_id=2),
    dict(id=5, name="Sprint B W3", status="active", team_id=2),
    dict(id=6, name="Sprint B W5", status="plan", team_id=2),
]

sprints = [Sprint(**s) for s in _sprints]