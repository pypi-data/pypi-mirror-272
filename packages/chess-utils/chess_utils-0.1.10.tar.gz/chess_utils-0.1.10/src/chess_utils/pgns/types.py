from typing import Literal, TypeAlias
from pydantic import BaseModel, ConfigDict

Result: TypeAlias =  Literal["0-1", "1-0", "1/2-1/2", "*"]

class STRHeaders(BaseModel):
  Event: str
  Site: str
  Date: str
  Round: str
  White: str
  Black: str
  Result: Result

class PGNHeaders(STRHeaders):
  model_config = ConfigDict(extra='allow')