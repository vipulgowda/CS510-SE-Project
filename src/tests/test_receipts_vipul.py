import pytest
from datetime import datetime
from flask import Flask
from core.database import db, init_db
from domain.receipts import update_receipt
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
        bill_type="restaurant",
        vendor_name="Test Restaurant",
        date_time=datetime.now(),
        total_amount=50.00,
        city="Test City",
        state="Test State",
        country="Test Country"
    )

def test_update_receipt_success(app_context, mocker, mock_db_session, sample_receipt):
    # Configure the mock
    mock_query = mocker.patch('schemas.receipt_schema.Receipt.query')
    mock_query.get.return_value = sample_receipt

    # Test data for update
    update_data = {
        "vendor_name": "Updated Restaurant",
        "total_amount": 75.00
    }

    # Execute the function
    result = update_receipt(1, update_data)

    # Verify the results
    assert "message" in result
    assert sample_receipt.vendor_name == "Updated Restaurant"
    assert sample_receipt.total_amount == 75.00
    assert mock_db_session.commit.called

def test_update_receipt_not_found(app_context, mocker):
    # Configure the mock to return None (receipt not found)
    mock_query = mocker.patch('schemas.receipt_schema.Receipt.query')
    mock_query.get.return_value = None

    # Execute the function
    result = update_receipt(999, {"vendor_name": "Test"})

    # Verify the results
    assert "error" in result
    assert result["error"] == "Receipt not found"

def test_update_receipt_error(app_context, mocker, mock_db_session, sample_receipt):
    mock_query = mocker.patch('schemas.receipt_schema.Receipt.query')
    mock_query.get.return_value = sample_receipt
    mock_db_session.commit.side_effect = Exception("Database error")
    
    result = update_receipt(1, {"vendor_name": "Test"})
    assert "error" in result