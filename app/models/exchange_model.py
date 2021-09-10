from typing import Dict

from pydantic import BaseModel, PositiveFloat


class Exchange(BaseModel):
    last_updated: str
    value: PositiveFloat


class Rates(BaseModel):
    rates: Dict[str, Exchange]
