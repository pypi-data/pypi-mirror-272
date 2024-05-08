from typing import NotRequired, TypedDict, TypeVar
from q.api import ReadQueue, WriteQueue
import uvicorn
from moveread.pipelines.game_correction.types import Result, Input
from moveread.pipelines.game_correction.sdk import CorrectionAPI
from moveread.pipelines.game_correction.api import fastapi
from dslog import Logger

S = TypeVar('S')

class Params(TypedDict):
  images_path: str
  port: NotRequired[int]
  host: NotRequired[str]
  prefix: NotRequired[str]

def run_api(
  Qin: ReadQueue[tuple[Input, S]],
  Qout: WriteQueue[tuple[Result, S]], *,
  images_path: str,
  port: int = 8001,
  host: str = '0.0.0.0',
  logger = Logger.click().prefix('[GAME CORRECTION]'),
):
  sdk = CorrectionAPI(Qin, Qout)
  uvicorn.run(fastapi(sdk, images_path, logger=logger), port=port, host=host)