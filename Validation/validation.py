from datetime import datetime
from typing import Tuple
from Models.credit_card import CreditCard
from Models.debit_card import DebitCard
from sqlalchemy.orm import Session


def validate_credit_card(
    db: Session,
    card_number: str,
    expiration_month: int,
    expiration_year: int,
    cvv: str,
    amount: float,
) -> Tuple[bool, str]:
    try:
        # Perform credit card validation logic
        # Return True if the credit card is valid, False otherwise
        # You can implement your own validation rules here
        credit_card = db.query(CreditCard).filter_by(card_number=card_number).first()
        if not credit_card:
            return False, "Invalid card number"

        current_date = datetime.now()
        expiration_date = datetime(expiration_year, expiration_month, 1)
        if expiration_date < current_date:
            return False, "Card has expired"

        if cvv != credit_card.cvv:
            return False, "Invalid CVV"

        if amount > credit_card.balance:
            return False, "Insufficient funds"

        # Reduce the balance from the credit card
        credit_card.balance -= amount
        db.commit()

        return True, ""
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def validate_debit_card(
    db: Session,
    card_number: str,
    expiration_month: int,
    expiration_year: int,
    cvv: str,
    amount: float,
) -> Tuple[bool, str]:
    try:
        # Perform debit card validation logic
        # Return True if the debit card is valid, False otherwise
        # You can implement your own validation rules here
        debit_card = db.query(DebitCard).filter_by(card_number=card_number).first()
        if not debit_card:
            return False, "Invalid card number"

        current_date = datetime.now()
        expiration_date = datetime(expiration_year, expiration_month, 1)
        if expiration_date < current_date:
            return False, "Card has expired"

        if cvv != debit_card.cvv:
            return False, "Invalid CVV"

        if amount > debit_card.balance:
            return False, "Insufficient funds"

        # Reduce the balance from the debit card
        debit_card.balance -= amount
        db.commit()

        return True, ""
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
