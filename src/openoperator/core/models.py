from pydantic import BaseModel


# --------------------------------------------------
# Legacy Agent Models
# --------------------------------------------------

class ActionIntent(BaseModel):
    """
    Legacy action model used by AgentBrain and orchestrator tests.
    """

    action: str
    target: str | None = None
    text: str | None = None


# --------------------------------------------------
# Vision Models
# --------------------------------------------------

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