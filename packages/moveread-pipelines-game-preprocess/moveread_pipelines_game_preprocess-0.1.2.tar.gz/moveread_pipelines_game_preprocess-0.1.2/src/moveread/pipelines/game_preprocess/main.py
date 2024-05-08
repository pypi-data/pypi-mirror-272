from typing import Literal, NotRequired, TypeVar, Unpack
from functools import partial
import os
from dslog import Logger
from kv.api import KV
from kv.fs import FilesystemKV, FilesystemAppendKV
from moveread.pipelines.preprocess import ApiParams
from .spec import Game
from .pipelines import preinput, preprocess, join
from .generated import run_local as _run_local, QueueIn, QueueOut, Join

T = TypeVar('T')

def kv_at(Type: type[T], path: str, protocol: Literal['sqlite', 'fs'] = 'sqlite') -> KV[T]:
  if protocol == 'sqlite':
    from kv.sqlite import SQLiteKV
    return SQLiteKV.validated(Type, path + '.sqlite')
  else:
    return FilesystemKV.validated(Type, path)
  
class LocalParams(ApiParams):
  base_path: str
  protocol: NotRequired[Literal['sqlite', 'fs']]

def run_local(
  Qin: QueueIn, Qout: QueueOut, *,
  base_path: str, protocol: Literal['sqlite', 'fs'] = 'sqlite',
  logger: Logger = Logger.rich().prefix('[GAME PREPROCESS]'),
  images: KV[bytes],
  **params: Unpack[ApiParams]
):
  games = kv_at(Game, os.path.join(base_path, 'games'), protocol=protocol)
  gameIds = kv_at(str, os.path.join(base_path, 'gameIds'), protocol=protocol)
  received_imgs = FilesystemAppendKV.validated(tuple[str, Join.In], os.path.join(base_path, 'received_imgs'))
  qs_path = os.path.join(base_path, 'queues')
  _run_local(
    Qin, Qout, queues_path=qs_path, protocol=protocol,
    logger=logger,
    preinput=partial(preinput, games=games, imgGameIds=gameIds, logger=logger.prefix('[PREINPUT]')),
    preprocess=partial(
      preprocess, queues_path=qs_path, protocol=protocol,
      logger=logger.prefix('[PREPROCESS]'), images=images, **params
    ),
    join=partial(
      join, logger=logger.prefix('[JOIN]'), games=games,
      imgGameIds=gameIds, received_imgs=received_imgs
    ),
  )