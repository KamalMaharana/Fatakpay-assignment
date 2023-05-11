from pydantic import BaseModel
from typing import Optional


class PaymentResponse(BaseModel):
    amount: float
    currency: str
    type: str
    card: dict
    status: str
    authorization_code: Optional[str]
    time: str
