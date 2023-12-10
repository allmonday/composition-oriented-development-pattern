from contextlib import asynccontextmanager
from fastapi import FastAPI
import src.db as db
import src.router.sample_1.router as s1_router
import src.router.sample_2.router as s2_router
import src.router.sample_3.router as s3_router
import src.router.sample_4.router as s4_router
import src.router.sample_5.router as s5_router

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