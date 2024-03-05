from typing import Annotated

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi import status

from auth.dependencies import get_current_user
from auth.schemas import CurrentUser

from context_manager import TransactionHandler
from dependencies import get_live_db_session, get_pagination_params
from game_items import schemas
from game_items.api.endpoind_docs.v1.route_game_items import (
    GET_GAME_ITEM_BY_ID_RESPONSES, POST_GAME_ITEMS_RESPONSES, PATCH_GAME_ITEMS_RESPONSES, DELETE_GAME_ITEMS_RESPONSES,
    GET_GAME_ITEMS_RESPONSES
)
from game_items.dependencies import validate_game_item_exists, validate_game_item_category_exists
from game_items.services import GameItemsService, GameItemsCategoryService
from pagination import PaginationParams

router = APIRouter()


@router.get(
    '/items/',
    response_model=list[schemas.GameItem],
    status_code=status.HTTP_200_OK,
    responses=GET_GAME_ITEMS_RESPONSES,
)
async def get_game_items(
        pagination: Annotated[PaginationParams, Depends(get_pagination_params)],
        user: CurrentUser = Depends(get_current_user),
        session: Session = Depends(get_live_db_session),
):
    return GameItemsService(session=session).get_list_game_items(
        pagination=pagination
    )


@router.get(
    '/items/{item_id:int}/',
    response_model=schemas.CreateOrUpdateGameItem,
    status_code=status.HTTP_200_OK,
    responses=GET_GAME_ITEM_BY_ID_RESPONSES,
)
async def get_game_item(
        game_item: Annotated[schemas.GameItem, Depends(validate_game_item_exists)],
        user: CurrentUser = Depends(get_current_user),
):
    return game_item


@router.post(
    '/items/',
    response_model=schemas.CreateOrUpdateGameItem,
    status_code=status.HTTP_201_CREATED,
    responses=POST_GAME_ITEMS_RESPONSES
)
async def create_game_item(
        item_data: schemas.CreateOrUpdateGameItem,
        user: CurrentUser = Depends(get_current_user),
        session: Session = Depends(get_live_db_session),
):
    with TransactionHandler(session):
        return GameItemsService(session=session).create_game_item(
            item_data=item_data
        )


@router.patch(
    '/items/{item_id:int}/',
    response_model=schemas.GameItem,
    status_code=status.HTTP_200_OK,
    responses=PATCH_GAME_ITEMS_RESPONSES
)
async def update_game_item(
        new_game_item_data: schemas.CreateOrUpdateGameItem,
        game_item: Annotated[schemas.GameItem, Depends(validate_game_item_exists)],
        user: CurrentUser = Depends(get_current_user),
        session: Session = Depends(get_live_db_session),
):
    with TransactionHandler(session):
        return GameItemsService(session=session).update_game_item(
            game_item=game_item,
            new_game_item_data=new_game_item_data,
        )


@router.delete(
    '/items/{item_id:int}/',
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETE_GAME_ITEMS_RESPONSES
)
async def delete_game_item(
        game_item: Annotated[schemas.GameItem, Depends(validate_game_item_exists)],
        user: CurrentUser = Depends(get_current_user),
        session: Session = Depends(get_live_db_session),
):
    with TransactionHandler(session):
        return GameItemsService(session=session).delete_game_item(
            game_item=game_item
        )


@router.get(
    '/categories/',
    response_model=list[schemas.CategoryGameItem],
    status_code=status.HTTP_200_OK,
    # responses=SIGN_UP_RESPONSES,
)
async def get_game_items(
        user: CurrentUser = Depends(get_current_user),
        session: Session = Depends(get_live_db_session),
):
    return GameItemsCategoryService(session=session).get_list_game_item_categories()


@router.post(
    '/categories/',
    response_model=schemas.CreateCategoryGameItem,
    status_code=status.HTTP_201_CREATED,
)
async def create_game_item(
        game_item_category_data: schemas.CreateCategoryGameItem,
        user: CurrentUser = Depends(get_current_user),
        session: Session = Depends(get_live_db_session),
):
    with TransactionHandler(session):
        return GameItemsCategoryService(session=session).create_game_item_category(
            game_item_category_data=game_item_category_data
        )


@router.delete(
    '/categories/{game_item_category_id:int}/',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_game_item_category(
        game_item_category: Annotated[schemas.CategoryGameItem, Depends(validate_game_item_category_exists)],
        user: CurrentUser = Depends(get_current_user),
        session: Session = Depends(get_live_db_session),
):
    with TransactionHandler(session):
        return GameItemsCategoryService(session=session).delete_game_item_category(
            game_item_category=game_item_category
        )
