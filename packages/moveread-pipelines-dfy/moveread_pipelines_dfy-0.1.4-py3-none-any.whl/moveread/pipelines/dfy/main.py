from typing import NotRequired, TypedDict, Unpack, Literal
from functools import partial
import os
from dslog import Logger
from kv.api import KV
from .generated import run_local as _run_local, QueueIn, QueueOut
from .pipelines import inputval, preprocess, ocr, gamecorr, OCRParams

class ApiParams(TypedDict):
  port: NotRequired[int]
  host: NotRequired[str]

class Params(TypedDict):
  inputval: NotRequired[ApiParams]
  preprocess: NotRequired[ApiParams]
  ocr: NotRequired[OCRParams]
  gamecorr: NotRequired[ApiParams]

def run_local(
  Qin: QueueIn, Qout: QueueOut, *,
  images: KV[bytes],
  base_path: str,
  images_path: str,
  protocol: Literal['sqlite', 'fs'] = 'sqlite',
  logger = Logger.rich().prefix('[DFY]'),
  **params: Unpack[Params]
):
  _run_local(
    Qin, Qout,
    inputval=partial(inputval, images_path=images_path, logger=logger.prefix('[INPUT VAL]'), **params.get('inputval', {})),
    preprocess=partial(preprocess, logger=logger.prefix('[PREPROCESS]'), images_path=images_path, images=images, base_path=os.path.join(base_path, 'preprocess'), **params.get('preprocess', {})),
    ocr=partial(ocr, images=images, logger=logger.prefix('[OCR]'), **params.get('ocr', {})),
    gamecorr=partial(gamecorr, images_path=images_path, logger=logger.prefix('[GAME CORR]'), **params.get('gamecorr', {})),
    queues_path=os.path.join(base_path, 'queues'), protocol=protocol, logger=logger
  )