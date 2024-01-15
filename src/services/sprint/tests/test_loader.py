from aiodataloader import DataLoader
import src.db
import src.services.sprint.loader as ld

async def test_loader2(session_factory, monkeypatch):
    monkeypatch.setattr(src.db, 'async_session', session_factory)
    loader = DataLoader(batch_load_fn=ld.team_to_sprint_loader)
    result = await loader.load(2)

    assert len(result) == 3

async def test_loader(session_factory, monkeypatch):
    monkeypatch.setattr(src.db, 'async_session', session_factory)
    loader = DataLoader(batch_load_fn=ld.team_to_sprint_loader)
    result = await loader.load(1)

    assert len(result) == 3
    