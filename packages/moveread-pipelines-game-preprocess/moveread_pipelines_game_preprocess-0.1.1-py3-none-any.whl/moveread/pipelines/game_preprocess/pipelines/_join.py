import asyncio
from haskellian import either as E, promise as P, iter as I
from dslog import Logger
from kv.api import KV, AppendableKV
from ..generated import Join
from ..spec import Game, Result

@P.run
async def join(
  Qin: Join.QueueIn, Qout: Join.QueueOut, *,
  logger: Logger = Logger.of(print).prefix('[JOIN]'),
  received_imgs: AppendableKV[tuple[str, Join.In]],
  games: KV[Game], imgGameIds: KV[str],
):
  @E.do()
  async def run_one():
    imgId, result = (await Qin.read()).unsafe()
    gameId = (await imgGameIds.read(imgId)).mapl(lambda err: f'Error reading image "{imgId}" gameId: {err}').unsafe()
    logger(f'Received "{imgId}" for "{gameId}"')
    game, received = await asyncio.gather(
      games.read(gameId).then(lambda e: e.mapl(lambda err: f'Error reading buffered game: {err}').unsafe()),
      received_imgs.read(gameId).then(E.get_or([])),
    )

    received_now = [*received, (imgId, result)]
    receivedIds = set(imgId for imgId, _ in received_now)
    requiredIds = set(game.imgIds)
    logger('Received:', receivedIds, 'Required', requiredIds, level='DEBUG')

    if receivedIds == requiredIds:
      next = Join.next('output', Result(preprocessed_imgs=[res for _, res in received_now], state=game.state))
      (await Qout.push(gameId, next)).unsafe()
      E.sequence(await asyncio.gather(
        games.delete(gameId),
        received_imgs.delete(gameId),
      )).unsafe()
    else:
      (await received_imgs.append(gameId, [(imgId, result)])).unsafe()
    
    (await imgGameIds.delete(imgId)).unsafe()
    (await Qin.pop(imgId)).unsafe()

  while True:
    r = await run_one()
    if r.tag == 'left':
      logger(r.value, level='ERROR')
      await asyncio.sleep(1)
    