from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.routing import APIRoute
import src.db as db
import src.router.sample_1.router as s1_router
import src.router.sample_2.router as s2_router
import src.router.sample_3.router as s3_router
import src.router.sample_4.router as s4_router
import src.router.sample_5.router as s5_router
import src.router.sample_6.router as s6_router
import src.router.sample_7.router as s7_router
import src.router.demo.router as demo_router
from fastapi_voyager import create_voyager
from src.services.er_diagram import BaseEntity
from pydantic_resolve import config_global_resolver

diagram = BaseEntity.get_diagram()

config_global_resolver(diagram)

async def startup():
    print('start')
    await db.init()
    await db.prepare()
    print('done')

async def shutdown():
    print('end start')
    await db.engine.dispose()
    print('end done')

@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()

app = FastAPI(debug=True, lifespan=lifespan)


app.include_router(s1_router.route)
app.include_router(s2_router.route)
app.include_router(s3_router.route)
app.include_router(s4_router.route)
app.include_router(s5_router.route)
app.include_router(s6_router.route)
app.include_router(s7_router.route)
app.include_router(demo_router.route)

app.mount('/voyager', 
          create_voyager(
            app, 
            er_diagram=diagram,
            module_color={'src.services': 'purple'}, 
            module_prefix='src.services', 
            swagger_url="/docs",
            ga_id="G-R64S7Q49VL",
            initial_page_policy='first',
            online_repo_url='https://github.com/allmonday/composition-oriented-development-pattern/blob/master',
            enable_pydantic_resolve_meta=True))


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name  # in this case, 'read_items'

use_route_names_as_operation_ids(app)