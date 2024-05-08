from typing import TypeVar, Unpack, TypeAlias
import base64
import asyncio
from haskellian import iter as I, either as E, funcs as F
from kv.api import KV, ReadError as KVReadError
from q.api import ReadQueue, WriteQueue, ReadError as QReadError
import tf.serving as tfs
from dslog import Logger
from .types import Input, Preds

State = TypeVar('State')

Err: TypeAlias = QReadError | KVReadError | tfs.PredictErr

class Params(tfs.Params):
  ...
  
async def run(
  Qin: ReadQueue[tuple[Input, State]],
  Qout: WriteQueue[tuple[Preds, State]], *,
  images: KV[bytes],
  logger = Logger.rich().prefix('[OCR PREDS]'),
  **params: Unpack[tfs.Params]
):
  """Runs predections by reading task images as keys of `images`. Appends a `State` entry first, then all `Preds`"""
  
  @E.do[Err]()
  async def run_one():
    id, (task, state) = (await Qin.read()).unsafe()
    logger(f'Predicting "{id}"')
    
    imgs = await asyncio.gather(*[
      asyncio.gather(*[images.read(url).then(E.unsafe) for url in ply_urls])
      for ply_urls in task.ply_boxes
    ])
    b64imgs = I.ndmap(F.flow(base64.urlsafe_b64encode, bytes.decode), imgs)

    results: Preds = []
    for i, batch in I.batch(8, b64imgs).enumerate():
      logger(f'"{id}": Batch {i}')
      preds = (await tfs.multipredict(batch, **params)).unsafe()
      results.extend(preds)
    
    logger(f'Done predicting "{id}"')
    (await Qout.push(id, (results, state))).unsafe()
    (await Qin.pop(id)).unsafe()
  
  while True:
    res = await run_one()
    if res.tag == 'left':
      logger(f'Error predicting "{id}"', res.value, level='ERROR')
      await asyncio.sleep(1)
    else:
      await asyncio.sleep(0) # release the loop