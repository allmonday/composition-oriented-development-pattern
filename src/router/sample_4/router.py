from fastapi import APIRouter
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import  Depends
from pydantic_resolve import Resolver
import src.db as db
from .schema import Sample4TeamDetail
import src.services.team.query as tmq
import src.services.user.loader as ul

route = APIRouter(tags=['sample_4'], prefix="/sample_4")

@route.get('/teams-with-detail', response_model=List[Sample4TeamDetail])
async def get_teams_with_detail(session: AsyncSession = Depends(db.get_session)):
    teams = await tmq.get_teams(session)
    teams = [Sample4TeamDetail.model_validate(t) for t in teams]
    teams = await Resolver().resolve(teams)
    return teams