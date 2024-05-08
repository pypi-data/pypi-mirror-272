from q.pipelines import Task, Tasks
from .types import Result, Input, Extracted, Corrected, RootOutput

TASKS = Tasks(
  input_task='extract', Output=Result,
  tasks=dict[str, Task](
    extract=Task(Input, 'validate', 'correct'),
    validate=Task(Extracted, 'preoutput', 'correct', 'select'),
    correct=Task(Input, 'extract', 'reextract'),
    reextract=Task(Corrected, 'revalidate', 'select'),
    revalidate=Task(Extracted, 'preoutput', 'select'),
    select=Task(Corrected, 'preoutput', 'correct'),
    preoutput=Task(RootOutput, 'output')
  )
)

def codegen():
  TASKS.codegen(__file__, 'TASKS')

if __name__ == '__main__':
  codegen()