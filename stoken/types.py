from typing import List, Dict

import pydantic


class Config(pydantic.BaseModel):
    suffix: List[str]
    token: Dict[str, str]
