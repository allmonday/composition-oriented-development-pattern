from fastapi import APIRouter
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import  Depends
from pydantic2_resolve import Resolver
import src.db as db
from .schema import Sample2TeamDetail, Sample2TeamDetailMultipleLevel, SeniorMemberLoader, JuniorMemberLoader
import src.services.team.query as tmq
import src.services.user.loader as ul

route = APIRouter(tags=['sample_2'], prefix="/sample_2")

@route.get('/teams-with-detail', response_model=List[Sample2TeamDetail])
async def get_teams_with_detail(session: AsyncSession = Depends(db.get_session)):
    """1.1 teams with senior members"""
    teams = await tmq.get_teams(session)
    teams = [Sample2TeamDetail.model_validate(t) for t in teams]
    teams = await Resolver(loader_filters={
        ul.UserByLevelLoader: {
            "level": 'senior'
        }
    }).resolve(teams)
    return teams


@route.get('/teams-with-detail-of-multiple-level', response_model=List[Sample2TeamDetailMultipleLevel])
async def get_teams_with_detail_of_multiple_level(session: AsyncSession = Depends(db.get_session)):
    """1.2 teams with senior and junior members"""
    teams = await tmq.get_teams(session)
    teams = [Sample2TeamDetailMultipleLevel.model_validate(t) for t in teams]
    teams = await Resolver(loader_filters={
        SeniorMemberLoader: {
            "level": 'senior'
        },
        JuniorMemberLoader: {
            "level": 'junior'
        }
    }).resolve(teams)
    return teams