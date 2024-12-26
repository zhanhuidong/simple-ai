from .dto import SensitiveCheckResult
from abc import ABC, abstractmethod

class AbsSensitiveDetector(ABC):
    '''抽象类，用于敏感词解析'''

    def __init__(self) -> None:
        pass

    @abstractmethod
    def check_sensitive(self, text: str) -> SensitiveCheckResult:
        '''校验给定的信息是否触发敏感
        
        返回一个包含两个字段的对象:
        - is_sensitive: bool, 表示是否触发敏感
        - sensitive_message: str, 被触发的信息
        '''
        pass
