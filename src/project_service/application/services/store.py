from pathlib import Path

from loguru import logger
from minio import Minio
from types_aiobotocore_s3.client import S3Client


async def generate_unique_object_key(s3_client: S3Client, bucket: str, base_path: str, filename: str):
    name = Path(filename).stem
    ext = Path(filename).suffix
    attempt = 0

    while True:
        suffix = f"_{attempt}" if attempt > 0 else ""
        object_key = f"{base_path}/{name}{suffix}{ext}"

        try:
            await s3_client.head_object(Bucket=bucket, Key=object_key)
            attempt += 1
        except s3_client.exceptions.ClientError as error:
            if error.response["Error"]["Code"] == "404":
                return object_key
            else:
                raise
