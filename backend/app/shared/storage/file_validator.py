from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from app.core.settings import settings


class FileValidator:

    def validate(self, file: UploadFile) -> None:
        extension = Path(file.filename or "").suffix.lower()

        if extension not in settings.ALLOWED_FILE_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File type is not allowed.",
            )

        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)

        if size > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size exceeds maximum allowed.",
            )