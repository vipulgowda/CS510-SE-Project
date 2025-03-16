from flask import Flask
from flask_cors import CORS
from config.settings import Config
from core.database import init_db
from api.v1.routes import api
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "hello")
# Initialize database
init_db(app)

# Register API routes
app.register_blueprint(api, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
