from typing import Unpack
from moveread.pipelines.game_correction import Input, Result, run_api, Params
from ..generated import Gamecorr

def pre(state: Gamecorr.In) -> tuple[Input, Gamecorr.In]:
  return Input(ply_boxes=state.ply_boxes, ocrpreds=state.ocrpreds), state

def post(entry: tuple[Result, Gamecorr.In]) -> Gamecorr.Out:
  res, state = entry
  if res.root.tag == 'badly-preprocessed':
    return Gamecorr.next('inputval', state)
  else:
    return Gamecorr.next('output', state.correct(res.root))

def gamecorr(
  Qin: Gamecorr.QueueIn, Qout: Gamecorr.QueueOut,
  **params: Unpack[Params]
):
  run_api(Qin.map(pre), Qout.premap(post), **params)