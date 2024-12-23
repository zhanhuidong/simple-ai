from pydantic import BaseModel, Field
import os
from typing import Optional, List
from abc import ABC, abstractmethod

class BaseSplitParameter(BaseModel):
    text:str
    chunk_size:int = 500
    chunk_overlap:int = 100
    separator: str = "\n\n"
    is_separator_regex: bool = False





class AbsSpliter(ABC):
    
    @abstractmethod
    def split(self, parameter:BaseSplitParameter) -> list[str]:
        pass

