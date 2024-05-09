from bson import ObjectId
from typing import Annotated, Optional
from arbitro_typing.data_types import Bank, Product, ReceivePay
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

PyObjectId = Annotated[str, BeforeValidator(str)]

class Operation(BaseModel):
    deal_number: Optional[str] = Field(default=None)
    product: Product
    receive_pay: ReceivePay
    counterparty: Bank
    amount: int
    maturity: int
    rate: float
    client: Bank
    model_config = ConfigDict(
        populate_by_name=True,
    )

class OperationDaily(Operation):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    client_confirmed_status: Optional[bool] = Field(default=False)
    confirmed_status: Optional[bool] = Field(default=False)
    operation_pair: Optional[PyObjectId] = Field(default=None)
    model_config = ConfigDict(
        populate_by_name=True,
    )

class UpdateOperation(BaseModel):
    deal_number: Optional[str] = None
    client: Optional[Bank] = None
    product: Optional[Product] = None
    receive_pay: Optional[ReceivePay] = None
    counterparty: Optional[Bank] = None
    amount: Optional[int] = None
    maturity: Optional[int] = None
    rate: Optional[float] = None
    client_confirmed_status: Optional[bool] = None
    confirmed_status: Optional[bool] = None
    operation_pair: Optional[PyObjectId] = None
    model_config = ConfigDict(
        json_encoders={ObjectId: str},
    )

class OperationHistorical(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    pay_leg: Operation
    receive_leg: Operation