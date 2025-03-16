from flask import Blueprint, request, jsonify, session
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
import os
import requests

api = Blueprint("api", __name__, url_prefix="/v1")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
REDIRECT_URI = "http://localhost:3000/api/auth/callback"

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

@api.route("/v1/auth/google", methods=["GET"])
def google_login():
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid email profile"
    )
    return jsonify({"auth_url": google_auth_url})

@api.route("/v1/auth/callback", methods=["GET"])
def google_callback():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "No authorization code provided"}), 400

    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()

    if "access_token" in token_json:
        user_info = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {token_json['access_token']}"},
        ).json()

        session["user"] = user_info
        session.permanent = True  # Ensure session persists

        return jsonify({"user": user_info, "message": "Login successful"})

    return jsonify({"error": "Invalid token response"}), 400

@api.route("/v1/auth/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"message": "Logged out successfully"})

@api.route("/v1/auth/user", methods=["GET"])
def get_user():
    user = session.get("user")
    if user:
        return jsonify({"user": user})
    return jsonify({"message": "No user logged in"}), 401
