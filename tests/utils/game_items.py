from sqlalchemy.orm import Session

from context_manager import TransactionHandler
from game_items.schemas import CreateOrUpdateGameItem, CreateCategoryGameItem
from game_items.services import GameItemsService, GameItemsCategoryService


def create_test_game_item(session: Session) -> dict:
    with TransactionHandler(session):
        return GameItemsService(session=session).create_game_item(
            item_data=CreateOrUpdateGameItem(**get_test_data_for_game_item())
        ).dict()


def create_category_test_game_item(session: Session) -> dict:
    with TransactionHandler(session):
        return GameItemsCategoryService(session=session).create_game_item_category(
            game_item_category_data=CreateCategoryGameItem(**get_test_data_for_game_item_category())
        ).dict()


def get_test_data_for_game_item() -> dict:
    return {
        'name': 'test_name',
        'description': 'test_description',
        'quantity': 2,
        'price': 22.1,
        'category_id': 1,
    }


def get_test_update_data_for_game_item() -> dict:
    return {
        'name': 'test_name_2',
        'description': 'test_description_2',
        'quantity': 3,
        'price': 44.2,
        'category_id': 1,
    }


def get_test_update_data_for_game_item_failed_name() -> dict:
    return {
        'name': 'test_name',
        'description': 'test_description_2',
        'quantity': 3,
        'price': 44.2,
        'category_id': 1,
    }


def get_test_data_for_game_item_category() -> dict:
    return {
        'name': 'test_name',
        'description': 'test_name',
    }
