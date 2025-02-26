from google.cloud import storage
import re

def get_bucket_and_prefix(gcs_uri):
    """Extract bucket name and file prefix from a GCS URI."""
    match = re.match(r"gs://([^/]+)/?(.*)", gcs_uri.strip())
    return match.group(1), match.group(2)

def list_blobs(bucket_name, prefix):
    """List all blobs in a bucket with the given prefix."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    return [blob for blob in bucket.list_blobs(prefix=prefix) if not blob.name.endswith("/")]

def download_blob(blob):
    """Download a blob's content."""
    return blob.download_as_bytes().decode("utf-8")
