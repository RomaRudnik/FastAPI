from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    price: float
    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    category_id: int | None = None


class ProductOut(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
