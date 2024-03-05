from sqlalchemy.orm import Session

from auth import schemas
from auth.services import AuthService
from context_manager import TransactionHandler


def create_test_user(session: Session):
    user_data = {
        'name': f'user_name',
        'description': 'test_description',
        'hashed_password': 'test_password'
    }
    with TransactionHandler(session):
        return AuthService(session=session).create_user(
            user_data=schemas.CreateUser(**user_data)
        )
