from .base import(
    AbsSensitiveDetector
)
from .dto import SensitiveCheckResult


class BaseSensitiveDetector(AbsSensitiveDetector):
    '''
    基础的敏感词检测器
    数据库校验
    '''

    def __init__(self) -> None:
        super().__init__()

    def check_sensitive(self, text: str) -> SensitiveCheckResult:
        '''检测敏感词'''
        pass