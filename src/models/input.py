from pydantic import BaseModel, HttpUrl
from typing import Optional


class FileInput(BaseModel):
    file_base64: str
    model_name: Optional[str] = "yolo11l"


class UriInput(BaseModel):
    uri: str
    model_name: Optional[str] = "yolo11l"


class UrlInput(BaseModel):
    url: HttpUrl
    model_name: Optional[str] = "yolo11l"


class ModelInput(BaseModel):
    model_name: Optional[str] = "yolo11l"
