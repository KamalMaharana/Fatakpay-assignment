from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CreditCard(Base):
    __tablename__ = "credit_cards"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String, unique=True)
    expiration_month = Column(Integer)
    expiration_year = Column(Integer)
    cvv = Column(String)
    balance = Column(Float)


class DebitCard(Base):
    __tablename__ = "debit_cards"

    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String, unique=True)
    expiration_month = Column(Integer)
    expiration_year = Column(Integer)
    cvv = Column(String)
    balance = Column(Float)


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    currency = Column(String)
    type = Column(String)
    card_number = Column(String)
    status = Column(String)
    authorization_code = Column(String)
    time = Column(DateTime)
    reason = Column(String, default="")

    def __init__(
        self,
        amount,
        currency,
        type,
        card_number,
        status,
        authorization_code,
        time,
        reason="",
    ):
        self.amount = amount
        self.currency = currency
        self.type = type
        self.card_number = card_number
        self.status = status
        self.authorization_code = authorization_code
        self.time = time
        self.reason = reason
