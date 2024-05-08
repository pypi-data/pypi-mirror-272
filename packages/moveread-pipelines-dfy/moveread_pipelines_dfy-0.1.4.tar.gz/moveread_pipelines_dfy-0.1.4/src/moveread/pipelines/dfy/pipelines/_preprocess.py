from typing import Unpack
from kv.api import KV
from moveread.pipelines.game_preprocess import run_local, LocalParams, Input, Result
from ..generated import Preprocess

def pre(input: Preprocess.In) -> Input:
  return Input(model=input.model, imgs=list(input.imgs), state=input.model_dump())

def post(result: Result) -> Preprocess.Out:
  state = Preprocess.In.model_validate(result.state)
  next = state.preprocess(result.preprocessed_imgs)
  return Preprocess.next('ocr', next)

def preprocess(
  Qin: Preprocess.QueueIn, Qout: Preprocess.QueueOut,
  images: KV[bytes],
  **params: Unpack[LocalParams]
):
  run_local(Qin.map(pre), Qout.premap(post), images=images, **params)