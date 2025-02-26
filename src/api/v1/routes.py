from flask import Blueprint, request, jsonify
from services.file_service import upload_image
from flask_cors import CORS
from domain.receipts import (
    get_all_receipts,
    insert_receipt,
    update_receipt,
    delete_receipt,
    search_receipts,
    get_analytics,
)

api = Blueprint("api", __name__)

# Enable global CORS
CORS(api, resources={r"/*": {"origins": "http://localhost:3000"}})

# ✅ Upload a receipt (Refactored)
@api.route("/v1/receipt", methods=["POST"])
def upload_receipt_api():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files["image"]
    if image.filename == "":
        return jsonify({"error": "No image file provided"}), 400

    response = insert_receipt(upload_image(image))
    return jsonify(response)


# ✅ Fetch all receipts
@api.route("/v1/receipts", methods=["GET"])
def get_all_receipts_api():
    """Fetch all receipts."""
    return jsonify(get_all_receipts())


# ✅ Update a receipt (Fixed naming to plural "receipts")
@api.route("/v1/receipts/<int:receipt_id>", methods=["POST"])
def update_receipt_api(receipt_id):
    """Update an existing receipt."""
    updated_data = request.json
    return jsonify(update_receipt(receipt_id, updated_data))


# ✅ Delete a receipt (Fixed naming)
@api.route("/v1/receipts/<int:receipt_id>", methods=["DELETE"])
def delete_receipt_api(receipt_id):
    """Delete a receipt."""
    return jsonify(delete_receipt(receipt_id))


# ✅ Search receipts with filters (Optimized)
@api.route("/v1/receipts/search", methods=["GET"])
def search_receipts_api():
    """Search for receipts with multiple filter parameters."""
    search_params = request.args.to_dict(flat=True)  # Automatically extracts all query parameters
    results = search_receipts(**search_params)
    return jsonify(results)


# ✅ Get receipt analytics (Optimized)
@api.route("/v1/receipts/analytics", methods=["GET"])
def get_analytics_api():
    """Get analytics data for receipts."""
    analytics_params = request.args.to_dict(flat=True)  # Automatically extracts all query parameters
    return jsonify(get_analytics(**analytics_params))