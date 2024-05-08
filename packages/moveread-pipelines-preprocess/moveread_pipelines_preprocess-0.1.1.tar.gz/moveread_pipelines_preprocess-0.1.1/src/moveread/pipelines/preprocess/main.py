from typing import NotRequired, TypedDict, Sequence, Unpack, Literal
from multiprocessing import Process
from haskellian import promise as P
from dslog import Logger
from kv.api import KV
from .adapters import run_extract, run_reextract, \
  fastapi, correction_api, revalidation_api, validation_api, selection_api, \
  run_preoutput
  
from .generated import connect, Queues, QueueIn, QueueOut, queues

def auto_processes(
  queues: Queues, *,
  logger = Logger.click().prefix('[AUTO]'),
  images: KV[bytes]
) -> Sequence[tuple[str, Process]]:
  return [
    ('extract', Process(
      target=P.run(run_extract), args=(queues['extract'],),
      kwargs=dict(logger=logger.prefix('[EXTRACT]'), images=images)
    )),
    ('re-extract', Process(
      target=P.run(run_reextract), args=(queues['reextract'],),
      kwargs=dict(logger=logger.prefix('[REEXTRACT]'), images=images)
    ))
  ]

class ApiParams(TypedDict):
  images_path: str | None
  port: NotRequired[int]
  host: NotRequired[str]

def api_process(
  queues: Queues, *, images: KV[bytes], images_path: str | None = None,
  port: int = 8000, host: str = '0.0.0.0', log_config: dict | None = None,
  logger = Logger.rich().prefix('[API]')
) -> Process:
  app = fastapi(
    corr_api=correction_api(queues['correct'], images=images),
    reval_api=revalidation_api(queues['revalidate']),
    val_api=validation_api(queues['validate']),
    sel_api=selection_api(queues['select']),
    images_path=images_path, logger=logger
  )
  import uvicorn
  return Process(target=uvicorn.run, args=(app,), kwargs=dict(port=port, host=host, log_config=log_config))

def processes(
  Qin: QueueIn, Qout: QueueOut, queues: Queues, *,
  logger = Logger.rich().prefix('[PREPROCESS]'),
  images: KV[bytes],
  **params: Unpack[ApiParams]
) -> Sequence[tuple[str, Process]]:
  """Returns a sequence of unstarted processes"""
  logger = params.get('logger') or Logger.click().prefix('[PREPROCESS]')
  return [
    *auto_processes(queues, logger=logger.prefix('[AUTO]'), images=images),
    ('api', api_process(queues, images=images, logger=logger.prefix('[API]'), **params)),
    ('connect', Process(
      target=P.run(connect), args=(Qin, Qout),
      kwargs=dict(queues=queues, logger=logger.prefix('[CONNECT]'))
    )),
    ('preoutput', Process(
      target=P.run(run_preoutput), args=(queues['preoutput'],),
      kwargs=dict(logger=logger.prefix('[PREOUTPUT]'), images=images)
    ))
  ]

def run(
  Qin: QueueIn, Qout: QueueOut, queues: Queues, *,
  logger = Logger.rich().prefix('[PREPROCESS]'),
  images: KV[bytes],
  **params: Unpack[ApiParams]
):
  ps = processes(Qin, Qout, queues, logger=logger, images=images, **params)
  for name, p in ps:
    p.start()
    logger(f'Started process "{name}" at PID = {p.pid}')
  
  for name, p in ps:
    p.join()
    logger(f'Process "{name}" finished')

class LocalParams(ApiParams):
  queues_path: str
  protocol: NotRequired[Literal['fs', 'sqlite']]
  logger: NotRequired[Logger]

def run_local(
  Qin: QueueIn, Qout: QueueOut, *,
  queues_path: str, protocol: Literal['fs', 'sqlite'] = 'sqlite',
  logger = Logger.rich().prefix('[PREPROCESS]'),
  images: KV[bytes],
  **params: Unpack[ApiParams]
):
  Qs = queues(queues_path, protocol=protocol)
  run(Qin, Qout, Qs, logger=logger, images=images, **params)