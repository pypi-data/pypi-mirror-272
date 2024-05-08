from typing import TypeVar, Generic, NamedTuple
from dataclasses import dataclass
from q.api import ReadQueue, WriteQueue, ReadError
from haskellian import either as E
from .types import Input, Item, Result

S = TypeVar('S')

def make_item(entry: tuple[str, tuple[Input, S]]):
  id, (task, _) = entry
  return Item(gameId=task.gameId, imgs=task.imgs, taskId=id)

class Queues(NamedTuple, Generic[S]):
  inp: ReadQueue[tuple[Input, S]]
  out: WriteQueue[tuple[Result, S]]

@dataclass
class InputValidationAPI(Generic[S]):

  Qin: ReadQueue[tuple[Input, S]]
  Qout: WriteQueue[tuple[Result, S]]

  @classmethod
  def of(cls, queues: Queues[S]):
    return InputValidationAPI(*queues)
  
  def tasks(self):
    return self.Qin.items().map(lambda e: e.fmap(make_item))
  
  @E.do[ReadError]()
  async def validate(self, taskId: str, result: Result):
    _, state = (await self.Qin.read(taskId)).unsafe()
    (await self.Qout.push(taskId, (result, state))).unsafe()
    (await self.Qin.pop(taskId)).unsafe()