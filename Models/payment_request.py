from pydantic import BaseModel


class Card(BaseModel):
    number: str
    expirationMonth: str
    expirationYear: str
    cvv: str


class PaymentRequest(BaseModel):
    amount: float
    currency: str
    type: str
    card: Card
