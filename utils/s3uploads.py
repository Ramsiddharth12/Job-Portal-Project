import boto3
import os

s3 = boto3.client("s3")

def upload_resume(file, filename):

    bucket = os.getenv("S3_BUCKET_NAME")

    s3.upload_fileobj(
        file,
        bucket,
        filename
    )

    return f"https://{bucket}.s3.amazonaws.com/{filename}"