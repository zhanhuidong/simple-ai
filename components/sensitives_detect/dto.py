from pydantic import BaseModel, Field
from typing import Optional


class SensitiveCheckResult(BaseModel):
    '''敏感词检查结果'''
    is_sensitive: bool = Field(description="是否触发敏感")
    sensitive_message: Optional[str] = Field(default=None, description="触发的敏感信息，只有敏感的时候才会有值")