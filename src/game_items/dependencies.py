from typing import Annotated

from fastapi import Depends, status
from sqlalchemy.orm import Session

import utils
from dependencies import get_live_db_session

from game_items.models import GameItem, CategoryGameItem
from game_items.services import GameItemsService, GameItemsCategoryService


def validate_game_item_exists(
        item_id: int,
        session: Annotated[Session, Depends(get_live_db_session)],
) -> GameItem:
    utils.raise_exception_if_true(
        item=not (game_item := GameItemsService(session=session).get_game_items_by_id(item_id)),
        on_error_message="The game item with id '%s' doesn't exist." % item_id,
        status_code=status.HTTP_404_NOT_FOUND
    )
    return game_item


def validate_game_item_category_exists(
        game_item_category_id: int,
        session: Annotated[Session, Depends(get_live_db_session)],
) -> CategoryGameItem:
    utils.raise_exception_if_true(
        item=not (
            category_game_item := GameItemsCategoryService(session=session).get_game_item_category_by_id(
                game_item_category_id
            )
        ),
        on_error_message="The game item category with id '%s' doesn't exist." % game_item_category_id,
        status_code=status.HTTP_404_NOT_FOUND
    )
    return category_game_item
