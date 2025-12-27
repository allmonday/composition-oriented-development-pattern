from fastapi import APIRouter
from pydantic_resolve import Resolver
from .schema import Sample6Root

route = APIRouter(tags=['sample_6'], prefix="/sample_6")

@route.get('/page-info', response_model=Sample6Root)
async def get_page_info_6():
    page = Sample6Root(summary="hello world")
    page = await Resolver().resolve(page)
    return page