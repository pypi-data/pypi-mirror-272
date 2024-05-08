from typing import Unpack
import uvicorn
from dslog.util import uvicorn_logconfig
from moveread.pipelines.input_validation import Input, Result, InputValidationAPI, fastapi, Params
from ..generated import Inputval

def pre(input: Inputval.In) -> tuple[Input, Inputval.In]:
  return Input(gameId=input.gameId, imgs=input.imgs), input

def post(entry: tuple[Result, Inputval.In]) -> Inputval.Out:
  res, state = entry
  return Inputval.next('preprocess', Inputval.In(gameId=res.gameId, imgs=res.imgs, model=state.model))

def inputval(
  Qin: Inputval.QueueIn, Qout: Inputval.QueueOut, *,
  port: int = 8002,
  host: str = '0.0.0.0',
  prefix: str = '[INPUT VAL API] ',
  **params: Unpack[Params]
):
  sdk = InputValidationAPI(Qin.map(pre), Qout.premap(post))
  app = fastapi(sdk, **params)
  uvicorn.run(app, port=port, host=host, log_config=uvicorn_logconfig(prefix))
