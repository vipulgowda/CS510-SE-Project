import pytest
from datetime import datetime
from flask import Flask
from core.database import db, init_db
from domain.receipts import insert_receipt
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
        bill_type="spa",
        vendor_name="abc spa",
        date_time=datetime.now(),
        total_amount=65.00,
        city="portland",
        state="oregon",
        country=""
    )

def test_insert_receipt_success(mock_db_session):
    # Test data
    receipt_data = {
        "formatted_data": '''{
            "bill_type": "spa",
            "vendor_name": "abc spa",
            "date_time": "2024-03-20T12:00:00-05:00",
            "total_amount": 65.00,
            "location": {
                "city": "portland",
                "state": "oregon",
                "country": "USA"
            }
        }'''
    }

    # Execute the function
    result = insert_receipt(receipt_data)

    # Verify the database interactions
    assert mock_db_session.add.called
    assert mock_db_session.commit.called
    assert "message" in result
    assert "receipt_id" in result

def test_insert_receipt_invalid_data(mock_db_session):
    # Test with invalid JSON data
    invalid_data = "invalid json"
    
    # Execute the function
    result = insert_receipt(invalid_data)

    # Verify the result
    assert "error" in result
    assert mock_db_session.rollback.called

def test_insert_receipt_missing_fields(mock_db_session):
    # Test with missing required fields
    receipt_data = {
        "formatted_data": '{"vendor_name": "abc spa"}'
    }
    
    result = insert_receipt(receipt_data)
    assert "error" in result

