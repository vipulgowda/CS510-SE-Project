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
        bill_type="cinema",
        vendor_name="regal",
        date_time=datetime.now(),
        total_amount=50.00,
        city="portland",
        state="oregon",
        country="USA"
    )



def test_delete_receipt_success(app_context, mocker, mock_db_session, sample_receipt):
    mock_query = mocker.patch('schemas.receipt_schema.Receipt.query')
    mock_query.get.return_value = sample_receipt
    
    result = delete_receipt(1)
    assert "message" in result
    assert mock_db_session.delete.called
    assert mock_db_session.commit.called

def test_delete_receipt_not_found(app_context, mocker):
    mock_query = mocker.patch('schemas.receipt_schema.Receipt.query')
    mock_query.get.return_value = None
    
    result = delete_receipt(999)
    assert "error" in result
    assert result["error"] == "Receipt not found"

def test_search_receipts_success(app_context, mocker, sample_receipt):
    mock_query = mocker.patch('schemas.receipt_schema.Receipt.query')
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = [sample_receipt]
    
    result = search_receipts(
        vendor="regal",
        city="portland",
        min_amount=10,
        max_amount=100,
        date="2024-03-20",
        state="oregon",
        country="USA",
        bill_type="cinema"
    )
    
    assert len(result) == 1
    assert result[0]["vendor_name"] == "regal"

def test_search_receipts_no_results(app_context, mocker):
    mock_query = mocker.patch('schemas.receipt_schema.Receipt.query')
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = []
    
    result = search_receipts(vendor="Nonexistent")
    assert len(result) == 0

def test_get_analytics_success(app_context, mocker, sample_receipt):
    mock_query = mocker.patch('schemas.receipt_schema.Receipt.query')
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = [sample_receipt]
    
    result = get_analytics(
        year=2024,
        month=3,
        vendor_name="regal",
        city="portland",
        state="oregon",
        country="USA",
        bill_type="cinema"
    )
    
    assert "total_spent" in result
    assert "receipt_count" in result
    assert "average_amount" in result
    assert "vendor_summary" in result

def test_get_analytics_no_data(app_context, mocker):
    mock_query = mocker.patch('schemas.receipt_schema.Receipt.query')
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = []
    
    result = get_analytics(year=2024)
    assert result["total_spent"] == 0
    assert result["receipt_count"] == 0
    assert result["average_amount"] == 0
    assert result["vendor_summary"] == {} 