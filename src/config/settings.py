import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class with environment variables."""

    # ✅ Database Configuration
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME')

    # Ensure critical database credentials are set
    if not all([DB_USER, DB_PASSWORD, DB_NAME]):
        raise ValueError("Missing required database environment variables.")

    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ✅ File Storage Paths
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    IMAGE_SAVE_PATH = os.getenv('IMAGE_SAVE_PATH', os.path.join(BASE_DIR, 'uploads/image.jpg'))
    PDF_OUTPUT_PATH = os.getenv('PDF_OUTPUT_PATH', os.path.join(BASE_DIR, 'outputs/pdf_file.pdf'))
    PDF_OUTPUT_FILE_NAME = os.getenv('PDF_OUTPUT_FILE_NAME', 'output.pdf')

    # ✅ Google Cloud Configuration
    GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "websec-gowda-vipulp")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    # 🔐 Ensure Google Credentials are Set
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not GOOGLE_APPLICATION_CREDENTIALS:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS is missing. Set it in the .env file.")

    # ✅ Cloud Storage Buckets
    BUCKET_NAME = os.getenv('BUCKET_NAME', 'default_bucket')
    DEST_BUCKET_NAME = os.getenv('DEST_BUCKET_NAME', 'destination_bucket')

    # ✅ General Settings
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"  # Converts "true" string to boolean
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")