from pydantic import BaseModel, Field
from typing import Optional, List
from abc import ABC, abstractmethod

DEFAULT_EMBEDDING_PATH = "/v1/embeddings"
DEFAULT_MAX_RETRIES = 3

class BaseEmbedParameter(BaseModel):
    '''做embedding的入参'''
    embed_content:str = Field(..., description="做embed的内容")  # 必需字段
    embed_key:str = Field(..., description="一类向量数据，缩小匹配的范围。例如：自由知识库-DK-成人")  # 必需字段
    embed_source:str = Field(..., description="来源，如果一份知识有多个来源，用来区分。各自业务自行设置和使用")  # 必需字段
    source_id:str = Field(..., description="来源出的对应的唯一记录")  # 必需字段
    meta_data:dict = Field(default={}, description="元素据，以上字段无法覆盖的信息")  # 可选字段，默认值为空字典

class EmbedConfig(BaseModel):
    '''embedding的配置'''
    model:str

class EmbedUsage(BaseModel):
    prompt_tokens:int
    total_tokens:int

class EmbedData(BaseModel):
    object:str = Field("embedding")
    embedding:List[float]
    index:int = Field(0)

class EmbedResponse(BaseModel):
    object:str = Field("list")
    data:list[EmbedData]
    model:str 
    usage:EmbedUsage 

class BuildEmbedParameter(BaseModel):
    api_key:str = Field(None, description="需要apikey的接口，需要设置这个参数")
    base_url:str = Field(None, description="需要拼接/v1/embedding的url")
    full_url:Optional[str] = Field(None, description="直接使用的接口，有先使用这个")
    max_retry:int = Field(DEFAULT_MAX_RETRIES, description="如果接口调用失败,最大尝试次数")
    model:str = Field("text-embedding-ada-002", description="模型")


class AbsEmbedModel(ABC):
    '''基础的embed模型'''
    api_key:str = Field(None, description="需要apikey的接口，需要设置这个参数")
    base_url:str = Field(None, description="需要拼接/v1/embedding的url")
    full_url:Optional[str] = Field(None, description="直接使用的接口，有先使用这个")
    max_retry:int = Field(DEFAULT_MAX_RETRIES, description="如果接口调用失败,最大尝试次数")
    model:str = Field("text-embedding-ada-002", description="模型")


    def __init__(self, parameter:BuildEmbedParameter) -> None:
        self.api_key = parameter.api_key
        self.base_url = parameter.base_url
        self.full_url = parameter.full_url
        self.max_retry = parameter.max_retry
        self.model = parameter.model
    
    @property
    def embed_url(self):
        if self.full_url:
            return self.full_url
        return self.base_url + DEFAULT_EMBEDDING_PATH

    @abstractmethod
    def embed(self, content:str) -> EmbedResponse:
        pass

    @abstractmethod
    async def async_embed(self, content: str) -> EmbedResponse:
        pass