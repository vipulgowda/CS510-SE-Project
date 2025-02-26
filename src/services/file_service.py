import os
import logging
from werkzeug.utils import secure_filename
from services.image_processing import image_to_pdf  # Assume you have this function
from config.settings import Config  # Import configuration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upload_image(image):
    """Handles image upload and processing."""

    try:
        # Ensure the uploaded file is valid
        if not image:
            raise ValueError("No file provided.")

        # Validate file type (Optional, but recommended)
        allowed_extensions = {'jpg', 'jpeg', 'png'}
        filename = secure_filename(image.filename)
        file_ext = filename.rsplit('.', 1)[-1].lower()

        if file_ext not in allowed_extensions:
            raise ValueError("Invalid file type. Only JPG, JPEG, and PNG are allowed.")

        # Get environment variables from Config
        image_save_path = Config.IMAGE_SAVE_PATH
        pdf_output_path = Config.PDF_OUTPUT_PATH
        bucket_name = Config.BUCKET_NAME
        dest_bucket_name = Config.DEST_BUCKET_NAME
        output_file_name = Config.PDF_OUTPUT_FILE_NAME

        # Ensure upload directory exists
        upload_dir = os.path.dirname(image_save_path)
        os.makedirs(upload_dir, exist_ok=True)

        # Save the uploaded file securely
        image_path = os.path.join(upload_dir, filename)
        image.save(image_path)

        logger.info(f"File uploaded successfully: {image_path}")

        # Process the image (Convert to PDF)
        formatted_data = image_to_pdf(image_path, pdf_output_path, bucket_name, dest_bucket_name, output_file_name)

        return {
            "message": "File uploaded and processed successfully!",
            "file_name": filename,
            "formatted_data": formatted_data
        }

    except ValueError as ve:
        logger.error(f"Validation Error: {ve}")
        return {"error": str(ve)}, 400

    except Exception as e:
        logger.error(f"Unexpected error during upload: {e}", exc_info=True)
        return {"error": "An error occurred while processing the image."}, 500
