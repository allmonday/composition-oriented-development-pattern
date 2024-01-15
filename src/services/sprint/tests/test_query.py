import src.services.sprint.query as sq

async def test_sprint_by_id2(session):
    result = await sq.get_sprints_by_ids([1], session)
    assert len(result) == 1
    assert result[0].name == 'Sprint A W1'
