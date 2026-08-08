"""
Sale SQL and API Tables
"""

# SQL Alchemy
from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, Enum as SqEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

# Pydantic
from pydantic import BaseModel, Field, field_validator

# Types
from datetime import date
from decimal import Decimal
from enum import Enum as PyEnum
import numpy as np

Base = declarative_base()


class TransactionTypeEnum(PyEnum):
    Cash = "Cash"
    Credit_Card = "Credit Card"


class TimeOfSaleEnum(PyEnum):
    Morning = "Morning"
    Afternoon = "Afternoon"
    Evening = "Evening"
    NA = "NA"

class SaleRecord(BaseModel):
    date: date
    order_id: int
    item_name: str | None = None
    item_price: Decimal = Field(gt=0)
    quantity: int = Field(gt=0)
    transaction_type: TransactionTypeEnum | None = None
    time_of_sale: TimeOfSaleEnum | None = None
    transaction_amount: Decimal = Field(gt=0)

    # --- NaN / missing cleanup ---
    @field_validator("time_of_sale", "item_name", "transaction_type", mode="before")
    @classmethod
    def handle_nan(cls, v):

        if v is None:
            return None

        # pandas / numpy missing
        if isinstance(v, float) and np.isnan(v):
            return None

        # strings
        if isinstance(v, str): 
            cleaned = v.strip().upper()

            if cleaned in {"NA", "N/A", "NONE", ""}:
                return None

            return v  # IMPORTANT: keep original string for enum parsing

        return v


class Sale_Schema_DDBB(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    order_id = Column(Integer, nullable=False, index=True)
    item_name = Column(String(255), nullable=False)
    item_price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)

    transaction_type = Column(SqEnum(TransactionTypeEnum))
    time_of_sale = Column(SqEnum(TimeOfSaleEnum))

    transaction_amount = Column(Numeric(10, 2), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self):
        return (
            f"<Sale(id={self.id}, order_id={self.order_id}, "
            f"item_name='{self.item_name}', transaction_amount={self.transaction_amount})>"
        )