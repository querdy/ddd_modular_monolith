from urllib.parse import quote

from dishka import FromDishka
from litestar import Controller, get, Response, status_codes, Request
from litestar.exceptions import HTTPException
from litestar.response import Stream
from types_aiobotocore_s3.client import S3Client


class DownloadController(Controller):
    path = "/files"
    tags = ["Download"]
    bucket = "files"

    @get(path="/{file_path:path}", summary="Скачать файл")
    async def get_file(self, file_path: str, s3: FromDishka[S3Client]) -> Response:
        try:
            response = await s3.get_object(Bucket=self.bucket, Key=file_path)
        except Exception:
            raise HTTPException(
                status_code=status_codes.HTTP_404_NOT_FOUND,
                detail=f"Невозможно получить запрошенный файл",
            )
        content_type = response.get("ContentType")
        if content_type.startswith("image/"):
            headers = {}
        else:
            headers = {"Content-Disposition": f"attachment; filename*=UTF-8''{quote(file_path.split('/')[-1])}"}
        headers["Content-Length"] = str(response.get("ContentLength", 0))
        return Stream(content=response["Body"], media_type=content_type, headers=headers)

    @get(path="/video/{file_path:path}", summary="Воспроизведение видео поддержкой Range")
    async def stream_video(self, file_path: str, request: Request, s3: FromDishka[S3Client]) -> Response:
        range_header = request.headers.get("range")

        if not range_header:
            try:
                s3_response = await s3.get_object(Bucket=self.bucket, Key=file_path)
            except Exception:
                raise HTTPException(
                    status_code=status_codes.HTTP_404_NOT_FOUND,
                    detail=f"Невозможно получить запрошенный файл",
                )
            return Stream(
                content=s3_response["Body"],
                media_type=s3_response["ContentType"],
            )

        byte_range = range_header.replace("bytes=", "").strip()
        start, end = byte_range.split("-") if "-" in byte_range else (byte_range, "")
        range_value = f"bytes={start}-{end}"
        try:
            s3_response = await s3.get_object(Bucket=self.bucket, Key=file_path, Range=range_value)
        except Exception:
            raise HTTPException(
                status_code=status_codes.HTTP_404_NOT_FOUND,
                detail=f"Невозможно получить запрошенный файл",
            )
        content_length = int(s3_response["ContentLength"])
        content_range = s3_response["ContentRange"]
        content_type = s3_response["ContentType"]

        return Stream(
            content=s3_response["Body"],
            media_type=content_type,
            headers={
                "Content-Range": content_range,
                "Accept-Ranges": "bytes",
                "Content-Length": str(content_length),
            },
            status_code=status_codes.HTTP_206_PARTIAL_CONTENT,
        )
