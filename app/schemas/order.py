from pydantic import BaseModel, ConfigDict


class OrderBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int = 1


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    user_id: int | None = None
    product_id: int | None = None
    quantity: int | None = None


class OrderOut(OrderBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
