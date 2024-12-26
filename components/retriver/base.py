from abc import ABC,abstractmethod
from .dto import (
    RetriverParameter,
    RetriverResult
)

import json
import traceback
'''
近似查询
'''
class AbsRetriver(ABC):
    '''
    近似查询抽象类
    '''
    
    def search(self, req:RetriverParameter) -> RetriverResult:
        result = self._doc_search(req)
        result = self._after_search(req, result)

        return result
    
    @abstractmethod
    def _doc_search(self, req:RetriverParameter) -> RetriverResult:
        pass
    
    def _after_search(self, req:RetriverParameter, result:RetriverResult):
        return result
