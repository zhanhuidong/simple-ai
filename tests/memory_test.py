from pydantic import BaseModel, Field
import os
from typing import Optional, List
from datetime import datetime
from abc import ABC, abstractmethod

import hashlib  
from datetime import datetime 
import uuid

'''
    唯一id生成器
''' 

# 使用uuid生成唯一id
def generate_by_uuid(name:str=None) -> str:  
    if not name or len(name) == 0:
        # 如果种子是空，则使用当前时间作为种子
        return uuid.uuid4().__str__().replace('-','')
    # 生成uuid5
    return uuid.uuid5(uuid.NAMESPACE_X500, name).__str__().replace('-','')


def get_current_timestamp():
    return datetime.now().timestamp() * 1000

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

# 所有使用本地内存的记忆
# {用户：{id:消息}}
memories:dict[str,dict[str,MessageInfo]] = {}

class BaseMemory(AbsMemory):
    '''
        基础记忆
        使用本地内存实现
    '''
    
    
    def __init__(self):
        # 初始化引擎
        self.memories = memories

    def save_message(self, message:MessageInfo) -> str:
        '''
            保存或者更新消息
            message: 要保存的消息
            return: 该消息对应的id
        '''
        if not message.id:
            # 新增保存
            id = generate_by_uuid()
            message.id = id
            if not message.created:
                message.created = get_current_timestamp()
            user_memory = self.memories.get(message.user_id, {})
            user_memory[message.id] = message
            self.memories[message.user_id] = user_memory
        else:
            # 更新
            message_in_memory = self.memories.get(message.user_id, {}).get(message.id)
            if message_in_memory:
                message_in_memory.system_message = message.system_message if message.system_message else message_in_memory.system_message
                message_in_memory.user_message = message.user_message if message.user_message else message_in_memory.user_message
                message_in_memory.assistant_message = message.assistant_message if message.assistant_message else message_in_memory.assistant_message
        return message.id
        

    def list_message(self, parameter:MessageListParameter) -> List[MessageInfo]:
        '''
            查询消息列表
            parameter: 查询参数
            return: 根据条件查询到的消息记录
        '''
        user_memory = self.memories.get(parameter.api_key, {})
        if not user_memory:
            return []
        
        messages = [mem for mem in list(user_memory.values()) if mem.created > parameter.created]
        messages.sort(key=lambda x: x.created, reverse=parameter.desc)
        return messages[:parameter.limit]
        


if __name__ == "__main__":
    message_1 = MessageInfo(user_id="user_1", system_message="system", user_message="user", assistant_message="assistant")
    message_2 = MessageInfo(user_id="user_1", system_message="system", user_message="user", assistant_message="assistant")
    message_3 = MessageInfo(user_id="user_1", system_message="system", user_message="user", assistant_message="assistant")
    message_4 = MessageInfo(user_id="user_2", system_message="system", user_message="user", assistant_message="assistant")

    client = BaseMemory()

    client.save_message(message_1)
    client.save_message(message_2)
    created = get_current_timestamp()
    client.save_message(message_3)
    client.save_message(message_4)

    messages = client.list_message(MessageListParameter(api_key="user_1", created=created, limit=2))

    for message in messages:
        print(message.model_dump())