from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base, int_pk, str_name_256, str_description_512


class CategoryGameItem(Base):
    __tablename__ = 'category_game_items'

    id: Mapped[int_pk]
    name: Mapped[str_name_256]
    description: Mapped[str_description_512]


class GameItem(Base):
    __tablename__ = 'game_items'

    id: Mapped[int_pk]
    name: Mapped[str_name_256]
    description: Mapped[str_description_512]
    quantity: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('category_game_items.id'), nullable=False)
