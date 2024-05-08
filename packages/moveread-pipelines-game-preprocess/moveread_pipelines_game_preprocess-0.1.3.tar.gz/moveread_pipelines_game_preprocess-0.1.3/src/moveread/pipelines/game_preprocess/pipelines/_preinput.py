import asyncio
from haskellian import either as E, promise as P
from dslog import Logger
from kv.api import KV
from ..generated import Preinput
from ..spec import Game, PreInput

@P.run
async def preinput(
  Qin: Preinput.QueueIn, Qout: Preinput.QueueOut,
  *, games: KV[Game], imgGameIds: KV[str],
  logger = Logger.rich().prefix('[PREINPUT]')
):
  @E.do()
  async def input_one():
    gameId, task = (await Qin.read()).unsafe()
    imgIds = [f'{gameId}-{i}' for i in range(len(task.imgs))]
    (await games.insert(gameId, Game(model=task.model, imgIds=imgIds, state=task.state))).unsafe()
    tasks = [
      Qout.push(imgId, Preinput.next('preprocess', PreInput(model=task.model, img=img)))
      for imgId, img in zip(imgIds, task.imgs)
    ] + [
      imgGameIds.insert(imgId, gameId)
      for imgId in imgIds
    ]
    E.sequence(await asyncio.gather(*tasks)).unsafe()
    (await Qin.pop(gameId)).unsafe()

  while True:
    r = await input_one()
    if r.tag == 'left':
      logger(r.value, level='ERROR')
      await asyncio.sleep(1)