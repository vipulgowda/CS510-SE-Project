import pytest
from datetime import datetime
from flask import Flask
from core.database import db, init_db
from domain.receipts import insert_receipt, get_all_receipts, update_receipt, delete_receipt, search_receipts, get_analytics
from schemas.receipt_schema import Receipt
from config.settings import Config

@pytest.fixture
def app():
    """Create a Flask application for testing."""
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app)
    return app

@pytest.fixture
def app_context(app):
    """Create an app context for testing."""
    with app.app_context():
        yield

@pytest.fixture
def mock_db_session(mocker):
    """Fixture to mock database session"""
    session_mock = mocker.Mock()
    mocker.patch.object(db, 'session', session_mock)
    return session_mock

@pytest.fixture
def sample_receipt():
    """Fixture to create a sample receipt"""
    return Receipt(
        id=1,
        bill_type="Hotel",
        vendor_name="find Hotel",
        date_time=datetime.now(),
        total_amount=50.00,
        city="find City",
        state="find State",
        country="find Country"
    )
def test_get_all_receipts_success(app_context, mocker):
    # Create mock receipts
    mock_receipts = [
        Receipt(
            id=1,
            bill_type="Hotel",
            vendor_name="find Hotel 1",
            date_time=datetime.now(),
            total_amount=50.00,
            city="find City",
            state="find State",
            country="find Country"
        ),
        Receipt(
            id=2,
            bill_type="",
            vendor_name="find Store",
            date_time=datetime.now(),
            total_amount=100.00,
            city="find City 2",
            state="find State 2",
            country="find Country"
        )
    ]

def find_get_all_receipts_empty(app_context, mocker):
    mock_query = mocker.patch('schemas.receipt_schema.Receipt.query')
    mock_query.all.return_value = []
    
    result = get_all_receipts()
    assert len(result) == 0

def find_get_all_receipts_error(app_context, mocker):
    mock_query = mocker.patch('schemas.receipt_schema.Receipt.query')
    mock_query.all.side_effect = Exception("Database error")
    
    result = get_all_receipts()
    assert "error" in result

