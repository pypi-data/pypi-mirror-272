from datetime import timedelta
import asyncio
from sqlalchemy import Engine
from sqlalchemy.exc import DatabaseError
from sqlmodel import select, Session
from haskellian import Left, either as E
from dslog import Logger
from q.api import WriteQueue
from moveread.pipelines.dfy import Input
from scoresheet_models import ModelID
from ..types import Game, GameId

async def puller(
  Qin: WriteQueue[Input], engine: Engine, *,
  tournId: str, model: ModelID, polling_interval: timedelta = timedelta(seconds=30),
  logger = Logger.rich().prefix('[PULLER]')
):
  @E.do()
  async def pull_once():
    try:
      with Session(engine) as ses:
        stmt = select(Game).where(Game.tournId == tournId, Game.status == None)
        games = ses.exec(stmt).all()
        for game in games:
          id = GameId.of(game)
          task = Input(gameId=id.dict(), model=model, imgs=[img.url for img in game.imgs]) # type: ignore (id's are structurally identical)
          logger(f'Inputting new task for "{id}":', task)
          (await Qin.push(id.stringify(), task)).unsafe()
          game.status = Game.Status.doing
          ses.add(game)
        ses.commit()
    except DatabaseError as e:
      Left(e).unsafe()

  while True:
    r = await pull_once()
    if r.tag == 'left':
      logger('Error while pulling', r.value, level='ERROR')
    
    await asyncio.sleep(polling_interval.total_seconds())
