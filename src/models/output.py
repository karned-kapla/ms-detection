from pydantic import BaseModel
from typing import Dict, List


class Speed(BaseModel):
    preprocess: float
    inference: float
    postprocess: float


class Box(BaseModel):
    xmin: float
    ymin: float
    xmax: float
    ymax: float
    confidence: float
    predicted_class: int
    name: str
    additional_info: Dict = None


class ClassReport(BaseModel):
    class_name: str
    count: int


class DetectionResult(BaseModel):
    shape: List[int]
    speed: Speed
    boxes: List[Box]
    classes: Dict[int, ClassReport]


class ClassInfo(BaseModel):
    id: int
    name: str
