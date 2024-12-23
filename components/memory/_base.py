from pydantic import BaseModel, Field
import os
from typing import Optional, List
from datetime import datetime
from abc import ABC, abstractmethod

class MessageInfo(BaseModel):
    '''保存的消息'''
    # 消息id
    id:Optional[str] = Field(None)
    # 用户身份识别,比如api_key
    user_id:str
    system_message:Optional[str] = Field(None)
    user_message:Optional[str] = Field(None)
    assistant_message:Optional[str] = Field(None)
    # 创建时间
    created:Optional[float] = Field(0)

class MessageListParameter(BaseModel):
    '''查询消息列表的参数'''
    # 用户身份识别
    api_key:str
    # 取出的条数
    limit:int = 3
    # 倒序，取最近的数据
    desc:bool = True
    # 开始时间
    created:float = 0

class AbsMemory(ABC):

    @abstractmethod
    def save_message(self, message:MessageInfo) -> str:
        '''
            保存或者更新消息
            message: 要保存的消息
            return: 该消息对应的id
        '''
        pass

    @abstractmethod
    def list_message(self, parameter:MessageListParameter) -> List[MessageInfo]:
        '''
            查询消息列表
            parameter: 查询参数
            return: 根据条件查询到的消息记录
        '''
        pass