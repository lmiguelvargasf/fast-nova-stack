from contextlib import asynccontextmanager

from fastapi import FastAPI
from piccolo.apps.user.tables import BaseUser
from piccolo_admin.endpoints import create_admin
from strawberry.fastapi import GraphQLRouter

from .db import close_database_connection_pool, open_database_connection_pool
from .schema import schema


@asynccontextmanager
async def lifespan(app: FastAPI):
    open_database_connection_pool()
    yield
    close_database_connection_pool()


app = FastAPI(lifespan=lifespan)
graphql_app = GraphQLRouter(schema, path="/graphql")
app.include_router(graphql_app)


@app.get("/health")
def health_check():
    return {"status": "ok"}


admin = create_admin(tables=[BaseUser])
app.mount("/admin/", admin)
