from typing import List
from utils import (
    identifier_util, 
    datetime_util
)

from ._base import AbsMemory
from .dto import (
    MessageInfo,
    MessageListParameter
)

# 所有使用本地内存的记忆
# {用户：{id:消息}}
memories:dict[str,dict[str:MessageInfo]] = {}

class DbMemory(AbsMemory):
    '''
        存储在DB中的记忆
        关系型数据库
        redis等非关系型数据库
    '''
    
    def __init__(self):
        # 初始化引擎
        pass

    def save_message(self, message:MessageInfo) -> str:
        '''
            保存或者更新消息
            message: 要保存的消息
            return: 该消息对应的id
        '''
        pass
        

    def list_message(self, parameter:MessageListParameter) -> List[MessageInfo]:
        '''
            查询消息列表
            parameter: 查询参数
            return: 根据条件查询到的消息记录
        '''
        pass