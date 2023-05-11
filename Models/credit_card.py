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
