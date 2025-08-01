from dishka import FromDishka
from litestar import Controller, get, Response
from loguru import logger
from types_aiobotocore_s3.client import S3Client


class DownloadController(Controller):
    path = "/files"
    tags=["Download"]

    @get(
        path="/{file_path:path}",
        summary="Скачать файл"
    )
    async def get_file(self, file_path: str, s3: FromDishka[S3Client]) -> Response:
        logger.info(file_path)
        response = await s3.get_object(Bucket="files", Key=file_path)
        file_data = await response["Body"].read()
        content_type = response.get("ContentType", "application/octet-stream")
        return Response(
            content=file_data,
            media_type=content_type,
            headers={
                "Content-Disposition": f"attachment; filename={file_path.split('/')[-1]}",
            }
        )