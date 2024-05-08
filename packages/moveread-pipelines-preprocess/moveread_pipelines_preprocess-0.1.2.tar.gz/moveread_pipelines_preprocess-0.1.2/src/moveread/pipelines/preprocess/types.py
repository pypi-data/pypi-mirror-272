from typing import Literal
from pydantic import BaseModel, RootModel
from dataclasses import dataclass
from pure_cv import Rotation
from scoresheet_models import ModelID
from moveread.annotations import ModelID, Corners, Contours, Rectangle, ImageMeta

class ImageResult(BaseModel):
  img: str
  meta: ImageMeta

class Result(BaseModel):
  original: ImageResult
  corrected: ImageResult
  boxes: list[str]

@dataclass
class Discarded:
  reason: Literal['manually-discarded'] = 'manually-discarded'

class Input(BaseModel):
  img: str
  model: ModelID
  blobs: list[str] = []

  def correct(self, corners: Corners, corrected: str, confirmed: bool = True) -> 'Corrected':
    return Corrected(blobs=self.blobs + [corrected], img=self.img, model=self.model, corners=corners, corrected=corrected, confirmed=confirmed)
  def rotate(self, rotation: Rotation, rotated: str) -> 'Rotated':
    return Rotated(blobs=self.blobs + [rotated], img=rotated, model=self.model, rotation=rotation)
  def extract(self, corners: Corners | None, corrected: str, contours: Contours, contoured: str) -> 'Extracted':
    return Extracted(blobs=self.blobs + [contoured, corrected], img=self.img, model=self.model, corners=corners, corrected=corrected, confirmed=False, contours=contours, contoured=contoured)


class Corrected(Input):
  corners: Corners | None
  corrected: str
  confirmed: bool

  def select(self, grid_coords: Rectangle) -> 'Selected':
    return Selected(blobs=self.blobs, img=self.img, model=self.model, corners=self.corners, corrected=self.corrected, confirmed=self.confirmed, grid_coords=grid_coords)
  
  def re_extract(self, contours: Contours, contoured: str) -> 'Extracted':
    return Extracted(blobs=self.blobs + [contoured], img=self.img, model=self.model, corners=self.corners, corrected=self.corrected, confirmed=self.confirmed, contours=contours, contoured=contoured)

class Rotated(Input):
  rotation: Rotation

class Extracted(Corrected):
  contours: Contours
  contoured: str

  def ok(self) -> 'Contoured':
    return Contoured(blobs=self.blobs, img=self.img, model=self.model, corners=self.corners, corrected=self.corrected, confirmed=self.confirmed, contours=self.contours, contoured=self.contoured)

  def perspective_ok(self) -> 'Corrected':
    return Corrected(blobs=self.blobs, img=self.img, model=self.model, corners=self.corners, corrected=self.corrected, confirmed=self.confirmed)

class Selected(Corrected):
  grid_coords: Rectangle
  tag: Literal['grid'] = 'grid'

class Contoured(Extracted):
  tag: Literal['contoured'] = 'contoured'

Output = Selected | Contoured
class RootOutput(RootModel):
  root: Output

__all__ = [
  'Discarded', 'Input', 'Corrected', 'Rotated', 'Extracted', 'Selected', 'Contoured', 'Output', 'RootOutput',
  'Task', 'ImageResult', 'Result',
]
