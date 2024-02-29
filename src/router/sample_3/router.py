from fastapi import APIRouter
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import  Depends
from pydantic_resolve import Resolver
import src.db as db
from .schema import Sample3TeamDetail
import src.services.team.query as tmq
import src.services.user.loader as ul

route = APIRouter(tags=['sample_3'], prefix="/sample_3")

@route.get('/teams-with-detail', response_model=List[Sample3TeamDetail])
async def get_teams_with_detail(session: AsyncSession = Depends(db.get_session)):
    """
    1.1 expose (provide) ancestor data to descendant node. 
    """
    teams = await tmq.get_teams(session)
    teams = [Sample3TeamDetail.model_validate(t) for t in teams]
    teams = await Resolver().resolve(teams)
    return teams