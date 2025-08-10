from pydantic import BaseModel, Field

class ConsumableAddSchema(BaseModel):
    name: str = Field(max_length=100)
    erp_code: str = Field(max_length=10)
    qty: int = Field(ge=1)
    department: str = Field(max_length=100)

class ConsumableSchema(ConsumableAddSchema):
    id: int

class ConsumablePatchSchema(BaseModel):
    name: str | None = Field(default=None, max_length=100)
    erp_code: str = Field(max_length=100)
    qty: int | None  = Field(default=None, ge=1)
    department: str | None = Field(default=None, max_length=100)