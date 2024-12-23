from pydantic import BaseModel, Field
from typing import Optional, List
from abc import ABC, abstractmethod

class PageContent(BaseModel):
    file_name:str = Field(description="文件名")
    page_content:str = Field(description="页面内容")
    page_num:int = Field(description="页码")


class AbsResolver(ABC):
    file_path:list[str] = Field(None, description="文件路径")

    def __init__(self, file_path:list[str]) -> None:
        self.file_path = file_path


    @abstractmethod
    def resolve(self) -> List[PageContent]:
        '''
            解析文件并返回页面内容列表
            file_path: 文件路径
            return: PageContent列表
        '''
        pass