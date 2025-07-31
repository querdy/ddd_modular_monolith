from pathlib import Path

from minio import Minio


def generate_unique_object_key(minio: Minio, bucket: str, base_path: str, filename: str):
    name = Path(filename).stem
    ext = Path(filename).suffix
    attempt = 0

    while True:
        suffix = f"_{attempt}" if attempt > 0 else ""
        object_key = f"{base_path}/{name}{suffix}{ext}"

        try:
            minio.stat_object(bucket, object_key)
            attempt += 1
        except Exception as e:
            if "NoSuchKey" in str(e) or "not found" in str(e).lower():
                return object_key
            else:
                raise
