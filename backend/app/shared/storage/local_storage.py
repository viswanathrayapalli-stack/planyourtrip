from pathlib import Path
import shutil
import uuid

from fastapi import UploadFile

from app.core.settings import settings
from app.shared.storage.storage_service import StorageService


class LocalStorageService(StorageService):

    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def save_file(self, file: UploadFile) -> tuple[str, str]:
        original_extension = Path(file.filename or "").suffix
        generated_filename = f"{uuid.uuid4()}{original_extension}"
        file_path = self.upload_dir / generated_filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return generated_filename, str(file_path.resolve())