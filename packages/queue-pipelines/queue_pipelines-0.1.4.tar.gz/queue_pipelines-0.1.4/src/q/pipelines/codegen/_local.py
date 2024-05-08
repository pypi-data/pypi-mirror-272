# BEGIN
from typing_extensions import Literal, Any, Unpack, TypedDict, NotRequired
from dslog import Logger
from q.api import ReadQueue, WriteQueue
from q.kv import QueueKV
import q.pipelines as qp
AnyT: type = Any # type: ignore
# UNCOMMENT from MODULE import INPUT, OUTPUT, SPEC_VARIABLE
# UNCOMMENT from TYPES import Queues, Pipelines
from ._types import Queues, Pipelines # DELETE
INPUT = int # DELETE
OUTPUT = int # DELETE

def input_queue(
  input_path: str, *, protocol: Literal['sqlite', 'fs'] = 'sqlite'
) -> QueueKV[INPUT]:
  return QueueKV.at(INPUT, input_path, protocol=protocol)

def output_queue(
  output_path: str, *, protocol: Literal['sqlite', 'fs'] = 'sqlite'
) -> QueueKV[OUTPUT]:
  return QueueKV.at(OUTPUT, output_path, protocol=protocol)

SPEC_VARIABLE = ... # DELETE
def queues(
  path: str, *,
  protocol: Literal['sqlite', 'fs'] = 'sqlite',
) -> Queues:
  return qp.local.local_queues(path, SPEC_VARIABLE, protocol=protocol) # type: ignore

async def connect(
  Qin: ReadQueue[INPUT],
  Qout: WriteQueue[OUTPUT],
  queues: Queues, *,
  logger = Logger.rich().prefix('[CONNECT]')
):
  await qp.connect(Qin, Qout, queues, input_task='INPUT_TASK', logger=logger) # type: ignore

def run_pipelines(queues: Queues, **pipelines: Unpack[Pipelines]):
  qp.run_pipelines(queues, **pipelines) # type: ignore

def run(
  Qin: ReadQueue[INPUT],
  Qout: WriteQueue[OUTPUT],
  queues: Queues, *,
  logger = Logger.rich(),
  **pipelines: Unpack[Pipelines]
):
  ps = qp.run(Qin, Qout, queues, input_task='INPUT_TASK', connect_logger=logger.prefix('[CONNECT]'), **pipelines) # type: ignore
  for name, p in ps.items():
    p.start()
    logger(f'Started process "{name}" at PID = {p.pid}')
  
  for name, p in ps.items():
    p.join()
    logger(f'Process "{name}" finished')

class Params(TypedDict):
  queues_path: str
  protocol: NotRequired[Literal['sqlite', 'fs']]
  logger: NotRequired[Logger]

def run_local(
  Qin: ReadQueue[INPUT],
  Qout: WriteQueue[OUTPUT], *,
  queues_path: str,
  protocol: Literal['sqlite', 'fs'] = 'sqlite',
  logger = Logger.rich(),
  **pipelines: Unpack[Pipelines]
):
  Qs = queues(queues_path, protocol=protocol)
  run(Qin, Qout, Qs, logger=logger, **pipelines)

__all__ = ['input_queue', 'output_queue', 'queues', 'connect', 'run_pipelines', 'run', 'run_local', 'Params']

# END
from templang import parse
from q.pipelines import Tasks

def local(tasks: Tasks, module: str, types_module: str, spec_variable: str) -> str:
  translations = {
    'MODULE': module,
    'TYPES': types_module,
    'INPUT_TASK': tasks.input_task,
    'INPUT': tasks.Input.__name__,
    'OUTPUT': tasks.Output.__name__,
    'SPEC_VARIABLE': spec_variable
  }

  with open(__file__) as f:
    source = f.read()
  
  return parse(source, translations)
