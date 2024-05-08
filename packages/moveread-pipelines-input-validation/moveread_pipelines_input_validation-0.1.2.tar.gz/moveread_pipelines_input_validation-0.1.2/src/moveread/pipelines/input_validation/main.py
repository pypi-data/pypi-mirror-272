from typing import Unpack, TypeVar
import uvicorn
from q.api import ReadQueue, WriteQueue
from moveread.pipelines.input_validation import Input, Result, InputValidationAPI, fastapi, Params

S = TypeVar('S')

def run_local(
  Qin: ReadQueue[tuple[Input, S]], Qout: WriteQueue[tuple[Result, S]], *,
  port: int = 8002,
  host: str = '0.0.0.0',
  **params: Unpack[Params]
):
  sdk = InputValidationAPI(Qin, Qout)
  app = fastapi(sdk, **params)
  uvicorn.run(app, port=port, host=host)
