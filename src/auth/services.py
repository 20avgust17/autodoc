import logging
from datetime import datetime, timedelta

from passlib.hash import bcrypt
from fastapi import HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError, ExpiredSignatureError
from pydantic import ValidationError
from sqlalchemy.orm import Session

import utils
from auth import schemas, models
from config import settings


class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):

    async def __call__(self, request: Request = None):
        try:
            return await super().__call__(request)
        except HTTPException as e:
            raise e


oauth2_scheme = CustomOAuth2PasswordBearer(tokenUrl='/auth/sign-in/')


class AuthService:

    def __init__(self, session: Session):
        self.session = session

    def create_user(
            self,
            user_data: schemas.CreateUser
    ) -> schemas.Token:
        try:
            user = self._create_user(
                name=user_data.name,
                plain_password=user_data.hashed_password,
                description=user_data.description,
            )
            self.session.add(user)
            self.session.flush()
            self.session.commit()
            return self.create_token(user)
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Detail: {ex}",
            )

    def authenticate_user(
            self,
            username: str,
            password: str
    ):
        exception_kwargs = {
            'status_code': status.HTTP_401_UNAUTHORIZED,
            'headers': {'WWW-Authenticate': 'Bearer'},
        }
        user = self.get_user_by_username(username)
        utils.raise_exception_if_true(
            item=not user,
            on_error_message="User with the following username %s doesn't exist" % username,
            status_code=status.HTTP_404_NOT_FOUND
        )
        self.validate_user_is_active(
            user=user,
            on_error_message='User with the following username %s is not active' % username
        )
        self._validate_password(
            plain_password=password,
            hashed_password=user.hashed_password,
            on_error_message="Provided password isn't correct",
            **exception_kwargs
        )
        return self.create_token(user)

    def verify_user(self, token: str) -> models.User:
        return self._get_user_by_id(self.verify_token(token).id)

    def _get_user_by_id(self, user_id: int) -> models.User | None:
        user = self.session.query(models.User).filter(models.User.id == user_id).first()
        return user

    def _create_user(
            self,
            name: str,
            plain_password: str,
            description: str,
    ) -> models.User:
        """
        Creates a new `db.User` instance. Automatically hashes a provided
        password.
        """
        return models.User(
            name=name,
            hashed_password=self.hash_password(plain_password),
            description=description,
        )

    @staticmethod
    def verify_token(
            token: str
    ) -> schemas.CurrentUser:
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )
            user = schemas.CurrentUser.parse_obj(payload.get('user'))
            return user
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Your authorization token was expired. Please update it in your Pulse profile',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        except (JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate credentials',
                headers={'WWW-Authenticate': 'Bearer'},
            )

    def get_user_by_username(self, name: str) -> models.User | None:
        return self.session.query(models.User).filter(models.User.name == name).first()

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hash(password)

    @staticmethod
    def _validate_password(
            plain_password: str,
            hashed_password: str,
            on_error_message: str,
            status_code: int,
            **kwargs
    ) -> bool:
        """
        Verifies that the provided password's hash equals to the already
        hashed password.
        """
        return utils.raise_exception_if_true(
            item=not bcrypt.verify(plain_password, hashed_password),
            on_error_message=on_error_message,
            status_code=status_code,
            **kwargs
        )

    @classmethod
    def create_token(
            cls,
            user: models.User,
    ) -> schemas.Token:
        user_data = schemas.CurrentUser.from_orm(user)
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE),
            'sub': str(user_data.id),
            'user': user_data.dict(),
        }
        token = jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        return schemas.Token(access_token=token)

    @staticmethod
    def validate_user_is_active(user: models.User, on_error_message: str):
        """
        Validates that the provided user is activated.
        """
        return utils.raise_exception_if_true(
            item=not user.is_active,
            on_error_message=on_error_message,
            status_code=status.HTTP_403_FORBIDDEN
        )
