import moveread.pipelines.extract_validation as val
from ..types import RootOutput
from ..generated import Validate, Revalidate

In = Validate.In | Revalidate.In

def pre(state: In) -> tuple[val.Task, In]:
  return val.Task(contoured=state.contoured, already_corrected=state.confirmed), state

def next_task_val(ann: val.Annotation, state: Validate.In) -> Validate.Out:
  match ann:
    case 'correct': return ('preoutput', RootOutput(state.ok()))
    case 'incorrect': return ('correct', state)
    case 'perspective-correct': return ('select', state)

def post_val(entry: tuple[val.Annotation, Validate.In]) -> Validate.Out:
  ann, state = entry
  return next_task_val(ann, state)

def next_task_reval(ann: val.Reannotation, state: Revalidate.In) -> Revalidate.Out:
  match ann:
    case 'correct': return ('preoutput', RootOutput(state.ok()))
    case 'incorrect': return ('select', state)

def post_reval(entry: tuple[val.Reannotation, Revalidate.In]) -> Revalidate.Out:
  ann, state = entry
  return next_task_reval(ann, state)

def validation_api(queues: Validate.Queues) -> val.ValidationAPI:
  Qin, Qout = queues
  return val.ValidationAPI(
    Qin.map(pre),
    Qout.premap(post_val)
  )

def revalidation_api(queues: Revalidate.Queues) -> val.ValidationAPI:
  Qin, Qout = queues
  return val.ValidationAPI(
    Qin.map(pre),
    Qout.premap(post_reval)
  )
