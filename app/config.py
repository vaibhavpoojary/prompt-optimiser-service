# config.py
import os
import boto3

# --- Load from environment variables ---
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")  # Default to us-east-1
MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

def get_bedrock_client():
    """Returns a configured Bedrock client instance."""
    return boto3.client(
        'bedrock-runtime',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=REGION_NAME
    )

# Create a global instance if needed
bedrock = get_bedrock_client()
