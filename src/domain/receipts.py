import json
from datetime import datetime
from core.database import db
from schemas.receipt_schema import Receipt


def insert_receipt(data):
    """Parses extracted data and inserts it into PostgreSQL database."""
    try:
        if isinstance(data, str):
            data = json.loads(data)

        # Extract the formatted_data if it exists
        if "formatted_data" in data:
            data = json.loads(data["formatted_data"])

        # Create new Receipt entry
        new_receipt = Receipt(
            bill_type=data.get("bill_type"),
            vendor_name=data.get("vendor_name"),
            date_time=datetime.fromisoformat(data.get("date_time")),
            total_amount=data.get("total_amount"),
            city=data.get("location", {}).get("city"),
            state=data.get("location", {}).get("state"),
            country=data.get("location", {}).get("country"),
        )
        # Insert into DB
        db.session.add(new_receipt)
        db.session.commit()

        return {
            "message": "Data inserted into PostgreSQL successfully!",
            "receipt_id": new_receipt.id,
        }

    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to insert data: {str(e)}"}


def get_all_receipts():
    """Retrieves all receipts from the database."""
    try:
        # Query all receipts from the database
        receipts = Receipt.query.all()
        return [receipt.to_dict() for receipt in receipts]
    except Exception as e:
        return {"error": f"Failed to retrieve receipts: {str(e)}"}


def update_receipt(receipt_id, data):
    """Updates a receipt by its ID in the database."""
    try:
        # Query the receipt by its ID
        receipt = Receipt.query.get(receipt_id)
        if receipt:
            # Update the receipt with the new data
            for key, value in data.items():
                setattr(receipt, key, value)

            # Commit the changes to the database
            db.session.commit()
            return {"message": "Receipt updated successfully!"}
        else:
            return {"error": "Receipt not found"}
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to update receipt: {str(e)}"}


def delete_receipt(receipt_id):
    """Deletes a receipt by its ID from the database."""
    try:
        # Query the receipt by its ID
        receipt = Receipt.query.get(receipt_id)
        if receipt:
            # Delete the receipt from the database
            db.session.delete(receipt)
            db.session.commit()
            return {"message": "Receipt deleted successfully!"}
        else:
            return {"error": "Receipt not found"}
    except Exception as e:
        db.session.rollback()
        return {"error": f"Failed to delete receipt: {str(e)}"}


def search_receipts(
    vendor=None,
    city=None,
    min_amount=None,
    max_amount=None,
    date=None,
    state=None,
    country=None,
    bill_type=None,
):
    """Search receipts with multiple filter parameters."""
    try:
        query = Receipt.query

        if vendor:
            query = query.filter(Receipt.vendor_name.ilike(f"%{vendor}%"))
        if city:
            query = query.filter(Receipt.city.ilike(f"%{city}%"))
        if min_amount:
            query = query.filter(Receipt.total_amount >= min_amount)
        if max_amount:
            query = query.filter(Receipt.total_amount <= max_amount)
        if date:
            query = query.filter(db.func.date(Receipt.date_time) == date)
        if state:
            query = query.filter(Receipt.state.ilike(f"%{state}%"))
        if country:
            query = query.filter(Receipt.country.ilike(f"%{country}%"))
        if bill_type:
            query = query.filter(Receipt.bill_type.ilike(f"%{bill_type}%"))

        receipts = query.all()
        return [receipt.to_dict() for receipt in receipts]
    except Exception as e:
        return {"error": f"Failed to search receipts: {str(e)}"}


def get_analytics(
    year=None,
    month=None,
    vendor_name=None,
    city=None,
    state=None,
    country=None,
    bill_type=None,
):
    """Get analytics data for receipts."""
    try:
        query = Receipt.query

        # Apply filters
        if year:
            query = query.filter(
                db.func.extract("year", Receipt.date_time) == int(year)
            )
        if month:
            query = query.filter(
                db.func.extract("month", Receipt.date_time) == int(month)
            )
        if vendor_name:
            query = query.filter(Receipt.vendor_name.ilike(f"%{vendor_name}%"))
        if city:
            query = query.filter(Receipt.city.ilike(f"%{city}%"))
        if state:
            query = query.filter(Receipt.state.ilike(f"%{state}%"))
        if country:
            query = query.filter(Receipt.country.ilike(f"%{country}%"))
        if bill_type:
            query = query.filter(Receipt.bill_type.ilike(f"%{bill_type}%"))

        receipts = query.all()

        # Calculate analytics
        total_spent = sum(receipt.total_amount for receipt in receipts)
        receipt_count = len(receipts)
        avg_amount = total_spent / receipt_count if receipt_count > 0 else 0

        # Group by vendor
        vendor_summary = {}
        for receipt in receipts:
            if receipt.vendor_name not in vendor_summary:
                vendor_summary[receipt.vendor_name] = {"count": 0, "total": 0}
            vendor_summary[receipt.vendor_name]["count"] += 1
            vendor_summary[receipt.vendor_name]["total"] += receipt.total_amount

        return {
            "total_spent": total_spent,
            "receipt_count": receipt_count,
            "average_amount": avg_amount,
            "vendor_summary": vendor_summary,
        }
    except Exception as e:
        return {"error": f"Failed to get analytics: {str(e)}"}
