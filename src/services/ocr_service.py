from google.cloud import vision
import json
from services.cloud_storage import get_bucket_and_prefix, list_blobs, download_blob
from langchain_google_genai import GoogleGenerativeAI
from concurrent.futures import ThreadPoolExecutor
import asyncio
import os
llm = GoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)


def async_detect_document(gcs_source_uri, gcs_destination_uri):
    """Performs OCR on PDF files stored in Google Cloud Storage."""
    mime_type = "application/pdf"
    batch_size = 2

    client = vision.ImageAnnotatorClient()
    feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

    input_config = vision.InputConfig(
        gcs_source=vision.GcsSource(uri=gcs_source_uri), mime_type=mime_type
    )
    output_config = vision.OutputConfig(
        gcs_destination=vision.GcsDestination(uri=gcs_destination_uri),
        batch_size=batch_size,
    )

    async_request = vision.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config, output_config=output_config
    )
    operation = client.async_batch_annotate_files(requests=[async_request])

    operation.result(timeout=420)

    bucket_name, prefix = get_bucket_and_prefix(gcs_destination_uri)
    blob_list = list_blobs(bucket_name, prefix)

    if not blob_list:
        return {"error": "No OCR output found."}
    response = json.loads(download_blob(blob_list[0]))
    first_page_response = response["responses"][0]
    annotation = first_page_response.get("fullTextAnnotation", {})
    return (
        process_text(annotation["text"])
        if "text" in annotation
        else {"error": "No text found"}
    )


def process_text(text):
    """Generates structured JSON from OCR text using LLM."""
    prompt = f"""You are an AI trained to convert the given text into a structured JSON response. Analyze the text provided in the context, and return the response strictly in JSON format. Use 'nan' for any missing fields.
    Extract and classify the context into a JSON structure as per the given specification. Ensure the bill_type is classified into one of the specified categories: 'restaurant', 'public transport', 'hotel', 'retail', 'taxi', 'tourist attraction'. The response should only include the fields: bill_type, total_amount, vendor_name, date and time (with timezone), and geographical location (city, state, and country). If there is no total amount visible, use the subtotal and add the tax if it's a numerical value; if tax is not numerical or not present, use just the subtotal.
    
    context: {text}
    
    Example: 
    If hotel the json will look like below
    "bill_type": "hotel",
    "vendor_name": "Hotel Example",
    "date_time": "2024-06-05T12:00:00-05:00",
    "total_amount": 199.99,
    "location": 
      "city": "San Francisco",
      "state": "California",
      "country": "USA"
    
    If public_transport the json will look like below
    "bill_type": "public_transport",
    "vendor_name": "City Transit",
    "date_time": "2024-06-05T09:00:00-05:00",
    "total_amount": 3.50,
    "location": 
      "city": "Chicago",
      "state": "Illinois",
      "country": "USA"
   If restaurant the json will look like below 
    "bill_type": "restaurant",
    "vendor_name": "Grill House",
    "date_time": "2024-06-05T19:30:00-05:00",
    "total_amount": 45.75,
    "location": 
      "city": "Austin",
      "state": "Texas",
      "country": "USA"
    If retail the json will look like below
     "bill_type": "retail",
     "vendor_name": "Retail Store",
     "date_time": "2024-06-05T15:45:00-05:00",
     "total_amount": 80.20,
     "location": 
       "city": "New York",
       "state": "New York",
       "country": "USA"
    If taxi the json will look like below
    "bill_type": "taxi",
    "vendor_name": "City Cabs",
    "date_time": "2024-06-05T22:15:00-05:00",
    "total_amount": 27.00,
    "location": 
      "city": "Las Vegas",
      "state": "Nevada",
      "country": "USA"
    If tourist_attraction the json will look like below
    "bill_type": "tourist_attraction",
    "vendor_name": "City Museum",
    "date_time": "2024-06-05T14:00:00-05:00",
    "total_amount": 30.00,
    "location":
      "city": "Philadelphia",
      "state": "Pennsylvania",
      "country": "USA"
    If cafe the json will look like below
      "bill_type": "cafe",
      "vendor_name": "Central Perk",
      "date_time": "2024-06-05T10:30:00-05:00",
      "total_amount": 12.50,
      "location": 
        "city": "Seattle",
        "state": "Washington",
        "country": "USA"
    if gas the json will look like below
      "bill_type": "gas",
      "vendor_name": "Gas Station",
      "date_time": "2024-06-05T08:00:00-05:00",
      "total_amount": 50.00,
      "location": 
        "city": "Denver",
        "state": "Colorado",
        "country": "USA"
    """
    response = llm.invoke(prompt)
    formatted_data = response.strip("`json\n").strip("`\n")
    return formatted_data


async def process_blob(executor, blob_name, bucket_name, destination_bucket_name):
    """Asynchronous wrapper to process each blob using threading."""
    print(f"Processing file: {blob_name}")
    source_bucket = f"gs://{bucket_name}/{blob_name}"
    dest_bucket = f"gs://{destination_bucket_name}/{blob_name}-"

    formatted_data = await asyncio.get_running_loop().run_in_executor(
        executor, async_detect_document, source_bucket, dest_bucket
    )
    return formatted_data


async def process_specific_file(bucket_name, destination_bucket_name, filename):
    """Processes a specific file asynchronously."""
    with ThreadPoolExecutor() as executor:
        formatted_data = await process_blob(executor, filename, bucket_name, destination_bucket_name)
        return formatted_data
