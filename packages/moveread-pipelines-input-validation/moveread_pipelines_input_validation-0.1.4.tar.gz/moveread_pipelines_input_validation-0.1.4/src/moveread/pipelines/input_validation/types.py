import os
from pydantic import BaseModel

class GameId(BaseModel):
  group: str
  round: int
  board: int

class Input(BaseModel):
  gameId: GameId
  imgs: list[str]

class Item(Input):
  taskId: str

  def at_url(self, base_url: str) -> 'Item':
    copy = self.model_copy()
    copy.imgs = [os.path.join(base_url, img) for img in self.imgs]
    return copy

class Result(BaseModel):
  gameId: GameId
  imgs: list[str]

  def strip_url(self, base_url: str) -> 'Result':
    copy = self.model_copy()
    copy.imgs = [img.replace(base_url, '').strip('/') for img in self.imgs]
    return copy