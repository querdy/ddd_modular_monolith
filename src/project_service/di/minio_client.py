from dishka import Provider, provide, Scope
from minio import Minio


class MinioClientProvider(Provider):
    @provide(scope=Scope.APP)
    def get_minio_client(self) -> Minio:
        return Minio(
            endpoint="minio:9000",
            access_key="admin",
            secret_key="admin123",
            secure=False,
        )
