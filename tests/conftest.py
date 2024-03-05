import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from auth.api.v1.base import api_router as auth_router
from auth.models import User
from config import settings

from game_items.api.v1.base import api_router as game_items_router
from game_items.models import GameItem, CategoryGameItem
from .utils.auth import create_test_user
from .utils.game_items import (
    create_test_game_item, get_test_data_for_game_item, create_category_test_game_item,
    get_test_update_data_for_game_item, get_test_update_data_for_game_item_failed_name
)

engine = create_engine(settings.database_url_live, echo=False)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def start_application():
    """
    Creates and returns an instance of FastAPI app.
    """
    app = FastAPI()
    app.include_router(auth_router)
    app.include_router(game_items_router)
    return app


def drop_tables():
    """
    Drops all tables in live.
    """
    User.metadata.drop_all(bind=engine)
    GameItem.metadata.drop_all(bind=engine)
    CategoryGameItem.metadata.drop_all(bind=engine)


def create_tables():
    """
    Creates all tables in live.
    """
    User.metadata.create_all(bind=engine)
    GameItem.metadata.create_all(bind=engine)
    CategoryGameItem.metadata.create_all(bind=engine)


@pytest.fixture(scope='function', autouse=True)
def setup_tables():
    """
    Creates a db before each test and delete all of them after the test has
    been executed.
    """
    create_tables()
    yield
    drop_tables()


@pytest.fixture(scope='function')
def session(app: FastAPI) -> Session:
    """
    Returns a session to live DB.
    """
    session = SessionTesting()
    yield session
    session.close()


@pytest_asyncio.fixture
async def async_client(app):
    """
    Returns an async client to request app.
    """
    async with AsyncClient(app=app, base_url='http://localhost') as c:
        yield c


@pytest.fixture
def app() -> FastAPI:
    """
    Create a fresh database on each test case.
    """
    return start_application()


@pytest.fixture(scope='function')
def normal_user_token_headers(session: Session):
    return create_test_user(session=session)


@pytest.fixture(scope='function')
def get_game_items(session: Session):
    create_category_test_game_item(session=session)
    return create_test_game_item(session=session)


@pytest.fixture(scope='function')
def create_game_item(session: Session):
    create_category_test_game_item(session=session)
    return get_test_data_for_game_item()


@pytest.fixture(scope='function')
def update_game_item(session: Session):
    create_category_test_game_item(session=session)
    create_test_game_item(session=session)
    return get_test_update_data_for_game_item()


@pytest.fixture(scope='function')
def update_game_item_failed_name(session: Session):
    create_category_test_game_item(session=session)
    create_test_game_item(session=session)
    return get_test_update_data_for_game_item_failed_name()
