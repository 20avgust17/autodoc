from fastapi import FastAPI

from src.auth.api.v1.base import api_router as auth_router
from src.game_items.api.v1.base import api_router as game_items_router


def include_router(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(game_items_router)


def start_application():
    app = FastAPI(title='AutoDoc Test')
    include_router(app)
    return app


app = start_application()
