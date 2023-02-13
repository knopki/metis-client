"""Engine model"""

from dataclasses import dataclass
from typing import Any, Optional

from typing_extensions import TypedDict


class MetisEngineDTO(TypedDict):
    "Engine DTO"

    template: Optional[str]
    schema: Optional[Any]
    input: Optional[str]


@dataclass(frozen=True)
class MetisEngineModel:
    "Engine model"

    template: Optional[str]
    schema: Optional[Any]
    input: Optional[str]
