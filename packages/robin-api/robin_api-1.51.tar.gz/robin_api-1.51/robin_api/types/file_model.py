

from .._models import BaseModel
from typing import  Union
from typing_extensions import Literal
from typing import Any, Optional, cast

__all__ = ["FilesModel" , "IndexFile", "DeepLevel"]

        
class FilesModel(BaseModel):
        file_id: str


class IndexFile(BaseModel):
        url: Optional[str]
        folder_id: Optional[Any]=None
        file_id: Optional[str]


class DeepLevel(BaseModel):
        url: str
        folder_id: Optional[Any]=None
        deep_level:  Literal[
                1,
                2,
                3
            ]