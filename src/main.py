from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Query
import src.db as db
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic2_resolve import LoaderDepend, Resolver

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


# step 1.1
import src.services.user.query as uq
import src.services.user.schema as us
@app.get('/step1/user', response_model=List[us.User])
async def get_step_1_users(session: AsyncSession = Depends(db.get_session)):
    return await uq.get_users(session)


# step 1.2
import src.services.task.query as tq
import src.services.task.schema as ts
@app.get('/step1/tasks', response_model=List[ts.Task])
async def get_step_1_tasks(session: AsyncSession = Depends(db.get_session)):
    return await tq.get_tasks(session)


# step 1.3
import src.services.user.loader as ul
class TaskDetail(ts.Task):
    user: Optional[us.User] = None
    def resolve_user(self, loader=LoaderDepend(ul.user_batch_loader)):
        return loader.load(self.owner_id)

@app.get('/step1/tasks2', response_model=List[TaskDetail])
async def get_step_1_tasks_2(session: AsyncSession = Depends(db.get_session)):
    tasks = await tq.get_tasks(session)
    tasks = [TaskDetail.model_validate(t) for t in tasks]
    tasks = await Resolver().resolve(tasks)
    return tasks