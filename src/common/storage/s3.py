from typing import AsyncIterator

from aioboto3 import Session
from dishka import Provider, provide, Scope
from types_aiobotocore_s3.client import S3Client


class S3ClientProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=S3Client)
    async def get_s3_client(self) -> AsyncIterator[S3Client]:
        session = Session()
        async with session.client(
            service_name="s3",
            endpoint_url="http://minio:9000",
            aws_access_key_id="admin",
            aws_secret_access_key="admin123",
            use_ssl=False,
        ) as s3_client:
            yield s3_client
