from fastapi import APIRouter

from auth.api.v1.route_users import router

api_router = APIRouter()

api_router.include_router(
    router=router,
    prefix='/auth',
    tags=['Auth']
)

