from fastapi import APIRouter

from game_items.api.v1.route_game_items import router

api_router = APIRouter()

api_router.include_router(
    router=router,
    prefix='/items_manager',
    tags=['Manager items for CyberPunk 2077']
)

