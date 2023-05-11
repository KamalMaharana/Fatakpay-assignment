from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from Models.models import Base, Payment

SQLALCHEMY_DATABASE_URL = "sqlite:///Database/payment.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)  # Create tables if they don't exist


def save_payment(db: Session, payment: Payment):
    try:
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return True, ""
    except Exception as e:
        return False, e
