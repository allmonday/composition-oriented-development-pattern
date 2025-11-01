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
            module_color={'src.services': 'tomato'}, 
            module_prefix='src.services', 
            swagger_url="/docs",
            online_repo_url='https://github.com/allmonday/composition-oriented-development-pattern/blob/master'))


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