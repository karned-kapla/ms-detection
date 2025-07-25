from pydantic import BaseModel, HttpUrl
from typing import Optional

class UrlInput(BaseModel):
    uuid: str
    secret: str
    url: HttpUrl
    model: Optional[str] = "yolo11l"
