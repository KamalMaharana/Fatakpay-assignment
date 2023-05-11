import logging
import traceback
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.orm import Session
import secrets
from Models.payment import Payment
from Models.payment_request import PaymentRequest
from Models.payment_response import PaymentResponse
from Database.database import get_db, save_payment
from Validation.validation import validate_credit_card, validate_debit_card


app = FastAPI()


def generate_authorization_code() -> str:
    # Generate a unique authorization code for each successful transaction
    authorization_code = secrets.token_hex(16)
    return authorization_code


@app.post("/process_payment")
def process_payment(
    payment_request: PaymentRequest, db: Session = Depends(get_db)
) -> PaymentResponse:
    payment_record = Payment(
        amount=payment_request.amount,
        currency=payment_request.currency,
        type=payment_request.type,
        card_number="",
        status="success",
        authorization_code="",
        time=datetime.now(),
        reason="",
    )
    try:
        if payment_request.type.lower() not in ["creditcard", "debitcard"]:
            raise HTTPException(status_code=400, detail="Invalid payment type")

        card_type = payment_request.type
        card_number = payment_request.card.number

        expiration_month = int(payment_request.card.expirationMonth)
        expiration_year = int(payment_request.card.expirationYear)
        cvv = payment_request.card.cvv
        amount = float(payment_request.amount)
        error_message = ""
        if card_type == "creditcard":
            is_valid, error_message = validate_credit_card(
                db, card_number, expiration_month, expiration_year, cvv, amount
            )
        elif card_type == "debitcard":
            is_valid, error_message = validate_debit_card(
                db, card_number, expiration_month, expiration_year, cvv, amount
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid payment type")

        if not is_valid:
            raise HTTPException(status_code=400, detail=error_message)

        # Generate a unique authorization code
        authorization_code = generate_authorization_code()
        payment_record.card_number = card_number
        payment_record.authorization_code = card_number

    except HTTPException as http_exep:
        payment_record.status = "failure"
        payment_record.reason = http_exep.detail
        status, error = save_payment(db, payment_record)
        if status == False:
            logging.error(error)
        if http_exep.detail == "Insufficient funds":
            raise HTTPException(status_code=422, detail=http_exep.detail)
        raise HTTPException(status_code=400, detail=http_exep.detail)

    except Exception as e:
        db.rollback()  # rollback any database changes made so far
        traceback_str = traceback.format_exc()
        error_message = f"An error occurred:\n{traceback_str}"
        payment_record.status = "failure"
        payment_record.reason = error_message
        status, error = save_payment(db, payment_record)
        if status == False:
            logging.error(error)

        raise HTTPException(
            status_code=422, detail=f"Some error occured: {str(error_message)}"
        )

    # Save the payment details to the database
    save_payment(db, payment_record)

    if payment_record.id is not None:
        # Fetch the payment record from the database to ensure all fields are populated
        db.refresh(payment_record)
        db.close()
        payment_response = PaymentResponse(
            amount=payment_request.amount,
            currency=payment_request.currency,
            type=payment_request.type,
            card={"number": card_number},
            status="success" if authorization_code else "failure",
            authorization_code=authorization_code,
            time=payment_record.time.isoformat(),
        )
        return JSONResponse(
            content=payment_response.dict(),
            status_code=200,
        )
    else:
        db.close()
        return HTTPException(status_code=500, detail="Failed to save payment record")
