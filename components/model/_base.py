from pydantic import BaseModel, Field
import os
from typing import Optional, List

DEFAULT_MAX_RETRIES = 3
DEFAULT_MAX_NEW_TOKENS = 4096
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MODEL = "text-davinci-003"
DEFAULT_COMPLETION_PATH = "/v1/chat/completions"
MODEL_PATH = "/v1/models"
DEFAULT_MAX_NEW_TOKENS = 4096
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 0.95
DEFAULT_TOP_N = 50
DEFAULT_REPETITION_PENALTY= 1.1
        

class BaseMessage(BaseModel):
    role:str = Field("user", pattern="user|assistant|system", description="角色")
    content:Optional[str] = Field(default="")

class SystemMessage(BaseMessage):
    role:str = Field("system")

class UserMessage(BaseMessage):
    role:str = Field("user")

class AIMessage(BaseMessage):
    role:Optional[str] = Field("assistant")

class CompletionsChoice(BaseModel):
    message:Optional[AIMessage] = Field(default=None, description="非流式响应时候的消息")
    delta:Optional[AIMessage] = Field(default=None, description="流式响应时候的消息")
    index:int = Field(default=0, description="索引")
    logprobs:Optional[float] = Field(default=None, description="对数概率")
    finish_reason:Optional[str] = Field(default=None, description="结束原因")

class ModelResponse(BaseModel):
    id:str = Field(default=None, description="id")
    object:str = Field(default="chat.completions", description="object:chat.completions|chat.completions.chunk")
    created:int = Field(default=None, description="创建时间")
    choices:list[CompletionsChoice] = Field(default=[], description="消息列表")
    usage:Optional[dict] = Field(default=None, description="usage")
    model:str = Field(default="MIX", description="模型")
    system_fingerprint:str = Field(default="MIX", description="系统指纹")

class BaseLLMParameter(BaseModel):
    api_key:str = None
    base_url:str = None
    full_url:str = None
    max_retry:int = DEFAULT_MAX_RETRIES

class BaseLLMModel:
    api_key:str = None
    base_url:str = None
    full_url:str = None
    max_retry:int = 3

    def __init__(self, parameter:BaseLLMParameter) -> None:
        api_key = parameter.api_key
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        self.api_key = api_key
        self.base_url = parameter.base_url
        self.full_url = parameter.full_url
        self.max_retry = parameter.max_retry

    @property
    def completion_url(self):
        if self.full_url:
            return self.full_url
        return self.base_url + DEFAULT_COMPLETION_PATH
    
    def completion(self, **args):
        raise Exception("Not implemented completion method")

    def after_response(self, response:ModelResponse):
        # 保存日志
        pass


class BaseCompletionParameter(BaseLLMParameter):
    messages: List[BaseMessage]
    temperature: float = None 
    max_new_tokens: int = None
    model: str = None
    stream: bool = False
    