from typing import Literal, Unpack
from dslog import Logger
from kv.api import KV
from moveread.pipelines.preprocess import run_local, ApiParams
from ..generated import Preprocess

def preprocess(
  Qin: Preprocess.QueueIn, Qout: Preprocess.QueueOut,
  *, queues_path: str, protocol: Literal['fs', 'sqlite'] = 'sqlite',
  logger = Logger.rich().prefix('[PREPROCESS]'),
  images: KV[bytes],
  **params: Unpack[ApiParams]
):
  run_local(
    Qin, Qout.premap(lambda r: Preprocess.next('join', r)),
    queues_path=queues_path, protocol=protocol,
    images=images, logger=logger, **params
  )