import logging
from typing import Type

from sqlalchemy.orm import Session
from fastapi import status

import utils
from game_items import models, schemas
from game_items.models import GameItem
from pagination import PaginationParams


class GameItemsService:

    def __init__(self, session: Session):
        self.session = session

    def get_list_game_items(self, pagination: PaginationParams) -> list[Type[GameItem]]:
        return self.session.query(models.GameItem).offset(pagination.skip).limit(pagination.limit).all()

    def get_game_items_by_id(self, item_id: int) -> models.GameItem | None:
        return self.session.query(models.GameItem).filter(models.GameItem.id == item_id).first()

    def get_game_items_by_name(self, game_item_name: str) -> models.GameItem | None:
        return self.session.query(models.GameItem).filter(models.GameItem.name == game_item_name).first()

    def create_game_item(self, item_data: schemas.CreateOrUpdateGameItem) -> schemas.CreateOrUpdateGameItem:
        self.check_name_is_unique(item_data.name)
        self.exist_category(item_data.category_id)
        self.session.add(models.GameItem(**vars(item_data)))
        logging.info('Game item created with following data `%s`', item_data)
        return item_data

    def update_game_item(self, game_item, new_game_item_data: schemas.CreateOrUpdateGameItem) -> models.GameItem:
        self.check_name_is_unique(new_game_item_data.name)
        self.exist_category(new_game_item_data.category_id)
        # Updating game item with new data
        old_values = {}
        new_values = {}
        for field, new_value in new_game_item_data:
            if (old_value := getattr(game_item, field)) != new_value:
                old_values[field] = str(old_value)
                new_values[field] = str(new_value)
                setattr(game_item, field, new_value)

        logging.info('Game item updated with following data `%s`', new_game_item_data)
        return game_item

    def delete_game_item(self, game_item: models.GameItem) -> None:
        self.session.delete(game_item)
        logging.info('Game item with id `%s` was deleted', game_item.id)

    def check_name_is_unique(self, game_item_name: str):
        return utils.raise_exception_if_true(
            item=self.get_game_items_by_name(game_item_name=game_item_name),
            on_error_message='Name already exists.',
            status_code=status.HTTP_409_CONFLICT
        )

    def exist_category(self, category_id: int):
        return utils.raise_exception_if_true(
            item=not GameItemsCategoryService(self.session).get_game_item_category_by_id(category_id=category_id),
            on_error_message=f"Category with id: {category_id} doesn't exist.",
            status_code=status.HTTP_404_NOT_FOUND
        )


class GameItemsCategoryService:

    def __init__(self, session: Session):
        self.session = session

    def get_list_game_item_categories(self) -> list[Type[models.CategoryGameItem]]:
        return self.session.query(models.CategoryGameItem).all()

    def get_game_item_category_by_id(self, category_id: int):
        return self.session.query(models.CategoryGameItem).filter(models.CategoryGameItem.id == category_id).first()

    def get_game_item_category_by_name(self, category_name: str):
        return self.session.query(models.CategoryGameItem).filter(models.CategoryGameItem.name == category_name).first()

    def create_game_item_category(self, game_item_category_data: schemas.CreateCategoryGameItem):
        self.check_name_is_unique(game_item_category_data.name)
        self.session.add(models.CategoryGameItem(**vars(game_item_category_data)))
        logging.info('Game item category created with following data `%s`', game_item_category_data)
        return game_item_category_data

    def delete_game_item_category(self, game_item_category):
        self.session.delete(game_item_category)
        logging.info('Game item category with id `%s` was deleted', game_item_category.id)

    def check_name_is_unique(self, category_name):
        return utils.raise_exception_if_true(
            item=self.get_game_item_category_by_name(category_name=category_name),
            on_error_message='Name already exists.',
            status_code=status.HTTP_409_CONFLICT
        )
