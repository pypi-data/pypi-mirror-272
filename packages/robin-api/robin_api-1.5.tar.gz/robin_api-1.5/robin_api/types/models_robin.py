

from .._models import BaseModel
from typing import  Union
from typing_extensions import Literal
from typing import Any, Optional, cast

__all__ = ["Models", "DeepLevel"]

class Models(BaseModel):
        model: Union[
            str,
            Literal[
                "ROBIN_4",
                "ROBIN_3",
            ],
        ]

class DeepLevel(BaseModel):
        url: str
        folder_id: Optional[Any]=None
        deep_level:  Literal[
                1,
                2,
                3
            ]
        