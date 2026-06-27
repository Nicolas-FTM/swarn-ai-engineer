"""
Script to seed the database with the review and sales history 

This script creates: 
1. Read the csv file
2. Insert data into the tables
"""

# DDBB interaction
from shared.database.postgres import create

# Data Schema
from shared.schemas.sale import SaleRecord, Sale_Schema_DDBB
from shared.schemas.review import ReviewRecord, Review_Schema_DDBB

# Pandas
import pandas as pd

# Logger
import logging

logger = logging.getLogger(__name__)

def create_sales() -> None:
    """Create initial sales for the application."""
    df = pd.read_csv("rag_service/data/raw/sales/bakery_sales_data.csv")
    # NaN -> None with the ide of Pydantic doesnt fail with aditional fields
    df = df.where(pd.notnull(df), None)
    df = df.replace({"NA": None, "N/A": None, "nan": None, "None": None})
    df.drop_duplicates()

    logger.info(f"Number of Sales: {df.shape[0]}")

    records: list[SaleRecord] = []
    for i, row in enumerate(df.to_dict(orient="records")):

        r = SaleRecord(**row)

        sale_record = Sale_Schema_DDBB(
            date=r.date,
            order_id=r.order_id,
            item_name=r.item_name,
            item_price=r.item_price,
            quantity=r.quantity,
            transaction_type=r.transaction_type,
            time_of_sale=r.time_of_sale,
            transaction_amount=r.transaction_amount
        )
 
        flag = create(model=Sale_Schema_DDBB,
               instance=sale_record,
               unique_filters={
                   "order_id": sale_record.order_id
               }
        )
        
        if not flag:
            # logger.info(f"Record {i} not inserted: {sale_record.date}")
            pass

    logging.info("All sales inserted")


def create_reviews() -> None: 
    """Create initial reviews for the application."""
    df = pd.read_csv("rag_service/data/raw/sales/bakery_reviews_data.csv")
    # NaN -> None with the ide of Pydantic doesnt fail with aditional fields
    df = df.where(pd.notnull(df), None)
    df = df.replace({"NA": None, "N/A": None, "nan": None, "None": None})
    df.drop_duplicates()

    logger.info(f"Number of Reviews: {df.shape[0]}")

    for i, row in enumerate(df.to_dict(orient="records")):

        r = ReviewRecord(**row)

        review_record = Review_Schema_DDBB(
            date=r.date,
            rating=r.rating,
            review_title=r.review_title,
            review_content=r.review_content 
        ) 
 
        flag = create(model=Review_Schema_DDBB,
            instance=review_record,
            unique_filters={
                "date": review_record.date,
                "rating": review_record.rating,
                "review_title": review_record.review_title,
                "review_content": review_record.review_content
            }
        )

        if not flag:
            # logger.info(f"Record {i} not inserted: {review_record.date}")
            pass

    logger.info("All reviews inserted")
  
def main() -> None:
    """Main function to execute the seeding."""
    try:
        logger.info("Seeding sales...")
        create_sales()
        logger.info(f"Successfully created sales")
    except Exception as e:
        logger.error(f"Error seeding sales: {e}")

    try:
        logger.info("Seeding reviews...")
        create_reviews()
        logger.info(f"Successfully created reviews")
    except Exception as e:
        logger.error(f"Error seeding reviews: {e}")

if __name__ == "__main__":
    main()    