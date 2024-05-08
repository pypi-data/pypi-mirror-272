from pydantic import BaseModel
from q.pipelines import Task, Tasks
from scoresheet_models import ModelID
import moveread.pipelines.preprocess as pre

PreInput = pre.Input
PreInput.__name__ = 'PreInput'

PreResult = pre.Result
PreResult.__name__ = 'PreResult'


class Input(BaseModel):
  model: ModelID 
  imgs: list[str]
  state: dict | None = None

class Game(BaseModel):
  model: ModelID
  imgIds: list[str]
  state: dict | None = None

class Result(BaseModel):
  preprocessed_imgs: list[PreResult]
  state: dict | None = None

TASKS = Tasks(
  input_task='preinput', Output=Result,
  tasks=dict[str, Task](
    preinput=Task(Input, 'preprocess'),
    preprocess=Task(PreInput, 'join'),
    join=Task(PreResult, 'output')
  )
)

def codegen():
  TASKS.codegen(__file__, 'TASKS')
  TASKS.codegen_pipelines(__file__)

if __name__ == '__main__':
  codegen()