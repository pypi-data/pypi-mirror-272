from typing import TypeAlias, Sequence
from pydantic import BaseModel

class Input(BaseModel):
  ply_boxes: Sequence[Sequence[str]]

Preds: TypeAlias = Sequence[Sequence[Sequence[tuple[str, float]]]]
Preds.__name__ = 'Preds'