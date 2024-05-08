from typing import Sequence
from pydantic import BaseModel
from haskellian import Iter
from q.pipelines import Task, Tasks
from scoresheet_models import ModelID
from moveread.pipelines.input_validation import GameId
import moveread.pipelines.preprocess as pre
import moveread.pipelines.ocr_predict as ocr
import moveread.pipelines.game_correction as gamecorr

class Input(BaseModel):
  gameId: GameId
  model: ModelID
  imgs: Sequence[str]

  def preprocess(self, preprocessed_imgs: Sequence[pre.Result]) -> 'Preprocessed':
    ply_boxes = Iter(preprocessed_imgs) \
      .flatmap(lambda img: img.boxes) \
      .map(lambda box: [box]) \
      .sync() # OCR expects multiple boxes per ply
    return Preprocessed(preprocessed_imgs=preprocessed_imgs, gameId=self.gameId, model=self.model, imgs=self.imgs, ply_boxes=ply_boxes)

class Preprocessed(Input):
  ply_boxes: Sequence[Sequence[str]]
  preprocessed_imgs: Sequence[pre.Result]

  def predict(self, ocrpreds: ocr.Preds) -> 'Predicted':
    return Predicted(ocrpreds=ocrpreds, gameId=self.gameId, model=self.model, imgs=self.imgs, preprocessed_imgs=self.preprocessed_imgs, ply_boxes=self.ply_boxes)

class Predicted(Preprocessed):
  ocrpreds: ocr.Preds

  def correct(self, res: gamecorr.BaseResult) -> 'Result':
    return Result(
      ocrpreds=self.ocrpreds, gameId=self.gameId, model=self.model,
      imgs=self.imgs, preprocessed_imgs=self.preprocessed_imgs, ply_boxes=self.ply_boxes,
      annotations=res.annotations, pgn=res.pgn, early=res.early
    )

class Result(Predicted, gamecorr.BaseResult):
  ...

TASKS = Tasks(
  'inputval', Result,
  tasks=dict[str, Task](
    inputval=Task(Input, 'preprocess'),
    preprocess=Task(Input, 'ocr'),
    ocr=Task(Preprocessed, 'gamecorr'),
    gamecorr=Task(Predicted, 'output', 'inputval'),
  )
)

def codegen():
  TASKS.codegen(__file__, 'TASKS')
  TASKS.codegen_pipelines(__file__)