from abc import ABC, abstractmethod

from fastapi import UploadFile


class StorageService(ABC):
    """Storage abstraction for file providers."""

    @abstractmethod
    def save_file(
        self,
        file: UploadFile,
    ) -> tuple[str, str]:
        raise NotImplementedError