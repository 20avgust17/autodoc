from pydantic import BaseModel, constr


class CreateOrUpdateGameItem(BaseModel):
    name: constr(max_length=256)
    description: constr(max_length=512)
    quantity: int
    price: float
    category_id: int

    class Config:
        from_attributes = True


class GameItem(CreateOrUpdateGameItem):
    id: int


class CreateCategoryGameItem(BaseModel):
    name: constr(max_length=256)
    description: constr(max_length=512)


class CategoryGameItem(CreateCategoryGameItem):
    id: int

    class Config:
        from_attributes = True
