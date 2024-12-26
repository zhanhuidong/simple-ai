
from abc import ABC, abstractmethod

class AbsPrompt(ABC):
    '''抽象类，用于生成系统和用户消息'''

    def __init__(self, prompt_str: str) -> None:
        self.prompt = prompt_str

    @abstractmethod
    def generate_prompt(self, params:dict) -> str:
        '''根据参数处理prompt'''
        pass
