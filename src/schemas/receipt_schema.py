from core.database import db

class Receipt(db.Model):
    __tablename__ = "receipts"

    id = db.Column(db.Integer, primary_key=True)
    total_amount = db.Column(db.Float, nullable=True)
    bill_type = db.Column(db.String(50), nullable=True)
    vendor_name = db.Column(db.String(100), nullable=True)
    date_time = db.Column(db.DateTime, nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    country = db.Column(db.String(50), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'total_amount': self.total_amount,
            'bill_type': self.bill_type,
            'vendor_name': self.vendor_name,
            'date_time': self.date_time.isoformat() if self.date_time else None,
            'city': self.city,
            'state': self.state,
            'country': self.country
        }
    
