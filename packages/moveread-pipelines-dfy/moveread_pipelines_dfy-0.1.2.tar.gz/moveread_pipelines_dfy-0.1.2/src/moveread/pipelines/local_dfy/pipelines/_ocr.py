from typing import Unpack
import asyncio
from kv.api import KV
from moveread.pipelines.ocr_predict import Input, Preds, run, Params
from ..generated import Ocr

def pre(input: Ocr.In) -> tuple[Input, Ocr.In]:
  return Input(ply_boxes=input.ply_boxes), input

def post(entry: tuple[Preds, Ocr.In]) -> Ocr.Out:
  preds, state = entry
  return Ocr.next('gamecorr', state.predict(preds))

def ocr(
  Qin: Ocr.QueueIn, Qout: Ocr.QueueOut,
  images: KV[bytes],
  **params: Unpack[Params]
):
  coro = run(Qin.map(pre), Qout.premap(post), images=images, **params)
  asyncio.run(coro)