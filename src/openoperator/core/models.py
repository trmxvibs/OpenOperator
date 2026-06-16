from typing import Optional

from pydantic import BaseModel


class UIElement(BaseModel):
    id: str
    label: str
    x: int
    y: int
    width: int
    height: int
    element_type: str


class ActionIntent(BaseModel):
    action_type: str
    target_id: Optional[str] = None
    input_text: Optional[str] = None
