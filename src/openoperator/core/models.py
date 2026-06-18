from pydantic import BaseModel


class BoundingBox(BaseModel):
    """
    Spatial boundaries of a detected UI element.
    """

    x: int
    y: int
    width: int
    height: int


class UITarget(BaseModel):
    """
    Represents a detected UI target on screen.
    """

    text: str
    box: BoundingBox
    center_x: int
    center_y: int
    confidence: float