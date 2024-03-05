from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base, int_pk, str_name_256, str_description_512


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int_pk]
    name: Mapped[str_name_256]
    description: Mapped[str_description_512]
    is_active: Mapped[bool] = mapped_column(default=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)


