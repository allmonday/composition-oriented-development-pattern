from fastapi import APIRouter
from pydantic_resolve import Resolver
from .schema import Sample5Root

route = APIRouter(tags=['sample_5'], prefix="/sample_5")

@route.get('/page-info/{team_id}', response_model=Sample5Root)
async def get_page_info(team_id: int):
    page = Sample5Root(summary="hello world")
    page = await Resolver(context={'team_id': team_id}).resolve(page)
    return page