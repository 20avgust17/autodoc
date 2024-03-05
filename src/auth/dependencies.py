from fastapi import Depends
from sqlalchemy.orm import Session

from auth import schemas
from auth.services import oauth2_scheme, AuthService
from database import SessionLocalLive
from dependencies import get_live_db_session


def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_live_db_session),
) -> schemas.CurrentUser:
    """
    Returns a pydantic user model if the provided token is correct.
    """
    return schemas.CurrentUser.from_orm(AuthService(session=session).verify_user(token))
