from typing import Literal

from pydantic import BaseModel


class DemoRequest(BaseModel):
    scenario: Literal["normal", "reconnaissance", "progression", "suspicious"]


class DemoResponse(BaseModel):
    label: str
    scenario: str
    flows: list[dict]
