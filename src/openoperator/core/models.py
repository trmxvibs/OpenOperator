from pydantic import BaseModel


class BoundingBox(BaseModel):
    x: int
    y: int
    width: int
    height: int


class UITarget(BaseModel):
    text: str
    box: BoundingBox
    center_x: int
    center_y: int
    confidence: float