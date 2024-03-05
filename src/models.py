from typing import Annotated

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, mapped_column

int_pk = Annotated[int, mapped_column(primary_key=True)]
str_name_256 = Annotated[str, mapped_column(String(256), unique=True, nullable=False)]
str_description_512 = Annotated[str, mapped_column(String(512))]


class Base(DeclarativeBase):
    ...
