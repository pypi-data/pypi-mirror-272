import moveread.pipelines.manual_select as sel
from ..types import RootOutput
from ..generated import Select

def pre(state: Select.In) -> tuple[sel.Task, Select.In]:
  return sel.Task(img=state.corrected, model=state.model), state

def post(entry: tuple[sel.Result, Select.In]) -> Select.Out:
  res, state = entry
  match res.tag:
    case 'selected':
      return ('preoutput', RootOutput(state.select(res.grid_coords)))
    case 'recorrect':
      return ('correct', state)

def selection_api(queues: Select.Queues) -> sel.SelectAPI:
  Qin, Qout = queues
  return sel.SelectAPI(
    Qin.map(pre),
    Qout.premap(post)
  )