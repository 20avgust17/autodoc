from fastapi import APIRouter, Depends
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth import schemas

from auth.services import AuthService
from context_manager import TransactionHandler
from dependencies import get_live_db_session

router = APIRouter()


@router.post(
    '/sign-up/',
    response_model=schemas.Token,
    status_code=status.HTTP_201_CREATED,
)
async def sign_up(
        user_data: schemas.CreateUser,
        session: Session = Depends(get_live_db_session),
):
    with TransactionHandler(session):
        return AuthService(session=session).create_user(user_data)


@router.post(
    '/sign-in/',
    response_model=schemas.Token,
    status_code=status.HTTP_200_OK,
)
async def sign_in(
        auth_data: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_live_db_session),
):
    with TransactionHandler(session):
        return AuthService(session=session).authenticate_user(
            username=auth_data.username,
            password=auth_data.password,
        )
